"""Fano, projective orbit, and Curtis kitten scenes."""
from manim import *
from visual import *
import math_data as data
from math_data import paper


def fano(active=None, pair=()):
    a, b, c = (np.array([np.cos(t), np.sin(t), 0]) * 2
               for t in (PI/2, 7*PI/6, 11*PI/6))
    points = [a, b, c, (a+b)/2, (b+c)/2, (c+a)/2, ORIGIN]
    lines = VGroup(*(Line(points[i-1], points[k-1]) if j != 6 else Circle(radius=1)
                     for j, (i, k) in enumerate(((1,2),(2,3),(3,1),(1,5),(2,6),(3,4),(4,6)))))
    lines.set_stroke("#698DB1", width=3)
    if active is not None:
        lines[active].set_stroke(GOLD, width=6)
    offsets = [(0,.27),(-.21,-.23),(.21,-.23),(-.28,.1),(0,-.29),(.28,.1),(.23,.13)]
    nodes = VGroup(*(Dot(p, radius=.083, color=BLUE if i+1 in pair else
                        GOLD if active is not None and i+1 in data.FANO[active] else INK)
                     for i, p in enumerate(points)))
    digits = VGroup(*(label(i+1, p[0]+u, p[1]+v, size=21)
                      for i, (p, (u, v)) in enumerate(zip(points, offsets))))
    return VGroup(lines, nodes, digits)


class FanoSteiner(Chapter):
    index, title = 1, "The Fano plane and Steiner systems"

    def construct(self):
        diagram = fano().shift(LEFT*3.25)
        self.beat(VGroup(diagram, label("MINIMOGs and", 2.68,.75,49),
                         label("Mathematical Blackjack", 2.68,.04,45,BLUE)),
                  (10, label("7 points  •  7 lines", 2.68,-.96,29,GOLD)))
        self.beat(VGroup(fano(0,(1,4)).scale(.83).move_to(xy(-3,.15)),
                         label("1 and 4  →  2", -3,-2.28,34,GOLD)),
                  (7.4, VGroup(fano(6,(4,5)).scale(.83).move_to(xy(3,.15)),
                              label("4 and 5  →  6", 3,-2.28,34,GOLD))))
        self.beat(VGroup(heading("A STEINER SYSTEM"), label("S(2, 3, 7)", y=.75,size=76,color=BLUE)),
                  (5, label("2 prescribed points", -4.1,-.74,27)),
                  (8, label("3 points per block", 0,-.74,27)),
                  (11, label("7 points in all", 4.1,-.74,27)),
                  (13, foot("Every pair has exactly one completion.",GOLD)))
        self.beat(VGroup(label("S(5, 6, 12)", y=1.1,size=71,color=BLUE),
                         heading("Every five points determine one six-point block.", y=.05)),
                  (7, label("792 five-subsets  ÷  6 per block", y=-.94,size=42)),
                  (12, foot("= 132 hexads",GOLD)))


