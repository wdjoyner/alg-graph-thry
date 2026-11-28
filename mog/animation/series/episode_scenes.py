"""Manim scene for an episode's body: the kittens, the cards and the dialogue.

Render through make_episode.py, which also mixes the dialogue, adds the
titles and credits, and checks the length:

    python make_episode.py --episode 1 --draft

The body (scenes s01 to the last before s99) is played from three files:
epN/cues.json says what happens, epN/timing.json says on which frame, and
epN/audio_manifest.json gives each line's mouth envelope.  The kittens are
PAM figures (pam.cat.CatGraph, github.com/wdjoyner/pam); set PAM_DIR to
the folder of your PAM checkout if 'import pam' does not find it.  The
cards, totals and glyphs are the titles' own (title_scenes.py).

Every visual verb used in the cues has a method here, visual_<verb>; a cue
with no method is an error, and so is a step whose visuals run longer than
the step.  Every exchange goes through cue_tools.Table, which enforces the
rules, so the picture cannot show an illegal move the checker missed.

How the kittens act: each kitten is an Actor.  On every frame it builds
its pose from its seat's sitting pose, blended toward the pose of any
reaction under way, plus breathing; its mouth follows the loudness of its
own line's audio; it blinks now and then; and it looks at whoever is
speaking.  The cues only say which reaction starts when.
"""
import json
import math
import os
import random
import sys
from pathlib import Path

import numpy as np
from manim import *
from manim.animation.animation import prepare_animation

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


from pam_link import CatGraph, CAT_POSES, flip_pose  # noqa: E402


import title_scenes as ts                                  # noqa: E402
from title_scenes import BG, INK, MUTED, BLUE, GOLD, GREEN, PANEL, EDGE, FONT, card, text, xy  # noqa: E402
from cue_tools import (Table, steps, step_visuals, split_visual, visual_params,  # noqa: E402
                       montage_games, deal_cards, parse_move, down_moves)
from script_tools import parse                              # noqa: E402

FPS = 30
RED = "#FF6B6B"
from make_timing import MONTAGE_STUCK_SECONDS as MONTAGE_STUCK  # noqa: E402
EPISODE = int(os.environ.get("EPISODE", "1"))


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


SERIES = load("series.json")
CAST = load("cast.json")["characters"]
OBJ = load("math_objects.json")["objects"]
OUTLINE = load(f"ep{EPISODE}/outline.json")
CUES = load(f"ep{EPISODE}/cues.json")
TIMING = load(f"ep{EPISODE}/timing.json")
AUDIO = load(f"ep{EPISODE}/audio_manifest.json")["lines"]
SCRIPT = parse(HERE / f"ep{EPISODE}" / "script.fountain")

# ---------------------------------------------------------------- layout

GROUND = -3.62                       # the table's front edge, where the kittens sit
HAND_Y, PILE_Y = 1.18, 2.95
HAND_H, PILE_H = 1.15, 0.84
HAND_DX, PILE_DX = 1.3, 1.0
TOTAL_POS = xy(5.05, HAND_Y - 0.08)
CHIP_Y = (-0.2, -0.64)


def hand_slot(i):
    return xy((i - 2.5) * HAND_DX, HAND_Y)


def pile_slot(j):
    return xy((j - 2.5) * PILE_DX, PILE_Y)


def secs(frames):
    return frames / FPS


def chip(label, color=INK, fill=PANEL, size=22, pad=0.12, stroke=EDGE):
    t = text(label, size=size, color=color)
    box = RoundedRectangle(width=t.width + 2 * pad, height=t.height + 1.6 * pad, corner_radius=0.08,
                           fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=1.5)
    return VGroup(box, t.move_to(box))


def move_label(a, b):
    return f"{a} → {b}"


class Lazy(Succession):
    """A Succession that puts nothing on screen before its time.

    Manim adds the mobjects of a non-introducing animation to the scene when
    the play starts, and a Succession holding a FadeIn adds all its other
    members' mobjects; either would show a label meant to appear later.  A
    Lazy chain claims to introduce (so the scene adds nothing for it) and
    sets each member up only when that member's turn comes."""

    def __init__(self, *anims, **kw):
        super().__init__(*anims, introducer=True, **kw)

    def _setup_scene(self, scene):
        self.scene = scene


class FadeAway(FadeOut):
    """FadeOut that takes every member of a group off the screen.

    Scene.remove takes off only the mobject it is given; a group faded out
    as a whole would leave its members behind, at full opacity again."""

    def clean_up_from_scene(self, scene):
        super().clean_up_from_scene(scene)
        scene.remove(*self.mobject.get_family())


