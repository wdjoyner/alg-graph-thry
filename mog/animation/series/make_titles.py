"""Render the series titles and end credits, and assemble them per episode.

    python make_titles.py                 # 1920 x 1080, every episode
    python make_titles.py --draft         # 960 x 540, faster
    python make_titles.py --episodes 1 3  # only these episodes
    python make_titles.py --with-optional # include cards for optional scenes

Writes, in ../build/series/:
    epN_opening.mp4   main title + episode N's subtitle  (scene s00)
    epN_credits.mp4   credits roll + episode N's tail      (scene s99)
    contact/*.png     one contact sheet per clip, for review

Each assembled clip's frame count is checked against the outline's
target_seconds for that scene.  The clips are silent: no music is
chosen yet.
"""
import argparse
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent / "build" / "series"
FPS = 30


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def run(*args):
    subprocess.run([str(a) for a in args], check=True)


def frames(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
                                   "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", str(path)])
    return int(out.decode().strip().rstrip(","))


def scene_flags(outline, with_optional):
    """'when' flags whose cards play in this episode's credits."""
    flags = set()
    for scene in outline["scenes"]:
        for u in scene.get("beats") or [scene]:
            optional = scene.get("optional") or u.get("optional")
            people = {u.get("lead", scene.get("lead")), u.get("foil", scene.get("foil"))}
            for c in u.get("cameos", []):
                if with_optional or not c.get("optional"):
                    people.add(c["who"])
            if optional and not with_optional:
                continue
            flags |= people
    flags |= set(outline.get("uses", []))
    return {f for f in flags if f in ("pam",)}


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--draft", action="store_true", help="render at 960 x 540")
    parser.add_argument("--episodes", type=int, nargs="*")
    parser.add_argument("--with-optional", action="store_true",
                        help="include credits cards for characters who appear only in optional scenes")
    args = parser.parse_args()

    series = load("series.json")
    episodes = args.episodes or [e["number"] for e in series["episodes"]]
    outlines = {e["number"]: load(e["outline"]) for e in series["episodes"]}
    width, height = (960, 540) if args.draft else (1920, 1080)

    plan = {}
    for n in episodes:
        scenes = {s["id"]: s for s in outlines[n]["scenes"]}
        flags = scene_flags(outlines[n], args.with_optional)
        roll = "CreditsRollPam" if "pam" in flags else "CreditsRoll"
        opening = ["MainTitle" if scenes["s00"]["main_title"] == "full" else "MainTitleShort", f"Subtitle{n}"]
        plan[n] = {"opening": opening, "credits": [roll, f"Tail{n}"],
                   "flags": flags, "s00": scenes["s00"]["target_seconds"], "s99": scenes["s99"]["target_seconds"]}

    classes = sorted({c for p in plan.values() for c in p["opening"] + p["credits"]})
    media = BUILD / "media"
    run("manim", "render", "--disable_caching", "-r", f"{width},{height}", "--fps", FPS,
        "--media_dir", media, HERE / "title_scenes.py", *classes)
    videos = media / "videos" / "title_scenes" / f"{height}p{FPS}"

    contact = BUILD / "contact"
    contact.mkdir(parents=True, exist_ok=True)
    problems = []
    for n, p in plan.items():
        for part in ("opening", "credits"):
            listing = BUILD / f"ep{n}_{part}.txt"
            listing.write_text("".join(f"file '{(videos / (c + '.mp4')).as_posix()}'\n" for c in p[part]))
            out = BUILD / f"ep{n}_{part}.mp4"
            run("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", listing,
                "-c", "copy", "-movflags", "+faststart", out)
            want = p["s00"] if part == "opening" else p["s99"]
            got = frames(out)
            status = "ok" if got == round(want * FPS) else "WRONG LENGTH"
            if status != "ok":
                problems.append(out.name)
            print(f"{out.name}: {got} frames = {got / FPS:g}s (outline {want:g}s) {status}")
            run("ffmpeg", "-v", "error", "-y", "-i", out, "-vf",
                "fps=1,scale=384:-1,tile=6x10:padding=4:color=white", "-frames:v", "1",
                contact / f"ep{n}_{part}.png")
    if problems:
        raise SystemExit(f"Length check failed: {', '.join(problems)}")
    print(f"All clips match their outlines.  Output in {BUILD}")


if __name__ == "__main__":
    main()
