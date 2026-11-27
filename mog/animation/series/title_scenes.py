"""Manim scenes for the series titles and end credits.

Everything that can change lives in the series files: beat and card
lengths in titles/outline.json and end_credits/outline.json, wording in
series.json and credits.json, colors in cast.json, and the mathematics
(MINIMOG cells, the kitten triangle, the opening hand, the codeword) in
math_objects.json.  This file holds only the choreography: one function
per beat or card ID.  A screenplay ID with no function here is an error.

Render through make_titles.py, which also assembles each episode's
opening and credits and checks their lengths against the outlines.

Timing is counted in frames.  Each animation is given a run time half a
frame short of a whole number of frames, so Manim draws exactly that
many frames, and every beat is padded to exactly its screenplay length.
"""
import json
from pathlib import Path

import numpy as np
from manim import *

HERE = Path(__file__).resolve().parent
FPS = 30


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


SERIES = load("series.json")
CAST = load("cast.json")["characters"]
CREDITS = {s["id"]: s for s in load("credits.json")["sections"]}
TITLES = load("titles/outline.json")
ROLL = load("end_credits/outline.json")
OBJ = load("math_objects.json")["objects"]
EPISODES = {e["number"]: e for e in SERIES["episodes"]}

# Palette and font of the existing film (../visual.py).
BG, INK, MUTED = "#0D1524", "#EEF3FF", "#A9B9D0"
BLUE, GOLD, GREEN, PANEL, EDGE = "#64D9F2", "#FFD479", "#69E6B0", "#17253A", "#425777"
FONT = "DejaVu Sans"

MINIMOG = OBJ["minimog"]["rows"]
TRIANGLE = OBJ["kitten:triangle"]["spots"]
CORNERS = set(OBJ["kitten:triangle"]["corners"])
OPENING_HAND = OBJ["hand:example"]["cards"]
HEXAD = OBJ["hand:1to6"]["cards"]
DEGREE = OBJ["count:johnson"]["degree"]
WORD = OBJ["tetracode"]["word_a1_b1"]          # row of the lit cell in each column
assert OBJ["hand:1to6"]["hexad"] and DEGREE == 36


def xy(x, y):
    return np.array([x, y, 0.0])


def words(s, n=None):
    """Fill {series_title}, {tagline}, {number}, {title} placeholders."""
    ep = EPISODES.get(n, {})
    return s.format(series_title=SERIES["series_title"], tagline=SERIES["tagline"],
                    number=ep.get("number", ""), title=ep.get("title", ""))


def text(s, size=34, color=INK, width=12.8, slant=NORMAL, weight=NORMAL):
    m = Text(s, font=FONT, font_size=size, color=color, slant=slant, weight=weight)
    if m.width > width:
        m.scale_to_fit_width(width)
    return m


# ---------------------------------------------------------------- glyphs

def card(value, h=0.84, face=True):
    box = RoundedRectangle(width=h * 0.72, height=h, corner_radius=h * 0.11,
                           stroke_color=EDGE, stroke_width=2, fill_color=PANEL, fill_opacity=1)
    if not face:
        inner = RoundedRectangle(width=h * 0.5, height=h * 0.78, corner_radius=h * 0.07,
                                 stroke_color=BLUE, stroke_width=1.5, stroke_opacity=0.5)
        return VGroup(box, inner)
    return VGroup(box, text(str(value), size=34 * h / 0.84))


def lit(c, color):
    """Animations that color a face-up card."""
    return [c[0].animate.set_fill(color, 0.92).set_stroke(color), c[1].animate.set_color(BG)]


def kitten(key, scale=1.0):
    """A simple vector kitten in the character's colors (animatic stand-in)."""
    pal = CAST[key]["design"]["palette"]
    fur = pal["primary"]
    line = dict(stroke_color=INK, stroke_width=2, stroke_opacity=0.55)
    body = Ellipse(width=1.05, height=0.78, fill_color=fur, fill_opacity=1, **line).shift(DOWN * 0.62)
    tail = CubicBezier(xy(0.45, -0.75), xy(1.05, -0.8), xy(1.0, -0.1), xy(0.8, 0.1),
                       stroke_color=fur, stroke_width=9)
    head = Circle(radius=0.4, fill_color=fur, fill_opacity=1, **line)
    ears = VGroup(*(Polygon(xy(s * 0.36, 0.14), xy(s * 0.3, 0.55), xy(s * 0.06, 0.37),
                            fill_color=fur, fill_opacity=1, **line) for s in (-1, 1)))
    eye_color = GOLD if key == "sophie" else "#1B2230"
    eyes = VGroup(*(Ellipse(width=0.09, height=0.13, fill_color=eye_color, fill_opacity=1,
                            stroke_width=0).move_to(xy(s * 0.15, 0.05)) for s in (-1, 1)))
    nose = Triangle(fill_color="#F2A0B6", fill_opacity=1, stroke_width=0).scale(0.045)
    nose.rotate(PI).move_to(xy(0, -0.08))
    marks = VGroup()
    if key == "pascal":
        marks = VGroup(*(Line(xy(x, 0.38), xy(x * 0.8, 0.22), stroke_color=pal["stripes"], stroke_width=4)
                         for x in (-0.12, 0, 0.12)))
    elif key == "sophie":
        marks = Ellipse(width=0.42, height=0.36, fill_color=pal["bib"], fill_opacity=1,
                        stroke_width=0).move_to(xy(0, -0.5))
    elif key == "euphemia":
        marks = VGroup(Circle(radius=0.15, fill_color=pal["patch1"], fill_opacity=1, stroke_width=0).move_to(xy(-0.2, 0.2)),
                       Circle(radius=0.12, fill_color=pal["patch2"], fill_opacity=1, stroke_width=0).move_to(xy(0.2, 0.22)))
    face = VGroup(ears, head, marks if key != "sophie" else VGroup(), eyes, nose)
    k = VGroup(tail, body, marks if key == "sophie" else VGroup(), face)
    k.face, k.eyes = face, eyes
    k.scale(scale)
    return k


