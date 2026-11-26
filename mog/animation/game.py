"""Tetracode, Johnson graph, and blackjack scenes."""
from manim import *
from visual import *
import math_data as data
from math_data import paper


class ConwayMINIMOG(Chapter):
    index, title = 4, "Conway’s MINIMOG and the tetracode"

    def construct(self):
        projective = grid(paper.P,-3.25,0,{11},projective=True)
        shuffle = grid(paper.M,3.25,0,{0})
        transfer = projective.copy()
        self.beat(VGroup(projective,label("Projective labels",-3.25,1.8,30)),
                  (3, transfer), (4, Transform(transfer,shuffle)),
                  (5.1,label("Shuffle labels",3.25,1.8,30)),
                  (7,label("→",0,0,45,MUTED)),
                  (10,foot("Match cells   •   ∞ maps to 0",GOLD)))
        word = (1,1,2,0)
        marked = {paper.M[r][c] for c,r in enumerate(word)}
        self.beat(VGroup(heading("ONE ROW IN EACH COLUMN"),
                         label("(b, a, a + b, a + 2b)   mod 3",y=.97,size=42,color=BLUE)),
                  (5,grid(paper.M,-2.86,-.65,marked,step=.70)),
                  (7,label("a = 1,  b = 1",2.62,-.27,32)),
                  (9,label("(1, 1, 2, 0)",2.62,-1.06,37,GOLD)),
                  (12,foot("9 words   •   any two coordinates determine the word")))
        examples = []
        for i, (occupancy, picks, output) in enumerate((
                ("Empty",(),"?"),("Single",(1,),"1"),
                ("Double",(0,2),"1"),("Full",(0,1,2),"?"))):
            x = (i-1.5)*3
            examples.append(VGroup(label(occupancy,x,1.68,27),
                                   grid([(j,) for j in range(3)],x,.06,picks,step=.61),
                                   label(output,x,-1.35,40,GOLD)))
        self.beat(examples[1],(3,examples[2]),(5.8,examples[0]),(6.4,examples[3]),
                  (9,foot("Specified rows must extend to one word.",BLUE)),
                  (13,label("Always reject the occupancy multiset {0, 1, 2, 3}.",
                            y=-2.05,size=28,color=RED)))
        self.beat(VGroup(heading("A = " + set_text(data.HAND)),
                         grid(paper.M,-3.38,.01,data.HAND)),
                  (3,label("Occupancies   (2, 1, 2, 1)",2.45,1.18,32)),
                  (5,label("Read             (1, 1, 2, 2)",2.45,.43,32,GOLD)),
                  (8,label("Forced          (1, 1, 2, 0)",2.45,-.32,32,BLUE)),
                  (11,label("Mismatch in column 4",2.45,-1.14,26,RED)),
                  (13,foot("A is a nonhexad.",RED)))


class JohnsonGraph(Chapter):
    index, title = 5, "The Johnson graph and equitable partition"

    def construct(self):
        h = data.exchange(data.HAND, (4,3))
        self.beat(VGroup(heading("J(12, 6)"),hand_row(data.HAND,y=.86,marked={4},color=GOLD)),
                  (3, VGroup(Line(xy(0,.28),xy(0,-.33),stroke_width=4,color=BLUE),
                             hand_row(h,y=-.90,marked={3}))),
                  (9, label("924 vertices", -3.9,-2.35,31,BLUE)),
                  (12,label("Degree 6 × 6 = 36",3.9,-2.35,31,BLUE)))
        self.beat(VGroup(heading("INDEPENDENT SET"),
                         label("Five shared cards would have two hexad completions.",
                               y=.88,size=36,color=BLUE)),
                  (5,label("No two hexads are adjacent.",y=-.01,size=39)),
                  (9,label("6 five-subsets used per vertex",y=-.86,size=32)),
                  (12,foot("792 ÷ 6 = 132   •   maximum independent set",GOLD)))
        left,right = xy(-3.38,.10),xy(3.38,.10)
        nodes = VGroup(Circle(1.20,color=GREEN).move_to(left),
                       Circle(1.20,color=BLUE).move_to(right),
                       label("Hexads",-3.38,.32,31,GREEN), label("132",-3.38,-.34,28),
                       label("Nonhexads",3.38,.32,28,BLUE), label("792",3.38,-.34,28))
        to_h = VGroup(Arrow(xy(2.28,-.32),xy(-2.28,-.32),buff=0,color=GREEN),
                      label("6",y=-.73,size=29,color=GREEN))
        to_n = VGroup(Arrow(xy(-2.28,.50),xy(2.28,.50),buff=0,color=BLUE),
                      label("36",y=.9,size=29,color=BLUE))
        loop = VGroup(CurvedArrow(xy(4.25,.92),xy(4.42,-.51),angle=-4,color=BLUE),
                      label("30",5.18,.12,28,BLUE))
        self.beat(nodes,(5,to_h),(10,loop),(13,to_n),
                  (14.7,foot("Neighbor counts per vertex")))
        matrix = VGroup(label("Quotient matrix", -3.4,-1.5,26,MUTED))
        for x, column in ((-4.02, "H"), (-2.86, "N")):
            matrix.add(label(column, x, 1.10, 27, MUTED))
        for y, row, entries, color in ((.33, "H", (0, 36), GREEN),
                                       (-.43, "N", (6, 30), BLUE)):
            matrix.add(label(row, -5.15, y, 27, color))
            for x, entry in zip((-4.02, -2.86), entries):
                matrix.add(label(entry, x, y, 32, color))
        for x, inward in ((-4.69, .23), (-2.20, -.23)):
            matrix.add(VMobject(stroke_width=2, stroke_color=MUTED).set_points_as_corners(
                [xy(x+inward,.76), xy(x,.76), xy(x,-.87), xy(x+inward,-.87)]))
        up = "     ".join(f"{a} → {b}" for a,b in paper.exchanges if b>a)
        down = "     ".join(f"{a} → {b}" for a,b in data.MOVES)
        self.beat(matrix,(5,label("Exchanges from A to hexads",2.73,1.23,29)),
                  (8,label(up,2.73,.26,35,MUTED)),
                  (11,label(down,2.73,-.54,35,GREEN)),
                  (13,foot("Three raise the total. Three lower it.")))


