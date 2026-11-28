"""Render an episode's body, give it its dialogue, and assemble the episode.

    python make_episode.py --episode 1 --draft     # 960 x 540, for a look
    python make_episode.py --episode 1             # 1920 x 1080

Before this, in this folder:

    python make_voices.py --episode 1    # the dialogue clips and audio_manifest.json
    python make_timing.py --episode 1    # timing.json, from the cues and the clips
    python check_outline.py              # everything agrees
    python make_titles.py && python make_music.py   # the scored opening and credits

Steps, all written to ../build/series/:
  1. Renders episode_scenes.py's EpisodeN (the body, scenes s01 onward)
     and checks its frame count against timing.json.
  2. Lays every dialogue clip on its line's first frame (timing.json) into
     one track, brought to -16 LUFS (the music sits near -26 LUFS).
  3. Writes epN_body.mp4 (picture and dialogue) and epN.srt (captions in
     the script's written form, timed to the assembled episode).
  4. If epN_opening_scored.mp4 and epN_credits_scored.mp4 exist (from
     make_titles.py and make_music.py), joins opening, body and credits
     into epN.mp4 with the captions as a subtitle track, and checks the
     total length against timing.json.  A contact sheet of the body goes
     to contact/.

Needs what the titles need (Manim CE 0.19, FFmpeg, Cairo and Pango), PAM
with pam/cat.py (set PAM_DIR if 'import pam' does not find it) and numpy.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent / "build" / "series"
FPS = 30
RATE = 48000
DIALOGUE_LUFS = -16.0


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def run(*cmd, **kw):
    print("+", " ".join(str(c) for c in cmd))
    subprocess.run([str(c) for c in cmd], check=True, **kw)


def frames(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
                          "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(path)],
                         check=True, capture_output=True, text=True).stdout
    return int(out.strip())


def read_wav(path):
    with wave.open(str(path), "rb") as w:
        rate = w.getframerate()
        data = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32767
    if rate != RATE:                      # linear resample, plenty for speech
        t = np.arange(int(len(data) * RATE / rate)) * rate / RATE
        data = np.interp(t, np.arange(len(data)), data)
    return data


def measured_lufs(path):
    """Integrated loudness (EBU R128) of a sound file, from FFmpeg."""
    out = subprocess.run(["ffmpeg", "-nostats", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    vals = [line.split("I:")[1].split()[0] for line in out.splitlines() if line.strip().startswith("I:")]
    return float(vals[-1])


def write_mono(path, track):
    pcm = (np.clip(track, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(pcm.tobytes())


def dialogue_track(n, timing, out):
    total = int(round(timing["body_frames"] / FPS * RATE))
    track = np.zeros(total, dtype=np.float32)
    audio_dir = BUILD / f"ep{n}" / "audio"
    for lid, ln in timing["lines"].items():
        clip = read_wav(audio_dir / f"{lid}.wav")
        a = int(round(ln["start"] / FPS * RATE))
        b = min(total, a + len(clip))
        track[a:b] += clip[:b - a]
    # bring the dialogue to -16 LUFS (the music sits near -26), measured by FFmpeg;
    # a soft knee keeps the rare loud peak under full scale
    write_mono(out, track)
    track *= 10 ** ((DIALOGUE_LUFS - measured_lufs(out)) / 20)
    track = np.where(np.abs(track) > 0.8, np.sign(track) * (0.8 + 0.2 * np.tanh((np.abs(track) - 0.8) / 0.2)), track)
    write_mono(out, track)
    print(f"dialogue: {measured_lufs(out):.1f} LUFS")


def srt_time(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def write_srt(n, timing, out, offset_frames):
    manifest = load(f"ep{n}/audio_manifest.json")["lines"]
    cast = load("cast.json")["characters"]
    rows = []
    for k, (lid, ln) in enumerate(sorted(timing["lines"].items(), key=lambda kv: kv[1]["start"]), 1):
        a = (ln["start"] + offset_frames) / FPS
        b = (ln["start"] + offset_frames + ln["audio_frames"]) / FPS + 0.3
        who = cast[ln["speaker"]]["name"].upper()
        rows.append(f"{k}\n{srt_time(a)} --> {srt_time(b)}\n{who}: {manifest[lid]['text']}\n")
    out.write_text("\n".join(rows), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--episode", type=int, default=1)
    ap.add_argument("--draft", action="store_true", help="render at 960 x 540")
    ap.add_argument("--skip-render", action="store_true", help="reuse the last body render")
    args = ap.parse_args()
    n = args.episode
    timing = load(f"ep{n}/timing.json")
    width, height = (960, 540) if args.draft else (1920, 1080)
    BUILD.mkdir(parents=True, exist_ok=True)
    media = BUILD / "media"
    silent = media / "videos" / "episode_scenes" / f"{height}p{FPS}" / f"Episode{n}.mp4"
    if not args.skip_render:
        env = dict(os.environ, EPISODE=str(n))
        run("manim", "render", "--disable_caching", "-r", f"{width},{height}", "--fps", FPS,
            "--media_dir", media, HERE / "episode_scenes.py", f"Episode{n}", cwd=HERE, env=env)
    got, want = frames(silent), timing["body_frames"]
    print(f"body: {got} frames, timing.json says {want}: {'ok' if got == want else 'MISMATCH'}")
    if got != want:
        sys.exit(1)

    wav = BUILD / f"ep{n}_dialogue.wav"
    dialogue_track(n, timing, wav)
    body = BUILD / f"ep{n}_body.mp4"
    run("ffmpeg", "-v", "error", "-y", "-i", silent, "-i", wav, "-map", "0:v", "-map", "1:a",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", RATE, "-ac", "2", "-shortest", body)

    contact = BUILD / "contact"
    contact.mkdir(exist_ok=True)
    run("ffmpeg", "-v", "error", "-y", "-i", silent, "-vf",
        "fps=1/5,scale=384:-1,tile=6x14:padding=4:color=white", "-frames:v", "1",
        contact / f"ep{n}_body.png")

    opening = BUILD / f"ep{n}_opening_scored.mp4"
    credits = BUILD / f"ep{n}_credits_scored.mp4"
    if not (opening.exists() and credits.exists()):
        write_srt(n, timing, BUILD / f"ep{n}_body.srt", 0)
        print(f"wrote {body.name} and ep{n}_body.srt; run make_titles.py and make_music.py to assemble the episode")
        return
    srt = BUILD / f"ep{n}.srt"
    write_srt(n, timing, srt, timing["body_offset_frames"])
    full = BUILD / f"ep{n}.mp4"
    parts = [opening, body, credits]
    inputs = [x for p in parts for x in ("-i", p)]
    vf = "".join(f"[{i}:v]scale={width}:{height},setsar=1,fps={FPS}[v{i}];" for i in range(3))
    af = "".join(f"[{i}:a]aformat=sample_rates={RATE}:channel_layouts=stereo[a{i}];" for i in range(3))
    concat = "".join(f"[v{i}][a{i}]" for i in range(3)) + "concat=n=3:v=1:a=1[v][a]"
    run("ffmpeg", "-v", "error", "-y", *inputs, "-i", srt, "-filter_complex", vf + af + concat,
        "-map", "[v]", "-map", "[a]", "-map", "3:s", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-c:s", "mov_text",
        "-metadata:s:s:0", "language=eng", full)
    got, want = frames(full), timing["frames"]
    print(f"{full.name}: {got} frames = {got / FPS:.1f}s, timing.json says {want}: {'ok' if got == want else 'MISMATCH'}")


if __name__ == "__main__":
    main()
