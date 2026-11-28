"""Find PAM (github.com/wdjoyner/pam) for the series' scenes.

Set PAM_DIR to your PAM checkout if 'import pam' does not find it; a few
usual places beside this repository are tried as well.  PAM must include
pam/cat.py (CatGraph).
"""
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _import_pam():
    for d in [os.environ.get("PAM_DIR")] + [str(p) for p in (
            HERE.parents[3] / "pam", HERE.parents[4] / "pam", Path.home() / "pam",
            Path.home() / "Projects" / "pam")]:
        if d and Path(d, "pam", "cat.py").exists() and d not in sys.path:
            sys.path.insert(0, d)
            break
    try:
        from pam.cat import CatGraph
        from pam.poses import CAT_POSES, _flip_dog_pose
    except ImportError as e:
        raise SystemExit("PAM with pam/cat.py was not found: set PAM_DIR to your PAM checkout "
                         f"(github.com/wdjoyner/pam). ({e})")
    return CatGraph, CAT_POSES, _flip_dog_pose


CatGraph, CAT_POSES, flip_pose = _import_pam()
