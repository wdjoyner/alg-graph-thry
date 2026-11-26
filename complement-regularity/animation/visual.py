"""Shared Manim typography, layout, timing and transformations."""
from manim import FadeIn, FadeOut, Line, RoundedRectangle, Scene, Text, UP, VGroup
from timeline import BEAT
from math_data import INF

BG = "#0B1422"
PANEL = "#14243A"
INK = "#F3F7FF"
MUTED = "#A9BAD1"
BLUE = "#71CEFF"
GOLD = "#FFCA73"
GREEN = "#7CE0B5"
RED = "#FFA092"
LINE = "#4C6382"
FIBERS = (BLUE, GOLD, GREEN, "#F6A1DE", "#BAACFF", RED)


def label(s, size=32, color=INK, mono=False):
    return Text(str(s), font="DejaVu Sans Mono" if mono else "DejaVu Sans",
                font_size=size, color=color, disable_ligatures=True)


def place(obj, x, y):
    return obj.move_to([x,y,0])


def aligned(s, x, y, size=30, color=INK):
    obj = label(s,size,color)
    return place(obj,x+obj.width/2,y)


def point(x):
    return "∞" if x == INF else str(x)


def tuple_label(xs):
    return "(" + ", ".join(map(point,xs)) + ")"


def set_label(xs):
    return "{" + ", ".join(map(point,xs)) + "}"


def card(s, w=1.4, h=.65, color=BLUE, size=27):
    rect = RoundedRectangle(width=w, height=h, corner_radius=.12,
                            stroke_width=1.6, stroke_color=color,
                            fill_color=PANEL, fill_opacity=1)
    return VGroup(rect,label(s,size,color))


def fmt_cycles(p):
    done = set()
    out = []
    for i in range(len(p)):
        if i in done:
            continue
        run = []
        while i not in done:
            run.append(i+1)
            done.add(i)
            i = p[i]
        if len(run)>1:
            out.append("("+" ".join(map(str,run))+")")
    return "".join(out) or "1"


class Chapter(Scene):
    def open(self,title):
        self.camera.background_color = BG
        self.add(aligned("WHICH SYMMETRIC GROUPS HAVE A COMPLEMENT?", -6.5, 3.55, 16, BLUE),
                 aligned(title, -6.5, 2.95, 40),
                 Line([-6.5,2.48,0],[6.5,2.48,0],stroke_width=1,color=LINE),
                 aligned("DAVID JOYNER  /  DRAFT 6", -6.5,-3.63,15,MUTED))
        self.beat_start = 0

    def advance(self, *remove):
        remaining = self.beat_start + BEAT - self.time
        if remaining < .5:
            raise ValueError(f"Beat overran at {self.time}")
        if remove:
            self.wait(remaining-.4)
            self.play(*(FadeOut(obj) for obj in remove),run_time=.4)
        else:
            self.wait(remaining)
        self.beat_start += BEAT

    def reveal(self, *objs, seconds=1):
        self.play(*(FadeIn(obj,shift=.12*UP) for obj in objs),run_time=seconds)
