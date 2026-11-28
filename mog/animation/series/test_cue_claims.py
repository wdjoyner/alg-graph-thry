"""Plant wrong claims in Episode 3's cues and make sure the checker catches each one.

    python test_cue_claims.py            # every planted error must be caught
    python test_cue_claims.py --build    # also run check_outline.py on a copy with one planted error

Each case changes one claim in a copy of ep3/cues.json (or one value in a copy
of math_objects.json) and plays the episode through cue_tools.simulate, the
same code check_outline.py runs.  The unchanged cues must give no errors; every
changed one must give at least one.  --build copies the series folder, plants
one wrong claim and checks that check_outline.py exits with status 1.
"""
import copy
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from cue_tools import simulate, visual_name

HERE = Path(__file__).resolve().parent


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


# (beat, visual name, phase or None, key, wrong value)
CUE_CASES = [
    ("s01.b01", "fly_to_minimog", "fly", "rows", [[6, 3, 0, 9], [5, 2, 7, 10], [4, 1, 11, 8]]),
    ("s02.b01", "clock_mod:3", "add", "shows", [2, 2, 0]),
    ("s02.b02", "recap_montage:kitten_wrap", "sums", "row_plus_column", [0, 0, 1]),
    ("s02.b02", "recap_montage:kitten_wrap", "grid", "cell_points", [6, 4, 8]),
    ("s03.b01", "assemble_codeword:slots", "slots", "slots", ["a", "b", "a+b", "a+2b"]),
    ("s03.b02", "assemble_codeword:a1_b1", "fill", "word", [1, 1, 2, 1]),
    ("s03.b02", "assemble_codeword:a1_b1", "fill", "last_before_wrap", 2),
    ("s03.b03", "assemble_codeword:all", None, "size", 8),
    ("s03.b04", "highlight:two_coordinates", "filter", "words", [[1, 1, 2, 0], [1, 1, 0, 2]]),
    ("s03.b04", "reveal_count:pairs_6", None, "distinct", [9, 9, 9, 9, 9, 8]),
    ("s04.b01", "highlight:column_one", None, "reading", 2),
    ("s04.b02", "highlight:column_two", None, "reading", 0),
    ("s04.b02", "write_along:odd_man_out", None, "to", 6),
    ("s04.b03", "highlight:column_wild", "full", "reading", 1),
    ("s04.b05", "highlight:column_counts", "shuffle", "orders", [[0, 1, 2, 3], [2, 2, 3, 1]]),
    ("s04.b05", "highlight:column_counts", "why", "hexads", 1),
    ("s04.b05", "highlight:column_counts", "why", "hands", 215),
    ("s05.b01", "highlight:hand_in_grid", "cards", "counts", [2, 1, 1, 2]),
    ("s05.b01", "highlight:hand_in_grid", "read", "readings", [1, 1, 2, 0]),
    ("s05.b01", "highlight:hand_in_grid", "cards", "hexad", True),
    ("s05.b02", "assemble_codeword:forced", None, "word", [1, 1, 0, 2]),
    ("s05.b02", "highlight:mismatch", None, "at", [2]),
    ("s05.b02", "highlight:mismatch", None, "word_rows", [1]),
    ("s05.b03", "highlight:hand_in_grid", "cards", "counts", [3, 3, 0, 1]),
    ("s05.b03", "highlight:hand_in_grid", "read", "passes", False),
    ("s05.b04", "highlight:hand_in_grid", "cards", "counts", [3, 1, 0, 2]),
    ("s05.b04", "highlight:column_counts", None, "forbidden", False),
    ("s05.b04", "highlight:column_counts", None, "words", []),
    ("s06.b01", "highlight:fix_column", None, "out", 7),
    ("s06.b01", "highlight:fix_column", None, "in", 10),
    ("s06.b01", "card_exchange:11_9", None, "hexad", False),
    ("s06.b01", "card_exchange:11_9", None, "readings", [1, 1, 2, 2]),
    ("s06.b02", "card_exchange:repairs", "all", "swaps", 35),
    ("s06.b02", "card_exchange:repairs", "all", "repairs", [[0, 1], [2, 10], [4, 3], [6, 8], [7, 5], [10, 9]]),
    ("s06.b02", "card_exchange:repairs", "up", "totals", [31, 38, 33]),
    ("s06.b02", "card_exchange:repairs", "down", "repairs", [[4, 3], [7, 5]]),
    ("s06.b03", "highlight:7_5", None, "readings", [None, 1, 2, 2]),
    ("s06.b03", "assemble_codeword:fits", None, "word", [2, 1, 0, 1]),
    ("s06.b03", "reveal_count:three_of_fourteen", None, "legal_moves", 13),
]