class ProjectiveLine(Chapter):
    index, title = 2, "The projective-line construction"

    def construct(self):
        circle = VGroup()
        for i in range(12):
            angle = PI/2 - i*TAU/12
            circle.add(tile(name(i),i in data.Q,size=.65)
                       .move_to(xy(-3.05+2.16*np.cos(angle),.04+2.16*np.sin(angle))))
        self.beat(VGroup(circle,label("ℙ¹(𝔽₁₁)",3.11,1.02,63,BLUE)),
                  (5, label("0, 1, …, 10, ∞",3.11,.04,35)),
                  (9, label("Q = "+set_text(data.Q,True),3.11,-1.12,29,GOLD)))
        rows = [
            VGroup(label("α(x) = x + 1", -3.1,.73,39,BLUE),
                   label(set_text(data.ALPHA_Q,True), 2.38,.73,37)),
            VGroup(label("β(x) = −1/x", -3.1,-.49,39,BLUE),
                   label(set_text(data.BETA_Q,True), 2.38,-.49,37)),
        ]
        self.beat(heading("Q = " + set_text(data.Q,True)),
                  (2, rows[0]), (7.4, rows[1]),
                  (11, foot("α fixes ∞     •     β exchanges 0 and ∞",GOLD)))
        self.beat(VGroup(heading("Orbit of Q under PSL(2, 11)"),
                         label("Q", -4.7,.28,54,BLUE)),
                  (2, label("→", -3.12,.28,48,MUTED)),
                  (4, label("α(Q), β(Q)", -.95,.28,43)),
                  (7, label("→   ⋯", 2.03,.28,48,MUTED)),
                  (10.7, label("132",4.57,.28,66,GOLD)),
                  (13, foot("Queue each new set exactly once.")))
        five = sorted(data.Q)[:-1]
        self.beat(VGroup(heading("Delete one point in all six possible ways"),
                         label(set_text(data.Q,True), y=.93,size=44, color=BLUE)),
                  (2.5, label("↓  delete 9", y=.02,size=29,color=MUTED)),
                  (4.5, label(set_text(five,True), y=-.69,size=42)),
                  (9.5, foot("132 × 6 = 792 distinct five-subsets   •   multiplicity 1",GOLD)))


class CurtisKitten(Chapter):
    index, title = 3, "Curtis’s kitten"

    def construct(self):
        triangle = Polygon(xy(-3.55,-2.3),xy(3.55,-2.3),xy(0,2.55),
                           color="#6687A9",stroke_width=2)
        digits = VGroup(*(label(name(v),x*.58,(y-3)*.66,29,
                                GOLD if v in data.D else BLUE if v==6 else INK)
                          for x,y,v in data.TRIANGLE))
        self.beat(VGroup(triangle,digits),
                  (7, label("Distinguished points",4.65,1.1,24,MUTED)),
                  (8.5, label("∞, 0, 1",4.65,.49,40,GOLD)),
                  (12, label("Repeated 6s mark\nthe same point.",-4.85,-.35,23,BLUE)))
        views = []
        for i, (corner, values) in enumerate(paper.projective_views.items()):
            x = (i-1)*4.29
            rows = [values[j:j+3] for j in (0,3,6)]
            marked = data.line(values,1,1,0) if i == 0 else ()
            views.append(VGroup(label("View at "+name(corner),x,1.6,29,GOLD),
                                grid(rows,x,-.07,marked,projective=True)))
        self.beat(views[0],(3,views[1]),(5,views[2]),
                  (10,foot("Highlighted modular line   r + c = 0 in 𝔽₃",BLUE)))
        rows = [data.V[j:j+3] for j in (0,3,6)]
        panels = []
        for x, title, subset, color in (
                (-4.25,"Axial cross",data.AXIAL,BLUE),
                (0,"Diagonal cross",data.DIAGONAL,BLUE),
                (4.25,"Complementary square",data.SQUARE,GOLD)):
            panels.append(VGroup(label(title,x,1.5,27,color),
                                 grid(rows,x,-.17,subset,color=color,projective=True)))
        self.beat(panels[0],(5,panels[1]),(10,panels[2]),
                  (13,foot("View at ∞   •   18 crosses and 18 complementary squares")))
        rows = []
        descriptions = ("Line + all three corners","Two parallel lines",
                        "Cross + its corner","Square + the other corners")
        for i, (h, description, count) in enumerate(zip(data.KITTEN,descriptions,(12,12,54,54))):
            y = 1.52 - .92*i
            rows.append(VGroup(label(description,-3.77,y,27),
                               label(set_text(h,True),.77,y,29,BLUE),
                               label(count,4.92,y,35,GOLD)))
        self.beat(heading("FOUR FAMILIES IN THE PROJECTIVE LABELING", y=2.36),
                  (1,rows[0]),(4,rows[1]),(7,rows[2]),(10,rows[3]),
                  (13,foot("12 + 12 + 54 + 54 = 132 hexads",GOLD)))
