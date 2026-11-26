"""The exact PCS₈ factorization and the worked example."""
from manim import Indicate, TransformFromCopy, VGroup

from math_data import BASE, G, H, INF, TAU, U, apply
from visual import (
    BLUE, GOLD, GREEN, MUTED, Chapter, aligned, card, label, place,
    point, tuple_label,
)


class ThreeFactors(Chapter):
    def construct(self):
        self.open("Three factors for S₁₂")
        eq = place(label("S₁₂ = P C S₈",55),0,1.55)
        points = (0,1,INF,*range(2,11))
        xs = {p:(i-5.5)*.98 for i,p in enumerate(points)}
        tiles = {p:place(card(point(p),.82,.76,BLUE if p in BASE[:3]
                              else GOLD if p==2 else MUTED),xs[p],.20)
                 for p in points}
        p_note = place(label("P = PGL₂(11)   ·   sharply 3-transitive",26,BLUE),0,-.75)
        c_note = place(label("σ = (2 3 4 5 6 7 8 9 10)    C = ⟨σ⟩",28,GOLD),0,-1.42)
        h_note = place(label("H = S₈   ·   fixes (0, 1, ∞, 2) pointwise",26,GREEN),0,-2.08)
        self.reveal(eq,*tiles.values())
        self.reveal(p_note)
        self.wait(4)
        self.reveal(c_note)
        self.play(Indicate(VGroup(*(tiles[p] for p in range(2,11))),color=GOLD))
        self.wait(2)
        self.reveal(h_note)
        self.advance(eq,*tiles.values(),p_note,c_note,h_note)

        head = place(label("g = (0 1)",46),0,1.58)
        triple = place(label("(0, 1, ∞)  ↦  "+tuple_label(apply(G,BASE[:3]))+
                             "     u(x) = 1 − x",38,BLUE),0,.56)
        img = place(label("u⁻¹(g(2)) = u⁻¹(2) = "+str(U[G[2]]),39,GOLD),0,-.60)
        c_power = place(label("σ⁸(2) = "+str(TAU[2])+"     τ = σ⁸",38,GOLD),0,-1.75)
        self.reveal(head)
        self.wait(2)
        self.reveal(triple)
        self.wait(3)
        self.reveal(img)
        self.wait(3)
        self.reveal(c_power)
        self.advance(head,triple,img,c_power)

        product = place(label("g = u τ h   ·   apply h, then τ, then u",39),0,1.65)
        residue = place(label("h = (3 10)(4 9)(5 8)(6 7)",31,GREEN),0,.94)
        current = BASE
        current_row = None
        shown_rows = []
        self.reveal(product,residue)
        for i,(name,p,color) in enumerate((("Input",None,MUTED),("h",H,GREEN),
                                           ("τ",TAU,GOLD),("u",U,BLUE))):
            y = .19-i*.70
            if p is not None:
                current = apply(p,current)
            header = aligned(name,-4.57,y,27,color)
            cells = VGroup(*(place(card(point(value),1.22,.54,color,25),x,y)
                             for x,value in zip((-2.2,-.6,1,2.6),current)))
            self.reveal(header)
            if current_row is None:
                self.reveal(cells)
            else:
                self.play(*(TransformFromCopy(a,b) for a,b in zip(current_row,cells)),
                          run_time=1.1)
                self.wait(1.25)
            current_row = cells
            shown_rows += [header,cells]
        self.advance(product,residue,*shown_rows)

        rows = (("First three images","u ∈ P","1,320",BLUE),
                ("Fourth image after undoing u","τ ∈ C","9",GOLD),
                ("Residual (uτ)⁻¹g","h ∈ S₈","40,320",GREEN))
        blocks = []
        for i,(desc,s,count,color) in enumerate(rows):
            y = 1.25-i*1.1
            block = VGroup(aligned(desc,-5.5,y,26),place(card(s,1.9,.66,color),1.6,y),
                           place(label(count,35,color),4.35,y))
            blocks.append(block)
            self.reveal(block)
            self.wait(2.3)
        footer = place(label("1,320 × 9 × 40,320 = 12!   ·   bijective multiplication map",26,MUTED),0,-2.25)
        self.reveal(footer)
        self.advance()
