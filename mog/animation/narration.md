# MINIMOGs and Mathematical Blackjack
## 1. The Fano plane
### A finite geometry
How can a diagram tell you which card to play? We’ll get there by starting with seven points. In the Fano plane, the triangle’s sides, its three medians, and the circle are all lines. Each contains exactly three marked points.
### A unique completion
Pick points one and four. Only one line contains both, and it supplies point two. Pick four and five instead. Their line is the circle, and it supplies six. The circle works just like any other line for this incidence rule.
### The Steiner rule
Every pair appears exactly once among the seven triples. That is what the notation S of two, three, seven means. The first number tells us how many points we prescribe. The second gives the block size. The last gives the size of the entire point set.
### From triples to hexads
Now ask for six-point blocks on twelve points, with every five points in exactly one block. There are seven hundred ninety-two five-point subsets, and each block accounts for six of them. So the design must contain a hundred thirty-two blocks, called hexads.
## 2. The projective line
### Points and seed
To construct the small Witt design, start with residues modulo eleven and one additional point, infinity. Highlight zero and the five nonzero squares. Together they give our seed set, Q, on this twelve-point projective line.
### Two generators
There are two ways to move the seed. The first adds one modulo eleven, fixing infinity. The second takes the negative reciprocal, interchanging zero and infinity. Each acts as a permutation of the twelve labels, so a six-point set remains a six-point set.
### Close the orbit
Apply both permutations to each new set. Keep a set when it appears for the first time, and queue it for the same treatment. The process stops at a hundred thirty-two distinct sets. These are the orbit of the seed.
### Count the incidences
Now delete one point in each possible way from every block and count the results. The verifier finds seven hundred ninety-two distinct five-point subsets, each occurring once. That exhausts the five-point subsets of twelve points and establishes the Steiner property.
## 3. Curtis’s kitten
### The triangular kitten
Curtis’s kitten gives us a geometric way to recognize those blocks. The corners are infinity, zero, and one. The other labels are repeated around the triangle. Whenever a label appears twice, the two appearances represent the same point.
### Three affine views
At each corner, arrange the same nine ordinary points into a three-by-three affine plane over the field of three elements. Rows and columns are lines. The other two directions wrap around the grid, as the highlighted modular diagonal shows.
### Crosses and squares
Choose a row and a column. Their union has five points because they share one point. The two modular diagonal directions also give perpendicular pairs in this field. Either kind of union is a cross. The four points left over form a square.
### Four types
A line plus all three corners gives a hexad. So do two parallel lines. A cross takes the corner of its own view. A square takes the other two corners. The four families have twelve, twelve, fifty-four, and fifty-four blocks, exactly the projective orbit.
## 4. Conway’s MINIMOG
### Relabel the cells
Conway’s MINIMOG puts the twelve points into a three-by-four array. Match the projective and shuffle arrays cell by cell. Infinity becomes zero, for example. The geometry is carried along by this relabeling, and the new numbers will serve as card values.
### The tetracode
Each tetracode word specifies one row in each of the four columns. Choose a and b modulo three. The row indices are b, a, a plus b, and a plus twice b. There are nine words, and any two coordinates determine the entire word.
### The odd man out
In a column with one marked cell, read the marked row. With two marked cells, read the missing row. Full and empty columns give wildcards. The specified rows must fit one codeword. A hand with column counts zero, one, two, and three is always rejected.
### Test a hand
Here is the hand we’ll play. The columns specify one, one, two, two. The first two entries force one, one, two, zero. The last column disagrees, so the hand is a nonhexad. We’ll look for a one-card exchange that repairs it.
## 5. Johnson graphs
### One exchange
Turn each six-card hand into a vertex. Join two vertices if their hands share five cards. This is the Johnson graph J of twelve, six. It has nine hundred twenty-four vertices. Each hand has thirty-six neighbors, from six choices out and six choices in.
### Independence
Two hexads cannot share five cards, because those five would then have two completions. So the hexads form an independent set. Any independent set uses six distinct five-subsets per vertex, with no overlap between vertices. The resulting upper bound is a hundred thirty-two.
### Equitable partition
For a nonhexad, remove any one of its six cards and complete the five remaining cards to their unique hexad. The six completions are distinct. So every nonhexad has six hexad neighbors and thirty nonhexad neighbors. Every hexad has thirty-six nonhexad neighbors.
### Six neighboring hexads
The matrix records these counts per vertex, with rows for the starting class and columns for the destination class. For our hand, there are six exchanges to hexads. Three increase the total and three decrease it. The direction will matter in the game.
## 6. Mathematical blackjack
### Rules
Both players see the same six cards, and the other six are in a shared pile. On your turn, replace one card with a smaller card from the pile. Keep the new total at least twenty-one. If you have no legal move, you lose.
### Three winning moves
Our hand totals thirty. The three decreasing moves to hexads are four to three, seven to five, and eleven to nine. Their new totals are twenty-nine, twenty-eight, and twenty-eight. Each leaves the opponent a losing position. Let’s play seven to five.
### Through twenty-eight and twenty-four
At twenty-eight, Player Two holds a hexad. Its odd-man-out pattern extends to the codeword two, one, zero, two. In this play, Player Two swaps eleven for seven. The total falls to twenty-four, and the resulting hand has the prohibited column counts.
### Finish at twenty-one
Player One replaces six with three. Now the total is exactly twenty-one, and the hand is a hexad again. Every exchange to a smaller card would go below the threshold. Player Two has no legal move, so Player One wins.
### Recursion on the directed graph
Direct every edge toward the smaller total and keep the vertices at twenty-one or above. Totals strictly decrease, so there are no directed cycles. Process hands in increasing total. A hand is losing exactly when none of its legal successors is losing.
### The kernel
Across all nine hundred five legal hands, the recursion finds exactly the hundred thirty-two shuffle hexads. There are no edges between them, and every other legal hand has a move into them. That makes them the kernel, and explains why repairing the design wins the game.