def bow(k, angle=0.45):
    """Tip the kitten's face forward about its neck."""
    neck = k.face.get_bottom()
    return Rotate(k.face, -angle, about_point=neck, rate_func=there_and_back)


def hop(k, height=0.5):
    return k.animate(rate_func=there_and_back).shift(UP * height)


def star(center=ORIGIN, radius=2.7):
    """One hand as a dot, with an edge to each of its 36 neighbors."""
    ends = [center + radius * np.array([np.cos(a), np.sin(a), 0])
            for a in np.linspace(PI / 2, PI / 2 - TAU, DEGREE, endpoint=False)]
    edges = VGroup(*(Line(center, e, stroke_color=BLUE, stroke_width=1.6, stroke_opacity=0.7) for e in ends))
    tips = VGroup(*(Dot(e, radius=0.045, color=BLUE) for e in ends))
    dot = Dot(center, radius=0.13, color=GREEN)
    return VGroup(edges, tips, dot), ends


def minimog_spots(center=ORIGIN, step=1.02):
    spots = {}
    for r, row in enumerate(MINIMOG):
        for c, v in enumerate(row):
            spots[v] = center + xy((c - 1.5) * step, (1 - r) * step * 1.18)
    return spots


def triangle_spots(center=ORIGIN, sx=0.6, sy=0.68):
    """Positions of the kitten's 18 labels; repeated labels are the same point."""
    return [(v, center + xy(x * sx, (y - 3) * sy)) for x, y, v in TRIANGLE]


def kitten_triangle(center=ORIGIN, scale=1.0, h=0.5):
    tri = Polygon(*(center + xy(x * 0.6, (y - 3) * 0.68) for x, y in ((-5, 0), (5, 0), (0, 6))),
                  stroke_color="#6687A9", stroke_width=2)
    cards = VGroup()
    for v, p in triangle_spots(center):
        c = card(v, h=h).move_to(p)
        if v in CORNERS:
            c[0].set_fill(GOLD, 0.92).set_stroke(GOLD)
            c[1].set_color(BG)
        cards.add(c)
    g = VGroup(tri, cards)
    return g.scale(scale, about_point=center)


def minimog_grid(center=ORIGIN, h=0.84, codeword=False):
    g = VGroup()
    for v, p in minimog_spots(center).items():
        c = card(v, h=h).move_to(p)
        if codeword and any(MINIMOG[WORD[col]][col] == v for col in range(4)):
            c[0].set_fill(GOLD, 0.92).set_stroke(GOLD)
            c[1].set_color(BG)
        g.add(c)
    return g


SIT = {"pascal": -4.6, "sophie": -1.55, "ada": 1.55, "euler": 4.6}


def sitting_row(y=-3.1, scale=0.55):
    return {k: kitten(k, scale).move_to(xy(x, y)) for k, x in SIT.items()}


def title_text():
    return text(words("{series_title}"), size=52, weight=BOLD).move_to(xy(0, 0.45))


def tagline_text():
    return text(words("{tagline}"), size=30, color=MUTED, slant=ITALIC).move_to(xy(0, -0.55))


# ---------------------------------------------------------------- timing

class Timed(Scene):
    """Frame-exact staging: go() plays, hold() waits, beat() pads to a length."""

    def setup(self):
        self.camera.background_color = BG
        self.frames = 0

    def go(self, *anims, t=0.5):
        k = max(1, round(t * FPS))
        self.play(*anims, run_time=(k - 0.5) / FPS)
        self.frames += k

    def hold(self, t=None, frames=None):
        k = frames if frames is not None else round(t * FPS)
        if k > 0:
            # A frozen wait repeats one frame int(duration * fps) times, rounding
            # down; draw every wait frame by frame instead, so it counts like play().
            self.wait((k - 0.5) / FPS, frozen_frame=False)
            self.frames += k

    def beat(self, seconds, body, name):
        start, target = self.frames, round(seconds * FPS)
        body()
        used = self.frames - start
        if used > target:
            raise ValueError(f"{name}: choreography takes {used} frames, screenplay allows {target}")
        self.hold(frames=target - used)

    def clear_all(self, t=0.4, keep=()):
        gone = [m for m in self.mobjects if m not in keep]
        if gone:
            self.go(*(FadeOut(m) for m in gone), t=t)


