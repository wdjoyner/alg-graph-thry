"""Check the four episode outlines against the series files.

    python check_outline.py

Errors (exit status 1) mean an outline breaks a series rule.  Warnings are
things to look at but not necessarily wrong.  The checks:

  * IDs: scenes s00..s99, beats sNN.bMM, all unique; s00 is the title card
    and s99 the end credits of every episode.
  * Show it before you name it: a concept may be named only in or after a
    beat (or scene) that shows it, in series order.
  * Threads: every setup is paid off later; every payoff was set up earlier.
  * Conjectures: every conjecture is later proved or refuted, or marked
    left_open; only proof or exhaustive_check beats may establish anything.
  * Math: every claim matches math_objects.json; every paper label exists.
  * Vocabulary: speakers come from cast.json, visual verbs and epistemic
    values from series.json.
  * Runtime: required scenes fit the episode's budget.
  * Credits: every credits section is shown, every card is up long enough
    to read, conditional cards play only where they apply, and each s99
    matches its cards plus its tail ('next_time' or 'finale') in length.
  * Titles: the titles screenplay has one subtitle per episode, text is held
    long enough to read (the same rule as the credits), and each s00 matches its main-title version plus
    subtitle in length.
  * Script (where epN/script.fountain exists): every beat of the outline is
    marked once, in outline order; every dialogue line has a stable ID in
    its beat; the outline's 'lines' lists match the script; speakers come
    from cast.json.
  * Cues (where epN/cues.json exists): every beat has cues, every line is
    cued once and in order, the outline's visuals all appear in their beat's
    cues, every verb, reaction and target is known, every predict_pause beat
    pauses, and the card game played through the cues obeys the rules and
    reaches the totals the cues claim.
  * Timing (where epN/timing.json exists): it is up to date with the cues and
    the audio manifest; the measured runtime is compared with the budget.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
errors, warnings = [], []


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def lookup(obj, path):
    for key in path.split("."):
        if isinstance(obj, list):
            obj = obj[int(key)]
        elif isinstance(obj, dict) and key in obj:
            obj = obj[key]
        else:
            raise KeyError(path)
    return obj


def units(scene):
    """The scene's beats, or the scene itself when it is outlined at scene level."""
    return scene.get("beats") or [scene]


def check_common(u, uid, ctx):
    """Checks shared by episode beats and title beats: vocabulary and math."""
    for who in (u.get("lead"), u.get("foil")):
        if who is not None and who not in ctx["cast"]:
            errors.append(f"{uid}: unknown character {who}")
    if u.get("epistemic") not in ctx["epistemic"]:
        errors.append(f"{uid}: epistemic {u.get('epistemic')!r} not allowed")
    if u.get("establishes") and u.get("epistemic") not in ("proof", "exhaustive_check"):
        errors.append(f"{uid}: only proof or exhaustive_check may establish a result")
    for v in u.get("visual", []):
        if v.split(":")[0] not in ctx["verbs"]:
            errors.append(f"{uid}: unknown visual verb in {v!r}")
    for m in u.get("math", []):
        ref = m["ref"]
        if ref not in ctx["objects"]:
            errors.append(f"{uid}: math ref {ref} not in math_objects.json")
            continue
        for path, want in m.get("claim", {}).items():
            try:
                got = lookup(ctx["objects"][ref], path)
            except (KeyError, IndexError, ValueError):
                errors.append(f"{uid}: {ref} has no field {path}")
                continue
            if got != want:
                errors.append(f"{uid}: {ref}.{path} is {got!r}, outline says {want!r}")


