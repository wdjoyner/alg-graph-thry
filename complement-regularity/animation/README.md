# Which symmetric groups have a complement?

A 7:12 narrated animation based on David Joyner’s *Which Sₘ have a complement in Sₙ?*, Draft 6. The film is a 1920 × 1080 H.264 MP4 at 30 fps with AAC narration, six chapter markers, and selectable English captions. The separate SRT can also be loaded in a video player.

| File | Purpose |
| --- | --- |
| [MP4](complement-regularity.mp4) | Finished film |
| [English subtitles](complement-regularity.srt) | SRT sidecar |
| [Source archive](complement-regularity-animation-source.zip) | Production source, script, storyboard, captions, and paper verifiers |
| [Narration](narration.md) and [storyboard](storyboard.md) | Spoken text and beat timings |
| `scenes.py`, `algebra.py`, `factorization.py`, `graph_scenes.py` | Six Manim scenes |
| `math_data.py`, `visual.py`, `timeline.py` | Verified diagram data, shared styling, and timing |
| `production.py`, `manim.cfg` | Narration, representative frame extraction, assembly, and media checks |

## Render and assemble

Use Python 3.12, FFmpeg and ffprobe, and DejaVu Sans. On Debian or Ubuntu, install the Cairo and Pango development headers, pkg-config, a C compiler, and the DejaVu fonts. Manim draws the diagrams with text and vector shapes, so the project needs no TeX installation.

From `complement-regularity/animation`, or from `animation` inside the extracted archive:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python math_data.py
manim scenes.py CubeStorage SharpTransitivity Classification ThreeFactors CayleyGraphs ForgettingOrder
python production.py inspect
```

The inspection command extracts a 960 × 540 frame from every beat into `build/inspection/`. Review those frames alongside the scene files in `build/media/videos/scenes/1080p30/`. To preview a single scene, pass its class name to Manim, optionally with `-ql --media_dir build/preview`.

The synthetic narration uses Piper’s US English Lessac medium voice, following the MINIMOG production. Download the model and its JSON configuration into the same directory and keep their original filenames. The script synthesizes sentences, adjusts their tempo to fit the storyboard when needed, and timestamps captions against the synthesized clips. Long sentences are divided into reading-length cues with subcue timings estimated by text length. [Voice model][voice] · [JSON configuration][config]

```sh
python production.py narrate --model /path/to/en_US-lessac-medium.onnx
cp build/complement-regularity.srt .
python production.py assemble
python production.py verify
```

Assembly normalizes the scene lengths to 72 seconds and muxes the six scenes with narration, chapters, and English subtitles. Verification reads the final container, checks the encoding and duration, measures the decoded audio in each chapter, and compares the embedded captions to the sidecar.

## Mathematical verification

```sh
python math_data.py
python ../scripts/verify_generators.py
OPENBLAS_NUM_THREADS=1 python ../scripts/verify_graph_section.py
python ../scripts/verify_examples_draft6.py
```

The animation checks all six products in the S₃ grid, the affine action on the twenty pairs, the worked S₁₂ permutation and all 11,880 possible ordered quadruple images, the affine Cayley edge set, and every fiber and neighborhood lift for the double cover. The same data drive the diagrams. Products act rightmost first.

The paper’s generator verifier computes orders and tuple orbits for the groups in degrees 10, 11, and 12. Its graph script includes numerical checks of spectra and finite computations of examples. The film’s general equivalence, three-factor uniqueness, and covering argument come from the paper’s proofs. The degree restrictions are cited classical results attributed to Zassenhaus and Jordan via Cameron and Dixon–Mortimer. The full arrangement-graph automorphism group and the six extra Cayley cases are attributed to Yin, Feng, Zhou, and Guo (2021). Draft 6 records that the classical classification had yet to be matched to specific textbook pages and that the graph classification was quoted from the abstract. The finite computations establish the examples they check.

Mathematics and the cuboctahedral layout come from the paper. The MINIMOG animation supplied the chapter pacing, production structure, and the basis for the narration and assembly script. The cube and all graphs were drawn in Manim. [Draft 6][paper] · [MINIMOG production][mog]

[paper]: https://github.com/wdjoyner/alg-graph-thry/blob/72357ccbccc80aa6a2aa976e5466e7cd757269f6/complement-regularity/complement-regularity.tex
[mog]: https://github.com/wdjoyner/alg-graph-thry/tree/72357ccbccc80aa6a2aa976e5466e7cd757269f6/mog/animation
[voice]: https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
[config]: https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
