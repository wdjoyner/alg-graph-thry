"""Stable vertex layouts and graph transformations from the verified data."""
import numpy as np
from manim import (
    ArcBetweenPoints, Arrow, Create, FadeIn, GrowArrow, Indicate, LaggedStart,
    Line, Transform, VGroup,
)
from math_data import (
    AFFINE, AFFINE_BASE, D, E4, E5, EXTRA, J4, JE4, LIFTS, T4, T5,
    affine_mul, forget,
)
from visual import (
    BLUE, FIBERS, GOLD, GREEN, LINE, MUTED, Chapter, aligned, card, label, place,
    set_label, tuple_label,
)


def edges_at(edges, v):
    return [e for e in edges if v in e]


def edge_line(e, xy, color=LINE, width=1.3, trim=.25):
    a,b = (xy[v] for v in e)
    direction = (b-a)/np.linalg.norm(b-a)
    return Line(a+trim*direction,b-trim*direction,color=color,stroke_width=width)


def grid_edge(e, xy, color=LINE, width=1.3):
    """Bow long edges away from intervening vertices in a row or column."""
    a,b = (xy[v] for v in e)
    delta = b-a
    distance = np.linalg.norm(delta)
    if distance < 1.5:
        return edge_line(e,xy,color,width)
    direction = delta/distance
    bend = (.17 if e[0][0] == e[1][0] else -.20) * (distance-1)
    return ArcBetweenPoints(a+.3*direction,b-.3*direction,angle=bend,
                            color=color,stroke_width=width)


def affine_text(ab):
    a,b = ab
    return ("x" if a==1 else f"{a}x")+(f"+{b}" if b else "")


class CayleyGraphs(Chapter):
    def construct(self):
        self.open("Arrangement graphs as Cayley graphs")
        xy = {(a,b):np.array([-5.91+1.38*b,1.62-.88*a,0]) for a,b in T5}
        nodes = {v:place(card(tuple_label(v),.85,.48,
                              GREEN if v==AFFINE_BASE else MUTED,17),*xy[v][:2])
                 for v in T5}
        all_edges = VGroup(*(grid_edge(e,xy) for e in E5))
        base = AFFINE_BASE
        base_edges = edges_at(E5,base)

        def star(edges):
            return VGroup(*(grid_edge(e,xy,BLUE if e[0][0]==e[1][0] else GOLD,4)
                            for e in edges))
        colors = {next(v for v in e if v!=base):
                  BLUE if e[0][0]==e[1][0] else GOLD for e in base_edges}
        bright = star(base_edges)
        self.add(all_edges.set_stroke(opacity=0))
        self.play(LaggedStart(*(FadeIn(nodes[v]) for v in T5),lag_ratio=.05),run_time=3)
        self.play(all_edges.animate.set_stroke(opacity=.6))
        self.add(bright.set_z_index(1))
        for node in nodes.values():
            node.set_z_index(2)
        self.play(Create(bright),run_time=1.3)
        note = VGroup(aligned("T(5,2)",1.1,1.48,44),
                      aligned("20 ordered pairs",1.1,.72,28,MUTED),
                      aligned("Change one coordinate",1.1,-.04,28),
                      aligned("Second slot changes",1.1,-.99,23,BLUE),
                      aligned("First slot changes",1.1,-1.52,23,GOLD))
        self.reveal(note)
        self.advance(note)

        self.play(*(Transform(nodes[v],place(card(affine_text(AFFINE[v]),.85,.48,
                         GREEN if v==base else colors.get(v,MUTED),17),*xy[v][:2]))
                    for v in T5),run_time=2)
        label_rule = VGroup(aligned("(b, a+b) ↦ ax+b",1.1,1.45,35),
                            aligned("D  ·  neighbors of x ↦ x",1.1,.57,25,MUTED),
                            aligned("2x,  3x,  4x",1.1,-.27,33,BLUE),
                            aligned("2x+4,  3x+3,  4x+2",1.1,-.98,30,GOLD))
        self.reveal(label_rule)
        self.advance(label_rule)

        neighbor = (1,2)
        translated_edges = [tuple(sorted(tuple((p+1)%5 for p in v) for v in e))
                            for e in base_edges]
        translated = star(translated_edges).set_z_index(1)
        move = VGroup(aligned("Translate by t ↦ t+1",1.1,1.4,30),
                      aligned("(0, 1) ↦ (1, 2)",1.1,.57,30,GREEN),
                      aligned("d  ↦  (t ↦ t+1) ∘ d",1.1,-.28,27,BLUE))
        self.reveal(move)
        self.wait(4)
        translated_colors = {tuple((p+1)%5 for p in v): c for v,c in colors.items()}
        recolor = []
        for v,node in nodes.items():
            color = GREEN if v==neighbor else translated_colors.get(v,MUTED)
            recolor.append(Transform(node,place(card(affine_text(AFFINE[v]),.85,.48,
                                                       color,17),*xy[v][:2])))
        self.play(Transform(bright,translated),*recolor,run_time=2)
        self.advance(move)

        rule = VGroup(aligned("Cay(AGL₁(5), D)",1.1,1.44,35),
                      aligned("At x, neighbors are xd",1.1,.57,26),
                      aligned("d ranges over D",1.1,-.13,26,MUTED),
                      aligned("u v ∼ x v  ⇔  (u⁻¹x)v ∼ v",1.1,-1.2,23,BLUE))
        self.reveal(rule)
        self.wait(5)
        index = {ab:v for v,ab in AFFINE.items()}
        target = index[affine_mul((1,1),(2,0))]
        self.play(Indicate(nodes[target],color=BLUE),run_time=1.7)
        self.advance()


