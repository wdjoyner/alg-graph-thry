# Kittens, MOGs, and Mathematical Blackjack

*Four adventures in finite geometry*: planning files for the four-episode series described in [future-plans-for-kittens.md](../future-plans-for-kittens.md).

The series is a mathematical mystery. Episode 1 poses it: in a twelve-card game, why do two hands with totals as different as 21 and 45 both lose? Each later episode uncovers part of the answer, and Episode 4 solves it. This page tells the story as the outlines have it. The outlines themselves (`ep1/` to `ep4/outline.json`, plus the titles and end-credits screenplays) are the authoritative version, and `check_outline.py` checks every card, total and count in them against the mathematics.

**The kittens:** Pascal, an orange tabby, card shark and bold conjecturer. Sophie, a tuxedo who thinks in pictures. Ada, a gray skeptic who checks everything. Euler, cream-colored, absent-minded, fond of symmetry and proofs. Optionally, Professor Euphemia, an older calico who answers questions with questions.

## The story

### Main title (every episode, 20 seconds)

A deck of twelve cards fans out face up, 0 through 11, with a flick of Pascal's paw. The cards fly into their cells of Conway's 3 × 4 MINIMOG, and Ada straightens the last one. The cells slide into Curtis's kitten, a triangle with corners 0, 1 and 6, and Sophie traces its last side with her tail. The cards 1 to 6 light up, shrink into a single dot, and 36 edges sprout from it while Euler leans in. Along those edges the title writes itself, **Kittens, MOGs, and Mathematical Blackjack**, as all four kittens pounce on the letters. The tagline follows: *Four adventures in finite geometry*.

Each step is one episode's picture, so the opening previews the whole series. A 6-second subtitle card then names the episode, over that episode's own picture.

### Episode 1: The Curious Game of Twenty-One

*Lead: Pascal.* Subtitle: the dot bursts back into cards, which deal themselves into the hand the episode begins with.

**Pascal deals.** Pascal announces blackjack. Sophie asks where the kings are. Ada points out that there are twelve cards, numbered 0 to 11: she counted. Six go face up into one hand that both players share, and the other six form the pile.

**The rules.** A move gives the hand one card and takes a smaller card from the pile, so the total only goes down. The new total must stay at 21 or more. Pascal tries to swap 11 for 1, and Ada stops him: that makes 20. A player with no legal move loses. Ada notes that every game must end, because the total keeps falling.