# ---------------------------------------------------------------- main title

class MainTitleBase(Timed):
    version = "full"

    def construct(self):
        spec = TITLES["main_title"]
        beats = {b["id"]: b for b in spec["beats"]}
        version = spec["versions"][self.version]
        self.cards = {v: card(v) for v in range(12)}
        self.kits = {}
        for bid in version["beats"]:
            seconds = version.get("seconds", {}).get(bid, beats[bid]["seconds"])
            fn = getattr(self, "beat_" + bid.replace(".", "_"), None)
            if fn is None:
                raise NotImplementedError(f"no choreography for {bid}")
            self.beat(seconds, fn, bid)

    def beat_mt_b01(self):
        """Pascal flicks the deck open: twelve cards fan out, 0 to 11."""
        deck = VGroup(*(self.cards[v] for v in range(12)))
        for i, c in enumerate(deck):
            c.move_to(xy(0.02 * i, -0.02 * i))
        pascal = kitten("pascal", 0.7).move_to(xy(-7.6, -2.6))
        self.kits["pascal"] = pascal
        self.add(deck)
        self.go(pascal.animate.move_to(xy(-5.6, -2.6)), t=0.4)
        self.go(LaggedStart(*(self.cards[v].animate.move_to(xy((v - 5.5) * 0.98, 0))
                              for v in range(12)), lag_ratio=0.05),
                hop(pascal, 0.3), t=1.2)

    def beat_mt_b02(self):
        """The cards fly into their MINIMOG cells; Ada straightens the last one."""
        spots = minimog_spots(xy(0, 0.2))
        last = MINIMOG[-1][-1]
        ada = kitten("ada", 0.7).move_to(xy(7.6, -2.6))
        self.kits["ada"] = ada
        order = [v for row in MINIMOG for v in row]
        moves = []
        for v in order:
            target = self.cards[v].copy().move_to(spots[v])
            if v == last:
                target.rotate(0.22)
            moves.append(self.cards[v].animate(path_arc=0.5).become(target))
        self.go(LaggedStart(*moves, lag_ratio=0.06), ada.animate.move_to(xy(5.6, -2.6)), t=2.0)
        self.go(Rotate(self.cards[last], -0.22), hop(ada, 0.25), t=0.6)

    def beat_mt_b03(self):
        """The cells slide into Curtis's kitten; Sophie traces the last side."""
        center = xy(0, 0.35)
        tri = kitten_triangle(center)
        outline, targets = tri[0], tri[1]
        sophie = kitten("sophie", 0.45).move_to(xy(-7.6, -1.6))
        self.kits["sophie"] = sophie
        first, extra = {}, []
        for v, t in zip((v for v, _ in triangle_spots(center)), targets):
            if v in first:
                extra.append((v, t))
            else:
                first[v] = t
        a, b, c = outline.get_vertices()
        sides = [Line(c, a), Line(a, b), Line(b, c)]
        for s in sides:
            s.set_stroke("#6687A9", 2)
        self.go(*(self.cards[v].animate.become(first[v]) for v in range(12)),
                Create(sides[0]), Create(sides[1]), self.kits["ada"].animate.shift(RIGHT * 2.5),
                sophie.animate.move_to(b + DOWN * 0.15), t=1.6)
        self.extra = [t.copy() for _, t in extra]
        self.go(*(TransformFromCopy(self.cards[v], m) for (v, _), m in zip(extra, self.extra)), t=0.5)
        self.go(Create(sides[2]), MoveAlongPath(sophie, Line(b + DOWN * 0.15, c + UP * 0.2)), t=1.0)
        self.sides = VGroup(*sides)

    def beat_mt_b04(self):
        """The hexad 1 to 6 lights up, shrinks to a dot, and 36 edges sprout."""
        euler = kitten("euler", 0.7).move_to(xy(7.6, -2.6))
        self.kits["euler"] = euler
        six = [self.cards[v] for v in HEXAD]
        self.go(*(a for c in six for a in lit(c, GREEN)), euler.animate.move_to(xy(5.6, -2.6)), t=0.6)
        g, _ = star()
        edges, tips, dot = g
        rest = [self.cards[v] for v in range(12) if v not in HEXAD] + self.extra + [self.sides]
        self.go(*(c.animate.move_to(ORIGIN).scale(0.05).set_opacity(0) for c in six),
                *(FadeOut(m) for m in rest), FadeOut(self.kits["sophie"]),
                FadeIn(dot, scale=3), t=0.8)
        self.remove(*six)
        self.go(LaggedStart(*(GrowFromPoint(e, ORIGIN) for e in edges), lag_ratio=0.02),
                FadeIn(tips, lag_ratio=0.02),
                euler.eyes.animate(rate_func=there_and_back).stretch(0.1, 1), t=1.2)
        self.go(euler.animate.shift(LEFT * 0.4 + UP * 0.15).rotate(0.12), t=0.4)
        self.star = g

    def beat_mt_b05(self):
        """The series title writes itself along the edges and settles; the kittens pounce."""
        final = title_text()
        _, ends = star()
        glyphs = final.copy()
        for i, gl in enumerate(glyphs):
            gl.move_to(ends[i % len(ends)]).scale(0.7)
        row = sitting_row()
        here = [k for k in ("pascal", "sophie", "ada", "euler") if k in self.kits]
        missing = {k: row[k].copy().shift(DOWN * 2) for k in SIT if k not in self.kits}
        self.add(*missing.values())
        self.kits.update(missing)
        self.go(LaggedStart(*(GrowFromPoint(gl, ORIGIN) for gl in glyphs), lag_ratio=0.03),
                self.star.animate.set_opacity(0.3),
                *(self.kits[k].animate.become(row[k]) for k in SIT), t=1.5)
        self.go(*(Transform(gl, t) for gl, t in zip(glyphs, final)), t=1.0)
        self.go(*(hop(self.kits[k], 0.7) for k in SIT), t=0.6)
        self.title = glyphs

    def beat_mt_b06(self):
        """The tagline fades in under the title."""
        self.go(FadeIn(tagline_text(), shift=UP * 0.15), t=0.8)


