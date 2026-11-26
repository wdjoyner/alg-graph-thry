"""Scenes for the cube question, sharp transitivity, and the classification."""
import numpy as np
from manim import (
    DOWN, RIGHT, LEFT, Arrow, Brace, Create, FadeIn, FadeOut, GrowArrow,
    GrowFromCenter, Indicate, LaggedStart, Line, Rectangle, SurroundingRectangle,
    TransformFromCopy, VGroup,
)
from math_data import (
    AFFINE, AFFINE_TARGET, CUBE_EDGES, DEGREE_12, FAMILIES, I3, MATHIEU, ROTATE, S3_GRID,
    SWAP, apply, inverse,
)
from visual import (
    BLUE, GOLD, GREEN, INK, LINE, MUTED, PANEL, RED, Chapter, aligned, card,
    fmt_cycles, label, place,
)


def cube_edges():
    def project(v):
        x,y,z = v
        return np.array([-3.35+x+.23*z, .3+y+.65*z, 0])

    lines = VGroup(*(Line(project(a),project(b),color=LINE,stroke_width=7)
                     for a,b in CUBE_EDGES))
    numbers = VGroup(*(card(i,w=.48,h=.42,color=BLUE,size=19)
                       .move_to((project(a)+project(b))/2)
                       for i,(a,b) in enumerate(CUBE_EDGES,1)))
    return lines,numbers


class CubeStorage(Chapter):
    def construct(self):
        self.open("The Rubik’s Cube storage question")
        lines,numbers = cube_edges()
        question = VGroup(label("12 edge positions",42,BLUE),
                          label("One permutation in S₁₂",28),
                          label("Can one coordinate lie in S₈?",29,GOLD))
        question.arrange(DOWN,aligned_edge=LEFT,buff=.35).move_to([2.7,.4,0])
        self.play(Create(lines),run_time=2)
        self.play(LaggedStart(*(FadeIn(x) for x in numbers),lag_ratio=.12),run_time=2)
        self.wait(1.5)
        self.reveal(question)
        self.advance(lines,numbers,question)

        formula = place(label("G = HK       H ∩ K = {1}",54,BLUE),0,1.15)
        rewrite = place(label("hk = h′k′   ⟹   h′⁻¹h = k′k⁻¹",43),0,-.10)
        unique = place(label("One product. One pair of subgroup coordinates.",30,GOLD),0,-1.75)
        self.reveal(formula)
        self.wait(4)
        self.reveal(rewrite)
        self.wait(3)
        self.reveal(unique)
        self.advance(formula,rewrite,unique)

        grid = VGroup()
        for col, p in enumerate((I3,ROTATE,inverse(ROTATE))):
            grid.add(place(label(fmt_cycles(p),30,GOLD),-2+col*2.4,1.45))
        for row, p in enumerate((I3,SWAP)):
            grid.add(place(label(fmt_cycles(p),30,BLUE),-4.2,.55-row*1.1))
            for col, value in enumerate(S3_GRID[row]):
                cell = card(fmt_cycles(value),1.85,.77,LINE)
                cell[1].set_color(INK)
                grid.add(place(cell,-2+col*2.4,.55-row*1.1))
        fact = place(label("S₃ = S₂ C₃",40),0,-2)
        self.play(LaggedStart(*(FadeIn(x) for x in grid),lag_ratio=.15),run_time=4)
        self.reveal(fact)
        self.advance()

        target = SurroundingRectangle(grid[-1],color=GREEN,buff=.08)
        self.play(Create(target))
        self.play(FadeOut(grid),FadeOut(fact),FadeOut(target))
        equation = place(label("(1 3) = (1 2)(1 3 2)",49),0,1.45)
        self.reveal(equation)
        # The tokens display the current image of each input along the row.
        rows = []
        values = I3
        for i,(name,p) in enumerate((("Input",I3),("Apply (1 3 2)",inverse(ROTATE)),("Apply (1 2)",SWAP))):
            y = .45-i*1.05
            step = aligned(name,-5,y,26,(MUTED,GOLD,BLUE)[i])
            values = apply(p,values)
            cells = [place(card(v+1,.9,.62,(MUTED,GOLD,BLUE)[i]),x,y)
                     for x,v in zip((-1,1,3),values)]
            row = VGroup(step,*cells)
            if rows:
                self.reveal(step)
                self.play(*(TransformFromCopy(a,b) for a,b in zip(rows[-1][1:],cells)))
            else:
                self.reveal(row)
            rows.append(row)
            self.wait(1.5)
        self.advance()


