"""Read an episode's cues.json and play its card game through, checking it.

cues.json says what happens on screen in each beat, step by step.  This
module is shared by check_outline.py, make_timing.py and the renderer:

  * steps(cues, beat)  - the beat's steps, normalized;
  * Table              - the cards on the table, changed cue by cue, with
                         every exchange checked against the rules;
  * montage_games()    - the games a recap_montage plays out, from the
                         game engine (Pascal keeps the total high; Ada
                         always replies into a hexad);
  * simulate(...)      - plays every cue of the episode through a Table and
                         returns the errors found.

Step forms (see the _about block of epN/cues.json):
  {"line": id, "with": [visual, ...]}      a dialogue line; visuals start with it
  {"do": [visual, ...], "seconds": s}      visuals with the stage to themselves
  {"pause": "predict", "seconds": s, "prompt": text}   a pause for the viewer
  {"hold": s}                              nothing new for s seconds
A visual is "verb:argument" or {"visual": "verb:argument", ...parameters}.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def visual_name(v):
    return v if isinstance(v, str) else v["visual"]


def visual_params(v):
    return {} if isinstance(v, str) else {k: x for k, x in v.items() if k != "visual"}


def split_visual(v):
    name = visual_name(v)
    verb, _, arg = name.partition(":")
    return verb, arg


def steps(cues, beat_id):
    out = []
    for s in cues["beats"].get(beat_id, []):
        s = dict(s)
        if "do" in s and not isinstance(s["do"], list):
            s["do"] = [s["do"]]
        s.setdefault("with", [])
        out.append(s)
    return out


def step_visuals(step):
    return list(step.get("do", [])) + list(step.get("with", []))


# ------------------------------------------------------------------ the game

def legal(hand, out, inn):
    """A legal move: out is in the hand, inn in the pile, inn < out, total stays >= 21."""
    return out in hand and inn not in hand and 0 <= inn < out <= 11 \
        and sum(hand) - out + inn >= 21


def down_moves(hand):
    pile = sorted(set(range(12)) - set(hand))
    return [(a, b) for a in sorted(hand) for b in pile if legal(hand, a, b)]


def montage_games(hand, openings):
    """Play each opening (Pascal's move, Ada's reply) to the end.

    After the opening, Pascal plays the legal move that keeps the total
    highest (ties: the larger card out), and Ada answers with a move into a
    hexad, the highest total she can (ties: the smaller card out).  Returns,
    for each game, the list of (player, (out, in), total) after the opening,
    ending with ("pascal", None, total) when Pascal is stuck.
    """
    from build_math_objects import HEXADS
    games = []
    for first, reply in openings:
        h = set(hand)
        for a, b in (first, reply):
            assert legal(h, a, b), (h, a, b)
            h = (h - {a}) | {b}
        seq = []
        while True:
            moves = down_moves(h)
            if not moves:
                seq.append(("pascal", None, sum(h)))
                break
            a, b = max(moves, key=lambda m: (sum(h) - m[0] + m[1], m[0]))
            h = (h - {a}) | {b}
            seq.append(("pascal", (a, b), sum(h)))
            replies = [m for m in down_moves(h) if frozenset((h - {m[0]}) | {m[1]}) in HEXADS]
            if not replies:
                raise AssertionError(f"Ada has no reply into a hexad from {sorted(h)}")
            a, b = max(replies, key=lambda m: (sum(h) - m[0] + m[1], -m[0]))
            h = (h - {a}) | {b}
            seq.append(("ada", (a, b), sum(h)))
        games.append(seq)
    return games


class Table:
    """The cards on the table: a hand in six slots and a pile in six slots.

    An exchange puts the incoming card in the outgoing card's slot, and the
    outgoing card in the incoming card's pile slot, so the two cards simply
    trade places on screen.
    """

    def __init__(self):
        self.hand, self.pile = [], []
        self.pending = None          # a tried-and-rejected or demo exchange to undo

    @property
    def total(self):
        return sum(self.hand)

    def deal(self, cards):
        cards = list(cards)
        self.hand = cards
        self.pile = sorted(set(range(12)) - set(cards))
        self.pending = None

    def exchange(self, out, inn, check=True):
        if check and not legal(self.hand, out, inn):
            raise ValueError(f"illegal move {out} for {inn} from {sorted(self.hand)} (total {self.total})")
        i, j = self.hand.index(out), self.pile.index(inn)
        self.hand[i], self.pile[j] = inn, out
        return i, j

    def flip(self):
        self.hand, self.pile = self.pile, self.hand


def parse_move(arg):
    """'7_5' -> (7, 5); '11_1_rejected' -> (11, 1)."""
    a, b = arg.split("_")[:2]
    return int(a), int(b)


def deal_cards(arg, objects):
    key = {"hand_and_pile": "hand:example", "1to6": "hand:1to6", "hexad_24": "hand:hexad_24",
           "complement_1to6": "hand:complement_1to6"}.get(arg)
    return None if key is None else objects[key]["cards"]


# ------------------------------------------------------------------ the board

class Board:
    """The diagram Sophie and Euler draw (Episode 2), changed cue by cue.

    It plays the board's visual verbs the way Table plays the card game:
    every set, completion, count and relabeling a cue shows is recomputed
    here from build_math_objects.py's definitions and compared with
    math_objects.json and with the claims written in the cue.  The renderer
    draws what this class computes, so the picture cannot disagree with the
    checker.

    layout: None, "line_up", "fano", "ring_blank", "ring", "triangle", "views"
    labels: "projective" (11 = infinity) or "card", for the kitten's views
    marked: the points marked on the ring
    """

    LAYOUTS = {"to_fano": (None, "line_up", "fano"), "to_ring": ("ring_blank",),
               "to_triangle": ("ring",), "triangle_to_views": ("triangle",),
               "projective_to_shuffle": ("views",)}

    def __init__(self, objects):
        import build_math_objects as bm
        self.bm, self.obj = bm, objects
        self.layout, self.labels, self.marked = None, "projective", frozenset()
        self.lit = frozenset()          # the hexad lit in the views, if any

    # -- geometry the renderer also uses

    def views(self):
        """[(corner, nine labels)], in display order, in the current labels."""
        bm = self.bm
        order = (bm.INF, 0, 1)
        if self.labels == "card":
            return [(bm.RHO[d], bm.VIEWS[bm.RHO[d]]) for d in order]
        return [(d, bm.PROJECTIVE_VIEWS[d]) for d in order]

    def view_dict(self):
        return dict(self.views())

    def parts_points(self, picture, parts):
        v = self.view_dict()[picture]
        return frozenset().union(*(self.bm.view_line(v, tuple(d), k) for d, k in parts))

    def family_example(self, name):
        return self.obj["kitten:projective"]["family_examples"][name]

    def hand_parts(self, key):
        """(family, picture, parts) of an Episode 1 hand in the card-labeled kitten."""
        return self.bm.decompose(frozenset(self.obj[key]["cards"]), self.bm.VIEWS)

    # -- the verbs; each returns a list of error strings

    def _need(self, *layouts):
        return [] if self.layout in layouts else [f"needs the {' or '.join(map(str, layouts))} on the board, has {self.layout}"]

    def _claim(self, p, key, got):
        if key in p and p[key] != got:
            return [f"{key} is {got!r}, cue says {p[key]!r}"]
        return []

    def play(self, verb, arg, p):
        fn = getattr(self, f"v_{verb}", None)
        return fn(arg, p) if fn else []

    def v_recap_montage(self, arg, p):
        if arg != "ep1_line_up":
            return []
        errs = [f"{k} is not a losing hand" for k in p.get("hands", []) if not self.obj[k]["losing"]]
        if p.get("question") not in p.get("hands", []):
            errs.append("the question mark must sit on one of the hands")
        self.layout = "line_up"
        return errs

    def v_morph_layout(self, arg, p):
        if arg not in self.LAYOUTS:
            return [f"unknown layout change {arg}"]
        errs = self._need(*self.LAYOUTS[arg])
        bm = self.bm
        if arg == "to_fano":
            f = self.obj["fano"]
            if not (f["straight_lines_collinear"] and f["circle_concyclic"]):
                errs.append("the Fano figure's positions do not match its lines")
            self.layout = "fano"
        elif arg == "to_ring":
            self.layout, self.marked = "ring", frozenset()
        elif arg == "to_triangle":
            k = self.obj["kitten:projective"]
            labels = {s[2] for s in k["spots"]}
            if labels != set(range(12)):
                errs.append("the triangle does not show all twelve points")
            if [s[2] for s in k["spots"] if (s[0], s[1]) in ((0, 6), (-5, 0), (5, 0))] != [bm.INF, 0, 1]:
                errs.append("the triangle's corners are not infinity, 0, 1")
            self.layout, self.marked = "triangle", frozenset()
        elif arg == "triangle_to_views":
            for d, v in self.views():
                if set(v) != set(range(12)) - set(bm.PROJECTIVE_VIEWS):
                    errs.append(f"the view at {d} is not the other nine points")
            self.layout = "views"
        elif arg == "projective_to_shuffle":
            if self.labels != "projective":
                errs.append("the views are already in card labels")
            if not self.obj["shuffle:rho"]["views_match"]:
                errs.append("relabeling the projective views does not give the card views")
            if {frozenset(bm.RHO[x] for x in h) for h in bm.ORBIT} != bm.HEXADS:
                errs.append("the relabeled orbit is not the card hexads")
            self.labels = "card"
        return errs

    def v_summon_completion(self, arg, p):
        bm = self.bm
        pts = p.get("points", [])
        if arg.startswith("fano_"):
            errs = self._need("fano")
            if len(pts) != 2:
                return errs + ["a Fano completion needs two points"]
            got = [bm.fano_completion(*pts)]
            want = self.obj["fano"]["completions"].get(",".join(map(str, pts)))
            if want is not None and [want] != got:
                errs.append(f"math_objects.json completes {pts} with {want}, the lines give {got}")
            if f"fano_{pts[0]}_{pts[1]}" != arg:
                errs.append(f"argument {arg} does not name the points {pts}")
            return errs + self._claim(p, "completes", got)
        if arg == "ring_five":
            errs = self._need("ring")
            if len(pts) != 5:
                return errs + ["a five-point completion needs five points"]
            got = [bm.five_completion(pts, bm.ORBIT)]
            ex = self.obj["ring:projective"]["five_example"]
            if ex["points"] == pts and [ex["completion"]] != got:
                errs.append("math_objects.json disagrees with the orbit")
            self.marked = frozenset(pts) | set(got) if p.get("phase") == "complete" else frozenset(pts)
            return errs + self._claim(p, "completes", got)
        return [f"unknown completion {arg}"]

    def v_highlight(self, arg, p):
        bm = self.bm
        if arg == "circle":
            errs = self._need("fano")
            c = self.obj["fano"]["circle"]
            if tuple(c) not in bm.FANO and not any(set(c) == set(l) for l in bm.FANO):
                errs.append("the circle is not a line of the Fano plane")
            return errs + self._claim(p, "points", sorted(c))
        if arg == "lines":
            errs = self._need("fano")
            sizes = {len(l) for l in bm.FANO}
            if not self.obj["fano"]["each_pair_once"]:
                errs.append("two points of the Fano plane do not lie on exactly one line")
            return errs + self._claim(p, "line_size", sizes.pop() if len(sizes) == 1 else None) \
                + self._claim(p, "lines", len(bm.FANO))
        if arg == "seed":
            errs = self._need("ring")
            q = sorted(bm.Q)
            if q != self.obj["seed:Q"]["points"] or set(q) != {0} | {i * i % 11 for i in range(1, 11)}:
                errs.append("the seed is not zero and the nonzero squares")
            if "order" in p and p["order"] != [0] + [i * i % 11 for i in range(1, 6)]:
                errs.append("order is not zero, then the squares of 1, 2, 3, 4, 5")
            self.marked = frozenset(bm.Q)
            return errs + self._claim(p, "points", q)
        if arg == "corners":
            errs = self._need("triangle", "views")
            return errs + self._claim(p, "points", self.obj["kitten:projective"]["corners"])
        if arg == "repeats":
            errs = self._need("triangle")
            n = sum(1 for s in self.obj["kitten:projective"]["spots"] if s[2] == p.get("label"))
            return errs + self._claim(p, "copies", n)
        if arg in bm.DIRECTIONS:
            errs = self._need("views")
            got = sorted(self.parts_points(p.get("picture"), [(bm.DIRECTIONS[arg], p.get("k", 0))]))
            ex = self.obj["kitten:projective"]["examples"].get(arg)
            if ex and p.get("picture") == ex["picture"] and p.get("k", 0) == 0 and ex["points"] != got:
                errs.append(f"math_objects.json's {arg} is {ex['points']}, the view gives {got}")
            return errs + self._claim(p, "points", got)
        if arg in ("cross", "square"):
            errs = self._need("views")
            parts = [((1, 0), p.get("row", 0)), ((0, 1), p.get("column", 0))]
            cross = self.parts_points(p.get("picture"), parts)
            got = sorted(cross if arg == "cross" else set(self.view_dict()[p.get("picture")]) - cross)
            return errs + self._claim(p, "points", got)
        if arg.startswith("family_"):
            errs = self._need("views")
            ex = self.family_example(arg)
            parts = [(tuple(d), k) for d, k in ex["parts"]]
            match = [hx for f, pic, ps, hx in bm.kitten_parts(bm.PROJECTIVE_VIEWS)
                     if f == ex["family"] and pic == ex["picture"] and ps == parts]
            if [sorted(h) for h in match] != [ex["hexad"]]:
                errs.append(f"{arg}: the example is not built from its parts")
            if frozenset(ex["hexad"]) not in bm.ORBIT:
                errs.append(f"{arg}: the example is not in the ring's orbit")
            count = len({hx for f, _, _, hx in bm.kitten_parts(bm.PROJECTIVE_VIEWS) if f == ex["family"]})
            self.lit = frozenset(ex["hexad"])
            return errs + self._claim(p, "hexad", ex["hexad"]) + self._claim(p, "count", count)
        if arg == "ep1_hands":
            errs = self._need("views")
            if self.labels != "card":
                errs.append("Episode 1's hands need the card labels")
            h = frozenset(self.obj[p["hand"]]["cards"])
            if h not in bm.HEXADS:
                errs.append(f"{p['hand']} is not a hexad")
            got = self.hand_parts(p["hand"])
            if got is None:
                return errs + [f"{p['hand']} is in none of the kitten's four families"]
            fam, pic, parts = got
            self.lit = h
            return errs + self._claim(p, "family", fam) + self._claim(p, "picture", pic)
        return []

    def v_clock_mod(self, arg, p):
        """Euler's clock (mod 11: its hand sweeps the hours, or ticks 10 + 1 = 0), or
        the three-hour clock that goes with the kitten's wrapped diagonals (mod 3)."""
        if arg == "11":
            errs = self._need("ring")
            if p.get("phase") == "sweep":
                a, b = p.get("hours", [0, 10])
                return errs + ([] if 0 <= a < b <= 10 else [f"the hand cannot sweep from {a} to {b}"])
            a, b, c = p.get("shows", [10, 1, 0])
            got = self.bm.translate(a) if b == 1 else None
            if got != c or self.obj["ring:projective"]["ten_plus_one"] != self.bm.translate(10):
                errs.append(f"{a} + {b} is {got} mod 11, cue says {c}")
            return errs
        if arg == "3":
            errs = self._need("views")
            a, b, c = p.get("shows", [2, 1, 0])
            if (a + b) % 3 != c:
                errs.append(f"{a} + {b} is {(a + b) % 3} mod 3, cue says {c}")
            return errs
        return [f"no clock mod {arg} in this episode"]

    def v_point_ring(self, arg, p):
        errs = self._need("ring")
        f = self.bm.RING_MAPS.get(arg)
        if f is None:
            return errs + [f"unknown map {arg}"]
        if not self.marked:
            errs.append("no points are marked on the ring")
        self.marked = frozenset(map(f, self.marked))
        if self.marked not in self.bm.ORBIT:
            errs.append("the map left the orbit")
        key = {"translate": "translate_seed", "invert": "invert_seed"}[arg]
        return errs + self._claim(p, "result", sorted(self.marked)) + \
            ([] if sorted(self.marked) == self.obj["ring:projective"][key] else [f"result is not math_objects.json's {key}"])

    def v_reveal_count(self, arg, p):
        from math import comb
        bm, obj = self.bm, self.obj
        if arg == "s_2_3_7":
            errs = self._need("fano")
            f = obj["fano"]
            got = {"t": 2 if f["each_pair_once"] else None, "k": f["line_size"], "v": f["points"]}
            if not all(len(l) == 3 for l in bm.FANO) or len({x for l in bm.FANO for x in l}) != 7:
                errs.append("the Fano lines do not make an S(2,3,7)")
            return errs + sum((self._claim(p, k, v) for k, v in got.items()), [])
        if arg == "s_5_6_12":
            if p.get("phase", "points") == "points":
                errs = self._need("fano")
                self.layout = "ring_blank"
            else:
                errs = self._need("ring_blank")
            d = obj["count:design"]
            got = {"t": 5, "k": 6, "v": 12} if d["each_five_once"] and d["hexads"] * 6 == comb(12, 5) else {}
            return errs + sum((self._claim(p, k, v) for k, v in got.items()), [])
        if arg == "792_over_6":
            errs = self._need("ring_blank")
            d = obj["count:design"]
            num, den = d["fives_formula"]
            from math import prod
            fives = prod(num) // prod(den)
            if fives != comb(12, 5) or d["five_subsets"] != fives or d["five_in_block"] != comb(6, 5) \
                    or d["blocks_from_counting"] != fives // comb(6, 5) or fives % comb(6, 5):
                errs.append("the count 792 / 6 = 132 does not check")
            return errs + self._claim(p, "fives", fives) + self._claim(p, "per_block", comb(6, 5)) \
                + self._claim(p, "blocks", fives // comb(6, 5))
        if arg == "orbit_132":
            errs = self._need("ring")
            layers = [len(l) for l in bm.orbit_layers(bm.Q)]
            if layers != obj["orbit:Q"]["layers"]:
                errs.append("the orbit's layers disagree with math_objects.json")
            self.marked = frozenset()
            return errs + self._claim(p, "layers", layers) + self._claim(p, "total", sum(layers))
        if arg == "fives_792":
            errs = self._need("ring")
            from collections import Counter
            from itertools import combinations
            fives = Counter(frozenset(s) for h in bm.ORBIT for s in combinations(h, 5))
            once = len(fives) == comb(12, 5) and set(fives.values()) == {1}
            return errs + self._claim(p, "blocks", len(bm.ORBIT)) + self._claim(p, "per_block", 6) \
                + self._claim(p, "fives", sum(fives.values())) + self._claim(p, "each_once", once)
        if arg == "12_12_54_54":
            errs = self._need("views")
            every = bm.kitten_parts(bm.PROJECTIVE_VIEWS)
            fams = [{hx for f, _, _, hx in every if f == i} for i in range(4)]
            if set.union(*fams) != bm.ORBIT or sum(map(len, fams)) != len(bm.ORBIT):
                errs.append("the four families are not exactly the ring's orbit")
            return errs + self._claim(p, "parts", [len(f) for f in fams]) + self._claim(p, "total", len(set.union(*fams)))
        return [f"unknown count {arg}"]


# ------------------------------------------------------------------ the code

class Code:
    """Ada's MINIMOG and tetracode (Episode 3), changed cue by cue.

    Like Board, it plays its visual verbs through the mathematics: the
    MINIMOG's cells, the three-hour clock, every codeword, every column
    count and odd-man-out reading, the word two readings force, where a
    hand disagrees with it, the forbidden counts, and every swap and repair
    are recomputed here from build_math_objects.py and compared with
    math_objects.json and with the claims written in the cue.  The renderer
    draws what this class computes.

    grid:    whether the MINIMOG is on the table; rows: whether its rows are numbered
    marked:  the cards lit in the grid (a hand, or one column's demo)
    hour:    where the three-hour clock's hand points (None: no clock)
    word:    the codeword on show beside the grid, if any
    """

    OWNS = ("fly_to_minimog", "clock_mod", "recap_montage", "assemble_codeword", "highlight",
            "write_along", "reveal_count", "card_exchange")
    SLOTS = ["b", "a", "a+b", "a+2b"]

    def __init__(self, objects):
        import build_math_objects as bm
        self.bm, self.obj = bm, objects
        self.grid, self.rows = False, False
        self.marked, self.hand_key = frozenset(), None
        self.hour, self.word, self.table = None, None, False
        self.ab = None

    # -- computed facts the renderer also uses

    def cell(self, card):
        """(row, column) of a card in the MINIMOG."""
        return next((r, c) for r, row in enumerate(self.bm.M) for c, v in enumerate(row) if v == card)

    def reading(self):
        """(column counts, odd-man-out readings) of the marked cards."""
        return self.bm.coordinates(self.marked)

    def test(self):
        return self.bm.test_hand(self.marked)

    def words(self):
        """The nine codewords, keyed by (a, b), from the formula."""
        return {(a, b): self.bm.tetra_word(a, b) for a in range(3) for b in range(3)}

    # -- helpers

    def _need(self, what, ok):
        return [] if ok else [f"needs {what}"]

    def _claim(self, p, key, got):
        if key in p and p[key] != got:
            return [f"{key} is {got!r}, cue says {p[key]!r}"]
        return []

    def _obj(self, ref, path, got):
        """Compare a computed value with math_objects.json."""
        o = self.obj[ref]
        for k in path.split("."):
            o = o[k]
        return [] if o == got else [f"math_objects.json {ref}.{path} is {o!r}, computed {got!r}"]

    def play(self, verb, arg, p):
        fn = getattr(self, f"v_{verb}", None)
        return fn(arg, p) if fn else [f"no {verb} in this episode"]

    # -- the verbs; each returns a list of error strings

    def v_fly_to_minimog(self, arg, p):
        bm = self.bm
        rows = [list(r) for r in bm.M]
        errs = self._obj("minimog", "rows", rows)
        if sorted(v for r in rows for v in r) != list(range(12)):
            errs.append("the MINIMOG does not hold each card once")
        self.grid = True
        return errs + self._claim(p, "rows", rows) + self._claim(p, "straighten", rows[-1][-1])

    def v_clock_mod(self, arg, p):
        if arg != "3":
            return [f"no clock mod {arg} in this episode"]
        phase = p.get("phase", "add")
        if phase == "sweep":
            a, b = p.get("hours", [0, 2])
            errs = [] if 0 <= a < b <= 2 else [f"the hand cannot sweep from {a} to {b}"]
            self.hour = b
            return errs + self._obj("clock:mod3", "hours", list(range(3)))
        if phase in ("name", "aside"):
            return self._need("a clock on screen", self.hour is not None)
        a, b, c = p.get("shows", [None, None, None])
        if self.hour is None:
            return ["there is no clock on screen"]
        got = (a + b) % 3
        errs = [] if got == c else [f"{a} + {b} is {got} mod 3, cue says {c}"]
        errs += self._obj("clock:mod3", f"sums.{a}+{b}", got)
        self.hour = got
        return errs

    def v_recap_montage(self, arg, p):
        if arg != "kitten_wrap":
            return [f"unknown recap {arg}"]
        bm = self.bm
        d = tuple(p.get("direction", [1, 1]))
        v = bm.PROJECTIVE_VIEWS[p.get("picture", bm.INF)]
        cells = sorted((r, c) for r in range(3) for c in range(3) if (d[0] * r + d[1] * c) % 3 == p.get("k", 0))
        got = [v[3 * r + c] for r, c in cells]
        errs = []
        if set(got) != set(bm.view_line(v, d, p.get("k", 0))):
            errs.append("the cells are not the kitten's line")
        sums = [(r + c) % 3 for r, c in cells]
        errs += self._obj("kitten:wrap", "cell_points", got) + self._obj("kitten:wrap", "row_plus_column", sums)
        return errs + self._claim(p, "cells", [list(x) for x in cells]) + self._claim(p, "cell_points", got) \
            + self._claim(p, "row_plus_column", sums)

    def v_assemble_codeword(self, arg, p):
        bm = self.bm
        if arg == "slots":
            # the slots are the formula's names; tetra_word must follow them
            errs = [] if self.obj["tetracode"]["formula"] == "(" + ", ".join(self.SLOTS) + ") mod 3" \
                else [f"the slots {self.SLOTS} do not match the formula {self.obj['tetracode']['formula']!r}"]
            if any(bm.tetra_word(a, b) != (b, a, (a + b) % 3, (a + 2 * b) % 3) for a in range(3) for b in range(3)):
                errs.append("tetra_word does not follow the slots")
            return errs + self._claim(p, "slots", self.SLOTS)
        if arg == "a1_b1":
            a, b = p.get("a", 1), p.get("b", 1)
            w = list(bm.tetra_word(a, b))
            errs = self._obj("tetracode", "word_a1_b1", w) if (a, b) == (1, 1) else []
            self.ab = (a, b)
            if p.get("phase", "fill") == "fill":
                self.word = w
                errs += self._claim(p, "last_before_wrap", a + 2 * b)
                errs += [] if self.hour is not None else ["the clock must be up to count a + 2b round"]
            return errs + self._claim(p, "word", w)
        if arg == "all":
            ws = self.words()
            errs = [] if sorted(ws.values()) == bm.T else ["the formula does not give the nine words"]
            errs += self._obj("tetracode", "size", len(set(ws.values())))
            self.table = True
            return errs + self._claim(p, "size", len(set(ws.values()))) + \
                self._claim(p, "kept", list(ws[self.ab]) if self.ab else None)
        if arg == "forced":
            errs = self._need("a hand in the grid", self.hand_key is not None)
            if errs:
                return errs
            pair = tuple(p.get("from", [0, 1]))
            w = list(bm.forced_word(self.marked, pair))
            if self.hand_key == "hand:example":
                errs += self._obj("test:example", "forced_word", w)
            self.word = w
            return errs + self._claim(p, "word", w) + self._claim(p, "from", list(pair))
        if arg == "fits":
            fits = self.test()["words_fitting"]
            if len(fits) != 1:
                return [f"the readings fit {len(fits)} words, not one"]
            self.word = fits[0]
            return self._claim(p, "word", fits[0]) + self._claim(p, "passes", self.test()["passes"])
        return [f"unknown codeword {arg}"]

    def v_highlight(self, arg, p):
        bm = self.bm
        if arg == "rows":
            errs = self._need("the MINIMOG", self.grid)
            self.rows = True
            return errs + self._obj("minimog", "row_labels", list(range(3))) + self._claim(p, "labels", list(range(3)))
        if arg == "dim":
            return self._need("the MINIMOG", self.grid)
        if arg == "two_coordinates":
            errs = self._need("the nine words", self.table)
            known = {int(k): v for k, v in p.get("known", {}).items()}
            got = [list(w) for w in bm.words_through(known)]
            if known == {0: 1, 1: 1}:
                errs += self._obj("tetracode", "first_two_1_1", got)
            return errs + self._claim(p, "words", got)
        if arg in ("column_one", "column_two", "column_wild"):
            errs = self._need("numbered rows", self.rows)
            c = p.get("column", 0)
            if arg == "column_wild":
                cards = [] if p.get("phase") == "empty" else [bm.M[r][c] for r in range(3)]
            else:
                cards = p.get("cards", [])
            rows = {r for r in range(3) if bm.M[r][c] in cards}
            if any(self.cell(x)[1] != c for x in cards):
                errs.append(f"cards {cards} are not all in column {c}")
            count, odd = bm.column_reading(rows)
            demo = {"column_one": "one", "column_two": "two"}.get(arg) or p.get("phase")
            ex = self.obj["odd_man_out:demo"]["demos"].get(demo)
            if ex and c == 0 and (ex["cards"] != sorted(cards, key=lambda x: self.cell(x)[0]) or ex["reading"] != odd):
                errs.append(f"math_objects.json's {demo} demo disagrees")
            self.marked, self.hand_key = frozenset(cards), None
            return errs + self._claim(p, "count", count) + self._claim(p, "reading", odd)
        if arg == "readings":
            errs = self._need("the nine words", self.table)
            self.marked, self.hand_key, self.word = frozenset(), None, None
            return errs + self._claim(p, "slots", 4)
        if arg == "column_counts":
            if "hand" in p:
                errs = self._need(f"{p['hand']} in the grid", self.hand_key == p["hand"])
                t = self.test()
                return errs + self._claim(p, "counts", t["column_counts"]) + self._claim(p, "forbidden", t["forbidden"]) \
                    + self._claim(p, "words", t["words_fitting"])
            errs = []
            for order in p.get("orders", []):
                if sorted(order) != [0, 1, 2, 3]:
                    errs.append(f"{order} is not an order of 0, 1, 2, 3")
            bad = [h for h in bm.HANDS if bm.forbidden(bm.coordinates(h)[0])]
            fit = all(bm.words_through({i: o for i, o in enumerate(bm.coordinates(h)[1]) if o is not None}) for h in bad)
            hexads = sum(h in bm.HEXADS for h in bad)
            errs += self._obj("count:forbidden", "hands", len(bad)) + self._obj("count:forbidden", "hexads", hexads)
            self.marked, self.hand_key = frozenset(), None
            return errs + self._claim(p, "hands", len(bad)) + self._claim(p, "fit_a_word", fit) \
                + self._claim(p, "hexads", hexads)
        if arg == "hand_in_grid":
            errs = self._need("numbered rows", self.rows)
            key = p.get("hand")
            if key not in self.obj:
                return errs + [f"unknown hand {key}"]
            self.marked, self.hand_key, self.word = frozenset(self.obj[key]["cards"]), key, None
            counts, odds = self.reading()
            errs += self._obj(key, "column_counts", counts) + self._obj(key, "odd_man_out", odds)
            return errs + self._claim(p, "counts", counts) + self._claim(p, "readings", odds) \
                + self._claim(p, "hexad", self.marked in bm.HEXADS) + self._claim(p, "passes", self.test()["passes"])
        if arg == "mismatch":
            errs = self._need("a word beside the grid", self.word is not None)
            if errs:
                return errs
            _, odds = self.reading()
            off = bm.disagreements(self.word, odds)
            if self.hand_key == "hand:example":
                errs += self._obj("test:example", "disagrees_at", off)
            return errs + self._claim(p, "at", off) + self._claim(p, "hand_rows", [odds[i] for i in off]) \
                + self._claim(p, "word_rows", [self.word[i] for i in off]) + self._claim(p, "agree", [
                    i for i, o in enumerate(odds) if o is not None and self.word[i] == o])
        if arg == "fix_column":
            errs = self._need("a word beside the grid", self.word is not None)
            if errs:
                return errs
            _, odds = self.reading()
            off = bm.disagreements(self.word, odds)
            if len(off) != 1:
                return errs + [f"the hand disagrees with the word at {off}, not at one coordinate"]
            c = off[0]
            out = next(x for x in self.marked if self.cell(x)[1] == c)
            inn = bm.M[self.word[c]][c]
            if self.hand_key == "hand:example":
                errs += self._obj("test:example", "fix", [out, inn])
            return errs + self._claim(p, "column", c) + self._claim(p, "out", out) + self._claim(p, "in", inn)
        if arg == "7_5":
            errs = self._need("the opening hand in the grid", self.hand_key == "hand:example")
            h = self.marked
            m = parse_move(arg)
            worked = self.obj["game:worked"]["steps"][0]["move"]
            if list(m) != worked:
                errs.append(f"Pascal's first move was {worked}, not {list(m)}")
            if m not in [tuple(x) for x in bm.repairs(h)]:
                errs.append(f"{m} is not a repair")
            k = bm.swap(h, m)
            self.marked, self.hand_key, self.word = k, None, None
            t = self.test()
            errs += self._obj("moves:example_to_hexads", "after_7_5.odd_man_out", t["odd_man_out"])
            return errs + self._claim(p, "total", sum(k)) + self._claim(p, "readings", t["odd_man_out"]) \
                + self._claim(p, "legal", legal(h, *m))
        return [f"unknown highlight {arg}"]

    def v_write_along(self, arg, p):
        if arg != "odd_man_out":
            return [f"unknown write_along {arg}"]
        counts, odds = self.reading()
        c = p.get("column", 0)
        errs = [] if counts[c] == 2 else [f"column {c} holds {counts[c]} cards, so it has no odd man out"]
        target = self.bm.M[odds[c]][c] if counts[c] == 2 else None
        return errs + self._claim(p, "to", target)

    def v_reveal_count(self, arg, p):
        bm = self.bm
        if arg == "all_hands":
            hands = len(bm.HANDS)
            agree = all(bm.test_hand(h)["passes"] == (h in bm.HEXADS) for h in bm.HANDS)
            passing = sum(bm.test_hand(h)["passes"] for h in bm.HANDS)
            errs = self._obj("count:test", "hands", hands) + self._obj("count:test", "test_agrees_with_hexads", agree) \
                + self._obj("count:test", "passing", passing)
            if not agree or passing != len(bm.HEXADS):
                errs.append("the test does not pick out exactly the hexads")
            return errs + self._claim(p, "hands", hands) + self._claim(p, "passing", passing)
        if arg == "three_of_fourteen":
            A = frozenset(self.obj["hand:example"]["cards"])
            moves = bm.down_moves(A)
            reps = [m for m in moves if bm.swap(A, m) in bm.HEXADS]
            errs = self._obj("moves:example_to_hexads", "legal_moves", len(moves)) \
                + self._obj("moves:example_to_hexads", "legal_repairs", len(reps))
            return errs + self._claim(p, "legal_moves", len(moves)) + self._claim(p, "legal_repairs", len(reps))
        if arg != "pairs_6":
            return [f"unknown count {arg}"]
        from itertools import combinations
        T = self.bm.T
        pairs = list(combinations(range(4), 2))
        distinct = [len({(w[i], w[j]) for w in T}) for i, j in pairs]
        errs = self._obj("tetracode", "distinct_pairs_per_choice", distinct)
        return errs + self._claim(p, "pairs", len(pairs)) + self._claim(p, "distinct", distinct) \
            + self._claim(p, "each_once", all(d == len(T) for d in distinct))

    def v_card_exchange(self, arg, p):
        bm = self.bm
        if arg == "repairs":
            phase = p.get("phase", "all")
            if self.hand_key != "hand:example":
                return ["the repairs start from the opening hand in the grid"]
            h = self.marked
            reps = bm.repairs(h)
            up = [list(m) for m in reps if m[1] > m[0]]
            down = [list(m) for m in reps if m[1] < m[0]]
            errs = self._obj("moves:example_to_hexads", "up", up) + self._obj("moves:example_to_hexads", "down", down)
            if any(legal(h, *m) for m in map(tuple, up)) or not all(legal(h, *m) for m in map(tuple, down)):
                errs.append("the down repairs are not exactly the legal ones")
            got = {"all": [list(m) for m in reps], "up": up, "down": down}[phase]
            return errs + self._claim(p, "swaps", len(bm.all_swaps(h))) + self._claim(p, "repairs", got) \
                + self._claim(p, "totals", [sum(bm.swap(h, tuple(m))) for m in got])
        if arg == "back":
            key = p.get("hand", "hand:example")
            self.marked, self.hand_key, self.word = frozenset(self.obj[key]["cards"]), key, None
            return []
        m = parse_move(arg)
        h = self.marked
        if m[0] not in h or m[1] in h:
            return [f"{m} is not a swap of the hand in the grid"]
        k = bm.swap(h, m)
        errs = []
        if self.word is not None and self.hand_key == "hand:example":
            errs += self._obj("test:example", "fixed_reading", bm.coordinates(k)[1])
        self.marked, self.hand_key = k, None
        errs += self._claim(p, "readings", bm.coordinates(k)[1]) + self._claim(p, "hexad", k in bm.HEXADS) \
            + self._claim(p, "legal", legal(h, *m)) + self._claim(p, "total", sum(k))
        return errs


def simulate(outline, cues, objects, cast, reactions):
    """Play the episode's cues through a Table and a Board; return a list of error strings."""
    errors = []
    board = Code(objects) if cues.get("board") == "minimog" else Board(objects)
    t = Table()
    tries = objects["tries:complement_1to6"]
    openings = [(tuple(x["move"]), tuple(x["replies"][i]["move"]))
                for x, i in zip(tries["tries"], (0, 3))]
    games_played = 0
    for scene in outline["scenes"]:
        for beat in scene.get("beats", []):
            bid = beat["id"]
            for s in steps(cues, bid):
                for v in step_visuals(s):
                    verb, arg = split_visual(v)
                    p = visual_params(v)
                    where = f"cues {bid} {visual_name(v)}"
                    try:
                        if verb in getattr(board, "OWNS", ()):
                            # Episode 3's MINIMOG plays these itself, cards included
                            for e in board.play(verb, arg, p):
                                errors.append(f"{where}: {e}")
                            continue
                        if verb == "card_deal":
                            if arg == "fan_12":
                                t.deal([])
                            else:
                                cards = deal_cards(arg, objects)
                                if cards is None:
                                    errors.append(f"{where}: unknown deal")
                                else:
                                    t.deal(cards)
                        elif verb == "card_exchange":
                            if arg == "demo":
                                a, b = p["move"]
                                t.exchange(a, b)
                                t.exchange(b, a, check=False)
                            elif arg.endswith("_rejected"):
                                a, b = parse_move(arg)
                                if p.get("phase", "try") == "try":
                                    if legal(t.hand, a, b):
                                        errors.append(f"{where}: this move is legal, not rejected")
                                    t.exchange(a, b, check=False)
                                    t.pending = (b, a)
                                else:
                                    t.exchange(*t.pending, check=False)
                                    t.pending = None
                            else:
                                a, b = parse_move(arg)
                                t.exchange(a, b)
                                if "total" in p and p["total"] != t.total:
                                    errors.append(f"{where}: total is {t.total}, cue says {p['total']}")
                        elif verb == "flip_hand":
                            t.flip()
                        elif verb == "recap_montage" and arg == "more_losses":
                            g = p.get("game", games_played)
                            start = deal_cards("complement_1to6", objects)
                            if sorted(t.hand) != sorted(
                                    set(start) - {openings[g][0][0], openings[g][1][0]}
                                    | {openings[g][0][1], openings[g][1][1]}):
                                errors.append(f"{where}: game {g} does not continue from its opening")
                            seq = montage_games(start, [openings[g]])[0]
                            for who, m, total in seq:
                                if m:
                                    t.exchange(*m)
                            if p.get("reset", True):
                                t.deal(start)
                            games_played += 1
                        elif verb == "react":
                            who, _, mood = arg.partition("_")
                            if who not in cast:
                                errors.append(f"{where}: unknown character {who}")
                            if mood not in reactions:
                                errors.append(f"{where}: unknown reaction {mood}")
                        elif verb == "point_at":
                            who, _, target = arg.partition("_")
                            if who not in cast:
                                errors.append(f"{where}: unknown character {who}")
                        if verb in ("recap_montage", "morph_layout", "summon_completion", "highlight",
                                    "point_ring", "reveal_count", "clock_mod"):
                            for e in board.play(verb, arg, p):
                                errors.append(f"{where}: {e}")
                    except (ValueError, KeyError, AssertionError, IndexError) as e:
                        errors.append(f"{where}: {e}")
    return errors