class MainTitle(MainTitleBase):
    version = "full"


class MainTitleShort(MainTitleBase):
    version = "short"

    def beat_mt_b05(self):
        # The short version reaches the title from the MINIMOG, not the star.
        final = title_text()
        row = sitting_row()
        for k in SIT:
            if k not in self.kits:
                self.kits[k] = row[k].copy().shift(DOWN * 2)
                self.add(self.kits[k])
        self.go(*(FadeOut(c) for c in self.cards.values()), Write(final),
                *(self.kits[k].animate.become(row[k]) for k in SIT), t=1.6)
        self.go(*(hop(self.kits[k], 0.7) for k in SIT), t=0.6)


def end_of_main_title(scene):
    """Rebuild the main title's last frame, so a subtitle can pick up from it."""
    g, _ = star()
    g.set_opacity(0.3)
    row = sitting_row()
    title, tag = title_text(), tagline_text()
    scene.add(g, title, tag, *row.values())
    return g, title, tag, row


# ---------------------------------------------------------------- subtitles

def subtitle_texts(n, y_episode, y_title, size=44):
    spec = next(s for s in TITLES["subtitles"] if s["episode"] == n)
    ep_line, title_line = (words(t, n) for t in spec["text"])
    return (text(ep_line, size=28, color=MUTED).move_to(xy(0, y_episode)),
            text(title_line, size=size, weight=BOLD).move_to(xy(0, y_title)))


