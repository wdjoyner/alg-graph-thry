# MINIMOGs and Mathematical Blackjack

A 7:34 narrated animation in six chapters with end credits, based on David Joyner’s *MINIMOGs and Mathematical Blackjack*, Draft 3. The film is a 1920 × 1080 H.264 MP4 at 30 fps with AAC narration, chapter markers, and selectable English captions. The separate SRT works in players that support sidecar captions.

| File | Purpose |
|---|---|
| `minimogs-blackjack.mp4` | Finished film |
| `minimogs-blackjack.srt` | English captions |
| `narration.md` and `storyboard.md` | Full spoken script and global visual timing |
| `scenes.py` | Six Manim entry points |
| `geometry.py`, `game.py`, and `visual.py` | Diagrams, scenes, and shared presentation |
| `math_data.py` and `verify_draft3.py` | Animation data, exact example checks, and the supplied verifier |
| `production.py` and `manim.cfg` | Narration, frame extraction, and encoding |

## Render from source

Use Python 3.12, Manim Community Edition, FFmpeg and ffprobe, and DejaVu Sans. On Debian or Ubuntu, install the Cairo and Pango development headers, pkg-config, a C compiler, the DejaVu fonts, and FFmpeg. The equations and diagrams use Manim text, shapes, and transformations, so this project needs no TeX installation.

From `wdjoyner/alg-graph-thry/mog/animation`:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python math_data.py
manim --media_dir build/media -r 1920,1080 --fps 30 scenes.py \
  FanoSteiner ProjectiveLine CurtisKitten ConwayMINIMOG JohnsonGraph Blackjack EndCredits
python production.py inspect
```

For a single-scene iteration, pass only its class name to Manim. The full inspection command writes one representative frame per storyboard beat to `build/inspection/`. Review them alongside the scene MP4s in `build/media/videos/scenes/1080p30/`.

## Narration and assembly

The supplied narration is synthetic speech from Piper’s US English Lessac medium voice. If reproducing the narration, download both the [ONNX model][model] and its [configuration][config] into the same directory. The production script reads the narration Markdown, synthesizes sentences, fits them into 17-second beats, and writes the WAV and English captions. The SRT cue boundaries within long sentences are estimated from their text lengths.

```sh
python production.py narrate --model /path/to/en_US-lessac-medium.onnx
python production.py assemble
cp build/minimogs-blackjack.srt .
```

If you have the supplied narration and captions in `build/`, you can go directly to assembly. Assembly rounds each scene to its storyboard duration by trimming or padding at the final frame, then muxes the visuals, narration, captions, and chapter markers. It writes `minimogs-blackjack.mp4` in the project directory.

## Mathematical checks and credits

`python math_data.py` runs the supplied Draft 3 verifier, retained verbatim as `verify_draft3.py` (MIT), and checks the examples introduced for the visuals. This includes Fano incidences, the two generator images, the kitten subsets, tetracode completions, all winning exchanges, the played sequence, and terminality at 21. The supplied verifier exhausts the 924 six-subsets and 905 legal game positions.

Mathematical source and figure layouts adapted from David Joyner, *MINIMOGs and Mathematical Blackjack*, Draft 3 (2026), CC BY 4.0. The geometric diagrams and visual treatment were redrawn and animated in Manim.

[model]: https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
[config]: https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json

## End credits

- Video authors: [David Joyner](https://github.com/wdjoyner) and [ChatGPT](https://chatgpt.com/) ([OpenAI on GitHub](https://github.com/openai)).
- Animation package: [Manim Community Edition](https://github.com/ManimCommunity/manim).
- Mathematics: [MINIMOGs and Mathematical Blackjack, Draft 3](https://github.com/wdjoyner/alg-graph-thry/tree/main/mog).

## Planned series

Planning files for the four-episode series *Kittens, MOGs, and Mathematical Blackjack* (see [future-plans-for-kittens.md](future-plans-for-kittens.md)) are in [`series/`](series/README.md): the series bible, cast and credits, the titles and end-credits screenplays, and the episode outlines, with a checker that tests them against the mathematics.