class SharpTransitivity(Chapter):
    def construct(self):
        self.open("From complements to sharp transitivity")
        text = place(label("k = n − m",47,BLUE),0,1.45)
        tiles = VGroup(*(card(s,w=1.05,color=c) for s,c in
                         [("1",MUTED),("2",MUTED),("…",MUTED),("m",MUTED),
                          ("m+1",GOLD),("…",GOLD),("n",GOLD)]))
        tiles.arrange(RIGHT,buff=.19)
        first = VGroup(*tiles[:4])
        last = VGroup(*tiles[4:])
        f = Brace(first,DOWN,color=MUTED)
        l = Brace(last,DOWN,color=GOLD)
        labels = VGroup(label("permuted by Sₘ",26,MUTED).next_to(f,DOWN),
                        label("v = (m+1, …, n)",26,GOLD).next_to(l,DOWN))
        self.reveal(text,tiles)
        self.wait(3)
        self.play(Indicate(last,color=GOLD),GrowFromCenter(l),GrowFromCenter(f))
        self.reveal(labels)
        self.advance(text,tiles,f,l,labels)

        eq = place(label("g = xh       ⟹       gv = xhv = xv",48,BLUE),0,1.35)
        uniq = place(label("xv = yv   ⟹   y⁻¹x ∈ K ∩ Sₘ   ⟹   x = y",39,GOLD),0,-.9)
        gnote = place(label("x ∈ K      h ∈ Sₘ",26,MUTED),0,.48)
        self.reveal(eq,gnote)
        self.wait(6)
        self.reveal(uniq)
        self.advance(eq,gnote,uniq)

        a,b = AFFINE[AFFINE_TARGET]
        fn = place(label(f"f(x) = {a}x + {b}   (mod 5)",45,BLUE),0,1.55)
        source = [place(card(s,1.2,.9,GOLD,43),x,.25) for x,s in zip((-1.25,1.25),(0,1))]
        target = [place(card(s,1.2,.9,GREEN,43),x,-1.4) for x,s in zip((-1.25,1.25),AFFINE_TARGET)]
        arrows = [Arrow(a.get_bottom(),b.get_top(),buff=.07,color=LINE)
                  for a,b in zip(source,target)]
        side = place(label("S₃ ≤ S₅",34,MUTED),-4.65,.25)
        credit = place(label("arithmetic in F₅",28,MUTED),4.5,.25)
        self.reveal(*source,side,credit)
        self.wait(4)
        self.reveal(*target)
        self.play(*(GrowArrow(arrow) for arrow in arrows))
        self.wait(2)
        self.reveal(fn)
        self.advance(fn,*source,*target,*arrows,credit,side)

        eq = place(label("(0, 1) ↦ (r, s)    ⟺    f(t) = (s − r)t + r",42),0,.85)
        proof = place(label("xv = gv    ⟹    x⁻¹g ∈ Sₘ",44,BLUE),0,-.55)
        end = place(label("Complement   ⇔   Sharply k-transitive subgroup",32,GOLD),0,-1.85)
        self.reveal(eq)
        self.wait(5)
        self.reveal(proof)
        self.wait(3)
        self.reveal(end)
        self.advance()


class Classification(Chapter):
    def construct(self):
        self.open("The classification")
        xs = (-5.85,-3.7,-1.6,3.37)
        headers = VGroup(*(aligned(s,x,1.65,23,MUTED)
                           for s,x in zip(("m","k","Condition  ·  n > 12","A complement"),xs)))
        self.reveal(headers)
        rows = []
        for i,row in enumerate(FAMILIES):
            y = .85-i*.84
            row_bg = place(Rectangle(width=12,height=.71,stroke_width=0,
                                     fill_color=PANEL,fill_opacity=1),0,y)
            rows.append(VGroup(row_bg,*(aligned(s,x,y,26 if j==2 else 28,BLUE if j==3 else INK)
                                        for j,(s,x) in enumerate(zip(row,xs)))))
        self.reveal(rows[0])
        self.wait(4)
        self.reveal(rows[1])
        self.advance()
        self.reveal(rows[2])
        self.wait(5)
        self.reveal(rows[3])
        self.advance(headers,*rows)

        cards = []
        for x,(n,k,m,order) in zip((-3.1,3.1),MATHIEU):
            panel = place(card("",5.4,2.55,LINE),x,.35)
            box = VGroup(panel,place(label(f"M{str(n).translate(str.maketrans('012','₀₁₂'))}",52,BLUE),x,1.04),
                        place(label(f"n = {n}    k = {k}    m = {m}",29),x,.25),
                        place(label(f"Group order  {order:,}",24,GOLD),x,-.52))
            cards.append(box)
        cites = place(label("Classical input  ·  Zassenhaus and Jordan",29,BLUE),0,-1.77)
        books = place(label("Cameron (1999)  ·  Dixon & Mortimer (1996)",24,MUTED),0,-2.34)
        self.reveal(cards[0])
        self.wait(2)
        self.reveal(cards[1])
        self.wait(5)
        self.reveal(cites,books)
        self.advance(*cards,cites,books)

        cells = VGroup(*(place(card(i,.85,.8,GREEN if i in DEGREE_12 else LINE),
                               (i-5.5)*1.1,.37) for i in range(1,11)))
        degree = place(label("n = 12  ·  allowed k highlighted",36),0,1.56)
        reject = place(label("S₈ would need k = 4",42,RED),0,-1.2)
        detail = place(label("Sharp 4-transitivity in this range requires n = 11.",25,MUTED),0,-2)
        self.reveal(degree,cells)
        self.wait(4)
        self.play(Indicate(cells[3],color=RED))
        self.reveal(reject,detail)
        self.advance()