def check_titles(series, ctx):
    """The titles screenplay: main title versions and one subtitle per episode.

    Returns {version: seconds} and {subtitle id: (episode, seconds)}."""
    card = series["cards"]["title_card"]
    titles = load(card["screenplay"])
    reading = card["reading"]

    def need(lines):
        return max(reading["min_seconds"],
                   reading["settle_seconds"] + words(lines) / reading["words_per_second"])

    titles_text = lambda lines, n=None: [l.format(series_title=series["series_title"], tagline=series["tagline"],
                                                  number=n or "", title=next((e["title"] for e in series["episodes"] if e["number"] == n), ""))
                                         for l in lines]
    beats = {b["id"]: b for b in titles["main_title"]["beats"]}
    if len(beats) != len(titles["main_title"]["beats"]):
        errors.append("titles: duplicate main-title beat id")
    for bid, b in beats.items():
        check_common(b, f"titles.{bid}", ctx)
    versions = {}
    for name, v in titles["main_title"]["versions"].items():
        if name.startswith("_"):
            continue
        total = 0.0
        for bid in v["beats"]:
            if bid not in beats:
                errors.append(f"titles.{name}: unknown beat {bid}")
                continue
            secs = v.get("seconds", {}).get(bid, beats[bid]["seconds"])
            if beats[bid].get("text") and secs < need(titles_text(beats[bid]["text"])) - 1e-9:
                errors.append(f"titles.{name}.{bid}: text held {secs}s, needs {need(titles_text(beats[bid]['text'])):.1f}s to read")
            total += secs
        if not any(beats[b].get("text") for b in v["beats"] if b in beats):
            errors.append(f"titles.{name}: version never shows the series title")
        versions[name] = total
    subtitles = {}
    episodes = {ep["number"] for ep in series["episodes"]}
    for s in titles["subtitles"]:
        check_common(s, f"titles.{s['id']}", ctx)
        if s["episode"] not in episodes:
            errors.append(f"titles.{s['id']}: no episode {s['episode']}")
        if s["seconds"] < need(titles_text(s["text"], s["episode"])) - 1e-9:
            errors.append(f"titles.{s['id']}: held {s['seconds']}s, too short to read")
        subtitles[s["id"]] = (s["episode"], s["seconds"])
    if sorted(e for e, _ in subtitles.values()) != sorted(episodes):
        errors.append("titles: need exactly one subtitle per episode")
    return versions, subtitles


def words(lines):
    return sum(1 for line in lines for w in line.split() if any(ch.isalnum() for ch in w))


def section_lines(section, cast):
    """The text a credits section puts on screen (cast placeholders for unchosen voices)."""
    lines = [section["heading"]]
    if section.get("from_cast"):
        for c in cast.values():
            if c.get("principal") or c.get("optional"):
                chosen = c["voice"].get("chosen") or "voice"
                lines.append(section["format"].format(name=c["name"], chosen=chosen))
    lines += section.get("names", [])
    if section.get("footer"):
        lines.append(section["footer"])
    return lines


def check_end_credits(series, ctx):
    """The end-credits screenplay: sections exist, cards are readable, tails are well formed."""
    spec = series["cards"]["end_credits"]
    roll = load(spec["screenplay"])
    sections = {s["id"]: s for s in load(spec["text"])["sections"]}
    reading = spec["reading"]

    def need(lines):
        return max(reading["min_seconds"],
                   reading["settle_seconds"] + words(lines) / reading["words_per_second"])

    used = set()
    for card in roll["cards"]:
        uid = f"credits.{card['id']}"
        check_common(card, uid, ctx)
        lines = []
        for sid in card["sections"]:
            if sid not in sections:
                errors.append(f"{uid}: no credits section {sid!r}")
                continue
            used.add(sid)
            lines += section_lines(sections[sid], ctx["cast"])
            if sections[sid].get("when") != card.get("when"):
                errors.append(f"{uid}: section {sid} has when={sections[sid].get('when')!r} "
                              f"but the card has when={card.get('when')!r}")
        if card["seconds"] < need(lines) - 1e-9:
            errors.append(f"{uid}: {words(lines)} words need {need(lines):.1f}s, card has {card['seconds']}s")
    for sid, s in sections.items():
        if sid not in used:
            errors.append(f"credits: section {sid} is never shown")
        if s.get("pending"):
            warnings.append(f"credits: section {sid} is still pending")
    for name, tail in roll["tails"].items():
        check_common(tail, f"credits.{tail['id']}", ctx)
    return roll, need


def episode_flags(scenes, outline):
    """Flags for 'when' cards: 'required' if used in a required scene, 'optional' if only in optional ones."""
    flags = {}
    for scene in scenes:
        for u in units(scene):
            optional = scene.get("optional") or u.get("optional")
            people = {u.get("lead", scene.get("lead")), u.get("foil", scene.get("foil"))}
            people |= {c["who"] for c in u.get("cameos", []) if not c.get("optional")}
            maybe = {c["who"] for c in u.get("cameos", []) if c.get("optional")}
            for who in people | maybe:
                level = "optional" if (optional or who in maybe - people) else "required"
                if flags.get(who) != "required":
                    flags[who] = level
    for use in outline.get("uses", []):
        flags[use] = "required"
    return flags


