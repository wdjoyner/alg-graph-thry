"""Render the title and credits music from a score, and add it to the clips.

    python make_music.py --survey            # list the score's measures and their times
    python make_music.py                     # render the cues and score every clip
    python make_music.py --episodes 1        # only these episodes
    python make_music.py --variant piano_soft --episodes 1 --cues opening
                                             # try a sound from music.json "variants"

Reads music.json.  For each cue it takes the chosen measures of the score,
moves them to a harpsichord, warps time so each anchored measure lands on
its moment in the clip (the tempo changes smoothly between anchors),
renders through FluidSynth with the FluidR3 GM SoundFont, and fits the
result to the clip's exact length with gentle fades.  The silent clips
from make_titles.py are kept; the scored copies are written beside them
as epN_opening_scored.mp4 and epN_credits_scored.mp4.
"""
import argparse
import json
import statistics
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent / "build" / "series"


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def run(*args):
    subprocess.run([str(a) for a in args], check=True)


def score_file(spec):
    if not spec["source"].get("file"):
        raise SystemExit("music.json: source.file is not set yet (see its _comment)")
    path = (HERE / spec["source"]["file"]).resolve()
    if not path.exists():
        raise SystemExit(f"score not found: {path}")
    return path


def load_score(path):
    import pretty_midi
    if path.suffix.lower() in (".mid", ".midi"):
        return pretty_midi.PrettyMIDI(str(path))
    # MusicXML or another notation format: convert through music21 first.
    from music21 import converter
    with tempfile.TemporaryDirectory() as tmp:
        midi = Path(tmp) / "score.mid"
        converter.parse(str(path)).write("midi", fp=str(midi))
        return pretty_midi.PrettyMIDI(str(midi))


def measure_times(pm):
    """Downbeat times; measure m (1-based) starts at times[m - 1]."""
    times = list(pm.get_downbeats())
    times.append(pm.get_end_time())
    return times


def warp(points):
    """Piecewise-linear map from score time to clip time through (score, clip) points."""
    def f(t):
        for (s0, c0), (s1, c1) in zip(points, points[1:]):
            if t <= s1 or (s1, c1) == points[-1]:
                return c0 + (t - s0) * (c1 - c0) / (s1 - s0)
        return points[-1][1]
    return f


def build_cue(pm, times, cue, seconds, program, name, velocity_scale=1.0, reverb_send=0):
    """A new MIDI holding the cue's measures, retimed to fill `seconds`."""
    import pretty_midi
    first, last = cue["measures"]
    start, end = times[first - 1], times[last]
    points = [(start, 0.0)]
    for m, at in cue.get("anchors", []):
        if not first <= m <= last:
            raise SystemExit(f"{name}: anchor measure {m} is outside measures {first}-{last}")
        points.append((times[m - 1], float(at)))
    points.append((end, seconds))
    for (s0, c0), (s1, c1) in zip(points, points[1:]):
        if not (s1 > s0 and c1 > c0):
            raise SystemExit(f"{name}: anchors must increase in both measure and time")
    rates = [(s1 - s0) / (c1 - c0) for (s0, c0), (s1, c1) in zip(points, points[1:])]
    f = warp(points)
    out = pretty_midi.PrettyMIDI(initial_tempo=120)
    keys = pretty_midi.Instrument(program=program, name="Keys")
    # Controller 91 is each note's send to FluidSynth's reverb (0 = dry).
    keys.control_changes.append(pretty_midi.ControlChange(number=91, value=int(reverb_send), time=0.0))
    for inst in pm.instruments:
        if inst.is_drum:
            continue
        for n in inst.notes:
            if start <= n.start < end:
                vel = max(1, min(127, round(n.velocity * velocity_scale)))
                keys.notes.append(pretty_midi.Note(velocity=vel, pitch=n.pitch,
                                                   start=f(n.start), end=min(f(min(n.end, end)), seconds)))
    out.instruments.append(keys)
    return out, rates