# (object, dotted path, wrong value): a stale or hand-edited math_objects.json
OBJECT_CASES = [
    ("minimog", "rows.0.0", 3),
    ("tetracode", "word_a1_b1", [1, 1, 2, 1]),
    ("hand:example", "odd_man_out", [1, 1, 2, 0]),
    ("test:example", "forced_word", [1, 1, 0, 2]),
    ("moves:example_to_hexads", "down", [[4, 3], [7, 5]]),
    ("count:forbidden", "hexads", 3),
]


def find(cues, beat, name, phase):
    for s in cues["beats"][beat]:
        for v in list(s.get("do", [])) + list(s.get("with", [])):
            if isinstance(v, dict) and visual_name(v) == name and (phase is None or v.get("phase") == phase):
                return v
    raise KeyError((beat, name, phase))


def set_path(obj, path, value):
    keys = path.split(".")
    for k in keys[:-1]:
        obj = obj[int(k)] if isinstance(obj, list) else obj[k]
    last = keys[-1]
    if isinstance(obj, list):
        obj[int(last)] = value
    else:
        obj[last] = value


def run(cues, objects):
    outline = load("ep3/outline.json")
    cast = load("cast.json")["characters"]
    reactions = {k for k in cues.get("reactions", {}) if not k.startswith("_")}
    return simulate(outline, cues, objects, cast, reactions)


def main():
    cues = load("ep3/cues.json")
    objects = load("math_objects.json")["objects"]
    base = run(cues, objects)
    if base:
        sys.exit("the unchanged cues give errors:\n  " + "\n  ".join(base))
    missed = []
    for beat, name, phase, key, wrong in CUE_CASES:
        c = copy.deepcopy(cues)
        v = find(c, beat, name, phase)
        assert key in v, (beat, name, key)
        v[key] = wrong
        errs = run(c, objects)
        print(f"{'caught' if errs else 'MISSED'}  cue {beat} {name}{'/' + phase if phase else ''} {key}={wrong!r}"
              + (f"\n          {errs[0]}" if errs else ""))
        if not errs:
            missed.append((beat, name, key))
    for ref, path, wrong in OBJECT_CASES:
        o = copy.deepcopy(objects)
        set_path(o[ref], path, wrong)
        errs = run(cues, o)
        print(f"{'caught' if errs else 'MISSED'}  math_objects.json {ref}.{path}={wrong!r}"
              + (f"\n          {errs[0]}" if errs else ""))
        if not errs:
            missed.append((ref, path))
    if "--build" in sys.argv:
        with tempfile.TemporaryDirectory() as tmp:
            dst = Path(tmp) / "animation" / "series"
            shutil.copytree(HERE, dst, ignore=shutil.ignore_patterns("__pycache__"))
            c = copy.deepcopy(cues)
            find(c, "s05.b02", "assemble_codeword:forced", None)["word"] = [1, 1, 0, 2]
            (dst / "ep3" / "cues.json").write_text(json.dumps(c, indent=1))
            r = subprocess.run([sys.executable, "check_outline.py"], cwd=dst, capture_output=True, text=True)
            caught = r.returncode == 1 and "assemble_codeword:forced" in r.stdout
            print(f"{'caught' if caught else 'MISSED'}  check_outline.py on a copy with a wrong forced word: exit {r.returncode}")
            if not caught:
                missed.append("check_outline.py")
    n = len(CUE_CASES) + len(OBJECT_CASES) + ("--build" in sys.argv)
    print(f"{n - len(missed)} of {n} planted errors caught")
    return 1 if missed else 0


if __name__ == "__main__":
    sys.exit(main())