# Polar embedding from Draft 6, Figure “The arrangement graph T(4,2)”.
POLAR = {
    (1,2):(45,1), (1,3):(0,2), (1,4):(315,1), (2,1):(225,3.3),
    (2,3):(315,3.3), (2,4):(270,2), (3,1):(180,2), (3,2):(135,1),
    (3,4):(225,1), (4,1):(135,3.3), (4,2):(90,2), (4,3):(45,3.3),
}


def polar(angle,r,x,y):
    theta = np.deg2rad(angle)
    return np.array([x+r*np.cos(theta),y+r*np.sin(theta),0])


class ForgettingOrder(Chapter):
    def construct(self):
        self.open("Forgetting order")
        colors = dict(zip(J4,FIBERS))
        txy = {v:polar(a,r*.69,-3.32,-.19) for v,(a,r) in POLAR.items()}
        # Place complementary subsets opposite on the hexagon.
        j_order = ((1,2),(1,3),(1,4),(3,4),(2,4),(2,3))
        jxy = {v:polar(90-60*i,1.57,3.26,-.18) for i,v in enumerate(j_order)}
        upstairs = VGroup(*(edge_line(e,txy,LINE,1.65) for e in E4))
        downstairs = VGroup(*(edge_line(e,jxy,LINE,1.65) for e in JE4))
        t_nodes = {v:card(tuple_label(v),.77,.43,colors[forget(v)],16).move_to(txy[v])
                   for v in T4}
        j_nodes = {v:card(set_label(v),.91,.48,colors[v],18).move_to(jxy[v]) for v in J4}
        for node in (*t_nodes.values(),*j_nodes.values()):
            node.set_z_index(2)
        left = place(label("T(4,2)   ·   ordered",30),-3.32,1.99)
        right = place(label("J(4,2)   ·   unordered",30),3.26,1.99)
        arrow = Arrow([-.78,-.19,0],[.74,-.19,0],color=MUTED,buff=0)
        footer = place(label("(1, 2), (2, 1)  ↦  {1, 2}",29,colors[(1,2)]),0,-2.82)
        self.reveal(left,*t_nodes.values())
        self.play(Create(upstairs),run_time=1.5)
        self.wait(3)
        self.reveal(right,*j_nodes.values())
        self.play(Create(downstairs),GrowArrow(arrow))
        self.reveal(footer)
        self.advance(footer)

        highlight = VGroup(*(edge_line(e,txy,BLUE,4) for e in LIFTS),
                           edge_line(((1,2),(1,3)),jxy,BLUE,4)).set_z_index(1)
        lift = place(label("Replace 2 by 3 in the same slot.",30,BLUE),0,-2.82)
        self.play(Create(highlight[-1]))
        self.wait(3)
        self.play(Create(highlight[0]),Create(highlight[1]),run_time=2)
        self.reveal(lift)
        self.advance(lift,highlight)

        # Use copies of the actual upstairs edges and vertices so their originals
        # remain available as a stable reference during the quotient animation.
        copies = VGroup(*(t_nodes[v].copy() for v in T4))
        wires = VGroup(*(edge_line(e,txy,BLUE,1.5) for e in E4)).set_z_index(1)
        self.add(wires,copies)
        self.wait(1)
        self.play(*(Transform(c,j_nodes[forget(v)].copy()) for c,v in zip(copies,T4)),
                  *(Transform(w,edge_line(tuple(map(forget,e)),jxy,BLUE,1.5))
                    for w,e in zip(wires,E4)),run_time=3)
        self.remove(wires,copies)
        count = place(label("k! orders per set   ·   one edge lift at each ordered tuple",26,BLUE),0,-2.82)
        self.reveal(count)
        self.advance(count,left,right,arrow,upstairs,downstairs,*t_nodes.values(),*j_nodes.values())

        main = place(label("A complement gives a Cayley representation",38,BLUE),0,1.37)
        wider = place(label("Aut(T(n,k)) ≅ Sₙ × Sₖ",43),0,.34)
        pairs = place(label("    ".join(tuple_label(p) for p in EXTRA),25,GOLD),0,-1.03)
        subtitle = place(label("Six extra Cayley cases (n, k)",24,MUTED),0,-.53)
        cites = place(label("Yin, Feng, Zhou & Guo (2021)   ·   classification cited in Draft 6",22,MUTED),0,-2.22)
        self.reveal(main)
        self.wait(2)
        self.reveal(wider)
        self.wait(3)
        self.reveal(subtitle,pairs,cites)
        self.advance()