def render(midi, seconds, cue, spec, wav):
    """FluidSynth render, then fit to exactly `seconds` with fades and loudness."""
    rate = spec["sample_rate"]
    with tempfile.TemporaryDirectory() as tmp:
        mid, raw = Path(tmp) / "cue.mid", Path(tmp) / "raw.wav"
        midi.write(str(mid))
        rv = spec.get("reverb") or {}
        room = ["-o", "synth.chorus.active=0", "-o", f"synth.reverb.active={1 if rv else 0}"]
        for key in ("room-size", "damp", "width", "level"):
            if key in rv:
                room += ["-o", f"synth.reverb.{key}={rv[key]}"]
        run("fluidsynth", "-ni", "-q", *room, "-g", "0.6", "-r", rate, "-F", raw, spec["soundfont"]["file"], mid)
        samples = round(seconds * rate)
        filters = []
        if spec.get("lowpass_hz"):
            # Two gentle poles: rolls off the buzz above the cutoff without muffling the line.
            filters += [f"lowpass=f={spec['lowpass_hz']}:p=2"]
        filters += [f"apad=whole_len={samples}", f"atrim=end_sample={samples}",
                   f"loudnorm=I={spec['loudness_lufs']}:TP=-2:LRA=11", f"aresample={rate}",
                   f"apad=whole_len={samples}", f"atrim=end_sample={samples}"]
        if cue.get("fade_in"):
            filters.append(f"afade=t=in:d={cue['fade_in']}")
        if cue.get("fade_out"):
            filters.append(f"afade=t=out:st={seconds - cue['fade_out']}:d={cue['fade_out']}")
        run("ffmpeg", "-v", "error", "-y", "-i", raw, "-af", ",".join(filters), "-ar", rate, "-ac", 2, wav)


def mux(video, wav, out):
    run("ffmpeg", "-v", "error", "-y", "-i", video, "-i", wav, "-map", "0:v", "-map", "1:a",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out)


def duration(path, stream):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", stream, "-show_entries",
                                   "stream=duration", "-of", "csv=p=0", str(path)])
    return float(out.decode().strip())


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--survey", action="store_true", help="list measures and exit")
    parser.add_argument("--episodes", type=int, nargs="*")
    parser.add_argument("--cues", nargs="*", choices=("opening", "credits"))
    parser.add_argument("--variant", help="a sound from music.json 'variants' (default: 'default_variant')")
    args = parser.parse_args()

    spec = load("music.json")
    name = args.variant or spec.get("default_variant")
    suffix = "scored" if not args.variant else f"scored_{name}"
    if name:
        if name not in spec.get("variants", {}):
            raise SystemExit(f"music.json has no variant {name!r}")
        for key, value in spec["variants"][name].items():
            if key.startswith("_"):
                continue
            if key == "fade_in":
                for cue in spec["cues"].values():
                    cue["fade_in"] = value
            else:
                spec[key] = value
    pm = load_score(score_file(spec))
    times = measure_times(pm)
    if args.survey:
        for m, (t0, t1) in enumerate(zip(times, times[1:]), 1):
            notes = sorted({n.pitch for i in pm.instruments for n in i.notes if t0 <= n.start < t1})
            print(f"m{m:3d}  {t0:7.2f}s  {t1 - t0:5.2f}s  {len(notes):2d} pitches")
        return

    series = load("series.json")
    episodes = args.episodes or [e["number"] for e in series["episodes"]]
    music = BUILD / "music"
    music.mkdir(parents=True, exist_ok=True)
    for n in episodes:
        outline = load(f"ep{n}/outline.json")
        scenes = {s["id"]: s for s in outline["scenes"]}
        for part, scene in (("opening", "s00"), ("credits", "s99")):
            if args.cues and part not in args.cues:
                continue
            cue = spec["cues"][part]
            if not cue.get("measures"):
                raise SystemExit(f"music.json: cues.{part}.measures is not set yet")
            seconds = scenes[scene]["target_seconds"]
            midi, rates = build_cue(pm, times, cue, seconds, spec["instrument"]["gm_program"], part,
                                    spec.get("velocity_scale", 1.0), spec.get("reverb_send", 0))
            med = statistics.median(rates)
            worst = max(abs(r / med - 1) for r in rates)
            if worst > spec["max_tempo_change"]:
                print(f"warning: ep{n} {part}: tempo varies {worst:.0%} between anchors "
                      f"(limit {spec['max_tempo_change']:.0%}); consider moving an anchor")
            wav = music / f"ep{n}_{part}{'' if not args.variant else '_' + name}.wav"
            render(midi, seconds, cue, spec, wav)
            video = BUILD / f"ep{n}_{part}.mp4"
            out = BUILD / f"ep{n}_{part}_{suffix}.mp4"
            mux(video, wav, out)
            a, v = duration(out, "a:0"), duration(out, "v:0")
            ok = abs(a - seconds) < 0.03 and abs(v - seconds) < 0.03
            print(f"{out.name}: video {v:.2f}s, music {a:.2f}s, outline {seconds:g}s, "
                  f"played at {med:.2f} times the score's speed  {'ok' if ok else 'LENGTH MISMATCH'}")
            if not ok:
                raise SystemExit("length mismatch")


if __name__ == "__main__":
    main()