class Stage(AnimationGroup):
    """All of a step's visuals, side by side; each sets itself up (see Lazy)."""

    def __init__(self, *anims, **kw):
        super().__init__(*anims, introducer=True, lag_ratio=0, **kw)

    def _setup_scene(self, scene):
        for anim in self.animations:
            anim._setup_scene(scene)


def opacity_to(m, op, run):
    """Fade m to opacity op, from whatever it is when the animation begins.

    (.animate would capture m's whole state when the cue is built, and drag a
    card back to where it was then if it has moved since.)"""
    start = {}

    def f(mob, a):
        if "o" not in start:
            drawn = [x for x in mob.get_family() if len(x.points)]
            start["o"] = drawn[0].get_fill_opacity() if drawn else 1.0
        mob.set_opacity(start["o"] + (op - start["o"]) * a)
    return UpdateFromAlphaFunc(m, f, run_time=run)


def mini_hand(cards, h=0.5, total=True, color=INK):
    g = VGroup(*(card(v, h=h) for v in cards)).arrange(RIGHT, buff=h * 0.12)
    out = VGroup(g)
    if total:
        out.add(text(str(sum(cards)), size=int(64 * h), color=color).next_to(g, RIGHT, buff=0.25))
    return out


# ---------------------------------------------------------------- actors

def lerp_pose(a, b, w):
    return {k: a[k] + w * (b[k] - a[k]) for k in a}


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


REACT_POSE = {
    "proud": "cat_proud", "confident": "cat_proud", "smug": "cat_proud",
    "puzzled": None, "surprised": "cat_proud", "thinking": None,
    "searching": "cat_lean_in", "lean_in": "cat_lean_in", "nod": None,
    "deals": "cat_paw_tap", "paw_up": "cat_paw_up", "paw_tap": "cat_paw_tap",
    "paw_on_card": "cat_paw_tap", "bows": "cat_bow", "flustered": None,
    "deflates": "cat_slump", "sulk": "cat_slump", "shifty": None,
    "grabs_chalk": "cat_paw_up", "looks_up": None, "point": "cat_paw_up",
}


class Actor:
    """One kitten: a PAM CatGraph driven frame by frame."""

    def __init__(self, key, seat, size, seed):
        pal = CAST[key]["design"]["palette"]
        style = {"coat": pal["primary"], "outline_color": INK}
        if key == "pascal":
            style.update(markings="tabby", marking_color=pal["stripes"])
        elif key == "sophie":
            style.update(markings="tuxedo", marking_color=pal["bib"], eye_color=GOLD,
                         outline_opacity=0.75)
        else:
            style.update(accent=pal.get("accent"))
        self.key = key
        self.x = seat["x"]
        self.facing = seat["facing"]
        self.fig = CatGraph(offset=[self.x, GROUND + 0.65, 0], facing=self.facing, size=size, style=style)
        self.fig.decor.clear_updaters()
        self.base = self.fig.facing_pose("cat_sitting")
        self.acts = []                      # (start, end, reaction)
        self.talk = []                      # (start, envelope)
        self.rng = random.Random(seed)
        self.blinks = set()
        f = self.rng.randint(20, 90)
        while f < TIMING["body_frames"] + 10:
            for k in range(4):
                self.blinks.add(f + k)
            f += self.rng.randint(80, 170)
        self.phase = self.rng.random() * 6.28
        self.chalk = None
        self.name = text(CAST[key]["name"], size=18, color=MUTED).move_to(xy(self.x, GROUND - 0.22))
        self.group = VGroup(self.fig.group)

    def pose_named(self, name):
        return self.fig.facing_pose(name)

    def at(self, frame, speaker_x):
        """Set the kitten's pose and face for this frame."""
        fig, s = self.fig, self.fig.sign
        pose = dict(self.base)
        look_x, look_y, blink, dy = 0.0, 0.0, 0.0, 0.0
        shake = 0.0
        chalk_on = False
        for start, end, kind in self.acts:
            if not (start <= frame < end + 12):
                continue
            w = ease((frame - start) / 8) * (1 - ease((frame - end) / 12))
            t = (frame - start) / FPS
            target = REACT_POSE.get(kind)
            if target:
                pose = lerp_pose(pose, self.pose_named(target), w)
            if kind in ("puzzled", "thinking"):
                pose["head"] = pose["head"] + w * np.array([-s * 0.06, -0.03, 0])
                look_y += w * (0.8 if kind == "thinking" else 0.3)
            if kind == "searching":
                look_x += w * math.sin(t * 7.5) * 1.6
                look_y -= w * 0.6
            if kind == "shifty":
                look_x += w * (-s * 1.6) * (1 if (t % 1.6) < 0.9 else 0.2)
            if kind == "flustered":
                shake += w * math.sin(t * 28) * 0.035
            if kind == "nod":
                pose["head"] = pose["head"] + w * np.array([s * 0.02, -0.06 * abs(math.sin(t * 6)), 0])
            if kind == "surprised":
                dy += w * 0.08 * max(0, math.sin(min(t, 0.5) * math.pi * 2))
                blink -= 0.3 * w
            if kind == "smug":
                blink += 0.45 * w
            if kind in ("deflates", "sulk"):
                look_y -= 0.7 * w
                if kind == "sulk":
                    look_x -= s * 1.2 * w
            if kind == "looks_up":
                look_y += 0.6 * w
            if kind == "grabs_chalk" and frame >= start + 6:
                chalk_on = True
        # breathing
        b = 0.010 * math.sin(frame / FPS * 2 * math.pi / 3.4 + self.phase)
        for j in ("head", "neck", "spine_front"):
            pose[j] = pose[j] + np.array([shake, b + dy, 0])
        # talking
        mouth = 0.0
        for start, env in self.talk:
            k = frame - start
            if 0 <= k < len(env):
                mouth = env[k] / 100.0
                pose["head"] = pose["head"] + np.array([0, 0.012 * mouth, 0])
        # gaze: toward the speaker, else toward the table
        if speaker_x is not None and abs(speaker_x - self.x) > 0.1:
            look_x += 0.8 * np.sign(speaker_x - self.x)
        if frame in self.blinks:
            blink = 1.0
        fig.mouth_open = mouth
        fig.blink = min(1.0, max(-0.3, blink))
        fig.look = (float(np.clip(look_x, -1.8, 1.8)), float(np.clip(look_y, -1, 1)))
        fig.set_pose(pose)
        if self.chalk is not None:
            self.chalk.set_opacity(1 if chalk_on else 0)
            self.chalk.move_to(fig.dots["fl_paw"].get_center() + UP * 0.12)
        return mouth > 0.05


