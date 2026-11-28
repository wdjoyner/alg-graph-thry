"""Speak every dialogue line of an episode with Kokoro and measure it.

    python make_voices.py --episode 1          # synthesize changed lines
    python make_voices.py --episode 1 --force  # synthesize every line

Reads epN/script.fountain (through script_tools.py), the chosen voices and
speeds in cast.json, and the respellings in pronunciation.json.  Writes one
WAV per line to ../build/series/epN/audio/<line id>.wav, and the manifest
epN/audio_manifest.json: for every line its speaker, voice, speed, the
spoken text, the clip's length in seconds and a mouth envelope (how open
the speaker's mouth is on each 30 fps frame, 0 to 100, from the clip's
loudness).  The manifest is small and is kept in the repository, so the
timing (make_timing.py) can be rebuilt without Kokoro.

A line is synthesized again only if its spoken text, voice or speed has
changed, or its WAV is missing.  A recast in cast.json therefore
regenerates exactly that character's lines.

Engines, in order of preference:
  * kokoro (pip install kokoro), the PyTorch package the Haynes film uses;
  * kokoro-onnx (pip install kokoro-onnx), the same Kokoro-82M v1.0 model
    run with ONNX Runtime.  It needs the model files kokoro-v1.0.onnx and
    voices-v1.0.bin (github.com/thewh1teagle/kokoro-onnx, release
    model-files-v1.0); point --onnx-dir or KOKORO_ONNX_DIR at their folder.
"""
import argparse
import json
import os
import re
import sys
import wave
from pathlib import Path

import numpy as np

from script_tools import parse

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent / "build" / "series"
SAMPLE_RATE = 24000
FPS = 30


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def respell(text, table):
    """Apply pronunciation.json's respellings, longest key first."""
    for key in sorted(table, key=len, reverse=True):
        if re.match(r"\w", key[0]) and re.match(r"\w", key[-1]):
            text = re.sub(rf"(?<!\w){re.escape(key)}(?!\w)", table[key], text)
        else:
            text = text.replace(key, table[key])
    return text


class Engine:
    def __init__(self, onnx_dir=None):
        self.name = None
        try:
            from kokoro import KPipeline
            self.pipeline = KPipeline(lang_code="a")
            self.name = "kokoro"
            return
        except Exception:
            pass
        from kokoro_onnx import Kokoro
        d = Path(onnx_dir or os.environ.get("KOKORO_ONNX_DIR", HERE.parent / "models"))
        self.onnx = Kokoro(str(d / "kokoro-v1.0.onnx"), str(d / "voices-v1.0.bin"))
        self.name = "kokoro-onnx"

    def speak(self, text, voice, speed):
        if self.name == "kokoro":
            parts = [np.asarray(a, dtype=np.float32) for _, _, a in
                     self.pipeline(text, voice=voice, speed=speed)]
            return np.concatenate(parts)
        audio, sr = self.onnx.create(text, voice=voice, speed=speed, lang="en-us")
        assert sr == SAMPLE_RATE
        return np.asarray(audio, dtype=np.float32)


def write_wav(path, audio):
    pcm = np.clip(audio, -1, 1)
    pcm = (pcm * 32767).astype("<i2")
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(pcm.tobytes())


def read_wav(path):
    with wave.open(str(path), "rb") as w:
        data = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2")
    return data.astype(np.float32) / 32767


def envelope(audio):
    """Mouth openness per 30 fps frame, 0..100, from short-time loudness."""
    hop = SAMPLE_RATE // FPS
    n = int(np.ceil(len(audio) / hop))
    rms = np.array([np.sqrt(np.mean(audio[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(n)])
    db = 20 * np.log10(rms + 1e-9)
    top = np.percentile(db, 95) if n else 0
    open_ = np.clip((db - (top - 30)) / 30, 0, 1)        # 30 dB window under the loud parts
    return [int(round(100 * v)) for v in open_]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--episode", type=int, default=1)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--onnx-dir")
    args = ap.parse_args()

    ep = f"ep{args.episode}"
    script = parse(HERE / ep / "script.fountain")
    if script["errors"]:
        sys.exit("script errors:\n  " + "\n  ".join(script["errors"]))
    cast = load("cast.json")["characters"]
    table = load("pronunciation.json")["respell"]
    reserved = set(load("cast.json").get("reserved_voices", {}))
    out_dir = BUILD / ep / "audio"
    man_path = HERE / ep / "audio_manifest.json"
    old = json.loads(man_path.read_text())["lines"] if man_path.exists() else {}

    engine = None
    lines = {}
    made = 0
    for lid, ln in script["lines"].items():
        who = ln["speaker"]
        if who not in cast:
            sys.exit(f"{lid}: unknown speaker {who}")
        v = cast[who]["voice"]
        voice, speed = v["chosen"], v.get("speed", 1.0)
        if voice in reserved:
            sys.exit(f"{lid}: voice {voice} is reserved")
        spoken = respell(ln["text"], table)
        wav = out_dir / f"{lid}.wav"
        prev = old.get(lid, {})
        same = (prev.get("spoken") == spoken and prev.get("voice") == voice
                and prev.get("speed") == speed and wav.exists())
        if same and not args.force:
            audio = read_wav(wav)
            engine_name = prev.get("engine")
        else:
            if engine is None:
                engine = Engine(args.onnx_dir)
                print(f"engine: {engine.name}")
            audio = engine.speak(spoken, voice, speed)
            write_wav(wav, audio)
            engine_name = engine.name
            made += 1
            print(f"  {lid} {who:7} {len(audio) / SAMPLE_RATE:5.2f}s  {spoken}")
        lines[lid] = {
            "speaker": who, "voice": voice, "speed": speed, "engine": engine_name,
            "text": ln["text"], "spoken": spoken,
            "seconds": round(len(audio) / SAMPLE_RATE, 4),
            "mouth": envelope(audio),
        }
    manifest = {
        "_about": [
            "Generated by make_voices.py; do not edit by hand.",
            "seconds is each clip's measured length; make_timing.py builds the episode's timing from it.",
            "mouth is the speaker's mouth openness on each 30 fps frame of the clip, 0 to 100.",
            f"Clips: ../build/series/{ep}/audio/<line id>.wav, mono, {SAMPLE_RATE} Hz.",
        ],
        "episode": args.episode,
        "sample_rate": SAMPLE_RATE,
        "fps": FPS,
        "lines": lines,
    }
    text = json.dumps(manifest, indent=1, ensure_ascii=False)
    # keep each envelope on one line
    text = re.sub(r'"mouth": \[\s*([\d,\s]*?)\s*\]',
                  lambda m: '"mouth": [' + ",".join(m.group(1).split()).replace(",,", ",") + "]", text)
    man_path.write_text(text + "\n", encoding="utf-8")
    total = sum(l["seconds"] for l in lines.values())
    print(f"{len(lines)} lines, {made} synthesized, {total:.1f}s of dialogue -> {man_path.relative_to(HERE)}")


if __name__ == "__main__":
    main()
