"""Manim scenes for the episode bodies: the kittens, the cards or diagrams, and the dialogue.

Render through make_episode.py, which also mixes the dialogue, adds the
titles and credits, and checks the length:

    python make_episode.py --episode 1 --draft
    python make_episode.py --episode 2 --draft

Every episode is an EpisodeScene (the kittens, the frame clock, steps,
transitions, reactions, pauses) plus a mixin with the episode's props and
visual verbs: Episode1 = TableVisuals (the card table), Episode2 =
BoardVisuals (Sophie's chalk diagrams, drawn from cue_tools.Board),
Episode3 = CodeVisuals (Ada's MINIMOG and tetracode, drawn from
cue_tools.Code).  BoardVisuals and CodeVisuals share CardLights (lighting
cards and putting them back).

The body (scenes s01 to the last before s99) is played from three files:
epN/cues.json says what happens, epN/timing.json says on which frame, and
epN/audio_manifest.json gives each line's mouth envelope.  The kittens are
PAM figures (pam.cat.CatGraph, github.com/wdjoyner/pam); set PAM_DIR to
the folder of your PAM checkout if 'import pam' does not find it.  The
cards, totals and glyphs are the titles' own (title_scenes.py).

Every visual verb used in the cues has a method here, visual_<verb>; a cue
with no method is an error, and so is a step whose visuals run longer than
the step.  Every exchange goes through cue_tools.Table, which enforces the
rules, so the picture cannot show an illegal move the checker missed; every
diagram goes through cue_tools.Board, which recomputes it from the
mathematics.

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
from cue_tools import (Table, Board, Code, steps, step_visuals, split_visual, visual_params,  # noqa: E402
                       montage_games, deal_cards, parse_move, down_moves)
from script_tools import parse                              # noqa: E402

FPS = 30
RED = "#FF6B6B"
from make_timing import MONTAGE_STUCK_SECONDS as MONTAGE_STUCK, body_scenes  # noqa: E402
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
    # Episode 2
    "draws": "cat_paw_up", "pleased": "cat_proud", "skeptical": None, "deadpan": None,
    "objects": "cat_paw_up",
    # Episode 3
    "delighted": "cat_proud", "ponders": None, "counts": None, "straightens": "cat_paw_tap",
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
        self.chalk_hold = None              # frame -> opacity, for a kitten that keeps her chalk
        self.breath = 0.010                 # breathing amplitude
        self.speak_gaze = None              # (look_x, look_y) while this kitten talks, or None
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
            if kind == "draws":
                # small chalk strokes: the raised paw circles
                for j, r in (("fl_paw", 0.07), ("fl_knee", 0.03)):
                    pose[j] = pose[j] + w * r * np.array([s * math.cos(t * 9.0), math.sin(t * 9.0), 0])
            if kind == "pleased":
                blink += 0.45 * w
                pose["head"] = pose["head"] + w * np.array([0, -0.04 * abs(math.sin(t * 4)), 0])
            if kind == "skeptical":
                pose["head"] = pose["head"] + w * np.array([-s * 0.05, 0.025, 0])
                blink += 0.35 * w
                look_x -= s * 0.7 * w
            if kind == "deadpan":
                blink += 0.5 * w
            if kind == "objects":
                shake += w * math.sin(t * 9) * 0.03
            if kind == "counts":
                # one small, crisp nod for each item: down fast, held, back up
                ph = (t % 0.55) / 0.55
                dip = 1.0 if ph < 0.35 else max(0.0, 1 - (ph - 0.35) / 0.2)
                pose["head"] = pose["head"] + w * np.array([s * 0.012, -0.045 * dip * (ph > 0.05), 0])
            if kind == "delighted":
                dy += w * 0.07 * abs(math.sin(min(t, 1.2) * 7.5))
                blink += 0.45 * w
                pose["fl_paw"] = pose["fl_paw"] + w * np.array([s * 0.05, 0.12, 0])
            if kind == "ponders":
                pose["head"] = pose["head"] + w * np.array([-s * 0.05, 0.03, 0]) * min(1.0, t / 1.5)
                look_y += 0.7 * w
                look_x -= s * 0.5 * w
        # breathing
        b = self.breath * math.sin(frame / FPS * 2 * math.pi / 3.4 + self.phase)
        for j in ("head", "neck", "spine_front"):
            pose[j] = pose[j] + np.array([shake, b + dy, 0])
        # talking
        mouth = 0.0
        talking = False
        for start, env in self.talk:
            k = frame - start
            if 0 <= k < len(env):
                mouth = env[k] / 100.0
                talking = True
                pose["head"] = pose["head"] + np.array([0, 0.012 * mouth, 0])
        if talking and self.speak_gaze is not None:
            # a precise speaker looks at what she is talking about
            look_x += self.speak_gaze[0]
            look_y += self.speak_gaze[1]
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
            op = 1 if chalk_on else 0
            if self.chalk_hold is not None:
                op = max(op, self.chalk_hold(frame))
            self.chalk.set_opacity(op)
            self.chalk.move_to(fig.dots["fl_paw"].get_center() + UP * 0.12)
        return mouth > 0.05


# ---------------------------------------------------------------- the scene

class EpisodeScene(Scene):
    """What every episode body shares: the kittens, the frame clock, frame-exact
    steps, scene transitions, reactions, pointing and the viewer's pauses.

    An episode's own props and visual verbs come from a mixin listed before
    this class: TableVisuals (Episode 1's cards) or BoardVisuals (Episode 2's
    diagrams).  The hooks setup_stage, setup_actors, transition_anims and
    point_target let the mixin take part without changing what is shared."""

    def setup(self):
        self.camera.background_color = BG
        self.frames = 0
        self.local_t = 0.0
        self.play_start = 0
        self.overlays = VGroup()
        self.setup_stage()
        seats = CUES["stage"]["seats"]
        size = CUES["stage"]["kitten_size"]
        self.actors = {k: Actor(k, seats[k], size, seed=i + 7) for i, k in enumerate(seats)}
        self.setup_actors()
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

    def setup_stage(self):
        """Make the episode's props (they go on screen through the cues)."""

    def setup_actors(self):
        """Dress the kittens for the episode, once they exist."""

    def transition_anims(self, n):
        """What the episode's props do at a change of scene, besides clearing overlays."""
        return []

    def point_target(self, target):
        """The mobject a point_at cue pulses, or None."""
        return None

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

    def clear_overlays(self, run=0.4):
        if len(self.overlays) == 0:
            return []
        gone = self.overlays
        self.overlays = VGroup()
        return [FadeAway(gone, run_time=run)]

    def pulse(self, m, run=0.6, k=1.12, color=None):
        return Indicate(m, scale_factor=k, color=color or GOLD, run_time=run)

    # -- the episode

    # -- the episode

    def construct(self):
        body = body_scenes(OUTLINE)
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
        anims += self.transition_anims(n)
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

    # ---------------------------------------------------------------- shared visuals

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
        m = self.point_target(target)
        if m is None or (isinstance(m, VGroup) and len(m) == 0):
            return []
        return [Succession(Wait(run_time=0.25), self.pulse(m, run=min(0.8, avail - 0.3)))]

    def pause_card(self, prompt, avail):
        msg = text(prompt, size=30, color=GOLD, slant=ITALIC)
        ring = Circle(radius=0.2, stroke_color=GOLD, stroke_width=4)
        g = VGroup(ring, msg).arrange(RIGHT, buff=0.3).move_to(xy(0, 3.62))
        sweep = Arc(radius=0.2, start_angle=PI / 2, angle=TAU, stroke_color=BG, stroke_width=5).move_arc_center_to(ring.get_center())
        return [FadeIn(g, run_time=0.4),
                Succession(Wait(run_time=0.4), Create(sweep, run_time=max(0.5, avail - 1.0), rate_func=linear)),
                Succession(Wait(run_time=avail - 0.45), FadeAway(VGroup(g, sweep), run_time=0.35))]


# ---------------------------------------------------------------- Episode 1: the card table

class TableVisuals:
    """Episode 1's props and visual verbs: the cards on the table, the total,
    exchanges, deals, the montage's game engine, line-ups and branch trees."""

    def setup_stage(self):
        """The cards, the total and the row labels (made here, put on screen by the cues)."""
        self.table = Table()
        self.cards = {v: card(v, h=HAND_H) for v in range(12)}
        self.on_table = set()
        self.total_label = text("total", size=20, color=MUTED).move_to(TOTAL_POS + UP * 0.62)
        self.total_text = None
        self.total_pos = TOTAL_POS
        self.label_shown = False
        self.row_labels = VGroup(text("pile", size=20, color=MUTED).move_to(xy(-3.55, PILE_Y)),
                                 text("hand", size=20, color=MUTED).move_to(xy(-4.55, HAND_Y)))
        self.tally = None
        self.table_faded = False
        self.games_played = 0

    def transition_anims(self, n):
        anims = []
        if self.table_faded:
            anims += self.fade_table(1.0, run=secs(n) * 0.5)
            self.table_faded = False
        if self.tally is not None:
            anims.append(FadeAway(self.tally, run_time=secs(n) * 0.5))
            self.tally = None
        return anims

    def point_target(self, target):
        return {"hand": VGroup(*(self.cards[v] for v in self.table.hand)),
                "pile": VGroup(*(self.cards[v] for v in self.table.pile)),
                "total": self.total_text,
                "cards": VGroup(*(self.cards[v] for v in self.on_table))}.get(target)

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

    # -- visuals

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


# ---------------------------------------------------------------- Episode 2: the board
#
# Sophie and Euler draw with chalk in the dark space above the table.  The
# board holds one diagram at a time: the Fano plane, a ring of twelve
# points, Curtis's triangular kitten, and its three 3 x 3 views.  Every
# point, line, set and count is computed by cue_tools.Board (the same code
# the checker runs) from build_math_objects.py's definitions; nothing here
# is typed in.  Diagrams stay up from scene to scene; captions, counters
# and chips are overlays, cleared at each change of scene.

CHALK = "#C9D3E6"                          # chalk strokes
FANO_C, FANO_R = xy(0, 1.05), 1.8          # the Fano figure, circumradius
BLANK_C, BLANK_R = xy(-2.3, 1.3), 1.55     # twelve blank points, before they have labels
RING_C, RING_R = xy(-0.9, 1.35), 1.9       # the projective line: 0..10 round, infinity in the middle
TRI_C = xy(0, 1.45)                        # the kitten triangle (the titles' spacing)
VIEW_X, VIEW_Y, CELL, VIEW_H = (-4.15, 0.0, 4.15), 1.7, 0.74, 0.6
CORNER_Y, CAPTION_Y, STRIP_Y = 3.3, 0.38, -0.32
PANEL_X = 4.25                             # captions and counts to the right of a diagram
# Points and cards are drawn over the chalk lines by a z_index above 0, never
# by putting lines below 0: the renderer sorts by z_index when it picks the
# mobjects that move, and anything sorted before the frame clock (z_index 0,
# added first) is painted once into the step's still background and never
# redrawn while the step plays.
FRONT = 0.3


def plabel(x, labels="projective"):
    """How a point is written: 11 is infinity in projective labels."""
    return "∞" if labels == "projective" and x == 11 else str(x)


def label_card(lab, h):
    """A card as in the titles (title_scenes.card), with any label."""
    box = RoundedRectangle(width=h * 0.72, height=h, corner_radius=h * 0.11,
                           stroke_color=EDGE, stroke_width=2, fill_color=PANEL, fill_opacity=1)
    return VGroup(box, text(lab, size=34 * h / 0.84)).set_z_index(FRONT)


def recolor(c, color, run):
    """Light a card in color (or put it back to plain with None), from whatever
    it is when the animation begins; its opacity is left alone."""
    start = {}
    fill_to, ink_to = ManimColor(color or PANEL), ManimColor(BG if color else INK)
    stroke_to = ManimColor(color or EDGE)

    def f(m, a):
        if not start:
            start.update(fill=m[0].get_fill_color(), stroke=m[0].get_stroke_color(),
                         ink=m[1].get_fill_color())
        m[0].set_fill(interpolate_color(start["fill"], fill_to, a))
        m[0].set_stroke(interpolate_color(start["stroke"], stroke_to, a))
        m[1].set_fill(interpolate_color(start["ink"], ink_to, a))
    return UpdateFromAlphaFunc(c, f, run_time=run)


def later(t, anim):
    """anim, starting t seconds into its step."""
    return Succession(Wait(run_time=t + 1e-3), anim) if t > 0 else anim


def hand_turn(hand, h0, h1, run, center=None, hours=11):
    """Turn a clock hand clockwise from hour h0 to hour h1 about its pin."""
    center = RING_C if center is None else center
    state = {}

    def f(m, alpha):
        if not state:
            state["copy"] = m.copy()
        m.become(state["copy"].copy().rotate(-(h1 - h0) * TAU / hours * alpha, about_point=center))
    return UpdateFromAlphaFunc(hand, f, run_time=run)


def mark(pos, color=GOLD, r=0.22):
    return Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color,
                  fill_opacity=0.22).move_to(pos)


def appear(m, t=0.0, run=0.4, scale=None):
    """m appears at t (an introducer, so nothing shows early)."""
    a = GrowFromCenter(m, run_time=run) if scale else FadeIn(m, run_time=run)
    return later(t, a)


def ring_pos(x, radius=RING_R):
    """Point x of the projective line: 0..10 clockwise from the top, infinity at the center."""
    if x == 11:
        return RING_C.copy()
    a = x * TAU / 11
    return RING_C + radius * np.array([np.sin(a), np.cos(a), 0])


def blank_pos(x):
    """The twelve points before they have labels: evenly round a circle."""
    a = x * TAU / 12
    return BLANK_C + BLANK_R * np.array([np.sin(a), np.cos(a), 0])