class SubtitleBase(Timed):
    episode = 1

    def construct(self):
        spec = next(s for s in TITLES["subtitles"] if s["episode"] == self.episode)
        fn = getattr(self, f"sub_ep{self.episode}", None)
        if fn is None:
            raise NotImplementedError(f"no choreography for {spec['id']}")
        self.state = end_of_main_title(self)
        self.beat(spec["seconds"], fn, spec["id"])

    def lead_only(self, lead, t=0.5):
        g, title, tag, row = self.state
        self.go(FadeOut(title), FadeOut(tag), *(FadeOut(row[k]) for k in row if k != lead), t=t)
        return g, row[lead]

    def sub_ep1(self):
        """The dot bursts back into cards, dealt into the opening hand and the pile."""
        g, pascal = self.lead_only("pascal")
        table = RoundedRectangle(width=11.6, height=3.5, corner_radius=0.3, fill_color="#12324A",
                                 fill_opacity=1, stroke_color=EDGE).move_to(xy(0, -1.25))
        ep, title = subtitle_texts(1, 2.55, 1.45)
        hand = [card(v).move_to(xy((i - 2.5) * 0.98, -0.45)) for i, v in enumerate(OPENING_HAND)]
        pile_values = [v for v in range(12) if v not in OPENING_HAND]
        pile = [card(v, face=False).scale(0.8).move_to(xy((i - 2.5) * 0.82, -2.1))
                for i, v in enumerate(pile_values)]
        self.go(FadeOut(g[0]), FadeOut(g[1]), FadeIn(table), Write(ep), Write(title),
                *(GrowFromPoint(c, ORIGIN) for c in hand + pile), t=1.0)
        self.remove(g[2])
        pascal.set_z_index(5)
        self.go(pascal.animate.move_to(xy(-4.9, -0.6)), t=0.5)
        self.go(hop(pascal, 0.25), *(a for a in lit(hand[0], GREEN)), t=0.4)
        self.go(*(a for a in [hand[0][0].animate.set_fill(PANEL, 1).set_stroke(EDGE),
                              hand[0][1].animate.set_color(INK)]), t=0.3)

    def sub_ep2(self):
        """Push into the kitten triangle; the subtitle writes along its base."""
        g, sophie = self.lead_only("sophie")
        center = xy(0, 0.05)
        tri = kitten_triangle(center, h=0.5)
        ep, title = subtitle_texts(2, 3.35, -3.3)
        push = 1.08
        apex = center + (tri[0].get_vertices()[2] - center) * push
        # Sophie climbs to the apex corner first, so she never crosses the title.
        self.go(FadeOut(g), GrowFromPoint(tri, ORIGIN), Write(ep),
                sophie.animate.scale(0.8).move_to(apex + UP * 0.5 + RIGHT * 0.55), t=0.9)
        self.go(tri.animate.scale(push, about_point=center), Write(title), t=0.9)
        self.go(ShowPassingFlash(tri[0].copy().set_stroke(GOLD, 5), time_width=0.4), t=0.9)

    def sub_ep3(self):
        """The MINIMOG returns and the codeword 1, 1, 2, 0 lights one cell per column."""
        g, ada = self.lead_only("ada")
        center = xy(0, 0.3)
        grid = minimog_grid(center)
        ep, title = subtitle_texts(3, 3.3, -2.75)
        self.go(FadeOut(g), *(GrowFromPoint(c, ORIGIN) for c in grid), Write(ep), Write(title), t=1.0)
        lit_cards = [c for c in grid if any(c[1].text == str(MINIMOG[WORD[col]][col]) for col in range(4))]
        self.go(LaggedStart(*(AnimationGroup(*lit(c, GOLD)) for c in lit_cards), lag_ratio=0.25),
                ada.animate.move_to(xy(4.6, -1.0)), t=1.0)
        brow = Arc(radius=0.12, start_angle=PI * 0.2, angle=PI * 0.6, stroke_color=INK,
                   stroke_width=3).move_to(ada.eyes[1].get_center() + UP * 0.14)
        self.go(FadeIn(brow, shift=UP * 0.08), t=0.3)

    def sub_ep4(self):
        """The star stays; the subtitle travels out along one edge."""
        g, euler = self.lead_only("euler")
        ep, title = subtitle_texts(4, 3.3, -3.25)
        start = title.copy().scale(0.15).move_to(ORIGIN).set_opacity(0)
        self.add(start)
        self.go(g.animate.set_opacity(1), Write(ep), t=0.5)
        self.go(Transform(start, title, path_func=straight_path()),
                euler.animate.move_to(xy(-5.2, -2.2)), t=1.2)


for _n in EPISODES:
    globals()[f"Subtitle{_n}"] = type(f"Subtitle{_n}", (SubtitleBase,), {"episode": _n})


# ---------------------------------------------------------------- end credits

def section_text(sid, flags):
    """Heading and lines of a credits section, as they appear on screen."""
    s = CREDITS[sid]
    lines = list(s.get("names", []))
    if s.get("from_cast") == "characters":
        lines = [c["name"] for k, c in CAST.items() if c.get("principal") or (k in flags)]
    elif s.get("from_cast") == "voices":
        lines = []
        for k, c in CAST.items():
            if c.get("principal") or (k in flags):
                chosen = c["voice"].get("chosen")
                lines.append(s["format"].format(name=c["name"], chosen=chosen) if chosen
                             else f"{c['name']} — Kokoro voice to be cast")
    return s["heading"], lines, s.get("footer")


def voice_lines(credit):
    """'Pascal — Kokoro voice to be cast' -> ['Kokoro voice', 'to be cast']."""
    voice = credit.split(" — ", 1)[1]
    return ["Kokoro voice", "to be cast"] if voice.endswith("to be cast") else [voice]


def heading(s, y=3.15):
    return text(s, size=26, color=MUTED).move_to(xy(0, y))


def block(lines, size=30, color=INK, buff=0.22, width=12.6, align=None):
    """Lines at one size; if the widest is too wide, the whole block shrinks together."""
    g = VGroup(*(text(l, size=size, color=color, width=1e9) for l in lines))
    g.arrange(DOWN, buff=buff, aligned_edge=align if align is not None else ORIGIN)
    widest = max(m.width for m in g)
    if widest > width:
        g.scale(width / widest)
    return g