class Blackjack(Chapter):
    index, title = 6, "Mathematical blackjack"

    def construct(self):
        h0 = data.HAND
        h1,h2,h3 = self.played_hands()
        self.beat(VGroup(heading("Shared hand   •   total 30"),
                         hand_row(h0,y=.98),
                         label("Shared pile",y=.12,size=26,color=MUTED),
                         hand_row(paper.X-h0,y=-.70)),
                  (7,foot("Exchange one card for a smaller one.",BLUE)),
                  (12,label("New total ≥ 21",y=-1.89,size=34,color=GOLD)))
        choices = VGroup()
        for i, (a,b) in enumerate(data.MOVES):
            target = data.exchange(h0,(a,b))
            x = (i-1)*4.17
            choices.add(VGroup(label(f"{a} → {b}",x,.38,47,GREEN),
                               label(f"total {sum(target)}",x,-.43,31),
                               label(set_text(target),x,-1.14,23,MUTED,width=3.89)))
        self.beat(VGroup(heading("Three moves to a hexad"),hand_row(h0,y=1.29)),
                  (3,choices[0]),(5,choices[1]),(7,choices[2]),
                  (12.5,foot("Choose 7 → 5",GOLD)))
        before = hand_row(h1,y=.48,marked={11})
        after = hand_row(h2,y=.48,marked={7},color=GOLD)
        status = label("28   •   P-position",y=-.43,size=36,color=GREEN)
        turn = heading("After Player One plays 7 → 5")
        pattern = label("(?, 1, 0, 2) extends to (2, 1, 0, 2)",y=-1.34,size=30,color=BLUE)
        self.beat(VGroup(turn,before,status),
                  (4, pattern),
                  (8.8, AnimationGroup(
                      Transform(before,after),
                      Transform(status,label("24   •   N-position",y=-.43,size=36,color=GOLD)),
                      Transform(turn,heading("Player Two plays 11 → 7")),
                      Transform(pattern,label("Prohibited occupancies {0, 1, 2, 3}",
                                              y=-1.34,size=30,color=RED)))))
        start = hand_row(h2,y=.48,marked={6},color=GOLD)
        in_place = [3 if card == 6 else card for card in sorted(h2)]
        assert set(in_place) == h3
        status = label("24",y=-.48,size=39,color=GOLD)
        self.beat(VGroup(heading("Player One plays 6 → 3"),start,status),
                  (3,AnimationGroup(
                      Transform(start,grid([in_place],y=.48,marked={3},step=.96,color=GREEN)),
                      Transform(status,label("21   •   P-position",y=-.48,size=39,color=GREEN)))),
                  (8, label("Every smaller exchange would go below 21.",y=-1.44,size=30)),
                  (12,foot("Player Two has no legal move. Player One wins.",GOLD)))
        weights = VGroup()
        for i, (w, tag) in enumerate(((30,"N"),(28,"P"),(24,"N"),(21,"P"))):
            x = -4.42+i*2.95
            color = GREEN if tag=="P" else GOLD
            weights.add(VGroup(Circle(.55,color=color).move_to(xy(x,.14)),
                               label(w,x,.14,31,color),
                               label(tag,x,-.66,24,color)))
        arrows = VGroup(*(Arrow(xy(x+.58,.14),xy(x+2.37,.14),buff=.05,color=BLUE)
                          for x in (-4.42,-1.47,1.48)))
        self.beat(VGroup(heading("A path in the directed game graph"),weights),
                  (2,arrows),
                  (6,foot("Totals strictly decrease along each legal edge.")),
                  (9, label("Evaluate positions from the lowest total upward.",y=-1.44,size=29)),
                  (13, label("Losing ⇔ no losing legal successor",y=-2.05,size=30,color=GREEN)))
        self.beat(VGroup(heading("THE KERNEL"),
                         label("905 legal hands",y=.93,size=43),
                         label("132 losing hands",y=.02,size=55,color=GREEN)),
                  (6,label("No edges between hexads.",y=-.89,size=30)),
                  (9,label("Every other legal hand has a move to a hexad.",y=-1.55,size=30)),
                  (14,foot("Small Witt design  •  Shuffle MINIMOG  •  Losing positions",BLUE)))

    @staticmethod
    def played_hands():
        current = data.HAND
        hands = []
        for move in data.PLAY:
            current = data.exchange(current,move)
            hands.append(current)
        return hands