def check_credits_scene(scene, n, last, series, roll, need, flags, where):
    """s99 must equal the credits it will play; returns seconds that play only with optional scenes."""
    tail_name = scene.get("tail")
    if tail_name not in roll["tails"]:
        errors.append(f"{where}: tail {tail_name!r} not in the end-credits screenplay")
        return 0.0
    if (tail_name == "finale") != (n == last):
        errors.append(f"{where}: the finale tail belongs to the last episode only")
    nxt = scene.get("next_episode")
    if tail_name == "next_time" and nxt != n + 1:
        errors.append(f"{where}: next_time tail needs next_episode {n + 1}")
    if tail_name == "finale" and nxt is not None:
        errors.append(f"{where}: finale tail needs next_episode null")
    tail = roll["tails"][tail_name]
    titles = {ep["number"]: ep["title"] for ep in series["episodes"]}
    text = [t.format(next_number=nxt, next_title=titles.get(nxt, "")) for t in tail.get("text", [])]
    if tail["seconds"] < need(text) - 1e-9:
        errors.append(f"{where}: tail text needs {need(text):.1f}s, has {tail['seconds']}s")
    required, optional = tail["seconds"], 0.0
    for card in roll["cards"]:
        level = flags.get(card["when"]) if card.get("when") else "required"
        if level == "required":
            required += card["seconds"]
        elif level == "optional":
            optional += card["seconds"]
    if abs(scene.get("target_seconds", 0) - required) > 1e-9:
        errors.append(f"{where}: target_seconds should be {required:g} (credits cards plus the {tail_name} tail)")
    return optional


def check_script_and_cues(n, outline, ctx):
    """Script, cues and timing of one episode, where they exist."""
    from script_tools import parse
    from cue_tools import steps, step_visuals, visual_name, split_visual, simulate
    where0 = f"ep{n}"
    path = HERE / f"ep{n}" / "script.fountain"
    if not path.exists():
        return
    script = parse(path)
    for e in script["errors"]:
        errors.append(f"{where0} script: {e}")
    beats = [b for sc in outline["scenes"] for b in sc.get("beats", [])]
    want = [b["id"] for b in beats]
    got = [b["id"] for b in script["beats"]]
    if got != want:
        missing = [b for b in want if b not in got]
        extra = [b for b in got if b not in want]
        errors.append(f"{where0} script: beat notes {'missing ' + ', '.join(missing) if missing else ''}"
                      f"{' unknown ' + ', '.join(extra) if extra else ''}{' out of order' if not missing and not extra else ''}")
    sl = {b["id"]: b["lines"] for b in script["beats"]}
    for b in beats:
        if b.get("lines", []) != sl.get(b["id"], []):
            errors.append(f"{where0}.{b['id']}: outline lines {b.get('lines')} differ from the script's {sl.get(b['id'])}")
    for lid, ln in script["lines"].items():
        if ln["speaker"] not in ctx["cast"]:
            errors.append(f"{where0} script {lid}: unknown speaker {ln['speaker']}")

    cpath = HERE / f"ep{n}" / "cues.json"
    if not cpath.exists():
        return
    cues = load(f"ep{n}/cues.json")
    reactions = {k for k in cues.get("reactions", {}) if not k.startswith("_")}
    targets = set(cues.get("targets", []))
    for bid in cues["beats"]:
        if bid not in want:
            errors.append(f"{where0} cues: unknown beat {bid}")
    cued = []
    for b in beats:
        bid = b["id"]
        st = steps(cues, bid)
        if not st:
            errors.append(f"{where0} cues {bid}: no cues")
            continue
        names = set()
        for s in st:
            kinds = [k for k in ("line", "do", "pause", "hold") if k in s]
            if len(kinds) != 1:
                errors.append(f"{where0} cues {bid}: a step needs exactly one of line, do, pause, hold")
            if "line" in s:
                cued.append(s["line"])
                if s["line"] not in b.get("lines", []):
                    errors.append(f"{where0} cues {bid}: line {s['line']} is not in this beat")
            if "do" in s and "seconds" not in s:
                errors.append(f"{where0} cues {bid}: a do step needs seconds")
            for v in step_visuals(s):
                names.add(visual_name(v))
                verb, arg = split_visual(v)
                if verb not in ctx["verbs"]:
                    errors.append(f"{where0} cues {bid}: unknown visual verb in {visual_name(v)!r}")
                if verb == "point_at" and arg.partition("_")[2] not in targets:
                    errors.append(f"{where0} cues {bid}: unknown target in {visual_name(v)!r}")
        for v in b.get("visual", []):
            if v not in names:
                errors.append(f"{where0} cues {bid}: outline visual {v} is not cued")
        if b.get("predict_pause") and not any(s.get("pause") == "predict" for s in st):
            errors.append(f"{where0} cues {bid}: predict_pause beat has no pause")
    if cued != list(script["lines"]):
        errors.append(f"{where0} cues: lines are not cued exactly once each, in script order")
    for e in simulate(outline, cues, ctx["objects"], ctx["cast"], reactions):
        errors.append(f"{where0} {e}")

    tpath = HERE / f"ep{n}" / "timing.json"
    if not tpath.exists():
        warnings.append(f"{where0}: no timing.json yet (run make_timing.py)")
        return
    from make_timing import build
    timing = load(f"ep{n}/timing.json")
    fresh = build(n)
    if fresh["scenes"] != timing["scenes"] or fresh["frames"] != timing["frames"]:
        errors.append(f"{where0}: timing.json is out of date (run make_timing.py)")
    return timing


