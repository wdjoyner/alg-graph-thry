"""Check the Cat Fugue transcription and write it as a MIDI file.

    python build_k30_midi.py           # check, then write scarlatti_k30_m1-44.mid
    python build_k30_midi.py --report  # also list strong-beat dissonances to review

Checks: every voice of every bar adds up to 6 eighths (6/8); ties join equal
pitches; and every entry of the fugue subject is an exact transposition of
the subject as it first appears (bars 1-4, left hand).  The MIDI file is at
Longo's tempo (dotted quarter = 120, one bar per second) with a 6/8 time
signature, so make_music.py can find the measures.
"""
import argparse
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "scarlatti_k30_m1-44.txt"
OUT = HERE / "scarlatti_k30_m1-44.mid"
STEP = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
EIGHTH = 1 / 6          # seconds, at dotted quarter = 120

# (hand-voice, first bar, expected pitch of the first note, description)
ENTRIES = [("LH1", 1, "G3", "subject, bass"), ("LH1", 6, "D3", "answer, bass"),
           ("LH1", 12, "G2", "subject, bass"), ("LH1", 17, "D2", "answer, bass")]
# Bars 27-30 bring the subject into the right hand with its fourth leap
# inverted (B-flat 5 drops to C-sharp 5), so it is checked for its first
# five notes and its tail.
VARIANT = ("RH1", 27, "G4")


def midi(name):
    m = re.fullmatch(r"([A-G])(b|#)?(-?\d)", name)
    if not m:
        raise ValueError(f"bad pitch {name!r}")
    letter, acc, octave = m.groups()
    return 12 * (int(octave) + 1) + STEP[letter] + {"b": -1, "#": 1, None: 0}[acc]


def parse():
    bars = {}
    for lineno, line in enumerate(SOURCE.read_text().splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):       # comments are whole lines ("#" also means sharp)
            continue
        head, body = line.split(":", 1)
        m = re.fullmatch(r"m(\d+) (RH|LH)(\d)", head.strip())
        bar, voice = int(m.group(1)), m.group(2) + m.group(3)
        events, total = [], 0
        for tok in body.split():
            pitch, dur = tok.rsplit(":", 1)
            tie = dur.endswith("~")
            dur = int(dur.rstrip("~"))
            if pitch == "r":
                notes = []
            elif pitch.startswith("["):
                notes = [midi(p) for p in pitch[1:-1].split(",")]
            else:
                notes = [midi(pitch)]
            events.append((total, dur, notes, tie))
            total += dur
        if total != 6:
            raise SystemExit(f"line {lineno}: bar {bar} {voice} adds up to {total} eighths, not 6")
        bars.setdefault(bar, {})[voice] = events
    return bars


def notes_of(bars):
    """Absolute notes (start, end, pitch, voice) with ties merged."""
    out, open_ties = [], {}
    for bar in sorted(bars):
        base = (bar - 1) * 6
        for voice, events in bars[bar].items():
            for start, dur, pitches, tie in events:
                for p in pitches:
                    key = (voice, p)
                    if key in open_ties and open_ties[key][1] == base + start:
                        s, _, _ = open_ties.pop(key)
                        note = [s, base + start + dur, p]
                    else:
                        note = [base + start, base + start + dur, p]
                    if tie:
                        open_ties[key] = (note[0], note[1], p)
                    else:
                        out.append((note[0], note[1], p, voice))
            for key, (s, e, p) in list(open_ties.items()):
                if e < base + 6 or key[0] != voice:
                    continue
        stale = [k for k, (s, e, p) in open_ties.items() if e < base + 6]
        for k in stale:
            raise SystemExit(f"bar {bar}: tie on {k} does not continue into the next bar")
    for (voice, p), (s, e, _) in open_ties.items():
        out.append((s, e, p, voice))
    return sorted(out)


def line_from(notes, voice, bar, count):
    seq = [n for n in notes if n[3] == voice and n[0] >= (bar - 1) * 6]
    return [n[2] for n in seq[:count]]


def check_entries(notes):
    subject = line_from(notes, "LH1", 1, 12)
    shape = [p - subject[0] for p in subject]
    for voice, bar, first, what in ENTRIES:
        got = line_from(notes, voice, bar, 12)
        want = [midi(first) + s for s in shape]
        status = "ok" if got == want else f"MISMATCH {got} vs {want}"
        print(f"bar {bar:2d} {voice} {what}: {status}")
        if got != want:
            raise SystemExit("subject entry does not match")
    voice, bar, first = VARIANT
    got = line_from(notes, voice, bar, 12)
    want = [midi(first) + s for s in shape]
    same = [g == w or (i == 5 and g == w - 12) for i, (g, w) in enumerate(zip(got, want))]
    tail = [g - got[6] for g in got[6:]] == [w - want[6] for w in want[6:]]
    ok = all(same[:5]) and tail
    print(f"bar {bar} {voice} subject, right hand (fourth leap inverted): {'ok' if ok else 'MISMATCH'}")
    if not ok:
        raise SystemExit("right-hand entry does not match")


def report(notes):
    """Seconds and sevenths sounding together on a dotted-quarter beat, for review."""
    end = max(n[1] for n in notes)
    for t in range(0, end, 3):
        sounding = sorted({n[2] for n in notes if n[0] <= t < n[1]})
        bad = [(a, b) for i, a in enumerate(sounding) for b in sounding[i + 1:] if (b - a) % 12 in (1, 2, 10, 11)]
        if bad:
            bar, beat = t // 6 + 1, (t % 6) // 3 + 1
            print(f"  bar {bar} beat {beat}: " + ", ".join(f"{a}-{b}" for a, b in bad))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()
    bars = parse()
    assert sorted(bars) == list(range(1, max(bars) + 1)), "missing bars"
    notes = notes_of(bars)
    print(f"{len(bars)} bars, {len(notes)} notes, every voice 6/8")
    check_entries(notes)
    if args.report:
        print("strong-beat seconds and sevenths (MIDI numbers):")
        report(notes)
    import pretty_midi
    pm = pretty_midi.PrettyMIDI(initial_tempo=180)          # quarter = 180, dotted quarter = 120
    pm.time_signature_changes.append(pretty_midi.TimeSignature(6, 8, 0))
    harpsichord = pretty_midi.Instrument(program=6, name="Harpsichord")
    for s, e, p, _ in notes:
        harpsichord.notes.append(pretty_midi.Note(velocity=84, pitch=p, start=s * EIGHTH, end=e * EIGHTH - 0.01))
    pm.instruments.append(harpsichord)
    pm.write(str(OUT))
    print(f"wrote {OUT.name}: {len(bars)} bars, {pm.get_end_time():.1f} s at dotted quarter = 120")


if __name__ == "__main__":
    main()