class CreditsBase(Timed):
    """The credits cards, in order.  'flags' turns on cards marked 'when'."""
    flags = ()

    def construct(self):
        for c in ROLL["cards"]:
            if c.get("when") and c["when"] not in self.flags:
                continue
            fn = getattr(self, "card_" + c["id"].replace(".", "_"), None)
            if fn is None:
                raise NotImplementedError(f"no choreography for {c['id']}")
            self.beat(c["seconds"], fn, c["id"])

    def card_ec_c01(self):
        """Series authors: Pascal deals three cards that flip to show the names."""
        self.clear_all()
        head, names, _ = section_text("authors", self.flags)
        h = heading(head, 2.2)
        pascal = kitten("pascal", 0.6).move_to(xy(-6.0, -2.6))
        backs, faces = [], []
        for i, nm in enumerate(names):
            x = (i - 1) * 4.2
            box = RoundedRectangle(width=3.9, height=1.5, corner_radius=0.16, fill_color=PANEL,
                                   fill_opacity=1, stroke_color=EDGE)
            back = VGroup(box.copy(), RoundedRectangle(width=3.5, height=1.1, corner_radius=0.1,
                                                       stroke_color=BLUE, stroke_opacity=0.5,
                                                       stroke_width=1.5)).move_to(xy(x, 0))
            face = VGroup(box.copy(), text(nm, size=30, width=3.6)).move_to(xy(x, 0))
            backs.append(back)
            faces.append(face)
        for b in backs:
            b.save_state()
            b.move_to(xy(-6.0, -1.8)).scale(0.3)
        self.go(FadeIn(h), FadeIn(pascal), t=0.3)
        self.go(LaggedStart(*(Restore(b) for b in backs), lag_ratio=0.25), hop(pascal, 0.25), t=0.9)
        for f in faces:
            f.stretch(0.02, 0)
        self.go(*(b.animate.stretch(0.02, 0) for b in backs), t=0.2)
        self.remove(*backs)
        self.go(*(f.animate.stretch(50, 0) for f in faces), t=0.25)

    def card_ec_c02(self):
        """Based on: the paper's title page slides in; Ada taps it."""
        self.clear_all()
        head, names, _ = section_text("based_on", self.flags)
        page = VGroup(Rectangle(width=1.7, height=2.3, fill_color=INK, fill_opacity=0.95, stroke_width=0),
                      *(Line(xy(-0.75, 0.9 - 0.32 * i), xy(0.75 if i else 0.4, 0.9 - 0.32 * i),
                             stroke_color=BG, stroke_width=3 if i else 5) for i in range(6))).move_to(xy(-5.4, -0.1))
        cite = names[0]
        first = cite.index(", ") + 1
        cut = cite.index(",\"") + 2 if ",\"" in cite else len(cite)
        lines = block([cite[:first], cite[first:cut].strip(), cite[cut:].strip()], size=32,
                      width=8.6, align=LEFT)
        lines.next_to(page, RIGHT, buff=0.6)
        ada = kitten("ada", 0.55).move_to(xy(-6.6, -2.5))
        self.go(FadeIn(heading(head, 2.4)), FadeIn(page, shift=RIGHT * 2), FadeIn(ada), t=0.6)
        self.go(AddTextLetterByLetter(lines[0]), t=0.3)
        self.go(AddTextLetterByLetter(lines[1]), t=0.8)
        self.go(AddTextLetterByLetter(lines[2]), t=0.3)
        self.go(ada.animate.move_to(page.get_corner(DL) + xy(0.1, -0.2)), t=0.4)
        self.go(hop(ada, 0.2), t=0.3)

    def card_ec_c03(self):
        """The mathematics of: each name beside the picture it gave the series."""
        self.clear_all()
        head, names, _ = section_text("mathematics", self.flags)
        icons = [kitten_triangle(ORIGIN, 0.16, h=0.6),
                 minimog_grid(ORIGIN, h=0.84).scale(0.2),
                 VGroup(*(Dot(0.3 * np.array([np.cos(a), np.sin(a), 0]), radius=0.06, color=GREEN)
                          for a in np.linspace(0, TAU, 6, endpoint=False))),
                 VGroup(RoundedRectangle(width=0.9, height=0.5, corner_radius=0.08, fill_color="#12324A",
                                         fill_opacity=1, stroke_color=EDGE),
                        *(card(v, h=0.3).move_to(xy((i - 1) * 0.24, 0)) for i, v in enumerate((0, 2, 4)))),
                 VGroup(*(Rectangle(width=0.75, height=0.14, fill_color=c, fill_opacity=1, stroke_width=0)
                          .move_to(xy(0.03 * i, 0.16 * i - 0.16)) for i, c in enumerate((BLUE, GOLD, GREEN))))]
        rows = VGroup()
        labels = block(names, size=28, width=10.6, align=LEFT)
        for i, (icon, label) in enumerate(zip(icons, labels)):
            y = 1.75 - 0.95 * i
            icon.move_to(xy(-5.6, y))
            label.move_to(xy(-4.75, y), aligned_edge=LEFT)
            rows.add(VGroup(icon, label))
        sophie = kitten("sophie", 0.45).move_to(xy(-7.4, -3.2))
        self.go(FadeIn(heading(head, 2.95)), FadeIn(sophie), t=0.4)
        self.go(LaggedStart(*(FadeIn(r, shift=RIGHT * 0.3) for r in rows), lag_ratio=0.35),
                sophie.animate.move_to(xy(5.8, -3.2)), t=2.4)

    def card_ec_c04(self):
        """Featuring and voices: the kittens bow in turn; Pascal topples, Euler is late."""
        self.clear_all()
        _, chars, _ = section_text("featuring", self.flags)
        _, voices, footer = section_text("voices", self.flags)
        keys = [k for k, c in CAST.items() if c.get("principal") or k in self.flags]
        n = len(keys)
        kits = {}
        for i, k in enumerate(keys):
            x = (i - (n - 1) / 2) * (12.0 / max(n, 4))
            kits[k] = kitten(k, 0.8).move_to(xy(x, 0.9))
        labels = VGroup()
        for i, k in enumerate(keys):
            x = kits[k].get_x()
            labels.add(VGroup(text(chars[i], size=30, weight=BOLD).move_to(xy(x, -0.55)),
                              block(voice_lines(voices[i]), size=20, color=MUTED, buff=0.08, width=2.6)
                              .next_to(xy(x, -0.8), DOWN, buff=0.05)))
        heads = VGroup(text("Featuring", size=26, color=MUTED), text("Voices", size=26, color=MUTED))
        heads.arrange(RIGHT, buff=0.6).move_to(xy(0, 2.75))
        foot = text(footer, size=22, color=MUTED).move_to(xy(0, -2.45))
        self.go(FadeIn(heads), *(FadeIn(kits[k], shift=UP * 0.3) for k in keys), FadeIn(labels), FadeIn(foot), t=0.6)
        for k in keys:
            if k == "pascal":
                pivot = kits[k].get_bottom() + RIGHT * 0.3
                self.go(Rotate(kits[k], -1.1, about_point=pivot), t=0.45)
                self.go(Rotate(kits[k], 1.1, about_point=pivot), t=0.45)
            elif k == "euler":
                self.hold(0.35)
                self.go(bow(kits[k]), t=0.6)
            else:
                self.go(bow(kits[k]), t=0.6)

    def card_ec_c05(self):
        """About Professor Euphemia: she nods from a doorway."""
        self.clear_all()
        head, names, _ = section_text("euphemia", self.flags)
        door = Rectangle(width=1.7, height=2.9, stroke_color=GOLD, stroke_width=3).move_to(xy(-4.8, -0.3))
        eu = kitten("euphemia", 0.8).move_to(door.get_bottom() + UP * 0.85)
        note = text(names[0].replace(" Not", "\nNot"), size=28, width=7.6).next_to(door, RIGHT, buff=0.7)
        self.go(FadeIn(heading(head, 2.6)), Create(door), FadeIn(eu), FadeIn(note), t=0.6)
        self.go(bow(eu, 0.3), t=0.6)

    def card_ec_c06(self):
        """Music: the credit writes along a staff that curls into a tail."""
        self.clear_all()
        head, names, _ = section_text("music", self.flags)
        staff = VGroup(*(ParametricFunction(
            lambda t, k=k: xy(t, 0.12 * k - 0.6 + 0.25 * np.sin(t * 0.8)) if t < 4.2
            else xy(4.2 + 0.6 * np.sin((t - 4.2) * 2.2), 0.12 * k - 0.6 + 0.25 * np.sin(4.2 * 0.8)
                    + 0.6 * (1 - np.cos((t - 4.2) * 2.2))),
            t_range=[-5.2, 5.6], stroke_color=BLUE, stroke_width=1.6) for k in range(5)))
        lines = block(names, size=30, buff=0.25, width=11.6).move_to(xy(0, 1.6))
        self.go(FadeIn(heading(head, 2.75)), Create(staff), t=0.8)
        self.go(Write(lines), t=1.0)

    def card_ec_c07(self):
        """Visual style and tools: the tools' names drop onto the table like cards."""
        self.clear_all()
        h1, style, _ = section_text("visual_style", self.flags)
        h2, tools, _ = section_text("made_with", self.flags)
        top = VGroup(text(h1, size=26, color=MUTED), text(style[0], size=32, slant=ITALIC)).arrange(DOWN, buff=0.25)
        top.move_to(xy(0, 2.2))
        sub = text(h2, size=26, color=MUTED).move_to(xy(0, 0.55))
        chips = VGroup()
        for t in tools:
            label = text(t, size=28)
            box = RoundedRectangle(width=label.width + 0.6, height=1.0, corner_radius=0.12,
                                   fill_color=PANEL, fill_opacity=1, stroke_color=EDGE)
            chips.add(VGroup(box, label))
        chips.arrange(RIGHT, buff=0.3)
        if chips.width > 12.6:
            chips.scale_to_fit_width(12.6)
        chips.move_to(xy(0, -0.75))
        for c in chips:
            c.save_state()
            c.shift(UP * 5)
        self.go(FadeIn(top), FadeIn(sub), t=0.5)
        self.go(LaggedStart(*(Restore(c, rate_func=rush_into) for c in chips), lag_ratio=0.25), t=1.0)

    def card_ec_c08(self):
        """Character animation (only if PAM is used)."""
        self.clear_all()
        head, names, _ = section_text("pam", self.flags)
        self.go(FadeIn(VGroup(heading(head, 1.0), block(names).move_to(xy(0, 0)))), t=0.5)

    def card_ec_c09(self):
        """Mathematical checks: a counter ticks through the hexads and stops at 132."""
        self.clear_all()
        head, names, _ = section_text("math_checks", self.flags)
        total = OBJ["count:design"]["hexads"]
        sentence = names[0]
        cut = sentence.index(" was ") + 1
        lines = block([sentence[:cut].strip(), sentence[cut:].strip()], size=30, width=12.4).move_to(xy(0, 1.65))
        dots = VGroup(*(Dot(radius=0.05, color=GREEN) for _ in range(total)))
        dots.arrange_in_grid(rows=6, buff=0.14).move_to(xy(0, -1.1))
        # A plain-text counter (Manim's Integer needs LaTeX, which this project avoids).
        count = ValueTracker(0)
        spot = xy(5.3, -1.1)
        counter = always_redraw(lambda: text(str(int(round(count.get_value()))), size=48,
                                             color=GOLD, weight=BOLD).move_to(spot))
        ada = kitten("ada", 0.5).move_to(xy(-5.9, -1.1))
        self.go(FadeIn(heading(head, 2.95)), FadeIn(lines), FadeIn(ada), t=0.5)
        self.add(counter)
        self.go(LaggedStart(*(FadeIn(d, scale=2) for d in dots), lag_ratio=0.02),
                count.animate(rate_func=linear).set_value(total), t=2.2)
        self.go(bow(ada, 0.25), Indicate(counter, color=GOLD), t=0.6)


