# Future plans: Kittens, MOGs, and Mathematical Blackjack

*Four adventures in finite geometry — a proposed educational animation series*

## The idea

What could a card game played by four kittens possibly have to do with geometry, error-correcting codes and the symmetry of mathematical objects? Quite a lot, as it turns out.

This project proposes four short animated films, each approximately five to ten minutes long, based on the accompanying [mathematical paper](../mog.tex). The films will begin with an accessible game and gradually uncover the surprisingly rich mathematics behind it. No previous knowledge of abstract algebra or coding theory will be assumed at the outset. Later episodes will introduce more advanced ideas visually, with the paper available for readers who want precise definitions, proofs and further references.

The series will combine mathematical exposition, character comedy and animated geometry. The kittens will take turns explaining ideas, challenging each other's conjectures and discovering connections. The goal is not merely to illustrate a lecture but to let viewers participate in the discovery of mathematics.

This is a future production plan, not an announcement that the four films have already been completed. The [existing mathematical blackjack animation](minimogs-blackjack.mp4) provides a starting point.

## Meet the kittens

| Character | Personality and mathematical interests |
| --- | --- |
| Pascal | An energetic orange tabby, competitive card player and enthusiastic experimental mathematician. He introduces mathematical blackjack, makes bold conjectures and sometimes discovers that his intuition has led him astray. |
| Sophie | A curious tuxedo kitten who thinks in pictures. She introduces finite geometry, Steiner systems and Curtis's kitten. |
| Ada | A gray kitten with a precise, skeptical disposition and dry sense of humor. She enjoys algorithms, coding theory, the MINIMOG and checking mathematical claims. |
| Euler | A thoughtful cream-colored kitten, somewhat absent-minded but fascinated by symmetry, graphs and proofs. He connects the discoveries made by the other kittens. |

All four principal characters should sometimes be teachers and sometimes students. Their visual designs, names and casting remain provisional until the prototype has been reviewed.

## The proposed films

### 1. The Curious Game of Twenty-One (7–8 minutes)

Pascal invites the other kittens to play mathematical blackjack, a two-player game quite different from ordinary casino blackjack. It uses twelve cards numbered 0 through 11. Six cards form a single visible hand shared by the players. On a turn, a player exchanges one card for an unused card of smaller value, provided that the new total is at least 21. The player who cannot make a legal move loses.

The audience will see a worked game, with cards traveling across the table and the total changing after each exchange. Viewers will be invited to predict moves before the kittens make them.

The central mystery is that the hand consisting of cards 1 through 6, whose total is 21, is a losing position for the player about to move. Surprisingly, its complementary hand, totaling 45, is also a losing position under optimal play, despite having legal moves. Why should these two hands have the same strategic status?

The kittens discover that a special collection of six-element sets, called hexads in this design, determines the winning strategy. The first episode introduces sets, complements, legal moves, winning and losing positions, and the distinction between experimenting with a game and proving a strategy.

### 2. The Geometry of a Kitten (8–10 minutes)

Sophie leads the investigation into finite geometry: geometries having only finitely many points. The familiar idea of points and lines is introduced through the seven-point Fano plane, where each pair of points lies on exactly one line.

The kittens then meet a twelve-point geometry with a stronger property: every five points belong to exactly one of 132 special six-point blocks. This is the small Witt design, a Steiner system denoted S(5,6,12). Here the word “hexad” means one of these distinguished blocks, not an arbitrary six-element subset.

The projective line over the field of eleven elements gives one construction. Its points can be permuted by simple fractional-linear transformations, which can be visualized as rearrangements of labeled points. A second, especially attractive construction is Curtis's kitten, a mathematical diagram comprising three related affine-plane pictures with distinguished points.

Animated lines, crosses and other configurations will reveal the four families of hexads in Curtis's construction, with respective sizes 12, 12, 54 and 54. Their total is 132. The shuffle labeling connects these configurations to the numbered cards from the first film.

The educational goal is to show how a complex collection of sets can arise from simple geometric patterns, and why several different pictures can represent the same combinatorial object.

### 3. The Secret Code of the MINIMOG (8–10 minutes)

Ada rearranges the twelve cards into the three-by-four array known as the MINIMOG, the miniature version of the Miracle Octad Generator (MOG). The challenge is to recognize a hexad without memorizing all 132 possibilities.

The kittens discover arithmetic modulo three, in which numbers cycle through three possible values. They use this arithmetic to build the tetracode, a small code consisting of nine four-coordinate words. Animated coordinates will show how the words arise from just two freely chosen values.

The MINIMOG's odd-man-out rule and column occupancy condition then become a practical visual test for whether a six-card hand is a hexad. The viewer will see the test applied to actual hands from the game, including the running example in the paper. More advanced signed patterns and the connection with the ternary Golay code can be introduced briefly or left as optional supplementary material.

This film teaches how arithmetic, geometry and coding theory can describe the same structure, and how a compact algorithm can replace a long list of cases. The emphasis is on understanding the test rather than memorizing it.

### 4. The Hidden Graph of the Game (8–10 minutes)

Euler proposes representing every possible six-card hand by a point, or vertex, in a graph. Two vertices are joined whenever their hands differ by exchanging one card. The resulting Johnson graph J(12,6) has 924 vertices, each with 36 neighbors.

Rather than displaying an unreadable tangle of all the edges, the animation will begin with small neighborhoods and progressively reveal the larger structure. The 132 hexads form an independent set: no two are joined by an edge. Every nonhexad has six hexad neighbors in the undirected graph. This remarkable regularity leads to an equitable partition and helps explain the connection between the Witt design and the Johnson graph. An optional advanced segment introduces the maximum independent-set result and its proof ideas.

