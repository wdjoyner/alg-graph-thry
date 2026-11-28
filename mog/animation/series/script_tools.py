"""Read an episode's Fountain script into beats and dialogue lines.

The script marks the outline's beats with [[beat: sNN.bMM]] notes and every
dialogue line with a [[line: sNN.bMM.lKK]] note.  This module is the one
place that parses them; the checker, the audio generator, the timing
builder and the renderer all read the script through it.

    python script_tools.py ep1/script.fountain      # list beats and lines
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

NOTE = re.compile(r"\[\[\s*(beat|line)\s*:\s*([A-Za-z0-9_.\-]+)\s*\]\]")
ANY_NOTE = re.compile(r"\[\[.*?\]\]", re.S)
BEAT_ID = re.compile(r"s\d\d\.b\d\d[a-z]?")
LINE_ID = re.compile(r"(s\d\d\.b\d\d[a-z]?)\.l\d\d[a-z]?")


def _is_character_cue(s):
    """A Fountain character cue: all caps, at least one letter, no trailing colon."""
    t = re.sub(r"\(.*?\)", "", s).strip()
    return bool(t) and t == t.upper() and any(c.isalpha() for c in t) \
        and not t.endswith(":") and not t.startswith(("INT.", "EXT.", "#", "[[", ">")) \
        and not t.startswith("MONTAGE")


def parse(path):
    """Return {"beats": [...], "lines": {id: line}, "errors": [...]}.

    Each beat: {"id", "order", "lines": [line ids]}.
    Each line: {"id", "beat", "speaker", "text", "parenthetical", "order"}.
    """
    text = Path(path).read_text(encoding="utf-8")
    # drop the title page (everything up to the first blank line)
    body = text.split("\n\n", 1)[1] if "\n\n" in text else text
    blocks = [b.strip("\n") for b in re.split(r"\n\s*\n", body) if b.strip()]
    beats, lines, errors = [], {}, []
    current = None
    for block in blocks:
        rows = block.split("\n")
        notes = NOTE.findall(block)
        for kind, ident in notes:
            if kind == "beat":
                if not BEAT_ID.fullmatch(ident):
                    errors.append(f"bad beat id {ident!r}")
                if any(b["id"] == ident for b in beats):
                    errors.append(f"beat {ident} marked twice")
                current = {"id": ident, "order": len(beats), "lines": []}
                beats.append(current)
        if _is_character_cue(rows[0]) and len(rows) >= 2 and not rows[0].startswith("[["):
            speaker = re.sub(r"\(.*?\)", "", rows[0]).strip().lower()
            paren, dialogue = None, []
            for r in rows[1:]:
                r = r.strip()
                if r.startswith("(") and r.endswith(")") and not dialogue:
                    paren = r[1:-1]
                else:
                    dialogue.append(r)
            ids = [i for k, i in notes if k == "line"]
            said = ANY_NOTE.sub("", " ".join(dialogue)).strip()
            if len(ids) != 1:
                errors.append(f"dialogue {said[:40]!r} needs exactly one [[line: id]] note, has {len(ids)}")
                continue
            lid = ids[0]
            m = LINE_ID.fullmatch(lid)
            if not m:
                errors.append(f"bad line id {lid!r}")
                continue
            if current is None or m.group(1) != current["id"]:
                errors.append(f"line {lid} is not inside beat {m.group(1)}")
            if lid in lines:
                errors.append(f"line {lid} used twice")
            lines[lid] = {"id": lid, "beat": m.group(1), "speaker": speaker, "text": said,
                          "parenthetical": paren, "order": len(lines)}
            if current is not None:
                current["lines"].append(lid)
        elif any(k == "line" for k, _ in notes):
            errors.append(f"[[line]] note outside dialogue: {block[:50]!r}")
    return {"beats": beats, "lines": lines, "errors": errors}


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "ep1" / "script.fountain"
    s = parse(path)
    for b in s["beats"]:
        print(b["id"])
        for lid in b["lines"]:
            ln = s["lines"][lid]
            print(f"  {lid}  {ln['speaker'].upper():7} {ln['text']}")
    for e in s["errors"]:
        print("ERROR:", e)
    return 1 if s["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
