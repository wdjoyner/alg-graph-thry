"""Manim entry points. The implementations live in geometry and game."""
import geometry
import game
from credits_timing import CREDITS_SECONDS
from manim import FadeIn, Scene, VGroup
from visual import BG, BLUE, GOLD, MUTED, label


class FanoSteiner(geometry.FanoSteiner):
    pass


class ProjectiveLine(geometry.ProjectiveLine):
    pass


class CurtisKitten(geometry.CurtisKitten):
    pass


class ConwayMINIMOG(game.ConwayMINIMOG):
    pass


class JohnsonGraph(game.JohnsonGraph):
    pass


class Blackjack(game.Blackjack):
    pass


class EndCredits(Scene):
    def construct(self):
        self.camera.background_color = BG
        card = VGroup(
            label("Based on David Joyner’s Draft 3", y=2.82, size=40, color=GOLD),
            label("Video authors", y=1.84, size=24, color=MUTED),
            label("David Joyner and ChatGPT", y=1.30, size=38),
            label("github.com/wdjoyner  •  chatgpt.com  •  github.com/openai", y=.73, size=26, color=BLUE),
            label("Animation package", y=-.04, size=24, color=MUTED),
            label("Manim Community Edition", y=-.54, size=34),
            label("github.com/ManimCommunity/manim", y=-1.05, size=26, color=BLUE),
            label("Mathematics", y=-1.82, size=24, color=MUTED),
            label("MINIMOGs and Mathematical Blackjack", y=-2.32, size=34),
            label("github.com/wdjoyner/alg-graph-thry/tree/main/mog",
                  y=-2.89, size=26, color=BLUE),
        )
        self.play(FadeIn(card), run_time=.8)
        self.wait(CREDITS_SECONDS - .8)