When the graph is oriented from higher totals to lower totals and hands below 21 are removed, it becomes the directed graph of the game. The kittens will discover how the hexads form its kernel, so that every legal nonhexad position has a move to a losing position, while no move connects two hexads. This explains the winning strategy and resolves the mystery from the first film.

The finale returns to the card table and plays through the strategy. It also explores the probability of receiving a winning hand: if a uniformly random hand is redealt whenever its total is at most 21, the first player has a winning strategy with probability 773/894, approximately 86.47%.

The series ends by bringing the cards, geometric diagrams, codewords and graph together. They are not four unrelated topics, but different ways of understanding the same mathematical structure.

## Visual and educational style

The visual inspiration is [Euphemia Haynes — Mathematics as an Open Door](https://github.com/wdjoyner/pam/tree/haynes-animation/haynes), a Manim-based film in which words follow curves, letters move with changing geometric objects, and mathematical ideas are expressed through transformations rather than static captions.

The kitten films will develop this approach further. Cards can fly into the MINIMOG array; five selected points can call forth the unique sixth point of a hexad; codewords can assemble from their generating coordinates; and the words describing a mathematical idea can travel along the curves or edges that illustrate it.

Motion should have a mathematical or dramatic purpose. The films should use generous visual whitespace, consistent colors, readable equations, and deliberate pauses for the viewer to think. Important expressions should remain on screen long enough to be read. The kittens' gestures and reactions should support the explanation, not distract from it.

The guiding educational principle is to show a phenomenon before naming it. The characters should learn through observation, experimentation, construction and reflection. Humor is welcome, but a visual example must never be presented as a proof of a general theorem.

## Voices and casting

Initial production will use free, locally executable Kokoro text-to-speech. The Haynes narrator voice, af_heart, is reserved for the Haynes film and will not be used by any kitten, even in a voice blend.

The following are audition candidates, not final casting decisions:

| Character | Kokoro candidates | Direction |
| --- | --- | --- |
| Pascal | am_puck; optionally a 70/30 blend of am_puck and am_michael | Energetic, mischievous; speed around 1.04 |
| Sophie | af_bella, af_jessica, af_river | Warm, imaginative and expressive |
| Ada | af_sarah, af_kore, bf_emma | Clear, confident and dryly humorous |
| Euler | bm_george | Thoughtful and professorial; speed around 0.90 |

Kokoro voice blending offers an additional way to obtain distinct voices without paid services. Weighted blends should combine compatible voice tensors before synthesis. The exact API and supported combinations will be tested against the installed version. Auditions should include mathematical terminology, jokes and conversations between characters.

**Future voice direction for Pascal:** A recognizable Brooklyn accent could be a particularly humorous choice for American audiences, given the contrast between a fast-talking neighborhood card player and a sophisticated combinatorialist. For now, the humor should come from his dialogue, timing and personality, using Kokoro. A human voice actor or another suitable voice engine could be considered once the films are perfected. Any future voice-cloning approach must respect consent and applicable licenses.

## Production approach

The initial production will be free, open-source and local, with no paid voice or rendering services required.

Manim will handle the mathematical diagrams, transformations and geometric typography. Reusable techniques such as CurveText and write_along from the Haynes film will be adapted. Simple vector kittens will suffice for the first animatics. PAM (Pose And Motion) and Blender can subsequently provide richer character acting, subject to testing their integration. Blender need not be a prerequisite for making the initial films.

The literary screenplays will be written in Fountain, with printable versions produced using fountain2latex. A structured JSON adaptation will describe dialogue, mathematical objects, visual cues and character actions. Character descriptions and casting will be maintained separately, so that changing a voice does not require editing the screenplay.

Each dialogue line will have a stable line ID and speaker ID. A voice-engine-independent audio generator will produce individual WAV clips and a timing manifest. The animation timeline will use measured clip lengths and semantic cues rather than relying solely on hard-coded timestamps. Sentence or phrase timing will be obtained through segmentation or alignment where necessary. Recasting will regenerate affected audio, recalculate timing and rerender affected scenes, without rewriting their mathematical animation instructions.

The mathematical backend will be independent of the visual renderer. Examples, card exchanges, hexad membership, geometric configurations and graph data should be generated and checked against the paper and its verification code. The films should have subtitles, mathematical references and appropriate credits. Software versions and asset licenses will be documented.

## Development milestones

1. Prepare a series bible, visual style guide, character descriptions, casting configuration and pronunciation guide.
2. Write and review a short Fountain screenplay and corresponding JSON animation script.
3. Build a 60–90 second prototype with two kittens, distinct Kokoro voices, legal card exchanges, a MINIMOG transformation and a comic reaction.
4. Evaluate mathematical correctness, visual readability, voice distinction, acting and timing before expanding the animation framework.
5. Write and mathematically review all four episodes, then produce low-resolution animatics.
6. Refine character acting where useful, render final films, add subtitles and publish the episodes individually.

The four-film structure, exact runtimes, final casting and degree of PAM/Blender integration remain open to refinement. The priority is to perfect the mathematics, storytelling, acting and geometric choreography before spending money on voices.

## Further reading and viewing

- [The accompanying mathematical paper](../mog.tex)
- [Existing mathematical blackjack animation](minimogs-blackjack.mp4)
- [MINIMOGs and Mathematical Blackjack](https://yetanothermathblog.com/2017/09/30/minimogs-and-mathematical-blackjack/)
- [Dodecahedral faces of M12](https://yetanothermathblog.com/2018/06/10/dodecahedral-faces-of-m12/)
- [Haynes animation source and production notes](https://github.com/wdjoyner/pam/tree/haynes-animation/haynes)
- [PAM animation project](https://github.com/wdjoyner/pam)

*Planning document developed through discussion with ChatGPT and Claude, November 2026.*