def main():
    series = load("series.json")
    cast = load("cast.json")["characters"]
    objects = load("math_objects.json")["objects"]
    concepts = {k for k in series["concepts"] if not k.startswith("_")}
    threads = {k for k in series["threads"] if not k.startswith("_")}
    verbs = {k for k in series["visual_verbs"] if not k.startswith("_")}
    epistemic = set(series["epistemic"]["values"])
    paper = (HERE / series["paper"]["file"]).resolve()
    labels = set(re.findall(r"\\label\{([^}]+)\}", paper.read_text())) if paper.exists() else None
    if labels is None:
        warnings.append(f"paper not found at {paper}; labels not checked")
    ctx = {"cast": cast, "objects": objects, "verbs": verbs, "epistemic": epistemic}
    versions, subtitles = check_titles(series, ctx)
    roll, need = check_end_credits(series, ctx)
    last = max(ep["number"] for ep in series["episodes"])

    shown, named = set(), {}
    setups, payoffs = {}, {}
    conjectures, resolved = {}, set()
    leads = {k: 0 for k, c in cast.items() if c.get("principal")}
    seen_ids = set()

    for ep in series["episodes"]:
        n = ep["number"]
        outline = load(ep["outline"])
        where0 = f"ep{n}"
        if outline.get("episode") != n or outline.get("title") != ep["title"]:
            errors.append(f"{where0}: episode number or title disagrees with series.json")
        scenes = outline["scenes"]
        if scenes[0]["id"] != "s00" or scenes[0].get("kind") != "title_card":
            errors.append(f"{where0}: first scene must be s00, kind title_card")
        if scenes[-1]["id"] != "s99" or scenes[-1].get("kind") != "end_credits":
            errors.append(f"{where0}: last scene must be s99, kind end_credits")
        flags = episode_flags(scenes, outline)
        credits_extra = check_credits_scene(scenes[-1], n, last, series, roll, need, flags,
                                            f"{where0}.s99")
        required = sum(s.get("target_seconds", 0) for s in scenes if not s.get("optional"))
        everything = sum(s.get("target_seconds", 0) for s in scenes) + credits_extra
        lo, hi = ep["runtime_seconds"]
        if not lo <= required <= hi:
            errors.append(f"{where0}: required scenes budget {required:g}s, outside {lo}-{hi}s")
        if everything > hi:
            warnings.append(f"{where0}: with optional scenes the budget is {everything:g}s (> {hi}s)")
        print(f"ep{n}: {required:g}s required, {everything:g}s with optional scenes (budget {lo}-{hi}s)")
        timing = check_script_and_cues(n, outline, ctx)
        if timing:
            measured = timing["frames"] / timing["fps"]
            print(f"ep{n}: {measured:.1f}s measured from the audio and cues")
            if not lo <= measured <= hi:
                warnings.append(f"{where0}: measured runtime {measured:.1f}s is outside {lo}-{hi}s")
            for sc in scenes:
                m = timing["scenes"].get(sc["id"])
                if m and sc.get("target_seconds") and abs(m["seconds"] - sc["target_seconds"]) > 0.25 * sc["target_seconds"]:
                    warnings.append(f"{where0}.{sc['id']}: measured {m['seconds']:.1f}s, target {sc['target_seconds']:g}s")
        ep_people = set()

        for scene in scenes:
            sid = scene["id"]
            if not re.fullmatch(r"s\d\d", sid):
                errors.append(f"{where0}.{sid}: bad scene id")
            if scene.get("kind") == "title_card":
                version, sub = scene.get("main_title"), scene.get("subtitle")
                if version not in versions:
                    errors.append(f"{where0}.{sid}: main_title {version!r} is not a version in the titles screenplay")
                elif sub not in subtitles or subtitles[sub][0] != n:
                    errors.append(f"{where0}.{sid}: subtitle {sub!r} is not episode {n}'s subtitle")
                else:
                    want = versions[version] + subtitles[sub][1]
                    if abs(scene.get("target_seconds", 0) - want) > 1e-9:
                        errors.append(f"{where0}.{sid}: target_seconds should be {want:g} "
                                      f"(main title {versions[version]:g}s + subtitle {subtitles[sub][1]:g}s)")
            for who in (scene.get("lead"), scene.get("foil")):
                if who is not None and who not in cast:
                    errors.append(f"{where0}.{sid}: unknown character {who}")
            if scene.get("lead") in leads and not scene.get("optional"):
                leads[scene["lead"]] += 1
            for label in scene.get("paper", []):
                if labels is not None and label not in labels:
                    errors.append(f"{where0}.{sid}: paper label {label} not in mog.tex")

            for u in units(scene):
                uid = f"{where0}.{u['id']}"
                if uid in seen_ids:
                    errors.append(f"{uid}: duplicate id")
                seen_ids.add(uid)
                if u is not scene and not u["id"].startswith(sid + ".b"):
                    errors.append(f"{uid}: beat id must start with {sid}.b")
                ep_people.add(u.get("lead", scene.get("lead")))
                ep_people.add(u.get("foil", scene.get("foil")))
                check_common(u, uid, ctx)

                for c in u.get("shows", []):
                    if c not in concepts:
                        errors.append(f"{uid}: unknown concept {c}")
                    shown.add(c)
                for c in u.get("names", []):
                    if c not in concepts:
                        errors.append(f"{uid}: unknown concept {c}")
                    elif c not in shown:
                        errors.append(f"{uid}: names {c} before showing it")
                    elif c in named:
                        warnings.append(f"{uid}: {c} already named at {named[c]}")
                    else:
                        named[c] = uid

                for t in u.get("setup", []):
                    if t not in threads:
                        errors.append(f"{uid}: unknown thread {t}")
                    setups.setdefault(t, uid)
                for t in u.get("payoff", []):
                    if t not in threads:
                        errors.append(f"{uid}: unknown thread {t}")
                    elif t not in setups:
                        errors.append(f"{uid}: pays off {t} before it is set up")
                    payoffs.setdefault(t, uid)

                for c in u.get("conjectures", []):
                    conjectures[c["id"]] = (uid, c.get("left_open", False))
                    if c.get("by") not in cast:
                        errors.append(f"{uid}: conjecture {c['id']} by unknown character")
                for key in ("proves", "refutes"):
                    for cid in u.get(key, []):
                        if cid not in conjectures:
                            errors.append(f"{uid}: {key} {cid}, which was never conjectured")
                        resolved.add(cid)
                if u.get("refutes") and u.get("epistemic") not in ("refutation", "exhaustive_check", "proof", "example"):
                    errors.append(f"{uid}: a refutation needs a refutation, example or proof beat")

        missing = {k for k in leads} - ep_people
        if missing:
            warnings.append(f"{where0}: no lead or foil role for {', '.join(sorted(missing))}")

    for t in threads - set(setups):
        warnings.append(f"thread {t} is never set up")
    for t, uid in setups.items():
        if t not in payoffs:
            errors.append(f"{uid}: thread {t} is never paid off")
    for cid, (uid, left_open) in conjectures.items():
        if cid not in resolved and not left_open:
            errors.append(f"{uid}: conjecture {cid} is never proved or refuted")
    for who, count in leads.items():
        if count == 0:
            errors.append(f"{who} never leads a scene")
    unshown = concepts - shown
    if unshown:
        warnings.append(f"concepts never shown: {', '.join(sorted(unshown))}")
    unnamed = shown - set(named)
    if unnamed:
        warnings.append(f"concepts shown but never named: {', '.join(sorted(unnamed))}")

    for w in warnings:
        print("warning:", w)
    for e in errors:
        print("ERROR:", e)
    print(f"{len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