class CreditsRoll(CreditsBase):
    flags = ()


class CreditsRollEuphemia(CreditsBase):
    flags = ("euphemia",)


# ---------------------------------------------------------------- tails

class TailBase(Timed):
    episode = 1

    def construct(self):
        last = max(EPISODES)
        name = "finale" if self.episode == last else "next_time"
        tail = ROLL["tails"][name]
        self.beat(tail["seconds"], lambda: getattr(self, name)(tail), tail["id"])

    def next_time(self, tail):
        """Next time: the next episode's subtitle picture, its lead kitten peeking in."""
        self.clear_all()
        n = self.episode + 1
        ep = EPISODES[n]
        lines = [t.format(next_number=n, next_title=ep["title"]) for t in tail["text"]]
        picture = {2: lambda: kitten_triangle(xy(0, -0.4), 0.85, h=0.5),
                   3: lambda: minimog_grid(xy(0, -0.3), h=0.72, codeword=True),
                   4: lambda: star(xy(0, -0.5), 2.2)[0]}[n]().fade(0.55)
        lead = {2: "sophie", 3: "ada", 4: "euler"}[n]
        k = kitten(lead, 0.9).move_to(xy(8.2, -2.4))
        top = text(lines[0], size=30, color=MUTED).move_to(xy(0, 3.1))
        title = text(lines[1], size=44, weight=BOLD).move_to(xy(0, 2.35))
        self.go(FadeIn(picture), FadeIn(top), FadeIn(title), t=0.6)
        self.go(k.animate.move_to(xy(6.3, -2.4)), t=0.5)
        self.go(hop(k, 0.2), t=0.4)

    def finale(self, tail):
        """The End: the series' pictures gather into one deck; the kittens sit in front."""
        self.clear_all()
        pictures = VGroup(VGroup(*(card(v, h=0.5) for v in range(12))).arrange(RIGHT, buff=0.05),
                          kitten_triangle(ORIGIN, 0.3, h=0.6), minimog_grid(ORIGIN, h=0.6).scale(0.6),
                          star(ORIGIN, 0.7)[0]).arrange(RIGHT, buff=0.7).move_to(xy(0, 0.6)).scale_to_fit_width(12)
        deck = VGroup(*(card(i, h=1.5, face=False).move_to(xy(0.035 * i, 0.55 - 0.035 * i)) for i in range(12)))
        the_end = text(tail["text"][0], size=64, weight=BOLD).move_to(xy(0, 2.6))
        pointer = text(tail["text"][1], size=24, color=MUTED).move_to(xy(0, -3.45))
        row = sitting_row(y=-1.6, scale=0.6)
        self.go(FadeIn(pictures), FadeIn(the_end), t=0.6)
        self.go(Transform(pictures, deck), t=1.2)
        self.go(*(FadeIn(row[k], shift=UP * 0.4) for k in SIT), FadeIn(pointer), t=0.6)


for _n in EPISODES:
    globals()[f"Tail{_n}"] = type(f"Tail{_n}", (TailBase,), {"episode": _n})
