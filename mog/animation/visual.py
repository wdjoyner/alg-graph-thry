"""Shared style and timed staging for the six Cairo scenes."""
import numpy as np
from manim import *

BG = "#0D1524"
INK = "#EEF3FF"
MUTED = "#A9B9D0"
BLUE = "#64D9F2"
GOLD = "#FFD479"
GREEN = "#69E6B0"
RED = "#FF9A9A"
PANEL = "#17253A"
BEAT = 17


def xy(x, y):
    return np.array([x, y, 0.0])


def label(text, x=0, y=0, size=34, color=INK, width=12.4):
    m = Text(str(text), font="DejaVu Sans", font_size=size, color=color)
    if m.width > width:
        m.scale_to_fit_width(width)
    return m.move_to(xy(x, y))


def name(i):
    return "∞" if i == 11 else str(i)


def set_text(values, projective=False):
    return "{" + ", ".join(name(i) if projective else str(i) for i in sorted(values)) + "}"


def tile(value, selected=False, size=0.72, color=BLUE):
    box = RoundedRectangle(width=size, height=size, corner_radius=0.11,
                           stroke_color=color if selected else "#425777",
                           stroke_width=2, fill_color=color if selected else PANEL,
                           fill_opacity=0.88 if selected else 1)
    return VGroup(box, label(value, size=26 * size / .72, color=BG if selected else INK))


def grid(rows, x=0, y=0, marked=(), *, step=.87, color=BLUE, projective=False):
    return VGroup(*(tile(name(v) if projective else v, v in marked, step*.86, color)
                    .move_to(xy(x + (c-(len(row)-1)/2)*step,
                                y + ((len(rows)-1)/2-r)*step))
                    for r, row in enumerate(rows) for c, v in enumerate(row)))


def heading(text, y=2.05, color=MUTED):
    return label(text, y=y, size=26, color=color)


def foot(text, color=MUTED):
    return label(text, y=-2.69, size=29, color=color)


def hand_row(hand, x=0, y=0, marked=(), color=GREEN):
    return grid([sorted(hand)], x, y, marked, step=.96, color=color)


class Chapter(Scene):
    index = 0
    title = ""

    def setup(self):
        self.camera.background_color = BG
        top = label(self.title, size=32).to_edge(LEFT, buff=.65).set_y(3.47)
        section = label("MINIMOGs  /  %d" % self.index, size=19, color=BLUE)
        section.to_edge(RIGHT, buff=.65).set_y(3.47)
        rule = Line(xy(-6.45, 3.10), xy(6.45, 3.10), stroke_width=1, color="#415573")
        self.add(top, section, rule)
        self.panel = None

    def beat(self, primary, *reveals):
        """Replace the panel, then reveal details at explicit beat-relative seconds."""
        start = self.renderer.time
        incoming = FadeIn(primary, shift=UP*.12)
        if self.panel is None:
            self.play(incoming, run_time=.8)
        else:
            self.play(FadeOut(self.panel, shift=UP*.12), incoming, run_time=.8)
        self.panel = VGroup(primary)
        self.remove(primary)
        self.add(self.panel)
        for at, item in reveals:
            self.wait(max(1/30, start + at - self.renderer.time))
            if isinstance(item, Animation):
                self.play(item, run_time=.9)
            else:
                self.play(FadeIn(item, shift=UP*.14), run_time=.7)
                self.remove(item)
                self.panel.add(item)
        self.wait(max(1/30, start + BEAT - self.renderer.time))