**A worked game.** The hand is {0, 2, 4, 6, 7, 11}, total 30, with fourteen legal moves. *Viewers are asked which they would play.* Pascal swaps 7 for 5 (28). Ada swaps 11 for 7 (24). Pascal swaps 6 for 3 (21), and Ada finds no smaller card that keeps the total at 21. Pascal wins. Euler asks whether that was skill or luck. "Skill. Obviously," says Pascal. Ada: "Prove it." *(Clue: Pascal's opening move, 7 for 5.)*

**The dead hand and its shadow.** Sophie deals 1, 2, 3, 4, 5, 6: total 21, no moves, and the player to move loses at once. Pascal notes that every time they hit 21, it's over. Euler swaps the hand with the pile. The complement, {0, 7, 8, 9, 10, 11}, totals 45 and has thirty legal moves. Pascal grabs it: "This one's mine." He tries 10 for 1, and Ada answers 7 for 3. He tries 11 for 1, and she answers 10 for 4. In a montage, game after game ends with Pascal stuck. Ada points out that they have tried only a handful of thirty moves, which makes this an experiment. Sophie poses the mystery: **21 loses and 45 loses. Why would those two be the same?**

**Pascal's conjecture.** Pascal has an answer: 21 and 45 are the bad totals, and anything in between wins. Euler: "That's a conjecture." Ada deals {0, 1, 2, 4, 7, 10}, total 24, right in between, and lets Pascal move. The hand has only five legal moves. All five fan out on screen as branches, and each has a reply that lands on exactly 21. Ada: "Five moves, five answers. I checked them all. That's not luck. It's a proof, for this hand." The conjecture falls, and the difference between experiment and proof gets its name.

**Special hands.** Sophie lines up the losing hands: 1 to 6, the 21 that ended the worked game, and the 24-hand. The 45-hand gets a question mark, because it was only tested. "They look special. But special how?" Euler wonders whether the 28 Pascal left Ada was one of them. Pascal says it was, naturally, though it's clear he doesn't know.

**A question to take home** *(optional)*. Professor Euphemia: when the same sets keep turning up, ask what they have in common, and sometimes a picture helps. Without her, Sophie says she needs to draw this.

### Episode 2: The Geometry of a Kitten

*Lead: Sophie.* Subtitle: the camera pushes into the kitten triangle.

**Special how?** A quick replay of Episode 1's line-up. Sophie needs a picture.

**Seven points.** The Fano plane: seven points and seven lines, and the circle counts as a line. Pick points 1 and 4 and their line supplies 2. Pick 4 and 5 and the circle supplies 6. Pascal objects that a circle can't be a line; Sophie says it obeys the rule.

**Twelve points, five at a time.** Sophie reads S(2,3,7) aloud, then asks for S(5,6,12): twelve points, where every five lie in exactly one six-point block. Counting settles the size. There are 792 five-point sets and each block contains six of them, so there must be 132 blocks. They are named **hexads**. Ada: "If such a thing exists."

**Two moves on a ring.** Euler arranges twelve labels on a ring: 0 to 10 mod 11, plus infinity. The seed is 0 together with the five nonzero squares. Two moves, adding one and taking the negative reciprocal, keep producing new six-point sets until the collection closes at exactly 132. Delete each point from each block and every five-point set appears exactly once. The design exists, and Ada's doubt is answered.

**Curtis's kitten.** The triangular kitten, with a 3 × 3 grid at each corner. Rows, columns and two wrapped diagonal directions are lines. (The wrapping is arithmetic mod 3; it is shown here and named in Episode 3.) A row plus a column makes a cross, and the four points left over make a square.

**Four families.** A line plus the three corners, two parallel lines, a cross plus its own corner, a square plus the other two corners: 12 + 12 + 54 + 54 = 132, the same blocks the ring produced. Two pictures, one object.

**Back to the cards.** Relabel the points as card values, and Episode 1's losing hands light up as hexads: 1 to 6, the 24-hand, the end of the worked game, and the 45-hand too. Euler's guess holds: the 28 Pascal left Ada is a hexad. *(Partial payoff: the special hands are hexads. Why hexads lose is still open.)*

**No memorizing.** Pascal proposes memorizing all 132 so he never loses. Ada: "Absolutely not." *(Clue.)*

### Episode 3: The Secret Code of the MINIMOG

*Lead: Ada.* Subtitle: the MINIMOG returns, and the codeword 1, 1, 2, 0 lights one cell in each column.

**Twelve cells.** True to her word, Ada doesn't memorize. She sends the twelve cards into Conway's 3 × 4 MINIMOG.

**A three-hour clock.** Arithmetic mod 3 on a clock with three hours. Sophie recognizes it as the diagonals that wrapped around in the kitten.

**Nine words.** Choose a and b mod 3, and the word is (b, a, a+b, a+2b). That gives nine words, the tetracode. *Viewers build the one for a = b = 1.* Any two coordinates pin down the whole word, which is Ada's favorite property.

**Odd man out.** Mark a hand in the grid. A column with one card gives that card's row, and a column with two gives the missing row. Empty and full columns are wildcards. The rows must fit one tetracode word, and column counts of 0, 1, 2 and 3 are always rejected.

**Test the hands.** Episode 1's opening hand reads 1, 1, 2, 2. Its first two coordinates force the word 1, 1, 2, 0, and the last coordinate disagrees, so it is not a hexad. The hand 1 to 6 is all wildcards, so it is one. The 24-hand Ada left Pascal in the worked game has the forbidden counts. (The test is shown on examples; the paper proves it always agrees with the design.)

**Repair.** Which single swaps turn the opening hand into a hexad? There are six: three up (0 for 1, 2 for 10, 6 for 8) and three down (4 for 3, 7 for 5, 11 for 9). Pascal: "Seven for five. That was my move!" *(Payoff: Pascal's opening move.)*

**Signed patterns** *(optional)*. A brief look at the ternary Golay code behind the test.

**Why does it work?** Euler notes that repairing the hand to a hexad seems to win every time, and he wants to know why. Pascal: "Who cares why? It works." *(Clue.)*

### Episode 4: The Hidden Graph of the Game

*Lead: Euler.* Subtitle: the subtitle travels out along one edge of the 36-edge star.

**Hands as dots.** Every six-card hand becomes a dot, and two dots are joined when the hands share five cards. Around the opening hand grow 6 cards out × 6 cards in = 36 neighbors. There are 924 dots in all, shown as a count, never as a tangle.

**No two hexads touch.** If two hexads shared five cards, those five would have two completions, and Sophie's rule from Episode 2 forbids that. So no edge joins two hexads.

**Nothing bigger** *(optional)*. Pascal bets he can fit more than 132 hands with no edges between them. Euler shows he can't. Each such hand uses up six five-card sets, no two hands share one, and there are only 792.

**Six neighbors each.** Take a hand that isn't a hexad, drop any one card, and complete the remaining five. That gives six different hexad neighbors and 30 other neighbors, while every hexad has 36 non-hexad neighbors. Ada recognizes Episode 3's six repairs. A 2 × 2 matrix records it.

**Downhill only.** Point every edge toward the lower total and remove the hands below 21. What remains are the game's moves, on 905 legal hands. Totals fall, so no sequence of moves returns to a hand, just as Ada said in Episode 1. Decide the hands in order of increasing total: a hand loses exactly when none of its moves reaches a losing hand.

**The kernel.** Run that over all 905 legal hands, and the losing hands are exactly the 132 hexads. No move joins two of them, and every other legal hand has a move into them. **The mystery is solved.** The hands 1 to 6 and its complement are both hexads, because the complement of a hexad is always a hexad. And repairing wins because it leaves the opponent stuck among the hexads.

**Replay.** Episode 1's game again, with the hexads glowing. Pascal's 7 for 5 lands on a hexad, Ada has to leave it, and his 6 for 3 lands on one again. Pascal: "Skill." Ada: "You won. You didn't know why." Pascal: "I do now." *(Payoff: skill or luck.)*

**A lucky deal.** Deal at random, and redeal whenever the total is 21 or less. The first player can force a win with probability 773/894, about 86.47%. And all eleven hands that total exactly 21 are hexads, so every dead end in Episode 1 was one of the special ones. *(Payoff.)*

**One structure.** The cards, the kitten, the tetracode words and the graph slide together: four pictures of one mathematical object. Optionally, Professor Euphemia asks what they'll look at next.

### End credits (every episode, about 52 seconds)

The credits are staged with the series' own pictures. Each card stays up long enough to read.

1. **Series authors:** David Joyner · Claude (Anthropic) · ChatGPT (OpenAI). *Pascal deals three cards face down; they flip, one name on each.*
2. **Based on:** David Joyner, "Kittens, MOGs, and mathematical blackjack," Draft 4 (2026), CC BY 4.0. *The paper's title page slides in, and Ada taps it as if checking the citation.*
3. **The mathematics of:** R. T. Curtis (the kitten and the MOG) · J. H. Conway (the tetracode and the MINIMOG) · E. Witt (the Steiner system S(5,6,12)) · J. Kahane and A. J. Ryba (*The Hexad Game*) · J. H. Conway and N. J. A. Sloane (*Sphere Packings, Lattices and Groups*). *Each name appears beside the picture it gave the series, and Sophie walks along the line.*
4. **Featuring and voices:** Pascal, Sophie, Ada, Euler, each with their Kokoro voice once cast, and the note "Synthetic voices generated locally with Kokoro text-to-speech." *The kittens bow in turn. Pascal bows too low and topples, and Euler bows a beat late.*
5. **About Professor Euphemia** *(only in episodes where she appears)*: A fictional character named in honor of mathematician and educator Euphemia Lofton Haynes. Not a portrayal of Haynes.
6. **Music:** *to be chosen.* A staff draws itself and curls into a tail, and the credit writes on above it.
7. **Visual style inspired by:** *Euphemia Haynes — Mathematics as an Open Door*. **Made with:** Manim Community Edition, Kokoro, FFmpeg, Python. *The tools' names drop onto the table like cards.*
8. **Character animation** *(only if PAM is used)*: PAM (Pose And Motion), Blender.
9. **Mathematical checks:** Every card, total and count on screen was checked by exhaustive computation against the paper's verifier (MIT License). *A counter ticks through the hexads and stops at 132, and Ada nods.*

Then the tail card. Episodes 1–3 end on **Next time: Episode N: *title***, over the next episode's subtitle picture, with that episode's lead kitten peeking in. Episode 4 ends on **The End**: the cards, the kitten, the MINIMOG and the graph gather into a single deck, and the four kittens sit in front of it. A last line points to the paper: *mog.tex in github.com/wdjoyner/alg-graph-thry*.

### How the mystery is built

Every clue planted in one episode is paid off in a later one, and the checker refuses an outline that drops one.

| Thread | Set up | Paid off |
|---|---|---|
| Why do 21 and 45 both lose? | Ep 1, the dead hand and its shadow | Ep 4, the kernel |
| The losing hands look special | Ep 1, special hands | Ep 2, back to the cards (they are hexads); Ep 4, the kernel (why hexads lose) |
| Skill or luck? | Ep 1, a worked game | Ep 4, replay |
| Pascal's 7 for 5 | Ep 1, a worked game | Ep 3, repair |
| Every dead end at 21 is special | Ep 1, the dead hand and its shadow | Ep 4, a lucky deal |
| No memorizing | Ep 2, no memorizing | Ep 3, twelve cells |
| Why does repairing win? | Ep 3, why does it work? | Ep 4, the kernel |

The kittens' guesses are settled on screen, never by assertion:

| Conjecture | Who | Settled |
|---|---|---|
| Only totals 21 and 45 lose | Pascal, Ep 1 | Refuted in the same scene, by checking all five moves of a 24-hand |
| The 28 Pascal left Ada is one of the special hands | Euler, Ep 1 | Confirmed in Ep 2: it is a hexad |
| A design S(5,6,12) exists | Ada asks, Ep 2 | Proved in the next scene, by the orbit on the ring |
| An independent set bigger than 132 | Pascal, Ep 4 *(optional)* | Refuted by counting five-card sets |

### Running times

These include the titles and credits.

| Episode | Required scenes | With optional scenes | Target |
|---|---|---|---|
| 1. The Curious Game of Twenty-One | 7:34 | 8:00 | 7–8 min |
| 2. The Geometry of a Kitten | 9:46 | 9:46 | 8–10 min |
| 3. The Secret Code of the MINIMOG | 9:14 | 9:59 | 8–10 min |
| 4. The Hidden Graph of the Game | 9:14 | 9:55 | 8–10 min |

## Files

| File | What it holds |
|---|---|
| `series.json` | Series title, episode list and runtime budgets, title and credits settings, and the shared vocabulary: concepts, plot threads, visual verbs, epistemic labels |
| `cast.json` | The kittens and Professor Euphemia: designs, personalities, Kokoro audition candidates. Recasting happens here only |
| `pronunciation.json` | Spoken respellings applied before text-to-speech (captions keep the written form) |
| `credits.json` | End-credits wording shared by all four episodes |
| `titles/outline.json` | Titles screenplay: the series main title and one subtitle card per episode; music candidates |
| `end_credits/outline.json` | End-credits screenplay: the credits cards in order, how each is staged, and the tail card (next time, or the finale) |
| `ep1/outline.json` | Episode 1, broken down to beats |
| `ep2/`–`ep4/outline.json` | Episodes 2–4, broken down to scenes; beats to come |
| `math_objects.json` | Every hand, move and count the outlines mention. **Generated; do not edit** |
| `build_math_objects.py` | Writes `math_objects.json`. `--cross-check` also compares the hexads with the paper's `verify.py` |
| `check_outline.py` | Checks all the outlines and screenplays against the files above |
| `title_scenes.py` | Manim scenes for the main title, the four subtitles, the credits roll and the tail cards |
| `make_titles.py` | Renders those scenes and assembles each episode's opening and credits |

## Rendering the titles and credits

The titles and end credits are already renderable, since they have no dialogue. From this folder:

```sh
python make_titles.py            # 1920 x 1080, all four episodes
python make_titles.py --draft    # 960 x 540, for a quick look
python make_titles.py --episodes 2 --with-optional   # one episode, with optional-scene cards
```

This writes `epN_opening.mp4` (scene `s00`: main title plus subtitle, 26 seconds) and `epN_credits.mp4` (scene `s99`: credits plus tail) for each episode into `../build/series/`, with a contact sheet of each in `../build/series/contact/`. It checks every clip's frame count against its outline and stops if one is off. The clips are silent until music is chosen.

`title_scenes.py` reads everything that can change from the series files: beat and card lengths from the two screenplays, wording from `series.json` and `credits.json`, kitten colors from `cast.json`, and the MINIMOG cells, kitten triangle, opening hand and codeword from `math_objects.json`. The file itself holds only the choreography, one function per beat or card ID. A screenplay ID with no function is an error, so a new beat needs choreography before it renders. If a beat's choreography runs longer than its screenplay allows, rendering stops and says by how many frames.

Requirements are the same as for the existing film: Manim Community Edition 0.19 (`pip install manim==0.19.1`), FFmpeg, the DejaVu fonts, and the Cairo and Pango libraries (`brew install pango pkg-config` on a Mac). No TeX is needed. The kittens are simple vector stand-ins, drawn in each character's colors, until the character designs are settled.

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

If you change the story, update "The story" above to match; the outlines are what the checker reads.

## Outline format

Every episode starts with scene `s00` (kind `title_card`) and ends with `s99` (kind `end_credits`). Their text comes from `series.json` and `credits.json`, so a retitle or a credits change is made in one place.

Scene `s00` names a version of the main title (`full`, used everywhere, or the 8-second `short` kept in reserve) and the episode's subtitle from `titles/outline.json`. Its `target_seconds` must equal their combined length. The titles have no dialogue, so their timing is fixed in seconds, and any text must stay on screen for at least 4 seconds.

Scene `s99` plays the end-credits screenplay, then a tail: `next_time` for Episodes 1–3, `finale` for Episode 4. Wording lives in `credits.json`; staging and timing live in the screenplay. Each card stays up at least 1 second plus 1 second per 4 words, and never under 3 seconds. A card marked `when` plays only where that thing is used. Professor Euphemia appears only in optional moments in Episodes 1 and 4, so her card counts toward their optional time.

A scene is either broken into `beats`, or, while `beats` is empty, outlined at scene level with the same fields:

| Field | Meaning |
|---|---|
| `id` | `sNN` for scenes, `sNN.bMM` for beats. Never renumber; add a suffix (`s03.b02a`) instead |
| `lead`, `foil` | Characters from `cast.json`. A beat inherits its scene's unless it says otherwise |
| `cameos` | Other characters who appear briefly, marked `optional` if they can be cut |
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