# ---------------------------------------------------------------- the scene

class EpisodeScene(Scene):
    def setup(self):
        self.camera.background_color = BG
        self.frames = 0
        self.local_t = 0.0
        self.play_start = 0
        self.table = Table()
        self.cards = {v: card(v, h=HAND_H) for v in range(12)}
        self.on_table = set()
        self.total_label = text("total", size=20, color=MUTED).move_to(TOTAL_POS + UP * 0.62)
        self.total_text = None
        self.total_pos = TOTAL_POS
        self.label_shown = False
        self.row_labels = VGroup(text("pile", size=20, color=MUTED).move_to(xy(-3.55, PILE_Y)),
                                 text("hand", size=20, color=MUTED).move_to(xy(-4.55, HAND_Y)))
        self.overlays = VGroup()
        self.tally = None
        self.table_faded = False
        self.games_played = 0
        seats = CUES["stage"]["seats"]
        size = CUES["stage"]["kitten_size"]
        self.actors = {k: Actor(k, seats[k], size, seed=i + 7) for i, k in enumerate(seats)}
        # who speaks on each frame, from the timing
        self.speaking = {}
        for lid, ln in TIMING["lines"].items():
            a = self.actors[ln["speaker"]]
            a.talk.append((ln["start"], AUDIO[lid]["mouth"]))
            for f in range(ln["start"], ln["start"] + ln["audio_frames"]):
                self.speaking[f] = ln["speaker"]
        # the frame clock: everything that moves by itself reads frame_now()
        self.clock = Mobject()
        self.clock.add_updater(self._tick)
        self.add(self.clock)

    # -- clock and frame-exact playing

    def _tick(self, m, dt):
        self.local_t += dt
        f = self.play_start + int(round(self.local_t * FPS))
        who = self.speaking.get(f)
        sx = self.actors[who].x if who else None
        for k, a in self.actors.items():
            a.at(f, sx if who != k else None)
            a.name.set_color(INK if who == k else MUTED)

    def go(self, *anims, frames):
        """Play anims (each with its own run time) inside exactly `frames` frames."""
        if frames <= 0:
            return
        # Each visual runs inside its own Lazy chain.  An AnimationGroup
        # finishes every member when it ends, which would re-apply an early
        # move of a card on top of a later one; a Succession finishes only
        # what is still running, and a Lazy one also shows nothing early.
        anims = [Lazy(prepare_animation(a)) for a in anims]
        self.play_start, self.local_t = self.frames, 0.0
        total = (frames - 0.5) / FPS
        pad = Wait(run_time=total)
        if anims:
            longest = max(a.get_run_time() for a in anims)
            if longest > total + 1e-6:
                raise ValueError(f"frame {self.frames}: visuals need {longest:.2f}s, the step has {total:.2f}s")
            self.play(Stage(*anims, pad), run_time=total, rate_func=linear)
        else:
            self.wait(total, frozen_frame=False)
        self.frames += frames

    # -- table helpers

    def total_anims(self, run=0.3):
        """Show the table's total.  One Text mobject is reshaped in place, so
        several changes queued in one step follow each other cleanly."""
        t = self.table.total
        color = RED if t < 21 else INK
        new = text(str(t), size=64, color=color, weight=BOLD).move_to(self.total_pos)
        if self.total_text is None:
            self.total_text = new
            out = [FadeIn(new, run_time=run)]
            if not self.label_shown:
                self.label_shown = True
                out.append(FadeIn(self.total_label, run_time=run))
            return out
        return [Transform(self.total_text, new, run_time=run)]

    def show_rows(self, run=0.4):
        """The 'pile' and 'hand' labels stay in the scene; only their opacity changes."""
        if self.row_labels not in self.mobjects:
            self.add(self.row_labels.set_opacity(0))
        return [opacity_to(self.row_labels, 1, run)]

    def clear_overlays(self, run=0.4):
        if len(self.overlays) == 0:
            return []
        gone = self.overlays
        self.overlays = VGroup()
        return [FadeAway(gone, run_time=run)]

    def fade_table(self, opacity, run=0.4):
        anims = [opacity_to(self.cards[v], opacity, run) for v in self.on_table]
        for m in (self.total_text, self.total_label, self.row_labels):
            if m is not None and m in self.mobjects:
                anims.append(opacity_to(m, opacity, run))
        return anims

    def gather(self, run=0.5):
        """All cards on the table slide into a deck at the center."""
        anims = []
        for i, v in enumerate(sorted(self.on_table)):
            anims.append(self.place_anim(v, xy(0.015 * i, 1.6 - 0.015 * i), 0.9, run))
        if self.total_text is not None:
            anims.append(FadeAway(self.total_text, run_time=run))
            self.total_text = None
        return anims

    def deal_to_table(self, cards, start=0.0, run=1.6):
        self.table.deal(cards)
        anims = []
        order = [("h", i, v) for i, v in enumerate(self.table.hand)] + [("p", j, v) for j, v in enumerate(self.table.pile)]
        for k, (row, i, v) in enumerate(order):
            if v not in self.on_table:
                self.cards[v].become(card(v, h=HAND_H * 0.9).move_to(xy(0, 1.6)))
                self.add(self.cards[v])
                self.on_table.add(v)
            pos, sc = (hand_slot(i), 1.0) if row == "h" else (pile_slot(i), PILE_H / HAND_H)
            d = start + run * 0.6 * k / 11
            anims.append(Succession(Wait(run_time=d + 1e-3), self.place_anim(v, pos, sc, run * 0.4, arc=0.6)))
        return anims

    def place_anim(self, v, pos, scale, run, arc=0.0):
        """Card v travels to pos at `scale` times the hand's card size, upright and opaque.

        The target is built afresh, not from the card's current state, so moves
        queued for later in the same step (which begin only when reached) land
        exactly where they should."""
        target = card(v, h=HAND_H * scale).move_to(pos)
        return Transform(self.cards[v], target, path_arc=arc, run_time=run)

    def exchange_anims(self, a, b, check=True, start=0.0, run=0.9):
        i, j = self.table.exchange(a, b, check=check)
        anims = [Succession(Wait(run_time=start + 1e-3), self.place_anim(a, pile_slot(j), PILE_H / HAND_H, run, arc=-0.9)),
                 Succession(Wait(run_time=start + 1e-3), self.place_anim(b, hand_slot(i), 1.0, run, arc=-0.9))]
        anims += [Succession(Wait(run_time=start + run * 0.85), x) for x in self.total_anims()]
        return anims

    def pulse(self, m, run=0.6, k=1.12, color=None):
        return Indicate(m, scale_factor=k, color=color or GOLD, run_time=run)

    # -- the episode

    def construct(self):
        body = [s for s in OUTLINE["scenes"] if s.get("kind") not in ("title_card", "end_credits")]
        trans = TIMING["transition_frames"]
        for si, scene in enumerate(body):
            sc = TIMING["scenes"][scene["id"]]
            assert self.frames == sc["start"], (scene["id"], self.frames, sc["start"])
            self.transition(first=(si == 0))
            for beat in scene["beats"]:
                bt = TIMING["beats"][beat["id"]]
                assert self.frames == bt["start"], (beat["id"], self.frames, bt["start"])
                for s, row in zip(steps(CUES, beat["id"]), bt["steps"]):
                    self.beat_id = beat["id"]
                    self.run_step(s, row)
                if beat["id"] == os.environ.get("STOP_AFTER"):
                    return                   # a partial render, for a quick look
            if scene["id"] == os.environ.get("STOP_AFTER"):
                return                       # a partial render, for a quick look
            if si == len(body) - 1:
                # fade to the background color under a curtain, so the kittens'
                # layered parts never show through each other as they fade
                curtain = Rectangle(width=config.frame_width + 1, height=config.frame_height + 1,
                                    fill_color=BG, fill_opacity=0, stroke_width=0)
                curtain.z_index = 100
                self.add(curtain)
                self.go(opacity_to(curtain, 1, secs(trans) * 0.8), frames=trans)
        assert self.frames == TIMING["body_frames"], (self.frames, TIMING["body_frames"])

    def transition(self, first):
        n = TIMING["transition_frames"]
        if first:
            for a in self.actors.values():
                a.at(0, None)
            anims = []
            for a in self.actors.values():
                anims.append(FadeIn(a.fig.group, run_time=secs(n) * 0.8))
                anims.append(FadeIn(a.name, run_time=secs(n) * 0.8))
            self.go(*anims, frames=n)
            return
        anims = self.clear_overlays(run=secs(n) * 0.5)
        if self.table_faded:
            anims += self.fade_table(1.0, run=secs(n) * 0.5)
            self.table_faded = False
        if self.tally is not None:
            anims.append(FadeAway(self.tally, run_time=secs(n) * 0.5))
            self.tally = None
        self.go(*anims, frames=n)

    def run_step(self, s, row):
        n, start = row["frames"], row["start"]
        assert self.frames == start
        end = start + n
        anims = []
        avail = secs(n)
        if s.get("pause") == "predict":
            anims += self.pause_card(s["prompt"], avail)
        for v in step_visuals(s):
            verb, arg = split_visual(v)
            fn = getattr(self, "visual_" + verb, None)
            if fn is None:
                raise NotImplementedError(f"no choreography for visual verb {verb}")
            anims += fn(arg, visual_params(v), start, end, avail) or []
        self.go(*anims, frames=n)

    # ---------------------------------------------------------------- visuals

    def visual_react(self, arg, p, start, end, avail):
        who, _, kind = arg.partition("_")
        a = self.actors[who]
        a.acts.append((start, end - 6, kind))
        if kind == "grabs_chalk" and a.chalk is None:
            a.chalk = RoundedRectangle(width=0.08, height=0.32, corner_radius=0.03, fill_color="#F4F1EA",
                                       fill_opacity=1, stroke_width=0).set_opacity(0)
            a.chalk.z_index = 8
            self.add(a.chalk)
        return []

    def visual_point_at(self, arg, p, start, end, avail):
        who, _, target = arg.partition("_")
        self.actors[who].acts.append((start, min(end, start + 50) - 6, "point"))
        m = {"hand": VGroup(*(self.cards[v] for v in self.table.hand)),
             "pile": VGroup(*(self.cards[v] for v in self.table.pile)),
             "total": self.total_text,
             "cards": VGroup(*(self.cards[v] for v in self.on_table))}.get(target)
        if m is None or (isinstance(m, VGroup) and len(m) == 0):
            return []
        return [Succession(Wait(run_time=0.25), self.pulse(m, run=min(0.8, avail - 0.3)))]

    def visual_total_counter(self, arg, p, start, end, avail):
        if self.total_text is None and self.table.hand:
            return self.total_anims(run=0.4)
        return []

    def visual_card_deal(self, arg, p, start, end, avail):
        anims = self.clear_overlays(run=0.3)
        if arg == "fan_12":
            for v in range(12):
                c = self.cards[v]
                c.move_to(xy(0, 1.5)).set_opacity(1)
                self.add(c)
                self.on_table.add(v)
            anims = []
            for v in range(12):
                ang = (v - 5.5) * 0.1
                pos = xy(10 * math.sin(ang), 1.75 + 10 * (math.cos(ang) - 1) + 0.25)
                target = card(v, h=HAND_H * 0.85).move_to(pos).rotate(-ang)
                anims.append(Succession(Wait(run_time=0.15 + 0.07 * v), Transform(self.cards[v], target, run_time=0.6)))
            return anims
        cards = deal_cards(arg, OBJ)
        gather = self.gather(run=0.5)
        if self.tally is not None:
            gather.append(FadeAway(self.tally, run_time=0.4))
            self.tally = None
        anims += [AnimationGroup(*gather)] if gather else []
        deal = self.deal_to_table(cards, start=0.65, run=min(2.0, avail - 1.2))
        anims += deal + self.show_rows(run=0.4)
        anims += [Succession(Wait(run_time=min(2.4, avail - 0.5)), x) for x in self.total_anims(run=0.4)]
        return anims

    def visual_card_exchange(self, arg, p, start, end, avail):
        if arg == "demo":
            a, b = p["move"]
            first = self.exchange_anims(a, b, run=0.9)
            back = self.exchange_anims(b, a, check=False, start=2.2, run=0.9)
            return first + back
        if arg.endswith("_rejected"):
            if p.get("phase", "try") == "try":
                a, b = parse_move(arg)
                anims = self.exchange_anims(a, b, check=False, run=0.8)
                self.pending = (b, a)
                return anims
            a, b = self.pending
            return self.exchange_anims(a, b, check=False, run=0.8)
        a, b = parse_move(arg)
        anims = self.exchange_anims(a, b, start=0.2, run=0.9)
        if "total" in p:
            assert self.table.total == p["total"], (arg, self.table.total)
        return anims

    def visual_flip_hand(self, arg, p, start, end, avail):
        self.table.flip()
        anims = []
        for i, v in enumerate(self.table.hand):
            anims.append(self.place_anim(v, hand_slot(i), 1.0, 1.2, arc=0.5))
        for j, v in enumerate(self.table.pile):
            anims.append(self.place_anim(v, pile_slot(j), PILE_H / HAND_H, 1.2, arc=0.5))
        anims += [Succession(Wait(run_time=1.1), x) for x in self.total_anims(run=0.4)]
        return anims

    def visual_highlight(self, arg, p, start, end, avail):
        if arg == "hand":
            box = SurroundingRectangle(VGroup(*(self.cards[v] for v in self.table.hand)), color=GOLD,
                                       buff=0.15, corner_radius=0.12, stroke_width=3)
            self.overlays.add(box)
            return [Create(box, run_time=0.6)]
        if arg == "legal_moves":
            moves = down_moves(self.table.hand)
            chips = VGroup(*(chip(f"{move_label(a, b)}  {self.table.total - a + b}", size=21)
                             for a, b in moves))
            per_row = 7
            rows = [chips[i:i + per_row] for i in range(0, len(chips), per_row)]
            for r, grp in enumerate(rows):
                VGroup(*grp).arrange(RIGHT, buff=0.16).move_to(xy(0, CHIP_Y[r]))
            head = text(f"{len(moves)} legal moves: card out \u2192 card in, new total", size=20,
                        color=GOLD).move_to(xy(0, CHIP_Y[0] + 0.42))
            both = VGroup(chips, head)
            return [LaggedStart(*(FadeIn(c, shift=UP * 0.1) for c in chips), lag_ratio=0.08,
                                run_time=min(2.2, avail - 0.5)), FadeIn(head, run_time=0.5),
                    Succession(Wait(run_time=avail - 0.45), FadeAway(both, run_time=0.35))]
        if arg == "dead_end":
            hand, pile = self.table.hand, self.table.pile
            tries = [(a, b) for a in sorted(hand) for b in pile if b < a]
            assert not down_moves(hand)
            chips = VGroup(*(chip(f"{move_label(a, b)}  {self.table.total - a + b}", color=RED, size=18)
                             for a, b in tries)).arrange(RIGHT, buff=0.14).move_to(xy(0, CHIP_Y[0]))
            label = text("every smaller card: under 21", size=20, color=RED).move_to(xy(0, CHIP_Y[1] - 0.05))
            self.overlays.add(chips, label)
            per = (avail - 2.4) / max(1, len(tries))
            anims = [Succession(Wait(run_time=0.3 + per * k), FadeIn(c, shift=UP * 0.1, run_time=0.3))
                     for k, c in enumerate(chips)]
            anims.append(Succession(Wait(run_time=0.4 + per * len(tries)), FadeIn(label, run_time=0.4)))
            anims += [Succession(Wait(run_time=avail - 1.4), opacity_to(self.cards[v], 0.45, 0.6)) for v in hand]
            return anims
        if arg == "question_mark_45":
            q = self.qmark
            return [Succession(Wait(run_time=0.2), Indicate(q, scale_factor=1.5, color=GOLD, run_time=1.0))]
        raise NotImplementedError(f"highlight:{arg}")

    def visual_recap_montage(self, arg, p, start, end, avail):
        if arg == "more_losses":
            return self.montage(p, avail)
        if arg == "move_7_5":
            hand = OBJ["hand:example"]["cards"]
            before = mini_hand(hand, h=0.46)
            after_cards = [5 if v == 7 else v for v in hand]
            after = mini_hand(after_cards, h=0.46)
            title = text("Pascal's first move", size=22, color=MUTED)
            panel = VGroup(title, before).arrange(DOWN, buff=0.15).move_to(xy(0, 3.25))
            after.move_to(before)
            frame = SurroundingRectangle(panel, color=EDGE, buff=0.15, corner_radius=0.1,
                                         fill_color=BG, fill_opacity=0.95, stroke_width=2)
            self.overlays.add(frame, title, before)
            seven = before[0][hand.index(7)]
            gl = after[0][hand.index(7)].copy()
            return [FadeIn(VGroup(frame, title, before), run_time=0.5),
                    Succession(Wait(run_time=1.0), Indicate(seven, color=GOLD, run_time=0.6),
                               Transform(before, after, run_time=0.6))]
        raise NotImplementedError(f"recap_montage:{arg}")

    def montage(self, p, avail):
        g = p["game"]
        tries = OBJ["tries:complement_1to6"]
        x = tries["tries"][g]
        reply = x["replies"][(0, 3)[g]]["move"]
        start_hand = OBJ["hand:complement_1to6"]["cards"]
        seq = montage_games(start_hand, [(tuple(x["move"]), tuple(reply))])[0]
        spm = p.get("seconds_per_move", 1.0)
        anims, t = [], 0.0
        if self.tally is None:
            self.tally = VGroup(text("Ada", size=22, color=MUTED), VGroup()).arrange(RIGHT, buff=0.3)
            self.tally.move_to(xy(-5.6, 3.55))
            anims.append(FadeIn(self.tally[0], run_time=0.4))
            self.add(self.tally)
        for who, m, total in seq:
            if m is None:
                stuck = text("Pascal is stuck", size=30, color=RED).move_to(xy(0, CHIP_Y[0] - 0.2))
                mark = Line(UP * 0.22, DOWN * 0.22, stroke_color=GOLD, stroke_width=5)
                tally_marks = self.tally[1]
                mark.next_to(self.tally[0], RIGHT, buff=0.3 + 0.2 * len(tally_marks))
                tally_marks.add(mark)
                # Two chains, not one: a Succession holding a FadeIn puts all its
                # other members' mobjects on screen at once, the FadeOut's too.
                anims.append(Succession(Wait(run_time=t), FadeIn(stuck, run_time=0.3)))
                anims.append(Succession(Wait(run_time=t + MONTAGE_STUCK - 0.3), FadeAway(stuck, run_time=0.3)))
                anims += [Succession(Wait(run_time=t), opacity_to(self.cards[v], 0.45, 0.4)) for v in self.table.hand]
                anims.append(Succession(Wait(run_time=t + 0.9), Create(mark, run_time=0.4)))
                self.actors["pascal"].acts.append((self.frames + int(t * FPS), self.frames + int((t + 1.5) * FPS), "flustered"))
                t += MONTAGE_STUCK
                break
            self.actors[who].acts.append((self.frames + int(t * FPS), self.frames + int((t + 0.7) * FPS), "paw_tap"))
            anims += self.exchange_anims(*m, start=t, run=spm * 0.65)
            t += spm
        # reset to the 45-hand
        if p.get("reset", True):
            start = list(start_hand)
            moves = []
            for i, v in enumerate(start):
                moves.append(self.place_anim(v, hand_slot(i), 1.0, 0.6))
            pile = sorted(set(range(12)) - set(start))
            for j, v in enumerate(pile):
                moves.append(self.place_anim(v, pile_slot(j), PILE_H / HAND_H, 0.6))
            self.table.deal(start)
            anims += [Succession(Wait(run_time=t), a) for a in moves + self.total_anims(run=0.4)]
            t += 0.8
        self.games_played += 1
        return anims

    def visual_line_up(self, arg, p, start, end, avail):
        if arg == "1to6_and_complement":
            hands = [OBJ["hand:1to6"]["cards"], OBJ["hand:complement_1to6"]["cards"]]
            groups = VGroup(*(mini_hand(h, h=0.72) for h in hands)).arrange(RIGHT, buff=1.2).move_to(xy(0, 1.9))
            tags = VGroup(*(text("loses", size=22, color=RED).next_to(g, DOWN, buff=0.22) for g in groups))
            self.overlays.add(groups, tags)
            self.table_faded = True
            return self.fade_table(0.05) + [Succession(Wait(run_time=0.3), FadeIn(groups, shift=DOWN * 0.2, run_time=0.8)),
                                             Succession(Wait(run_time=1.2), FadeIn(tags, run_time=0.5))]
        if arg == "losing_hands":
            keys = ["hand:1to6", "hand:game_after_3", "hand:hexad_24", "hand:complement_1to6"]
            hands = [sorted(OBJ[k]["cards"]) for k in keys]
            groups = VGroup(*(mini_hand(h, h=0.42) for h in hands)).arrange(RIGHT, buff=0.55).move_to(xy(0, 1.35))
            if groups.width > 13.4:
                groups.scale_to_fit_width(13.4)
            tags = VGroup()
            for g, k in zip(groups, keys):
                tag = text("?" if k == "hand:complement_1to6" else "loses", size=26 if k == "hand:complement_1to6" else 20,
                           color=GOLD if k == "hand:complement_1to6" else RED, weight=BOLD if k == "hand:complement_1to6" else NORMAL)
                tag.next_to(g, DOWN, buff=0.22)
                tags.add(tag)
            self.qmark = tags[-1]
            self.overlays.add(groups, tags)
            anims = self.gather(run=0.5) + [opacity_to(self.total_label, 0, 0.4)]
            for v in list(self.on_table):
                anims.append(FadeAway(self.cards[v], run_time=0.5))
            self.on_table = set()
            anims.append(opacity_to(self.row_labels, 0, 0.4))
            return anims + [Succession(Wait(run_time=0.4), LaggedStart(*(FadeIn(g, shift=DOWN * 0.2) for g in groups),
                                                                      lag_ratio=0.3, run_time=1.6)),
                            Succession(Wait(run_time=2.0), FadeIn(tags, run_time=0.5))]
        raise NotImplementedError(f"line_up:{arg}")

    def visual_branch_tree(self, arg, p, start, end, avail):
        tree = OBJ["tree:hexad_24"]
        if arg == "hexad_24":
            # the hand moves up into the pile's row; the pile steps aside
            anims = []
            for j, v in enumerate(self.table.pile):
                anims.append(opacity_to(self.cards[v], 0.0, 0.5))
            for i, v in enumerate(self.table.hand):
                anims.append(self.place_anim(v, xy((i - 2.5) * 0.85, PILE_Y + 0.1), 0.66, 0.8))
            anims.append(opacity_to(self.row_labels, 0, 0.4))
            root = xy(0, PILE_Y - 0.35)
            self.branch_nodes = []
            nodes, edges = VGroup(), VGroup()
            for k, br in enumerate(tree["branches"]):
                a, b = br["move"]
                node = chip(f"{move_label(a, b)}  {br['total']}", size=22).move_to(xy((k - 2) * 2.55, HAND_Y + 0.05))
                edge = Line(root, node.get_top(), stroke_color=EDGE, stroke_width=2.5)
                nodes.add(node)
                edges.add(edge)
                self.branch_nodes.append(node)
            self.overlays.add(edges, nodes)
            self.total_pos = xy(4.0, PILE_Y + 0.1)
            new_total = self.total_text.copy().move_to(self.total_pos)
            anims += [Transform(self.total_text, new_total, run_time=0.8),
                      self.total_label.animate(run_time=0.8).move_to(xy(4.0, PILE_Y + 0.6))]
            anims.append(Succession(Wait(run_time=0.8), LaggedStart(
                *(AnimationGroup(Create(e), FadeIn(n, shift=DOWN * 0.15)) for e, n in zip(edges, nodes)),
                lag_ratio=0.25, run_time=min(1.8, avail - 0.9))))
            return anims
        if arg == "hexad_24_replies":
            k = p["branch"]
            br = tree["branches"][k]
            rep = br["replies"][0]
            a, b = rep["move"]
            node = self.branch_nodes[k]
            r = chip(f"{move_label(a, b)}  {rep['total']}", color=BG, fill=GREEN, stroke=GREEN, size=22)
            r.next_to(node, DOWN, buff=0.55)
            edge = Line(node.get_bottom(), r.get_top(), stroke_color=GREEN, stroke_width=2.5)
            stuck = text("stuck", size=18, color=RED).next_to(r, DOWN, buff=0.12)
            self.overlays.add(edge, r, stuck)
            hi = Indicate(node, color=GOLD, run_time=0.6)
            return [hi, Succession(Wait(run_time=0.5), Create(edge, run_time=0.4)),
                    Succession(Wait(run_time=0.8), FadeIn(r, shift=DOWN * 0.1, run_time=0.4)),
                    Succession(Wait(run_time=min(1.6, avail - 0.5)), FadeIn(stuck, run_time=0.3))]
        raise NotImplementedError(f"branch_tree:{arg}")

    def pause_card(self, prompt, avail):
        msg = text(prompt, size=30, color=GOLD, slant=ITALIC)
        ring = Circle(radius=0.2, stroke_color=GOLD, stroke_width=4)
        g = VGroup(ring, msg).arrange(RIGHT, buff=0.3).move_to(xy(0, 3.62))
        sweep = Arc(radius=0.2, start_angle=PI / 2, angle=TAU, stroke_color=BG, stroke_width=5).move_arc_center_to(ring.get_center())
        return [FadeIn(g, run_time=0.4),
                Succession(Wait(run_time=0.4), Create(sweep, run_time=max(0.5, avail - 1.0), rate_func=linear)),
                Succession(Wait(run_time=avail - 0.45), FadeAway(VGroup(g, sweep), run_time=0.35))]


class Episode1(EpisodeScene):
    pass