def cell_pos(i, r, c):
    """Cell (r, c) of view i (rows top to bottom); r, c may run off the grid."""
    return xy(VIEW_X[i] + (c - 1) * CELL, VIEW_Y + (1 - r) * CELL)


class CardLights:
    """Lighting cards in a color and putting them back, shared by Episode 2's
    board and Episode 3's MINIMOG.  Needs self.lit (card -> color), self.faint
    (card -> opacity) and self.base (card -> its resting color)."""

    def light(self, colors, run=0.4, keep=False):
        """Recolor cards: colors maps card -> color; every other lit card goes back to plain unless keep."""
        anims, lit = [], {}
        for c in list(self.lit) + [c for c in colors if c not in self.lit]:
            want = colors.get(c, self.lit.get(c) if keep else None)
            if self.lit.get(c) != want:
                anims.append(recolor(c, want or self.base.get(c), run))
            if want:
                lit[c] = want
        self.lit = lit
        return anims

    def undim(self, run=0.4):
        anims = [opacity_to(m, 1.0, run) for m, op in self.faint.items() if op < 1]
        self.faint = {}
        return anims


class BoardVisuals(CardLights):
    """Episode 2's props and visual verbs: the board's diagrams."""

    def setup_stage(self):
        self.board = Board(OBJ)
        self.bm = self.board.bm
        self.points = {}        # the twelve points of the ring (blank, then labeled): x -> Dot
        self.point_labels = {}  # x -> Text
        self.ring_circle = None
        self.fano = None
        self.marks = {}         # x -> mark on the ring
        self.tri = []           # (label, card) of the triangle, in OBJ order
        self.tri_outline = None
        self.cells = {}         # (view, r, c) -> card
        self.cell_label = {}    # (view, r, c) -> point (projective label)
        self.corner_cards = {}  # view -> card
        self.captions = VGroup()
        self.lit = {}           # card -> color
        self.faint = {}         # card -> opacity, for cards shown faint
        self.base = {}          # card -> its resting color (the corners are gold)
        self.panel = {}         # named overlay texts
        self.strip = []         # chips or hands along the strip
        self.summoned = VGroup()

    def setup_actors(self):
        who = CUES["stage"].get("chalk")
        if not who:
            return
        a = self.actors[who]
        a.chalk = RoundedRectangle(width=0.08, height=0.32, corner_radius=0.03, fill_color="#F4F1EA",
                                   fill_opacity=1, stroke_width=0).set_opacity(0)
        a.chalk.z_index = 8
        self.add(a.chalk)
        n = TIMING["transition_frames"]
        a.chalk_hold = lambda f: min(1.0, max(0.0, f / (0.8 * n)))   # in her paw from the first fade-in

    def transition_anims(self, n):
        run = secs(n) * 0.5
        anims = [recolor(c, self.base.get(c), run) for c, col in self.lit.items() if col]
        self.lit = {}
        anims += self.undim(run)
        self.strip, self.panel, self.marks = [], {}, {}
        return anims

    def board_group(self):
        lay = self.board.layout
        if lay == "fano":
            return self.fano["group"]
        if lay in ("ring", "ring_blank"):
            return VGroup(*self.points.values())
        if lay == "triangle":
            return VGroup(*(c for _, c in self.tri))
        if lay == "views":
            return VGroup(*self.cells.values(), *self.corner_cards.values())
        return None

    def point_target(self, target):
        return self.board_group() if target == "board" else None

    def play_board(self, verb, arg, p):
        errs = self.board.play(verb, arg, p)
        if errs:
            raise ValueError(f"{self.beat_id} {verb}:{arg}: " + "; ".join(errs))

    def overlay(self, *ms):
        self.overlays.add(*ms)
        return ms[0] if len(ms) == 1 else ms

    def caption(self, s, pos, size=24, color=INK, **kw):
        return self.overlay(text(s, size=size, color=color, **kw).move_to(pos))

    # -- shared pieces

    def clear_strip(self, run=0.3):
        gone = [m for m in self.strip if m in self.overlays]
        self.strip = []
        for m in gone:
            self.overlays.remove(m)
        return [FadeAway(VGroup(*gone), run_time=run)] if gone else []

    def set_faint(self, bright, run=0.5):
        """Every view card not in bright goes faint; the rest come back."""
        anims = []
        for j in range(3):
            for m in self.view_members(j):
                want = 1.0 if m in bright else 0.3
                if self.faint.get(m, 1.0) != want:
                    anims.append(opacity_to(m, want, run))
                    self.faint[m] = want
        return anims

    def view_members(self, i):
        return [c for (j, _, _), c in self.cells.items() if j == i] + [self.corner_cards[i]]

    def view_index(self, picture):
        return [d for d, _ in self.board.views()].index(picture)

    def cells_of(self, i, points):
        return [c for (j, r, cc), c in self.cells.items() if j == i and self.cell_point(j, r, cc) in points]

    def cell_point(self, i, r, c):
        """The point in cell (r, c) of view i, in the board's current labels."""
        return self.board.views()[i][1][3 * r + c]

    def corners_of(self, points):
        corners = [d for d, _ in self.board.views()]
        return [self.corner_cards[i] for i, d in enumerate(corners) if d in points]

    def mark_set(self, points, run=0.3, t=0.0, color=GOLD):
        """Move the ring's marks to exactly these points (old marks fade, new ones grow)."""
        anims = []
        for x in [x for x in self.marks if x not in points]:
            m = self.marks.pop(x)
            anims.append(later(t, FadeAway(m, run_time=run)))
        for x in points:
            if x not in self.marks:
                m = self.overlay(mark(ring_pos(x), color))
                self.marks[x] = m
                anims.append(appear(m, t, run, scale=True))
        return anims

    def clear_marks(self, run=0.3, t=0.0):
        return self.mark_set([], run=run, t=t)

    # -- visuals

    def visual_recap_montage(self, arg, p, start, end, avail):
        self.play_board("recap_montage", arg, p)
        keys = p["hands"]
        hands = [sorted(OBJ[k]["cards"]) for k in keys]
        groups = VGroup(*(mini_hand(h, h=0.42) for h in hands)).arrange(RIGHT, buff=0.55).move_to(xy(0, 1.35))
        if groups.width > 13.4:
            groups.scale_to_fit_width(13.4)
        tags = VGroup()
        for g, k in zip(groups, keys):
            q = k == p["question"]
            tag = text("?" if q else "lost", size=26 if q else 20, color=GOLD if q else RED,
                       weight=BOLD if q else NORMAL).next_to(g, DOWN, buff=0.22)
            tags.add(tag)
        self.overlay(groups, tags)
        self.line_up = (groups, tags)
        return [later(0.2, LaggedStart(*(FadeIn(g, shift=DOWN * 0.2) for g in groups), lag_ratio=0.3, run_time=1.6)),
                later(min(2.0, avail - 0.6), FadeIn(tags, run_time=0.5))]

    def visual_morph_layout(self, arg, p, start, end, avail):
        self.play_board("morph_layout", arg, p)
        return getattr(self, "layout_" + arg)(p, avail)

    def layout_to_fano(self, p, avail):
        f = OBJ["fano"]
        pos = {int(k): FANO_C + FANO_R * xy(*v) for k, v in f["positions"].items()}
        anims = self.clear_overlays(run=0.4)
        pts, labs, lines = {}, {}, {}
        for k, q in sorted(pos.items()):
            pts[k] = Dot(q, radius=0.1, color=INK).set_z_index(FRONT)
            out = q - FANO_C
            d = out / np.linalg.norm(out) if np.linalg.norm(out) > 1e-6 else np.array([0.55, 0.55, 0]) / 0.78
            labs[k] = text(str(k), size=24, color=MUTED).move_to(q + 0.36 * d).set_z_index(FRONT)
        for line in f["lines"]:
            if set(line) == set(f["circle"]):
                m = Circle(radius=FANO_R * f["circle_radius"], stroke_color=CHALK, stroke_width=3).move_to(FANO_C)
            else:
                a, b = max(((u, v) for u in line for v in line), key=lambda uv: np.linalg.norm(pos[uv[0]] - pos[uv[1]]))
                m = Line(pos[a], pos[b], stroke_color=CHALK, stroke_width=3)
            lines[frozenset(line)] = m
        self.fano = {"pos": pos, "pt": pts, "lab": labs, "line": lines,
                     "group": VGroup(*lines.values(), *pts.values(), *labs.values())}
        run = avail - 0.4
        anims.append(later(0.3, LaggedStart(*(AnimationGroup(GrowFromCenter(pts[k]), FadeIn(labs[k]))
                                              for k in sorted(pts)), lag_ratio=0.25, run_time=run * 0.35)))
        anims.append(later(0.3 + run * 0.38, LaggedStart(*(Create(m) for m in lines.values()), lag_ratio=0.3,
                                                         run_time=run * 0.6)))
        return anims

    def layout_to_ring(self, p, avail):
        anims = []
        for x, d in self.points.items():
            anims.append(d.animate(run_time=1.4).move_to(ring_pos(x)).set_color(INK))
        self.ring_circle = Circle(radius=RING_R, stroke_color=CHALK, stroke_width=2, stroke_opacity=0.6).move_to(RING_C)
        labels = OBJ["ring:projective"]["labels"]
        for x in range(12):
            q = ring_pos(x, RING_R + 0.38) if x != 11 else RING_C + xy(0.3, 0.3)
            self.point_labels[x] = text(labels[x], size=26 if x == 11 else 24, color=MUTED).move_to(q).set_z_index(FRONT)
        anims.append(later(0.6, Create(self.ring_circle, run_time=1.0)))
        anims.append(later(1.2, LaggedStart(*(FadeIn(self.point_labels[x]) for x in range(12)),
                                            lag_ratio=0.15, run_time=min(2.2, avail - 1.4))))
        return anims

    def layout_to_triangle(self, p, avail):
        k = OBJ["kitten:projective"]
        corners = set(k["corners"])
        anims, first, self.tri = [], {}, []
        for x, y, lab in k["spots"]:
            target = label_card(plabel(lab), 0.5).move_to(TRI_C + xy(x * 0.6, (y - 3) * 0.68))
            if lab in corners:
                target[0].set_fill(GOLD, 0.92).set_stroke(GOLD)
                target[1].set_color(BG)
            if lab not in first:
                # the ring's point (dot and label) becomes its first card
                ghost = VGroup(self.points[lab].copy(), self.point_labels[lab].copy())
                anims.append(Transform(ghost, target, run_time=1.3, path_arc=0.4, introducer=True))
                first[lab] = target
            else:
                # a repeated label: a copy slides out from the first card to its own spot
                ghost = target.copy().move_to(first[lab])
                anims.append(later(1.4, Transform(ghost, target, run_time=0.7, introducer=True)))
            self.tri.append((lab, ghost))
        old = VGroup(*self.points.values(), *self.point_labels.values())
        anims.append(FadeAway(old, run_time=0.1))
        anims.append(FadeAway(self.ring_circle, run_time=0.6))
        self.points, self.point_labels = {}, {}
        verts = [TRI_C + xy(x * 0.6, (y - 3) * 0.68) for x, y in ((0, 6), (-5, 0), (5, 0))]
        self.tri_outline = Polygon(*verts, stroke_color="#6687A9", stroke_width=2)
        anims.append(later(1.0, Create(self.tri_outline, run_time=min(1.4, avail - 1.2))))
        return anims

    def layout_triangle_to_views(self, p, avail):
        views = self.board.views()
        src = {}
        for lab, c in self.tri:
            src.setdefault(lab, c)
        anims = []
        for i, (d, v) in enumerate(views):
            for r in range(3):
                for c in range(3):
                    lab = v[3 * r + c]
                    target = label_card(plabel(lab), VIEW_H).move_to(cell_pos(i, r, c))
                    ghost = src[lab].copy()
                    anims.append(later(0.15 * i + 0.05 * (3 * r + c), Transform(ghost, target, run_time=1.1,
                                                                             path_arc=0.3, introducer=True)))
                    self.cells[(i, r, c)] = ghost
                    self.cell_label[(i, r, c)] = lab
            corner = src[d]
            target = label_card(plabel(d), VIEW_H).move_to(xy(VIEW_X[i], CORNER_Y))
            target[0].set_fill(GOLD, 0.92).set_stroke(GOLD)
            target[1].set_color(BG)
            anims.append(Transform(corner, target, run_time=1.2, path_arc=0.3))
            self.corner_cards[i] = corner
            self.base[corner] = GOLD
            cap = text("picture at " + plabel(d), size=18, color=MUTED).move_to(xy(VIEW_X[i], CAPTION_Y))
            self.captions.add(cap)
        rest = VGroup(*(c for lab, c in self.tri if c not in self.corner_cards.values()), self.tri_outline)
        anims.append(later(1.3, FadeAway(rest, run_time=0.6)))
        anims.append(later(min(1.8, avail - 0.8), FadeIn(self.captions, run_time=0.6)))
        self.tri = []
        return anims

    def layout_projective_to_shuffle(self, p, avail):
        rho = OBJ["shuffle:rho"]["map"]
        anims = self.light({}, run=0.3) + self.clear_strip()
        pairs = "   ".join(f"{plabel(x)}→{rho[x]}" for x in [11] + list(range(11)))
        strip = self.overlay(text(pairs, size=20, color=MUTED).move_to(xy(0, STRIP_Y)))
        self.strip = [strip]
        anims.append(FadeIn(strip, run_time=0.5))
        # self.board now holds card labels; the cards on screen still show projective ones
        members = [(c, self.cell_label[key]) for key, c in sorted(self.cells.items())] + \
                  [(self.corner_cards[i], d) for i, d in enumerate(OBJ["kitten:projective"]["corners"])]
        per = (avail - 2.2) / len(members)
        for k, (c, lab) in enumerate(members):
            new = label_card(str(rho[lab]), VIEW_H)[1].move_to(c[1].get_center())
            if c in self.corner_cards.values():
                new.set_color(BG)
            # flash the box only: an Indicate on the whole card would replay its old label over the new one
            anims.append(later(0.4 + per * k, AnimationGroup(Transform(c[1], new, run_time=0.35),
                                                             Indicate(c[0], scale_factor=1.15, color=GOLD, run_time=0.5))))
        for key in self.cell_label:
            self.cell_label[key] = rho[self.cell_label[key]]
        new_caps = VGroup(*(text("picture at " + str(d), size=18, color=MUTED).move_to(cap)
                            for (d, _), cap in zip(self.board.views(), self.captions)))
        anims.append(later(avail - 1.4, Transform(self.captions, new_caps, run_time=0.6)))
        return anims

    def visual_summon_completion(self, arg, p, start, end, avail):
        self.play_board("summon_completion", arg, p)
        pts, phase = p["points"], p.get("phase", "complete")
        third = p["completes"][0]
        if arg.startswith("fano_"):
            pos = self.fano["pos"]
            if phase == "pick":
                anims = [FadeAway(self.summoned, run_time=0.3)] if len(self.summoned) else []
                if len(self.summoned):
                    self.overlays.remove(*self.summoned)
                self.summoned = VGroup(*(mark(pos[k]) for k in pts))
                self.overlay(*self.summoned)
                # the two marks land as their numbers are said, at the end of the line
                return anims + [appear(m, max(0.1, avail - 1.7) + 0.6 * i, 0.35, scale=True)
                                for i, m in enumerate(self.summoned)]
            line = self.fano["line"][frozenset(pts) | {third}]
            glow = line.copy().set_stroke(GOLD, 6)
            ring = mark(pos[third], GREEN, 0.26)
            lab = self.fano["lab"][third].copy().set_color(GREEN)
            self.summoned.add(glow, ring, lab)
            self.overlay(glow, ring, lab)
            return [later(0.1, Create(glow, run_time=0.8)),
                    later(0.9, ShowPassingFlash(line.copy().set_stroke(GREEN, 8), time_width=0.5, run_time=0.6)),
                    appear(ring, 1.2, 0.4, scale=True), appear(lab, 1.2, 0.4)]
        # ring_five
        if phase == "pick":
            anims = self.clear_marks()
            per = 0.32
            t0 = max(0.4, avail - 0.6 - 5 * per - 0.4)
            for i, x in enumerate(pts):
                m = self.overlay(mark(ring_pos(x)))
                self.marks[x] = m
                anims.append(appear(m, t0 + per * i, 0.3, scale=True))
            return anims
        rays = VGroup(*(Line(ring_pos(x), ring_pos(third), stroke_color=GREEN, stroke_width=4) for x in pts))
        m = self.overlay(mark(ring_pos(third), GREEN, 0.26))
        self.marks[third] = m
        block = sorted(pts + [third])
        cap = self.caption("the one block: {" + ", ".join(plabel(x) for x in block) + "}", xy(PANEL_X, -0.35),
                           size=22, color=GREEN)
        return [ShowPassingFlash(rays, time_width=0.6, run_time=0.9), appear(m, 0.7, 0.4, scale=True),
                appear(cap, 1.0, 0.5)]

    def visual_highlight(self, arg, p, start, end, avail):
        self.play_board("highlight", arg, p)
        delay = p.get("delay", 0.0)
        anims = getattr(self, "hl_" + (arg if not arg.startswith("family_") else "family"))(arg, p, avail - delay)
        return [later(delay, a) for a in anims] if delay else anims

    def hl_lines(self, arg, p, avail):
        """Each line lights up in turn, its three points with it; the two rules stay up beside the plane."""
        f = OBJ["fano"]
        rules = VGroup(text("the rules", size=24, color=GOLD),
                       text(f"every line has {f['line_size']} points", size=22),
                       text("any 2 points lie on", size=22), text("exactly 1 line", size=22))
        rules.arrange(DOWN, buff=0.14).move_to(xy(PANEL_X, 2.2))
        rules[3].next_to(rules[2], DOWN, buff=0.08)
        self.overlay(rules)
        self.panel["rules"] = rules
        per = (avail - 2.6) / len(f["lines"])
        anims = [appear(rules[0], 0.3, 0.4), appear(rules[1], avail * 0.42, 0.5), appear(VGroup(rules[2], rules[3]), avail * 0.66, 0.5)]
        for k, line in enumerate(f["lines"]):
            m = self.fano["line"][frozenset(line)]
            t = 0.4 + per * k
            anims.append(later(t, ShowPassingFlash(m.copy().set_stroke(GOLD, 7), time_width=0.7, run_time=per * 1.3)))
            anims += [later(t, Indicate(self.fano["pt"][x], color=GOLD, scale_factor=1.6, run_time=per * 1.2)) for x in line]
        return anims

    def hl_circle(self, arg, p, avail):
        circ = self.fano["line"][frozenset(OBJ["fano"]["circle"])]
        lab = self.caption("a line: 4, 5, 6", xy(PANEL_X, 0.85), size=22, color=GOLD)
        assert sorted(OBJ["fano"]["circle"]) == [4, 5, 6]
        return [later(0.2, Indicate(circ, color=GOLD, scale_factor=1.06, run_time=0.9)), appear(lab, 0.9, 0.5)]

    def hl_seed(self, arg, p, avail):
        q = sorted(self.board.marked)
        if p.get("phase") == "return":
            # back from x + 1 to x: each mark steps back one place round the clock
            moves = []
            for x, m in list(self.marks.items()):
                y = next(z for z in q if self.bm.translate(z) == x)
                moves.append((m, x, y))
            self.marks = {y: m for m, x, y in moves}
            cap = self.panel.pop("translate", None)
            out = [FadeAway(cap, run_time=0.3)] if cap is not None else []
            return out + [MoveAlongPath(m, self.ring_arc(x, y), run_time=0.9) for m, x, y in moves]
        order = p.get("order", q)
        anims = self.clear_marks()
        clock = self.panel.pop("clock", None)
        if clock is not None:
            anims.append(FadeAway(clock, run_time=0.4))
        per = (avail - 1.4) / len(order)
        for i, x in enumerate(order):
            m = self.overlay(mark(ring_pos(x)))
            self.marks[x] = m
            anims.append(appear(m, 0.5 + per * i, 0.3, scale=True))
        sq = OBJ["ring:projective"]["squares_in_order"]
        line1 = self.caption("seed: 0 and the squares", xy(PANEL_X, 3.2), size=24)
        line2 = self.caption("1², 2², 3², 4², 5² = " + ", ".join(map(str, sq)) + "  (mod 11)",
                             xy(PANEL_X - 0.4, 2.65), size=20, color=MUTED)
        self.panel["seed"] = VGroup(line1, line2)
        return anims + [appear(line1, 0.3, 0.4), appear(line2, 1.0, 0.5)]

    def ring_arc(self, x, y):
        """The path a mark takes from point x to point y of the ring."""
        a, b = ring_pos(x), ring_pos(y)
        if 11 in (x, y):
            return Line(a, b)
        if self.bm.translate(x) == y or self.bm.translate(y) == x:
            # one step round the circle
            ang = -TAU / 11 if self.bm.translate(x) == y else TAU / 11
            return Arc(radius=RING_R, start_angle=PI / 2 - x * TAU / 11, angle=ang, arc_center=RING_C)
        return ArcBetweenPoints(a, b, angle=0.6)

    def hl_corners(self, arg, p, avail):
        corners = set(OBJ["kitten:projective"]["corners"])
        cs = [c for lab, c in self.tri if lab in corners]
        return [later(0.8 + 0.6 * i, Indicate(c, scale_factor=1.3, color=GOLD, run_time=0.6)) for i, c in enumerate(cs)]

    def hl_repeats(self, arg, p, avail):
        copies = [c for lab, c in self.tri if lab == p["label"]]
        links = VGroup(*(DashedLine(a.get_center(), b.get_center(), stroke_color=GREEN, stroke_width=3, dash_length=0.12)
                         for a, b in zip(copies, copies[1:] + copies[:1])))
        self.overlay(links)
        back = avail - 0.7
        return [recolor(c, GREEN, 0.4) for c in copies] + [later(0.5, Create(links, run_time=0.9)),
                                                           later(back, FadeAway(links, run_time=0.5))] + \
            [later(back, recolor(c, None, 0.5)) for c in copies]

    def view_line_path(self, i, cells, wrap=False):
        """A chalk line through three cells of view i; a wrapped one leaves one edge and comes back at the other."""
        pts = [cell_pos(i, r, c) for r, c in cells]
        if not wrap:
            a, b = pts[0], pts[-1]
            d = (b - a) / np.linalg.norm(b - a)
            return VGroup(Line(a - 0.32 * d, b + 0.32 * d))
        (r0, c0), (r1, c1), _ = cells
        step = (np.array([r1 - r0, c1 - c0]) + 1) % 3 - 1     # the step mod 3, as -1, 0 or 1
        out = cell_pos(i, r0 + 0.66 * step[0], c0 + 0.66 * step[1])     # off one edge...
        back = cell_pos(i, r1 - 0.66 * step[0], c1 - 0.66 * step[1])    # ...and in at the other
        return VGroup(Line(pts[0], out).add_tip(tip_length=0.14), Line(back, pts[1]), Line(pts[1], pts[2]))

    def hl_line_cells(self, i, direction, k):
        a, b = direction
        cells = sorted((r, c) for r in range(3) for c in range(3) if (a * r + b * c) % 3 == k)
        assert {self.cell_point(i, r, c) for r, c in cells} == \
            set(self.bm.view_line(self.board.views()[i][1], direction, k))
        return cells

    def hl_row(self, arg, p, avail):
        i = self.view_index(p["picture"])
        if p.get("phase") == "again":
            # the same line once more: its cards pulse and the chalk line flashes
            cards = [c for c, col in self.lit.items() if col]
            line = self.panel.get("line")
            out = [later(0.4, LaggedStart(*(Indicate(c[0], color=GOLD, scale_factor=1.2) for c in cards),
                                          lag_ratio=0.4, run_time=1.4))]
            if line is not None:
                out.append(later(0.4, ShowPassingFlash(line.copy().set_stroke(GREEN, 7), time_width=0.6, run_time=1.2)))
            return out
        d = self.bm.DIRECTIONS[arg]
        cells = self.hl_line_cells(i, d, p.get("k", 0))
        if arg == "modular_diagonal":
            # walk the wrapped diagonal from its first cell: 6, then off the edge and back in, 4, then 9
            start = cells[0]
            step = (1, -1) if d == (1, 1) else (1, 1)
            cells = [((start[0] + n * step[0]) % 3, (start[1] + n * step[1]) % 3) for n in range(3)]
        path = self.view_line_path(i, cells, wrap=(arg == "modular_diagonal"))
        path.set_stroke(GOLD, 5)
        prev = self.panel.pop("line", None)
        self.panel["line"] = self.overlay(path)
        cards = {self.cells[(i, r, c)]: GOLD for r, c in cells}
        out = [FadeAway(prev, run_time=0.3)] if prev is not None else []
        return out + self.light(cards, run=0.35) + [later(0.15, Create(path, run_time=min(0.9, avail * 0.5)))]

    hl_column = hl_diagonal = hl_modular_diagonal = hl_row

    def hl_cross(self, arg, p, avail):
        i = self.view_index(p["picture"])
        cross = self.board.parts_points(p["picture"], [((1, 0), p.get("row", 0)), ((0, 1), p.get("column", 0))])
        pts = cross if arg == "cross" else set(self.board.view_dict()[p["picture"]]) - cross
        prev = self.panel.pop("line", None)
        out = [FadeAway(prev, run_time=0.3)] if prev is not None else []
        color = GOLD if arg == "cross" else BLUE
        cards = {c: color for c in self.cells_of(i, pts)}
        return out + self.light(cards, run=0.5, keep=(arg == "square"))

    hl_square = hl_cross

    FAMILY_NAMES = {"family_line": "line + corners", "family_parallel": "parallel lines",
                    "family_cross": "cross + corner", "family_square": "square + 2 corners"}

    def hl_family(self, arg, p, avail):
        ex = self.board.family_example(arg)
        i = self.view_index(ex["picture"])
        hexad = set(ex["hexad"])
        cards = {c: GOLD for c in self.cells_of(i, hexad) + self.corners_of(hexad)}
        anims = self.light(cards, run=0.5)
        # the corners the hexad leaves out go faint
        anims += self.set_faint(set(self.cells.values()) | set(cards))
        prev = self.panel.pop("line", None)
        if prev is not None:
            anims.append(FadeAway(prev, run_time=0.3))
        n = len(self.strip)
        count = len({hx for f, _, _, hx in self.bm.kitten_parts(self.bm.PROJECTIVE_VIEWS) if f == ex["family"]})
        c = chip(f"{self.FAMILY_NAMES[arg]}: {count}", size=18).move_to(xy(-4.8 + 3.2 * n, STRIP_Y))
        self.overlay(c)
        self.strip.append(c)
        self.family_counts = getattr(self, "family_counts", []) + [count]
        return anims + [appear(c, max(0.3, avail - 1.4), 0.5)]

    def hl_ep1_hands(self, arg, p, avail):
        fam, pic, parts = self.board.hand_parts(p["hand"])
        i = self.view_index(pic)
        hand = OBJ[p["hand"]]["cards"]
        cards = {c: GREEN for c in self.cells_of(i, set(hand)) + self.corners_of(set(hand))}
        assert len(cards) == 6, (p["hand"], len(cards))
        anims = self.light(cards, run=0.5)
        if self.strip and not getattr(self, "hand_strip", False):
            anims += self.clear_strip()
        self.hand_strip = True
        # the other two views and the unused corners go faint; the hand's own cards stay bright
        anims += self.set_faint({c for (j, _, _), c in self.cells.items() if j == i} | set(cards))
        n = len(self.strip)
        g = mini_hand(sorted(hand), h=0.34, color=GREEN)
        for cd in g[0]:
            cd[0].set_fill(GREEN, 0.92).set_stroke(GREEN)
            cd[1].set_color(BG)
        g.move_to(xy(-5.0 + 2.5 * n, STRIP_Y))
        self.overlay(g)
        self.strip.append(g)
        return anims + [appear(g, 0.4, 0.5)]

    def visual_point_ring(self, arg, p, start, end, avail):
        before = dict(self.marks)
        self.play_board("point_ring", arg, p)
        f = self.bm.RING_MAPS[arg]
        moves = [(m, x, f(x)) for x, m in before.items()]
        self.marks = {y: m for m, x, y in moves}
        run = min(1.6, avail - 2.0)
        t0 = max(0.3, avail * 0.45 - run / 2)
        anims = [later(t0, MoveAlongPath(m, self.ring_arc(x, y), run_time=run)) for m, x, y in moves if x != y]
        anims += [later(t0, Indicate(m, color=GOLD, run_time=run)) for m, x, y in moves if x == y]
        old = self.panel.pop("seed", None)
        if old is not None:
            anims.append(FadeAway(old, run_time=0.3))
        prev = self.panel.pop("translate", None)
        if prev is not None:
            anims.append(FadeAway(prev, run_time=0.3))
        if arg == "translate":
            assert self.bm.translate(11) == 11 and self.bm.translate(10) == 0
            head, rule, note = "move one: add one", "x → x + 1", "∞ stays put"
        else:
            assert self.bm.invert(0) == 11 and self.bm.invert(2) == 5 and self.bm.invert(5) == 2
            head, rule, note = "move two: negative reciprocal", "x → −1/x", "0 ↔ ∞,  2 ↔ 5"
        g = VGroup(text(head, size=24), text(rule, size=26, color=GOLD), text(note, size=21, color=MUTED),
                   text("{" + ", ".join(plabel(x) for x in sorted(self.board.marked)) + "}", size=22, color=GOLD))
        g.arrange(DOWN, buff=0.18).move_to(xy(PANEL_X, 2.55))
        self.overlay(g)
        self.panel["translate"] = g
        return anims + [appear(g[0], 0.2, 0.4), appear(g[1], 0.5, 0.4), appear(g[2], t0 + 0.2, 0.4),
                        appear(g[3], t0 + run, 0.4)]

    def visual_clock_mod(self, arg, p, start, end, avail):
        self.play_board("clock_mod", arg, p)
        if arg == "3":
            return self.three_hour_clock(p, avail)
        if p.get("phase") == "sweep":
            # the clock's hand, pinned at infinity, sweeps the hours as Euler counts them
            h0, h1 = p["hours"]
            self.hand_hour = h0
            hand = self.overlay(self.clock_hand(h0))
            self.panel["clock"] = VGroup(hand)
            run = min(2.0, avail - 1.4)
            labs = [self.point_labels[h] for h in range(h0, h1 + 1)]
            return [appear(hand, 0.6, 0.3),
                    later(0.9, hand_turn(hand, h0, h1, run)),
                    later(0.9, LaggedStart(*(Indicate(m, color=GOLD, scale_factor=1.5) for m in labs),
                                           lag_ratio=0.6, run_time=run))]
        a, b, c = p["shows"]
        assert self.bm.translate(a) == c
        hand = self.panel["clock"][0]
        eq = self.caption(f"{a} + {b} = {c}", xy(PANEL_X, 3.1), size=34, color=GOLD)
        mod = self.caption("arithmetic mod 11", xy(PANEL_X, 2.5), size=22, color=MUTED)
        self.panel["clock"].add(eq, mod)
        ten, zero = self.points[a], self.points[c]
        return [later(0.3, Indicate(ten, color=GOLD, scale_factor=1.8, run_time=0.6)),
                later(1.1, hand_turn(hand, a, a + 1, 0.5)),       # one hour on: 10 + 1 = 11, which is 0
                later(1.6, Indicate(zero, color=GOLD, scale_factor=1.8, run_time=0.6)), appear(eq, 1.3, 0.5),
                appear(mod, min(3.0, avail - 0.8), 0.5)]

    def clock_hand(self, hour, center=RING_C, length=RING_R - 0.3, hours=11, color=GOLD, width=6):
        a = PI / 2 - hour * TAU / hours
        tip = center + length * np.array([np.cos(a), np.sin(a), 0])
        return Line(center, tip, stroke_color=color, stroke_width=width).add_tip(tip_length=0.16)

    def three_hour_clock(self, p, avail):
        """A clock with three hours beside the grid: its hand goes 0, 1, 2 and back to 0."""
        a, b, c = p["shows"]
        center, r = xy(-2.05, -0.22), 0.36
        face = Circle(radius=r, stroke_color=CHALK, stroke_width=2).move_to(center)
        nums = VGroup(*(text(str(h), size=18, color=MUTED).move_to(
            center + (r + 0.17) * np.array([np.sin(h * TAU / 3), np.cos(h * TAU / 3), 0])) for h in range(3)))
        hand = Line(center, center + UP * (r - 0.06), stroke_color=GOLD, stroke_width=4).add_tip(tip_length=0.1)
        eq = text(f"{a} + {b} = {c}", size=20, color=GOLD).next_to(face, RIGHT, buff=0.35)
        self.overlay(face, nums, hand, eq)
        t0, step = 0.5, (avail - 1.4) / 3
        anims = [appear(face, 0.1, 0.4), appear(nums, 0.1, 0.4), appear(hand, 0.3, 0.3)]
        for k in range(3):
            anims.append(later(t0 + step * k, hand_turn(hand, k, k + 1, 0.35, center=center, hours=3)))
        anims.append(appear(eq, t0 + step * 2 + 0.3, 0.4))
        return anims

    def visual_reveal_count(self, arg, p, start, end, avail):
        self.play_board("reveal_count", arg, p)
        return getattr(self, "count_" + arg)(p, avail)

    def steiner_panel(self, t, k, v, words, at):
        head = VGroup(*(text(s, size=44, weight=BOLD, color=INK if s in "S(,)" else GOLD)
                        for s in ("S(", str(t), ",", str(k), ",", str(v), ")"))).arrange(RIGHT, buff=0.06)
        for m in head:
            if m.height < 0.3:
                m.align_to(head, DOWN)
        head.move_to(at)
        lines = VGroup(*(text(w, size=22, color=MUTED) for w in words)).arrange(DOWN, buff=0.16)
        lines.next_to(head, DOWN, buff=0.35)
        return head, lines

    def count_s_2_3_7(self, p, avail):
        t, k, v = p["t"], p["k"], p["v"]
        f = OBJ["fano"]
        head, lines = self.steiner_panel(t, k, v, (f"every {t} points", f"lie on exactly 1 line of {k}",
                                                   f"{v} points in all"), xy(PANEL_X, 2.75))
        self.overlay(head, lines)
        self.panel["s237"] = VGroup(head, lines)
        line = self.fano["line"][frozenset(f["lines"][0])]
        two = [self.fano["pt"][x] for x in f["lines"][0][:2]]
        per = (avail - 1.2) / 3
        return [appear(VGroup(head[0], head[2], head[4], head[6]), 0.2, 0.4),
                appear(head[1], 0.6, 0.3), appear(lines[0], 0.6, 0.4),
                *(later(0.6, Indicate(d, color=GOLD, scale_factor=1.8, run_time=0.7)) for d in two),
                appear(head[3], 0.6 + per, 0.3), appear(lines[1], 0.6 + per, 0.4),
                later(0.6 + per, ShowPassingFlash(line.copy().set_stroke(GOLD, 7), time_width=0.5, run_time=0.8)),
                appear(head[5], 0.6 + 2 * per, 0.3), appear(lines[2], 0.6 + 2 * per, 0.4),
                later(0.6 + 2 * per, LaggedStart(*(Indicate(d, color=GOLD, scale_factor=1.6)
                                                   for d in self.fano["pt"].values()), lag_ratio=0.1, run_time=0.9))]

    def count_s_5_6_12(self, p, avail):
        phase = p.get("phase", "points")
        ex = OBJ["ring:projective"]["five_example"]
        if phase == "points":
            # the Fano plane and its name step aside; twelve blank points stand in a ring
            mini = VGroup(self.fano["group"], self.panel.pop("s237"))
            self.overlays.add(self.fano["group"])
            target = mini.copy().scale(0.36).move_to(xy(-5.3, 3.05))
            anims = [Transform(mini, target, run_time=0.9)]
            for x in range(12):
                self.points[x] = Dot(blank_pos(x), radius=0.1, color=MUTED).set_z_index(FRONT)
            anims.append(later(0.9, LaggedStart(*(GrowFromCenter(self.points[x]) for x in range(12)),
                                                lag_ratio=0.12, run_time=1.4)))
            five = VGroup(*(mark(blank_pos(x)) for x in ex["points"]))
            q = blank_pos(ex["completion"])
            ask = VGroup(DashedVMobject(Circle(radius=0.24, stroke_color=GOLD, stroke_width=3).move_to(q), num_dashes=10),
                         text("?", size=24, color=GOLD, weight=BOLD).move_to(q + (q - BLANK_C) * 0.3))
            self.overlay(five, ask)
            self.panel["block"] = VGroup(five, ask)
            anims.append(later(2.4, LaggedStart(*(GrowFromCenter(m) for m in five), lag_ratio=0.2, run_time=0.8)))
            anims.append(appear(ask, min(3.3, avail - 0.5), 0.4))
            return anims
        if phase == "label":
            t, k, v = p["t"], p["k"], p["v"]
            head, lines = self.steiner_panel(t, k, v, (f"every {t} points", f"lie in exactly 1 block of {k}",
                                                       f"{v} points in all"), xy(PANEL_X - 0.3, 2.75))
            self.overlay(head, lines)
            self.panel["s5612"] = VGroup(head, lines)
            per = (avail - 2.0) / 3
            return [appear(VGroup(head[0], head[2], head[4], head[6]), 0.2, 0.4),
                    appear(head[5], 0.6, 0.3), appear(lines[2], 0.6, 0.4),
                    later(0.6, LaggedStart(*(Indicate(d, color=GOLD) for d in self.points.values()), lag_ratio=0.05, run_time=0.8)),
                    appear(head[3], 0.6 + per, 0.3), appear(lines[1], 0.6 + per, 0.4),
                    appear(head[1], 0.6 + 2 * per, 0.3), appear(lines[0], 0.6 + 2 * per, 0.4),
                    later(0.6 + 2 * per, Indicate(self.panel["block"][0], color=GOLD, scale_factor=1.2, run_time=0.8))]
        # name: the waiting block is a hexad, and so are the 132 the count promised
        q = blank_pos(ex["completion"])
        name = self.caption("hexad", BLANK_C + xy(0, 0.1), size=30, color=GOLD, weight=BOLD)
        res = self.panel["result"]
        new = text(f"{OBJ['count:design']['blocks_from_counting']} hexads", size=34, color=GOLD, weight=BOLD).move_to(res)
        return [appear(name, 0.3, 0.6), Transform(self.panel["block"][1], mark(q), run_time=0.6),
                later(0.4, Transform(res, new, run_time=0.6))]

    def count_792_over_6(self, p, avail):
        from math import prod
        d = OBJ["count:design"]
        num, den = d["fives_formula"]
        fives = prod(num) // prod(den)
        phase = p["phase"]
        if phase == "fives":
            old = self.panel.pop("s5612")
            head = old[0]
            anims = [FadeAway(old[1], run_time=0.4), head.animate(run_time=0.6).scale(0.8).move_to(xy(PANEL_X - 0.3, 3.45))]
            frac = VGroup(text(" · ".join(map(str, num)), size=26), Line(LEFT * 1.45, RIGHT * 1.45, stroke_color=INK, stroke_width=2),
                          text(" · ".join(map(str, den)), size=26)).arrange(DOWN, buff=0.12)
            eq = text(f"= {fives}", size=32, color=GOLD, weight=BOLD)
            g = VGroup(frac, eq).arrange(RIGHT, buff=0.3).move_to(xy(PANEL_X - 0.3, 2.35))
            cap = text("ways to choose 5 of the 12 points", size=20, color=MUTED).next_to(g, DOWN, buff=0.15)
            self.overlay(g, cap)
            return anims + [appear(frac, 0.6, 0.6), appear(eq, min(2.6, avail - 1.2), 0.5), appear(cap, min(3.1, avail - 0.7), 0.5)]
        if phase == "per_block":
            per = d["five_in_block"]
            g = text(f"each block of 6 holds {per} fives", size=24).move_to(xy(PANEL_X - 0.3, 1.2))
            note = text("and no five is in two blocks", size=20, color=MUTED).next_to(g, DOWN, buff=0.12)
            self.overlay(g, note)
            block = self.panel["block"]
            return [appear(g, 0.3, 0.5), later(0.5, Indicate(block, color=GOLD, scale_factor=1.15, run_time=0.9)),
                    appear(note, min(2.6, avail - 0.7), 0.5)]
        blocks = d["blocks_from_counting"]
        assert blocks == fives // d["five_in_block"]
        g = text(f"{fives} ÷ {d['five_in_block']} = {blocks}", size=30).move_to(xy(PANEL_X - 0.3, 0.2))
        res = text(f"{blocks} blocks", size=34, color=GOLD, weight=BOLD).move_to(xy(PANEL_X - 0.3, -0.42))
        self.overlay(g, res)
        self.panel["result"] = res
        return [appear(g, 0.3, 0.6), appear(res, min(2.6, avail - 0.8), 0.5)]

    def count_orbit_132(self, p, avail):
        layers = self.bm.orbit_layers(self.bm.Q)
        n = sum(len(l) for l in layers)
        anims = self.clear_marks(run=0.3)
        for key in ("translate", "seed"):
            old = self.panel.pop(key, None)
            if old is not None:
                anims.append(FadeAway(old, run_time=0.3))
        cols, step = 12, 0.24
        grid_c = xy(PANEL_X, 1.25)
        rows = -(-n // cols)
        spots = [grid_c + xy((k % cols - (cols - 1) / 2) * step, ((rows - 1) / 2 - k // cols) * step) for k in range(n)]
        self.orbit_dots = [Dot(q, radius=0.06, color=GOLD) for q in spots]
        counter = self.caption("1 set", xy(PANEL_X, 3.2), size=34, color=GOLD, weight=BOLD)
        self.overlay(*self.orbit_dots)
        per = (avail - 1.6) / len(layers)
        chain, k = [], 0
        for i, layer in enumerate(layers):
            t = 0.3 + per * i
            for _ in layer:
                anims.append(appear(self.orbit_dots[k], t, min(0.3, per), scale=True))
                k += 1
            # one set of the layer flashes on the ring
            ms = [self.overlay(mark(ring_pos(x))) for x in sorted(min(layer, key=sorted))]
            anims += [appear(m, t, 0.12) for m in ms] + [later(t + per * 0.8, FadeAway(m, run_time=0.1)) for m in ms]
            if i:      # the counter: one Text reshaped in place, layer by layer
                chain += [Wait(run_time=per - 0.12), Transform(counter, text(f"{k} sets", size=34, color=GOLD,
                                                                              weight=BOLD).move_to(counter), run_time=0.12)]
        assert k == n == OBJ["orbit:Q"]["hexads"]
        anims.append(appear(counter, 0.25, 0.2))
        anims.append(later(0.3 + 0.12, Succession(*chain)))
        orbit = self.caption("the orbit of the seed", xy(PANEL_X, 2.7), size=22, color=MUTED)
        anims.append(appear(orbit, avail - 1.0, 0.5))
        self.panel["counter"], self.panel["orbit"] = counter, orbit
        return anims

    def count_fives_792(self, p, avail):
        from collections import Counter
        from itertools import combinations
        from math import comb
        fives = Counter(frozenset(s) for h in self.bm.ORBIT for s in combinations(h, 5))
        total, distinct = sum(fives.values()), len(fives)
        assert distinct == comb(12, 5) and set(fives.values()) == {1}
        cols, step = 36, 0.085
        rows = -(-total // cols)
        grid_c = xy(PANEL_X, 1.25)
        tiny = [grid_c + xy((k % cols - (cols - 1) / 2) * step, ((rows - 1) / 2 - k // cols) * step) for k in range(total)]
        anims = []
        for k, d in enumerate(self.orbit_dots):
            six = VGroup(*(Dot(tiny[6 * k + j], radius=0.028, color=GOLD) for j in range(6)))
            anims.append(later(0.3 + 0.006 * k, Transform(d, six, run_time=1.2)))
        eq = self.caption(f"{len(self.bm.ORBIT)} × 6 = {total} fives", xy(PANEL_X, 2.7), size=24)
        ok = self.caption(f"all {comb(12, 5)} fives, each exactly once ✓", xy(PANEL_X, -0.0), size=21, color=GREEN)
        anims.append(appear(eq, 1.2, 0.5))
        anims.append(appear(ok, min(avail - 0.8, 4.5), 0.5))
        anims.append(FadeAway(self.panel.pop("orbit"), run_time=0.4))
        return anims

    def count_12_12_54_54(self, p, avail):
        parts = self.family_counts
        total = sum(parts)
        if p["phase"] == "sum":
            s = text(" + ".join(map(str, parts)) + f" = {total}", size=30, color=GOLD, weight=BOLD).move_to(xy(0, STRIP_Y))
            # the chips gather into the sum (an introduced copy: the chips' group is not itself in the scene)
            chips = VGroup(*self.strip)
            ghost = chips.copy()
            self.overlay(ghost)
            self.strip = [ghost]
            self.panel["sum"] = ghost
            return [FadeAway(chips, run_time=0.1), Transform(ghost, s, run_time=1.0, introducer=True)] + self.undim(0.5)
        s = self.panel["sum"]
        new = text(" + ".join(map(str, parts)) + f" = {total} = the orbit on Euler's clock ✓", size=28, color=GREEN,
                   weight=BOLD).move_to(xy(0, STRIP_Y))
        return [later(0.4, Transform(s, new, run_time=0.8))]


# ---------------------------------------------------------------- Episode 3: the MINIMOG
#
# Ada lays the twelve cards out as Conway's MINIMOG on the left of the space
# above the table, numbers its rows 0, 1, 2 and reads hands column by column.
# Under each column sit its count, its reading (the odd man out, or "?" for a
# wildcard) and, when one is on show, the codeword the hand is checked
# against.  The three-hour clock, the codewords and the repairs go on the
# right.  Every cell, word, count, reading and swap is computed by
# cue_tools.Code (the code the checker runs) from build_math_objects.py.
# The grid and its rows stay up all episode; readings, captions and chips
# are overlays, cleared at each change of scene.

GRID_X = (-4.45, -3.35, -2.25, -1.15)      # the MINIMOG's four columns
GRID_Y = (3.35, 2.35, 1.35)                # its three rows, 0 at the top
GRID_H = 0.84                              # card height in the grid (the titles' cards)
ROWNUM_X = -5.8                            # the row numbers 0, 1, 2
LANE_X = -6.35                             # the names of the lanes under the grid
COUNT_Y, READ_Y, WORD_Y = 0.6, 0.08, -0.45  # above the kittens' ears (about y = -0.8)
VERDICT = xy(GRID_X[3] + 1.6, WORD_Y)      # "a hexad", "not a hexad": right of the word lane
CLOCK_C, CLOCK_R = xy(2.6, 1.95), 1.0      # the three-hour clock, full size
CLOCK_SMALL_C, CLOCK_SMALL_R = xy(6.15, 3.25), 0.42
SLOT_X0, SLOT_DX, SLOT_Y = 1.15, 1.15, 2.95  # the four boxes of a codeword
TABLE_X = (2.0, 3.95, 5.9)                 # the nine words: one column for each b
TABLE_Y = (1.75, 1.0, 0.25)                # and one row for each a
WRAP_C, WRAP_CELL = xy(3.5, 1.95), 0.8    # Episode 2's grid at infinity, recalled
CLOCK_LEFT = xy(0.85, 1.95)                # where the clock steps to beside it
LIT, IN_COLOR = GOLD, GREEN                 # marked cards; a card swapped in


def grid_pos(r, c):
    return xy(GRID_X[c], GRID_Y[r])


def clock_point(center, radius, h, hours=3):
    a = h * TAU / hours
    return center + radius * np.array([np.sin(a), np.cos(a), 0])


def digit(v, size=30, color=INK):
    """A coordinate as written: its value, or ? for a wildcard."""
    return text("?" if v is None else str(v), size=size, color=color, weight=BOLD)


class CodeVisuals(CardLights):
    """Episode 3's props and visual verbs: Ada's MINIMOG and the tetracode."""

    def setup_stage(self):
        self.code = Code(OBJ)
        self.bm = self.code.bm
        M = self.bm.M
        self.cards = {M[r][c]: label_card(str(M[r][c]), GRID_H) for r in range(3) for c in range(4)}
        self.rownums = VGroup(*(text(str(r), size=30, color=MUTED).move_to(xy(ROWNUM_X, GRID_Y[r])) for r in range(3)))
        self.row_heads = VGroup(text("row", size=18, color=MUTED).move_to(xy(ROWNUM_X, GRID_Y[0] + 0.62)))
        self.lane_heads = {}       # "count", "reads", "word": the labels left of the rows under the grid
        self.slots = None          # the four reading boxes under the columns
        self.lit, self.faint, self.base = {}, {}, {}
        self.cols = {}             # (row name, column) -> the mobject shown there
        self.clock = None          # {"face", "nums", "hand", "center", "radius"}
        self.hour = None
        self.sums = []             # the clock's equations, top to bottom
        self.ab = {}               # "a", "b" -> chip by the clock
        self.boxes = None          # the four codeword boxes (with their labels)
        self.box_vals = {}
        self.table = None          # (a, b) -> VGroup of four digits
        self.table_group = None
        self.panel = {}            # named overlays
        self.chips = {}            # (out, in) -> chip, for the repairs

    def setup_actors(self):
        who = CUES["stage"].get("precise")
        if not who:
            return
        a = self.actors[who]
        a.base = lerp_pose(a.base, a.pose_named("cat_proud"), 0.35)    # sits very straight
        a.breath = 0.005
        a.speak_gaze = (-1.1, 0.75)                                    # looks up at the grid (left) as she speaks

    def transition_anims(self, n):
        run = secs(n) * 0.5
        anims = [recolor(c, self.base.get(c), run) for c, col in self.lit.items() if col]
        self.lit = {}
        anims += self.undim(run)
        self.cols, self.panel, self.chips = {}, {}, {}
        return anims

    def point_target(self, target):
        grid = VGroup(*self.cards.values())
        lit = [c for c, col in self.lit.items() if col]
        return {"grid": grid, "board": VGroup(*lit) if lit else grid,
                "clock": VGroup(self.clock["face"], self.clock["hand"]) if self.clock else None,
                "word": self.boxes, "words": self.table_group}.get(target)

    def play_code(self, verb, arg, p):
        errs = self.code.play(verb, arg, p)
        if errs:
            raise ValueError(f"{self.beat_id} {verb}:{arg}: " + "; ".join(errs))

    def overlay(self, *ms):
        self.overlays.add(*ms)
        return ms[0] if len(ms) == 1 else ms

    def drop(self, m, t=0.0, run=0.3):
        """Take an overlay off the screen at t."""
        if m is None:
            return []
        if m in self.overlays:
            self.overlays.remove(m)
        return [later(t, FadeAway(m, run_time=run))]

    # -- the lanes under the grid: counts, readings, the word

    def lane_head(self, name, t=0.0):
        if name in self.lane_heads:
            return []
        y = {"count": COUNT_Y, "reads": READ_Y, "word": WORD_Y}[name]
        m = text({"count": "cards", "reads": "reads", "word": "word"}[name], size=18, color=MUTED).move_to(xy(LANE_X, y))
        self.lane_heads[name] = m
        return [appear(m, t, 0.4)]

    def ensure_slots(self, t=0.0):
        if self.slots is not None:
            return []
        self.slots = VGroup(*(RoundedRectangle(width=0.62, height=0.5, corner_radius=0.08, stroke_color=EDGE,
                                               stroke_width=1.6, fill_color=PANEL, fill_opacity=1).move_to(xy(GRID_X[c], READ_Y))
                              for c in range(4)))
        return [appear(self.slots, t, 0.4)] + self.lane_head("reads", t)

    def put(self, lane, c, m, t=0.0, run=0.35, shift=None):
        """Show m in the lane (count, reads, word) under column c, replacing what was there."""
        y = {"count": COUNT_Y, "reads": READ_Y, "word": WORD_Y}[lane]
        m.move_to(xy(GRID_X[c], y)).set_z_index(FRONT + 0.1)
        anims = self.drop(self.cols.get((lane, c)), t, 0.2)
        self.cols[(lane, c)] = self.overlay(m)
        anims.append(later(t, FadeIn(m, shift=shift if shift is not None else DOWN * 0.12, run_time=run)))
        return anims

    def clear_lane(self, lane, t=0.0):
        anims = []
        for c in range(4):
            anims += self.drop(self.cols.pop((lane, c), None), t, 0.25)
        return anims

    def show_counts(self, counts, t0=0.0, per=0.35, color=MUTED):
        anims = self.lane_head("count", t0)
        for c, n in enumerate(counts):
            anims += self.put("count", c, text(str(n), size=24, color=color), t0 + per * c)
        return anims

    def show_readings(self, odds, t0=0.0, per=0.5, color=GOLD):
        anims = self.ensure_slots(t0)
        for c, o in enumerate(odds):
            anims += self.put("reads", c, digit(o, 28, MUTED if o is None else color), t0 + per * c)
        return anims

    def show_word(self, word, t0=0.0, per=0.4, color=INK, from_reads=()):
        anims = self.lane_head("word", t0)
        for c, w in enumerate(word):
            m = digit(w, 28, color)
            src = self.cols.get(("reads", c)) if c in from_reads else None
            if src is not None:
                # a reading that fixes the word drops into it
                ghost = src.copy()
                m.move_to(xy(GRID_X[c], WORD_Y)).set_z_index(FRONT + 0.1)
                anims += self.drop(self.cols.get(("word", c)), t0, 0.2)
                self.cols[("word", c)] = self.overlay(ghost)
                anims.append(later(t0 + per * c, Transform(ghost, m.set_color(color), run_time=0.45, introducer=True)))
            else:
                anims += self.put("word", c, m, t0 + per * c)
        return anims

    def mark_hand(self, cards, run=0.4, color=LIT):
        return self.light({self.cards[v]: color for v in cards}, run=run)

    # -- visuals

    def visual_fly_to_minimog(self, arg, p, start, end, avail):
        self.play_code("fly_to_minimog", arg, p)
        M = self.bm.M
        if p.get("phase") == "row":
            for v, c in self.cards.items():
                c.move_to(xy((v - 5.5) * 0.98, 1.6))
            return [LaggedStart(*(FadeIn(self.cards[v], shift=UP * 0.15) for v in range(12)), lag_ratio=0.08,
                                run_time=min(1.6, avail - 0.2))]
        last = M[-1][-1]
        anims = []
        order = [v for row in M for v in row]
        for k, v in enumerate(order):
            r, c = self.code.cell(v)
            target = label_card(str(v), GRID_H).move_to(grid_pos(r, c))
            if v == last:
                target.rotate(0.22)                  # lands crooked...
            anims.append(later(0.06 * k, Transform(self.cards[v], target, path_arc=0.5, run_time=1.1)))
        straighten = 0.06 * len(order) + 1.3
        r, c = self.code.cell(last)
        # ...and Ada straightens it (Rotate fixes its pivot when built, so name the cell)
        anims.append(later(straighten, Rotate(self.cards[last], -0.22, about_point=grid_pos(r, c), run_time=0.35)))
        self.actors["ada"].acts.append((start + int(straighten * FPS) - 8, start + int((straighten + 0.5) * FPS), "straightens"))
        return anims

    def visual_highlight(self, arg, p, start, end, avail):
        self.play_code("highlight", arg, p)
        return getattr(self, "hl_" + arg)(p, avail)

    def hl_rows(self, p, avail):
        per = min(0.8, (avail - 0.8) / 3)
        anims = []
        for r in range(3):
            row = VGroup(*(self.cards[self.bm.M[r][c]] for c in range(4)))
            anims += [appear(self.rownums[r], 0.4 + per * r, 0.3),
                      later(0.4 + per * r, Indicate(row, color=GOLD, scale_factor=1.06, run_time=0.5))]
        return anims

    def hl_two_coordinates(self, p, avail):
        """Cover the last two coordinates of every word; then keep only the words that start as given."""
        if p["phase"] == "cover":
            covers = VGroup()
            for w in self.table.values():
                box = SurroundingRectangle(VGroup(w[2], w[3]), buff=0.06, corner_radius=0.06, stroke_width=0,
                                           fill_color=EDGE, fill_opacity=1).set_z_index(FRONT + 0.2)
                covers.add(box)
            self.panel["covers"] = self.overlay(covers)
            return [later(0.8, LaggedStart(*(FadeIn(b, shift=LEFT * 0.1) for b in covers), lag_ratio=0.08,
                                           run_time=min(1.4, avail - 1.0)))]
        known = {int(k): v for k, v in p["known"].items()}
        keep = [ab for ab, w in self.table.items() if all(self.bm.tetra_word(*ab)[i] == v for i, v in known.items())]
        t = min(avail * 0.45, avail - 2.2)
        anims = []
        for ab, w in self.table.items():
            if ab not in keep:
                anims.append(later(t, opacity_to(w, 0.25, 0.5)))
                self.faint[w] = 0.25
        covers = self.panel.get("covers")
        for ab in keep:
            k = list(self.table).index(ab)
            anims.append(later(t + 0.6, FadeOut(covers[k], run_time=0.4)))
            anims.append(later(t + 0.9, Indicate(self.table[ab], color=GOLD, scale_factor=1.3, run_time=0.8)))
        for k, ab in enumerate(self.table):
            if ab not in keep:
                anims.append(later(t, opacity_to(covers[k], 0.25, 0.5)))
        return anims

    def hl_dim(self, p, avail):
        """The grid and its lanes dim while Euler wonders."""
        anims = self.light({}, run=0.5)
        parts = list(self.cards.values()) + list(self.rownums) + list(self.lane_heads.values()) + list(self.slots or [])
        for m in parts:
            anims.append(opacity_to(m, 0.35, 1.2))
            self.faint[m] = 0.35
        return anims

    def hl_column_one(self, p, avail):
        c = p["column"]
        cards = p["cards"]
        anims = self.clear_lane("count") + self.clear_lane("reads") + self.ensure_slots(0.0)
        anims += self.mark_hand(cards, run=0.35)
        box = SurroundingRectangle(VGroup(*(self.cards[self.bm.M[r][c]] for r in range(3))), color=EDGE,
                                   buff=0.1, corner_radius=0.1, stroke_width=2)
        self.panel["colbox"] = self.overlay(box)
        _, odd = self.bm.column_reading({self.code.cell(v)[0] for v in cards})
        t = min(avail * 0.62, avail - 0.9)
        anims += [appear(box, 0.1, 0.4), later(t - 0.5, Indicate(self.rownums[odd], color=GOLD, scale_factor=1.5, run_time=0.6))]
        anims += self.put("count", c, text(str(len(cards)), size=24, color=MUTED), 0.5) + self.lane_head("count", 0.5)
        anims += self.put("reads", c, digit(odd, 28, GOLD), t)
        return anims

    def hl_column_two(self, p, avail):
        c = p["column"]
        cards = p["cards"]
        _, odd = self.bm.column_reading({self.code.cell(v)[0] for v in cards})
        anims = self.mark_hand(cards, run=0.4)
        anims += self.put("count", c, text(str(len(cards)), size=24, color=MUTED), 0.4)
        anims += self.drop(self.cols.pop(("reads", c), None), 0.3, 0.25)
        t = min(avail * 0.75, avail - 0.8)
        anims += [later(t - 0.6, Indicate(self.rownums[odd], color=GOLD, scale_factor=1.5, run_time=0.6))]
        anims += self.put("reads", c, digit(odd, 28, GOLD), t)
        return anims

    def hl_column_wild(self, p, avail):
        c = p["column"]
        cards = [] if p["phase"] == "empty" else [self.bm.M[r][c] for r in range(3)]
        anims = self.mark_hand(cards, run=0.4)
        for key in ("oddring", "oddwords", "oddnote"):
            anims += self.drop(self.panel.pop(key, None), 0.0, 0.3)
        anims += self.put("count", c, text(str(len(cards)), size=24, color=MUTED), 0.3)
        anims += self.put("reads", c, digit(None, 28, MUTED), 0.7)
        if p["phase"] == "full":
            note = self.overlay(text("a wildcard fits any row", size=20, color=MUTED).move_to(xy(GRID_X[1] + 0.6, WORD_Y)))
            self.panel["wildnote"] = note
            anims += [appear(note, 0.9, 0.4)]
        return anims

    def hl_readings(self, p, avail):
        if p.get("phase") == "clear":
            anims = self.light({}, run=0.3) + self.ensure_slots(0.3)
            if self.clock is not None:
                cl = VGroup(self.clock["face"], self.clock["nums"], self.clock["hand"])
                anims.append(FadeAway(cl, run_time=0.5))
                self.clock, self.hour = None, None
            # (the grid's pulse comes from Ada's point_at: two Indicates at once on the
            # same cards would leave them in the first one's color)
            return anims
        # the rule: four readings, one codeword
        anims = self.light({}, run=0.3) + self.clear_lane("count") + self.drop(self.panel.pop("wildnote", None))
        anims += self.drop(self.panel.pop("colbox", None))
        anims += self.show_readings([None] * 4, 0.3, 0.12)
        arrow = Arrow(xy(GRID_X[3] + 0.5, READ_Y), xy(TABLE_X[0] - 1.6, TABLE_Y[2]), buff=0.05, stroke_width=3,
                      color=GOLD, max_tip_length_to_length_ratio=0.12)
        self.panel["rule_arrow"] = self.overlay(arrow)
        rule = self.overlay(text("the readings must spell a codeword", size=20, color=GOLD).move_to(xy(GRID_X[1] + 0.55, WORD_Y)))
        self.panel["rule"] = rule
        t = min(avail * 0.55, avail - 1.2)
        return anims + [appear(rule, max(0.5, t - 0.6), 0.4), later(t, GrowArrow(arrow, run_time=0.5)),
                        later(t + 0.4, Indicate(self.table_group, color=GOLD, scale_factor=1.05, run_time=0.8))]

    def hl_column_counts(self, p, avail):
        if "hand" in p:
            # Episode 1's 24-hand: its rows fit a word, but its counts are forbidden
            t = self.code.test()
            w = t["words_fitting"][0]
            anims = [later(0.2, Indicate(self.table[(w[1], w[0])], color=GREEN, scale_factor=1.25, run_time=0.8))]
            tm = min(avail * 0.4, avail - 2.0)
            for c in range(4):
                m = self.cols.get(("count", c))
                if m is not None:
                    anims.append(later(tm + 0.25 * c, recolor_text(m, RED, 0.3)))
            stamp = self.overlay(text(", ".join(map(str, t["column_counts"])) + ": forbidden", size=24, color=RED, weight=BOLD).move_to(xy(GRID_X[1] + 0.55, WORD_Y)))
            self.panel["stamp"] = stamp
            return anims + [appear(stamp, tm + 1.1, 0.4)]
        if p["phase"] == "shuffle":
            anims = self.light({}, run=0.3) + self.clear_lane("reads") + self.drop(self.panel.pop("rule_arrow", None)) \
                + self.drop(self.panel.pop("rule", None))
            anims += self.lane_head("count")
            orders = p["orders"]
            chips = {n: text(str(n), size=26, color=GOLD, weight=BOLD).move_to(xy(GRID_X[c], COUNT_Y))
                     for c, n in enumerate(orders[0])}
            self.overlay(*chips.values())
            self.panel["countchips"] = chips
            anims += [appear(VGroup(*chips.values()), 0.3, 0.4)]
            per = (avail - 1.2) / max(1, len(orders) - 1)
            for k, order in enumerate(orders[1:], 1):
                for c, n in enumerate(order):
                    anims.append(later(0.5 + per * (k - 0.5), chips[n].animate(run_time=min(0.5, per * 0.8), path_arc=0.8)
                                       .move_to(xy(GRID_X[c], COUNT_Y))))
            self.count_order = orders[-1]
            return anims
        # why: the full and empty columns give no row, so only two readings are left, and two always fit a word
        order = self.count_order
        anims = []
        for c, n in enumerate(order):
            # a full or empty column is a wildcard; the other two give a row each
            m = digit(None, 28, MUTED) if n in (0, 3) else text("row", size=18, color=GOLD)
            anims += self.put("reads", c, m, 0.3 + 0.2 * c)
        t = min(avail * 0.4, avail - 3.0)
        fit = self.overlay(text("two readings always fit a word", size=20, color=MUTED).move_to(xy(GRID_X[1] + 0.55, WORD_Y)))
        res = VGroup(text(f"{p['hands']} such hands", size=24),
                     text("the words pass all of them", size=20, color=MUTED),
                     text(f"hexads among them: {p['hexads']}", size=24, color=RED, weight=BOLD)).arrange(DOWN, buff=0.16)
        res.move_to(xy(3.95, 3.3))
        self.overlay(res)
        self.panel["why"] = VGroup(fit, res)
        return anims + [appear(fit, t, 0.4), appear(res[0], t + 0.9, 0.4), appear(res[1], t + 1.4, 0.4),
                        appear(res[2], min(t + 2.3, avail - 0.6), 0.4)]

    def hl_hand_in_grid(self, p, avail):
        counts, odds = self.code.reading()
        hand = sorted(self.code.marked)
        if p["phase"] == "cards":
            anims = []
            for key in ("why", "stamp", "colbox", "mismatch", "verdict"):
                anims += self.drop(self.panel.pop(key, None), 0.0, 0.3)
            anims += self.clear_lane("count") + self.clear_lane("reads") + self.clear_lane("word") + self.ensure_slots()
            anims += self.undim_table(0.3)
            # the cards light as they are named, then the counts appear
            per = min(0.45, (avail * 0.6) / len(hand))
            for k, v in enumerate(hand):
                anims += [later(0.5 + per * k, recolor(self.cards[v], LIT, 0.3))]
            for c in [c for c in self.lit if c not in [self.cards[v] for v in hand]]:
                anims.append(recolor(c, self.base.get(c), 0.3))
            self.lit = {self.cards[v]: LIT for v in hand}
            return anims + self.show_counts(counts, min(0.5 + per * len(hand), avail - 1.6), 0.3)
        # read: one column at a time, a reading drops into its slot
        per = min(0.55, (avail - 0.8) / 4)
        anims = []
        for c in range(4):
            col = VGroup(*(self.cards[self.bm.M[r][c]] for r in range(3)))
            anims.append(later(0.3 + per * c, Indicate(col, color=GOLD, scale_factor=1.04, run_time=min(0.5, per))))
        anims += self.show_readings(odds, 0.45, per)
        if p.get("passes"):
            # four wildcards fit every word: the whole table lights up
            words = list(self.table.values())
            t = min(0.45 + 4 * per + 0.3, avail - 1.2)
            verdict = self.overlay(text("fits every word: a hexad ✓", size=24, color=GREEN, weight=BOLD)
                                   .move_to(xy(GRID_X[1] + 0.55, WORD_Y)))
            self.panel["verdict"] = verdict
            anims += [later(t, LaggedStart(*(Indicate(w, color=GREEN, scale_factor=1.15) for w in words),
                                           lag_ratio=0.08, run_time=1.0)), appear(verdict, t + 0.6, 0.4)]
        return anims

    def undim_table(self, run):
        if self.table is None:
            return []
        anims = [opacity_to(w, 1.0, run) for w in self.table.values() if self.faint.get(w, 1.0) < 1]
        for w in self.table.values():
            self.faint.pop(w, None)
        return anims

    def hl_mismatch(self, p, avail):
        _, odds = self.code.reading()
        word = self.code.word
        if p.get("phase") == "only":
            # only one word to try: every other word fades
            w = tuple(word)
            anims = []
            for (a, b), m in self.table.items():
                if self.bm.tetra_word(a, b) != w:
                    anims.append(later(0.3, opacity_to(m, 0.25, 0.5)))
                    self.faint[m] = 0.25
            anims.append(later(0.6, Indicate(self.table[(w[1], w[0])], color=GOLD, scale_factor=1.3, run_time=0.8)))
            v = self.overlay(text("not a hexad", size=26, color=RED, weight=BOLD).move_to(VERDICT))
            self.panel["verdict"] = v
            return anims + [appear(v, min(avail - 1.0, 3.6), 0.4)]
        anims = []
        agree = [i for i, o in enumerate(odds) if o is not None and word[i] == o]
        off = self.bm.disagreements(word, odds)
        marks = VGroup()
        t3 = 0.3
        for i in agree:
            tick = text("✓", size=22, color=GREEN).move_to(xy(GRID_X[i] + 0.38, (READ_Y + WORD_Y) / 2))
            marks.add(tick)
            anims.append(appear(tick, t3 if i == 2 else 0.1, 0.3))
        tm = min(avail * 0.5, avail - 1.2)
        for i in off:
            for lane in ("reads", "word"):
                anims.append(later(tm, recolor_text(self.cols[(lane, i)], RED, 0.3)))
            cross = text("✗", size=26, color=RED, weight=BOLD).move_to(xy(GRID_X[i] + 0.4, (READ_Y + WORD_Y) / 2))
            marks.add(cross)
            anims.append(appear(cross, tm + 0.2, 0.3))
        self.overlay(marks)
        self.panel["mismatch"] = marks
        return anims

    def hl_fix_column(self, p, avail):
        c, out, inn = p["column"], p["out"], p["in"]
        col = VGroup(*(self.cards[self.bm.M[r][c]] for r in range(3)))
        box = SurroundingRectangle(col, color=GOLD, buff=0.1, corner_radius=0.1, stroke_width=3)
        self.panel["colbox"] = self.overlay(box)
        arrow = CurvedArrow(self.cards[out].get_right() + RIGHT * 0.08, self.cards[inn].get_right() + RIGHT * 0.08,
                            angle=-TAU / 4, color=GREEN, stroke_width=3, tip_length=0.15)
        self.panel["fix_arrow"] = self.overlay(arrow)
        t = min(avail * 0.55, avail - 1.0)
        return [appear(box, 0.4, 0.4), later(t - 0.5, Indicate(self.rownums[0], color=GOLD, scale_factor=1.5, run_time=0.6)),
                later(t, Create(arrow, run_time=0.6))]

    def hl_7_5(self, p, avail):
        out, inn = 7, 5
        chip_ = self.chips.get((out, inn))
        anims = []
        if chip_ is not None:
            anims.append(later(0.1, Indicate(chip_, color=GOLD, scale_factor=1.3, run_time=0.8)))
        anims += [later(0.5, recolor(self.cards[out], None, 0.4)), later(0.5, recolor(self.cards[inn], IN_COLOR, 0.4))]
        self.lit.pop(self.cards[out], None)
        self.lit[self.cards[inn]] = IN_COLOR
        counts, odds = self.code.reading()
        anims += self.clear_lane("word", 0.3) + self.drop(self.panel.pop("mismatch", None), 0.3)
        anims += self.show_counts(counts, 0.9, 0.12)
        anims += self.show_readings(odds, 1.1, 0.12)
        return anims

    def visual_write_along(self, arg, p, start, end, avail):
        """The words travel along a curve, letter by letter, to the odd man out (the Haynes technique)."""
        self.play_code("write_along", arg, p)
        target = self.cards[p["to"]]
        c = p["column"]
        top = self.cards[self.bm.M[0][c]]
        a = top.get_left() + LEFT * 0.12 + UP * 0.22
        b = target.get_left() + LEFT * 0.08
        path = ArcBetweenPoints(a, b, angle=1.5)        # bows out to the left, between the row numbers and the grid
        phrase = "odd man out"
        n = len(phrase)
        letters = VGroup()
        run = min(1.6, avail - 1.0)
        anims = []
        for k, ch in enumerate(phrase):
            if ch == " ":
                continue
            u = 0.06 + 0.84 * (k + 0.5) / n
            q = path.point_from_proportion(u)
            d = path.point_from_proportion(min(1, u + 0.01)) - path.point_from_proportion(max(0, u - 0.01))
            m = text(ch, size=19, color=GOLD, weight=BOLD).move_to(q).rotate(math.atan2(d[1], d[0]) + PI)
            letters.add(m)
            anims.append(appear(m, 0.15 + run * k / n, 0.25))
        ring = DashedVMobject(SurroundingRectangle(target, color=GOLD, buff=0.08, corner_radius=0.1, stroke_width=3), num_dashes=16)
        r = self.code.cell(p["to"])[0]
        note = text(f"row {r}: the odd man out", size=20, color=GOLD).move_to(xy(GRID_X[1] + 0.55, WORD_Y))
        self.overlay(letters, ring, note)
        self.panel["oddwords"], self.panel["oddring"], self.panel["oddnote"] = letters, ring, note
        return anims + [appear(ring, 0.3 + run, 0.4), appear(note, min(0.5 + run, avail - 0.5), 0.4)]

    def visual_clock_mod(self, arg, p, start, end, avail):
        self.play_code("clock_mod", arg, p)
        phase = p.get("phase")
        if phase == "sweep":
            h0, h1 = p["hours"]
            face = Circle(radius=CLOCK_R, stroke_color=CHALK, stroke_width=3).move_to(CLOCK_C)
            nums = VGroup(*(text(str(h), size=30, color=MUTED).move_to(clock_point(CLOCK_C, CLOCK_R + 0.32, h)) for h in range(3)))
            ticks = VGroup(*(Dot(clock_point(CLOCK_C, CLOCK_R, h), radius=0.06, color=CHALK) for h in range(3)))
            hand = self.clock_hand(h0)
            pin = Dot(CLOCK_C, radius=0.07, color=GOLD)
            self.clock = {"face": VGroup(face, ticks), "nums": nums, "hand": VGroup(hand, pin)}
            self.hour = h0
            per = (avail - 1.4) / (h1 - h0 + 1)
            anims = [appear(VGroup(face, ticks), 0.1, 0.5), appear(nums, 0.3, 0.5), appear(VGroup(hand, pin), 0.5, 0.3)]
            for k in range(h0, h1):
                anims += [later(0.9 + per * (k + 1) - 0.35, self.turn(k, k + 1, 0.35)),
                          later(0.9 + per * (k + 1) - 0.2, Indicate(nums[k + 1], color=GOLD, scale_factor=1.5, run_time=0.5))]
            anims.append(later(0.7, Indicate(nums[h0], color=GOLD, scale_factor=1.5, run_time=0.5)))
            self.hour = h1
            return anims
        if phase == "name":
            name = text("arithmetic mod 3", size=26, color=GOLD).move_to(CLOCK_C + xy(0, -CLOCK_R - 0.75))
            self.clock["name"] = name
            return [appear(name, min(1.2, avail * 0.3), 0.5)]
        if phase == "aside":
            # the clock shrinks to the corner, where it keeps counting for the codewords
            k = CLOCK_SMALL_R / CLOCK_R
            cur = self.clock.get("center", CLOCK_C)
            grp = VGroup(self.clock["face"], self.clock["nums"], self.clock["hand"])
            anims = [grp.animate(run_time=0.9).scale(k, about_point=cur).shift(CLOCK_SMALL_C - cur)]
            for m in [self.clock.pop("name", None)] + self.sums:
                if m is not None:
                    anims.append(FadeAway(m, run_time=0.4))
            self.sums = []
            self.clock["center"], self.clock["radius"] = CLOCK_SMALL_C, CLOCK_SMALL_R
            return anims
        a, b, c = p["shows"]
        anims = []
        t = 0.15
        if self.hour != a:
            # back to a: one quick step the other way round
            anims.append(later(0.1, self.turn(self.hour, self.hour - ((self.hour - a) % 3), 0.3)))
            t = 0.5
        per = max(0.3, min(0.55, (avail - t - 0.8) / b))
        for k in range(b):
            anims.append(later(t + per * k, self.turn(a + k, a + k + 1, min(0.3, per - 0.05))))
        land = min(t + per * b, avail - 0.5)
        anims.append(later(land, Indicate(self.clock["nums"][c], color=GOLD, scale_factor=1.6, run_time=0.45)))
        eq = text(f"{a} + {b} = {c}", size=34, color=GOLD, weight=BOLD)
        eq.move_to(xy(CLOCK_C[0] + CLOCK_R + 1.9, CLOCK_C[1] + 0.55 - 0.75 * len(self.sums)))
        self.sums.append(eq)
        self.hour = c
        return anims + [appear(eq, min(land, avail - 0.45), 0.4)]

    def clock_hand(self, hour):
        tip = clock_point(CLOCK_C, CLOCK_R - 0.22, hour)
        return Line(CLOCK_C, tip, stroke_color=GOLD, stroke_width=6).add_tip(tip_length=0.18)

    def turn(self, h0, h1, run):
        center = self.clock.get("center", CLOCK_C)
        return hand_turn(self.clock["hand"], h0, h1, run, center=center, hours=3)

    def visual_recap_montage(self, arg, p, start, end, avail):
        self.play_code("recap_montage", arg, p)
        phase = p.get("phase")
        if phase == "away":
            return self.drop(self.panel.pop("wrap", None), 0.0, 0.4)
        bm = self.bm
        v = bm.PROJECTIVE_VIEWS[p["picture"]]
        pos = lambda r, c: WRAP_C + xy((c - 1) * WRAP_CELL, (1 - r) * WRAP_CELL)
        if phase == "grid":
            out = [FadeAway(m, run_time=0.4) for m in self.sums]
            self.sums = []
            # the clock steps left (keeping its hand where it is) to make room
            grp = VGroup(self.clock["face"], self.clock["nums"], self.clock["hand"], self.clock["name"])
            out.append(grp.animate(run_time=0.8).shift(CLOCK_LEFT - CLOCK_C))
            self.clock["center"] = CLOCK_LEFT
            cards = {(r, c): label_card(plabel(v[3 * r + c]), 0.62).move_to(pos(r, c)) for r in range(3) for c in range(3)}
            cap = text("last time: the picture at ∞", size=18, color=MUTED).move_to(WRAP_C + xy(0.9, -1.4))
            d = tuple(p["direction"])
            cells = sorted((r, c) for r in range(3) for c in range(3) if (d[0] * r + d[1] * c) % 3 == p["k"])
            # walk the diagonal from its first cell: down a row, back a column, off the edge and in again
            walk = [((cells[0][0] + n) % 3, (cells[0][1] - n) % 3) for n in range(3)]
            assert sorted(walk) == cells
            pts = [pos(r, c) for r, c in walk]
            off = pos(walk[0][0] + 0.62, walk[0][1] - 0.62)
            back = pos(walk[1][0] - 0.62, walk[1][1] + 0.62)
            path = VGroup(Line(pts[0], off).add_tip(tip_length=0.12), Line(back, pts[1]), Line(pts[1], pts[2]))
            path.set_stroke(GOLD, 4)
            self.wrap = {"cards": cards, "walk": walk, "pos": pos}
            grp = VGroup(*cards.values(), cap, path)
            self.panel["wrap"] = self.overlay(grp)
            lit = [cards[rc] for rc in walk]
            t = min(1.4, avail * 0.3)
            return out + [appear(VGroup(*cards.values()), 0.3, 0.6), appear(cap, 0.5, 0.5),
                    later(t, Create(path, run_time=min(1.4, avail - t - 0.4)))] + \
                [later(t + 0.3 * k, recolor(m, GOLD, 0.3)) for k, m in enumerate(lit)]
        # sums: beside each row, the row plus the column of its diagonal card, on the clock
        w = self.wrap
        labels = VGroup()
        per = min(0.9, (avail - 1.4) / 3)
        anims = []
        for k, (r, c) in enumerate(w["walk"]):
            lab = text(f"row {r} + col {c} = {(r + c) % 3}", size=17, color=GOLD)
            lab.next_to(w["pos"](r, 2), RIGHT, buff=0.5)
            lab.set_z_index(FRONT + 0.2)
            labels.add(lab)
            anims.append(appear(lab, 0.5 + per * k, 0.35))
        self.panel["wrap"].add(labels)
        return anims

    def visual_assemble_codeword(self, arg, p, start, end, avail):
        self.play_code("assemble_codeword", arg, p)
        return getattr(self, "cw_" + arg)(p, avail)

    def cw_slots(self, p, avail):
        phase = p["phase"]
        if phase == "ab":
            cc, r = self.clock["center"], self.clock["radius"]
            chips = {k: chip(f"{k} = ?", color=GOLD, size=22).move_to(cc + xy(0, -0.95 - 0.55 * i))
                     for i, k in enumerate(("a", "b"))}
            self.ab = chips
            per = min(1.0, (avail - 1.0) / 2)
            return [appear(chips["a"], avail * 0.55, 0.4), appear(chips["b"], avail * 0.55 + per * 0.5, 0.4)]
        if phase == "slots":
            boxes, labs = VGroup(), VGroup()
            for i, lab in enumerate(self.code.SLOTS):
                x = SLOT_X0 + SLOT_DX * i
                boxes.add(RoundedRectangle(width=0.8, height=0.72, corner_radius=0.1, stroke_color=EDGE, stroke_width=2,
                                           fill_color=PANEL, fill_opacity=1).move_to(xy(x, SLOT_Y)))
                labs.add(text(lab.replace("+", " + "), size=20, color=MUTED).move_to(xy(x, SLOT_Y + 0.62)))
            self.boxes = VGroup(boxes, labs)
            # each box appears as its name is said
            per = (avail - 2.6) / 4
            anims = []
            for i in range(4):
                t = 0.9 + per * i
                anims += [appear(boxes[i], t, 0.3), appear(labs[i], t, 0.3)]
            return anims
        # name: a codeword, and its four coordinates
        boxes, labs = self.boxes
        name = text("a codeword: four coordinates", size=22, color=GOLD).move_to(xy(SLOT_X0 + 1.5 * SLOT_DX, SLOT_Y - 1.0))
        idx = VGroup(*(text(f"coordinate {i + 1}" if i == 0 else str(i + 1), size=16, color=MUTED)
                       .move_to(boxes[i].get_bottom() + DOWN * 0.2) for i in range(4)))
        self.boxes_name = VGroup(name, idx)
        t = min(avail * 0.5, avail - 1.4)
        return [appear(name, 0.3, 0.4), later(t, LaggedStart(*(FadeIn(m) for m in idx), lag_ratio=0.25, run_time=0.8))]

    def cw_a1_b1(self, p, avail):
        a, b = p["a"], p["b"]
        if p["phase"] == "set":
            anims = []
            for k, val in (("a", a), ("b", b)):
                old = self.ab[k]
                new = chip(f"{k} = {val}", color=BG, fill=GOLD, stroke=GOLD, size=22).move_to(old)
                anims.append(later(1.0 if k == "a" else 2.0, Transform(old, new, run_time=0.4)))
            if self.hour != a:
                anims.append(later(1.0, self.turn(self.hour, self.hour + ((a - self.hour) % 3), 0.4)))
                self.hour = a
            return anims
        # fill: b, a, a + b, then a + 2b counted round the clock from a
        word = self.bm.tetra_word(a, b)
        boxes, labs = self.boxes
        per = (avail - 1.0) / 5.2
        anims = []
        for i in range(4):
            t = 0.25 + per * (i if i < 3 else 3.2)
            m = digit(word[i], 34, GOLD).move_to(boxes[i])
            m.set_z_index(FRONT + 0.1)
            self.box_vals[i] = m
            anims += [appear(m, t + (per * 1.2 if i == 3 else 0), 0.35), later(t, Indicate(labs[i], color=GOLD, run_time=0.5))]
        # the last box: from a, two more hours round the clock
        t = 0.25 + per * 3.2
        h = self.hour
        for k in range(2 * b):
            anims.append(later(t + 0.35 * k, self.turn(h + k, h + k + 1, 0.28)))
        self.hour = (h + 2 * b) % 3
        anims.append(later(t + 0.35 * 2 * b, Indicate(self.clock["nums"][self.hour], color=GOLD, scale_factor=1.6, run_time=0.5)))
        return anims

    def cw_all(self, p, avail):
        """The word slides into its place in a table of all nine; the other eight fill in."""
        a0, b0 = self.code.ab
        anims = []
        self.table = {}
        heads = VGroup()
        for b in range(3):
            heads.add(text(f"b = {b}", size=18, color=MUTED).move_to(xy(TABLE_X[b], TABLE_Y[0] + 0.52)))
        for a in range(3):
            heads.add(text(f"a = {a}", size=18, color=MUTED).move_to(xy(TABLE_X[0] - 1.3, TABLE_Y[a])))
        for a in range(3):
            for b in range(3):
                w = self.bm.tetra_word(a, b)
                g = VGroup(*(digit(x, 26, INK) for x in w)).arrange(RIGHT, buff=0.16).move_to(xy(TABLE_X[b], TABLE_Y[a]))
                back = RoundedRectangle(width=g.width + 0.34, height=0.5, corner_radius=0.08, stroke_color=EDGE,
                                        stroke_width=1.2, fill_color=PANEL, fill_opacity=1).move_to(g)
                g.set_z_index(FRONT + 0.1)
                heads.add(back)
                self.table[(a, b)] = g
        cap = text("the tetracode: 9 codewords", size=22, color=GOLD).move_to(xy((TABLE_X[0] + TABLE_X[2]) / 2, TABLE_Y[2] - 0.62))
        self.table_group = VGroup(heads, *self.table.values(), cap)
        boxes, labs = self.boxes
        # the built word becomes its table entry
        kept = self.table[(a0, b0)]
        ghost = VGroup(*(self.box_vals[i] for i in range(4)))
        anims.append(Transform(ghost, kept.copy(), run_time=0.9, path_arc=-0.4))
        anims.append(later(0.9, FadeAway(ghost, run_time=0.01)))
        anims.append(appear(kept, 0.9, 0.01))
        anims.append(FadeAway(VGroup(boxes, labs, self.boxes_name), run_time=0.6))
        others = [self.table[k] for k in sorted(self.table) if k != (a0, b0)]
        anims.append(appear(heads, 0.6, 0.5))
        anims.append(later(1.0, LaggedStart(*(FadeIn(m, shift=DOWN * 0.1) for m in others), lag_ratio=0.12,
                                            run_time=min(2.2, avail - 1.6))))
        anims.append(appear(cap, min(3.4, avail - 0.5), 0.4))
        # the a and b chips and the clock go: the table names a and b now
        for k in ("a", "b"):
            anims.append(FadeAway(self.ab.pop(k), run_time=0.5))
        if self.clock is not None:
            anims.append(FadeAway(VGroup(self.clock["face"], self.clock["nums"], self.clock["hand"]), run_time=0.5))
            self.clock, self.hour = None, None
        self.boxes, self.box_vals = None, {}
        return anims

    def cw_forced(self, p, avail):
        """The first two readings drop into the word row; the word they force fills in from the table."""
        word = self.code.word
        pair = p["from"]
        if p.get("phase") == "quick":
            _, odds = self.code.reading()
            anims = self.show_counts(self.code.reading()[0], 0.3, 0.05) + self.show_readings(odds, 0.4, 0.05)
            return anims + self.show_word(word, 0.8, 0.05)
        anims = [later(0.2, Indicate(self.cols[("reads", c)], color=GOLD, scale_factor=1.4, run_time=0.6)) for c in pair]
        anims += self.show_word(word, 0.8, 0.3, from_reads=pair)
        rest = [c for c in range(4) if c not in pair]
        t = min(avail * 0.62, avail - 1.2)
        anims.append(later(t - 0.4, Indicate(self.table[(word[1], word[0])], color=GOLD, scale_factor=1.25, run_time=0.8)))
        for c in rest:
            m = self.cols[("word", c)]
            m.set_opacity(0)
            anims.append(later(t + 0.3 * rest.index(c), opacity_to(m, 1.0, 0.3)))
        return anims

    def cw_fits(self, p, avail):
        word = self.code.word
        _, odds = self.code.reading()
        anims = self.show_word(word, 0.3, 0.25, color=GREEN)
        marks = VGroup(*(text("✓", size=22, color=GREEN).move_to(xy(GRID_X[i] + 0.38, (READ_Y + WORD_Y) / 2))
                         for i, o in enumerate(odds) if o is not None))
        self.overlay(marks)
        self.panel["mismatch"] = marks
        verdict = self.overlay(text("a hexad ✓", size=26, color=GREEN, weight=BOLD).move_to(VERDICT))
        self.panel["verdict"] = verdict
        return anims + [appear(marks, 1.5, 0.4), appear(verdict, min(2.2, avail - 0.6), 0.4)]

    def visual_card_exchange(self, arg, p, start, end, avail):
        before = sorted(self.code.marked)
        self.play_code("card_exchange", arg, p)
        if arg == "back":
            anims = []
            for key in list(self.panel):
                anims += self.drop(self.panel.pop(key), 0.0, 0.3)
            if self.table_group is not None:
                anims.append(FadeAway(self.table_group, run_time=0.5))
                self.table_group, self.table = None, None
            anims += self.clear_lane("count") + self.clear_lane("reads") + self.clear_lane("word") + self.ensure_slots()
            anims += self.mark_hand(sorted(self.code.marked), run=0.5)
            return anims
        if arg == "repairs":
            return self.repairs(p, avail)
        out, inn = parse_move(arg)
        counts, odds = self.code.reading()
        anims = [later(0.3, recolor(self.cards[out], None, 0.4)), later(0.45, recolor(self.cards[inn], IN_COLOR, 0.4))]
        self.lit.pop(self.cards[out], None)
        self.lit[self.cards[inn]] = IN_COLOR
        anims += self.drop(self.panel.pop("fix_arrow", None), 0.9) + self.drop(self.panel.pop("colbox", None), 0.9)
        c = self.code.cell(inn)[1]
        anims += self.put("reads", c, digit(odds[c], 28, GREEN), 1.0)
        tick = self.overlay(text("✓", size=22, color=GREEN).move_to(xy(GRID_X[c] + 0.38, (READ_Y + WORD_Y) / 2)))
        verdict = self.overlay(text("a hexad ✓", size=26, color=GREEN, weight=BOLD).move_to(VERDICT))
        self.panel["verdict"], self.panel["tick"] = verdict, tick
        word_m = self.cols.get(("word", c))
        if word_m is not None:
            anims.append(later(1.0, recolor_text(word_m, GREEN, 0.3)))
        return anims + [appear(tick, 1.3, 0.3), appear(verdict, min(2.6, avail - 0.6), 0.4)]

    def repairs(self, p, avail):
        """The six repairs of the opening hand, as chips: card out → card in, and the new total."""
        phase = p["phase"]
        h = frozenset(self.code.marked)
        reps = self.bm.repairs(h)
        if phase == "all":
            head = text(f"{len(self.bm.all_swaps(h))} swaps, {len(reps)} repairs", size=26, color=GOLD).move_to(xy(3.55, 3.5))
            self.overlay(head)
            self.panel["rep_head"] = head
            anims = [appear(head, 0.3, 0.4)]
            per = (avail - 1.6) / len(reps)
            for k, m in enumerate(reps):
                up = m[1] > m[0]
                col, row = (0, [x for x in reps if x[1] > x[0]].index(m)) if up else (1, [x for x in reps if x[1] < x[0]].index(m))
                ch = chip(f"{move_label(*m)}   {sum(self.bm.swap(h, m))}", size=24).move_to(xy(1.95 + 3.2 * col, 2.45 - 0.68 * row))
                self.chips[m] = self.overlay(ch)
                t = 0.8 + per * k
                anims += [appear(ch, t, 0.3),
                          later(t, Indicate(self.cards[m[0]], color=RED, scale_factor=1.15, run_time=0.45)),
                          later(t + 0.15, Indicate(self.cards[m[1]], color=GREEN, scale_factor=1.15, run_time=0.45))]
            return anims
        up = phase == "up"
        mine = [m for m in reps if (m[1] > m[0]) == up]
        color = BLUE if up else GREEN
        lab = text("up: not a move" if up else "down: legal moves", size=22, color=color).move_to(xy(1.95 + 3.2 * (0 if up else 1), 3.0))
        self.overlay(lab)
        self.panel["lab_" + phase] = lab
        per = (avail - 1.4) / 3
        anims = [appear(lab, 0.2, 0.4)]
        for k, m in enumerate(mine):
            ch = self.chips[m]
            anims.append(later(0.7 + per * k, recolor(ch, color, 0.35)))
        return anims

    def visual_reveal_count(self, arg, p, start, end, avail):
        self.play_code("reveal_count", arg, p)
        if arg == "pairs_6":
            from itertools import combinations
            pairs = list(combinations(range(4), 2))
            chips_ = VGroup(*(chip(f"{i + 1} & {j + 1}  ✓", size=20, color=GREEN) for i, j in pairs)).arrange(RIGHT, buff=0.14)
            chips_.move_to(xy(3.85, 3.5))
            if chips_.width > 6.0:
                chips_.scale_to_fit_width(6.0)
            cap = text("each pair of places: 9 words, 9 different pairs", size=18, color=MUTED).next_to(chips_, DOWN, buff=0.14)
            self.overlay(chips_, cap)
            per = (avail - 1.6) / 6
            return [appear(c, 0.4 + per * k, 0.3) for k, c in enumerate(chips_)] + [appear(cap, min(avail - 0.8, 1.0), 0.4)] \
                + self.undim_table(0.5) + self.drop(self.panel.pop("covers", None), 0.2, 0.5)
        if arg == "all_hands":
            g = VGroup(text("the paper tests all 924 hands", size=24), text("passing: exactly the 132 hexads ✓", size=24, color=GREEN))
            g.arrange(DOWN, buff=0.16).move_to(xy(3.45, 3.05))
            self.overlay(g)
            t = min(avail * 0.35, avail - 2.0)
            return [appear(g[0], t, 0.4), appear(g[1], t + 1.0, 0.4)]
        if arg == "three_of_fourteen":
            g = text(f"{p['legal_repairs']} of {p['legal_moves']} legal moves are repairs", size=24, color=MUTED).move_to(xy(3.55, 0.35))
            self.overlay(g)
            return [appear(g, min(1.2, avail * 0.4), 0.4)]
        raise NotImplementedError(f"reveal_count:{arg}")


def recolor_text(m, color, run):
    """Turn a reading or count (a Text) to color, from whatever it is when the animation begins."""
    start = {}

    def f(mob, a):
        if not start:
            start["c"] = mob.get_fill_color()
        mob.set_fill(interpolate_color(start["c"], ManimColor(color), a))
    return UpdateFromAlphaFunc(m, f, run_time=run)


class Episode1(TableVisuals, EpisodeScene):
    pass


class Episode2(BoardVisuals, EpisodeScene):
    pass


class Episode3(CodeVisuals, EpisodeScene):
    pass
