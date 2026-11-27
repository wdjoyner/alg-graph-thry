# Kittens, MOGs, and Mathematical Blackjack: series files

Planning files for the four-episode series described in [future-plans-for-kittens.md](../future-plans-for-kittens.md). The outlines here come first; the Fountain screenplays are written from them, and the JSON animation cues come after the screenplays.

| File | What it holds |
|---|---|
| `series.json` | Series title, episode list and runtime budgets, title-card and credits layout, and the shared vocabulary: concepts, plot threads, visual verbs, epistemic labels |
| `cast.json` | The kittens and Professor Euphemia: designs, personalities, Kokoro audition candidates. Recasting happens here only |
| `pronunciation.json` | Spoken respellings applied before text-to-speech (captions keep the written form) |
| `credits.json` | End credits shared by all four episodes. Series authors: David Joyner, Claude (Anthropic), ChatGPT (OpenAI) |
| `math_objects.json` | Every hand, move and count the outlines mention. **Generated; do not edit** |
| `build_math_objects.py` | Writes `math_objects.json`. `--cross-check` also compares the hexads with the paper's `verify.py` |
| `check_outline.py` | Checks all four outlines against the files above |
| `titles/outline.json` | Titles screenplay: the series main title and one subtitle card per episode; music candidates |
| `end_credits/outline.json` | End-credits screenplay: the credits cards in order, how each is staged, and the tail card (next time, or the finale) |
| `ep1/outline.json` | Episode 1, broken down to beats |
| `ep2/`–`ep4/outline.json` | Episodes 2–4, broken down to scenes; beats to come |

## Workflow

```sh
python build_math_objects.py --cross-check   # after changing any example
python check_outline.py                      # after changing any outline
```

1. Outline all four episodes at scene level, so plants and payoffs line up across the series (done).
2. Break one episode into beats (Episode 1 done).
3. Write that episode's `epN/script.fountain`, putting a `[[beat: sNN.bMM]]` note on each beat and giving each dialogue line a stable ID in the beat's `lines` list.
4. Write `epN/cues.json`, keyed by beat ID, using the visual verbs in `series.json`.
5. Generate audio per line, measure it, and let the clip lengths set the timing.

## Outline format

Every episode starts with scene `s00` (kind `title_card`) and ends with `s99` (kind `end_credits`). Their text comes from `series.json` and `credits.json`, so a retitle or a credits change is made in one place.

Scene `s00` names a version of the main title and the episode's subtitle from `titles/outline.json`, and its `target_seconds` must equal their combined length. The main title runs 20 seconds: the deck fans out, flies into the MINIMOG, slides into Curtis's kitten, and the hexad 1–6 shrinks to a dot that sprouts its 36 neighbors. Then the series title writes itself along those edges. Each step is one episode's picture. Every episode uses the full version. A short version (8 seconds) keeps the fan, the fly-in and the title, in case it's needed later. Each subtitle (6 seconds) picks up from the main title's last frame with its own episode's picture. The titles have no dialogue, so their timing is fixed in seconds. Any text must stay on screen for at least 4 seconds.

A scene is either broken into `beats`, or, while `beats` is empty, outlined at scene level with the same fields:

| Field | Meaning |
|---|---|
| `id` | `sNN` for scenes, `sNN.bMM` for beats. Never renumber; add a suffix (`s03.b02a`) instead |
| `lead`, `foil` | Characters from `cast.json`. A beat inherits its scene's unless it says otherwise |
| `purpose` / `summary` | What the beat or scene is for |
| `epistemic` | What it claims to do: `observation`, `experiment`, `conjecture`, `example`, `exhaustive_check`, `proof`, and so on |
| `shows`, `names` | Concepts from `series.json`. A concept may be named only in or after a beat that shows it |
| `setup`, `payoff` | Threads from `series.json`; each setup must be paid off later |
| `conjectures`, `proves`, `refutes` | Every conjecture must be resolved, or marked `left_open` |
| `establishes` | Results the beat proves. Allowed only in `proof` and `exhaustive_check` beats |
| `math` | Objects from `math_objects.json` and the field values the beat relies on |
| `visual` | `verb` or `verb:argument`, using the verbs in `series.json` |
| `predict_pause` | Pause for viewers to guess before the answer |
| `paper` | `\label`s in `mog.tex` (stable across drafts) |
| `optional` | Scene can be cut for runtime; required scenes alone must fit the budget |
| `gist`, `lines` | Sketch of the dialogue; line IDs once the script exists |

Scene `s99` plays the end-credits screenplay, then a tail: `next_time` (Episodes 1–3) shows the next episode's subtitle picture, and `finale` (Episode 4) closes the series. Wording lives in `credits.json`; staging and timing live in the screenplay. Each card stays up at least 1 second plus 1 second per 4 words (never under 3 seconds). The Professor Euphemia card plays only where she appears. Episodes 1 and 4 use her only in optional moments, so her card counts toward their optional time. Credits run about 52 seconds.

With titles and credits included, the required scenes run 7:34, 9:46, 9:14 and 9:14, and the optional scenes bring that to 8:00, 9:46, 9:59 and 9:55.

## Threads across the series

| Thread | Set up | Paid off |
|---|---|---|
| Why do 21 and 45 both lose? | Ep 1 s04 | Ep 4 s06 |
| The losing hands look special | Ep 1 s06 | Ep 2 s07 (they are hexads), Ep 4 s06 (why hexads lose) |
| Skill or luck? | Ep 1 s03 | Ep 4 s07 |
| Pascal's 7 → 5 | Ep 1 s03 | Ep 3 s06 |
| Every dead end at 21 is special | Ep 1 s04 | Ep 4 s08 |
| No memorizing | Ep 2 s08 | Ep 3 s01 |
| Why does repairing win? | Ep 3 s08 | Ep 4 s06 |
