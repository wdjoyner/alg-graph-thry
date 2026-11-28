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


def simulate(outline, cues, objects, cast, reactions):
    """Play the episode's cues through a Table; return a list of error strings."""
    errors = []
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
                    except (ValueError, KeyError, AssertionError, IndexError) as e:
                        errors.append(f"{where}: {e}")
    return errors
