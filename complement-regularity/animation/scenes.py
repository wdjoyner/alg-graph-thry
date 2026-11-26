"""Manim CLI entry points."""
from algebra import Classification, CubeStorage, SharpTransitivity
from factorization import ThreeFactors
from graph_scenes import CayleyGraphs, ForgettingOrder

# Manim discovers Scene classes defined in the CLI module.
for scene_class in (
    CubeStorage, SharpTransitivity, Classification, ThreeFactors, CayleyGraphs,
    ForgettingOrder,
):
    scene_class.__module__ = __name__
del scene_class
