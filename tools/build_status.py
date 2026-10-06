#!/usr/bin/env python3
"""Build status.tsv for Judge's crosswords from blitz's puzzle list plus manual.tsv.

    python tools/build_status.py [--blitz URL-or-path]

Everything it reads is public, so it runs in CI on every push and daily.
blitz (github.com/EveryPuzzleProject/blitz) keeps one row per Judge puzzle
with its review state; manual.tsv adds puzzles blitz doesn't list yet and
notes, and overrides the state for its rows.
"""
import argparse
import csv
import io
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLITZ = "https://raw.githubusercontent.com/EveryPuzzleProject/blitz/main/publications/judge/puzzles.tsv"
COLUMNS = ["xdid", "date", "number", "run", "state", "blitz_state", "note"]
# blitz state -> ours. Ours, in order: missing, need-image, need-ocr, need-review,
# in-review, needs-person, reviewed, in-gxd.
STATE = {"missing": "missing", "later": "need-review", "open": "in-review",
         "needs-person": "needs-person", "restored": "reviewed"}
SECOND_RUN = "1927-04-30"  # Judge restarted its numbering with No. 1 here


def read(text: str) -> list[dict]:
    return list(csv.DictReader(io.StringIO(text), delimiter="\t", quoting=csv.QUOTE_NONE))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--blitz", default=BLITZ, help="blitz's publications/judge/puzzles.tsv (URL or path)")
    a = ap.parse_args()
    if a.blitz.startswith("http"):
        text = urllib.request.urlopen(a.blitz, timeout=60).read().decode("utf-8")
    else:
        text = Path(a.blitz).read_text(encoding="utf-8")

    rows = {}
    for b in read(text):
        rows[b["xdid"]] = {"xdid": b["xdid"], "date": b["date"], "number": b["number"],
                           "state": STATE.get(b["state"], b["state"]), "blitz_state": b["state"],
                           "note": b["reason"] if b["state"] in ("needs-person", "missing") else ""}
    for m in read((ROOT / "manual.tsv").read_text(encoding="utf-8")):
        r = rows.setdefault(m["xdid"], {"xdid": m["xdid"], "date": m["date"], "number": m["number"], "blitz_state": "", "state": ""})
        if m["state"]:
            r["state"] = m["state"]
        r["note"] = "; ".join(x for x in (r.get("note", ""), m["note"]) if x)
    for r in rows.values():
        r["run"] = "" if not r["number"] else ("1927" if r["date"] >= SECOND_RUN else "1924")
    out = sorted(rows.values(), key=lambda r: (r["date"], r["xdid"]))
    with open(ROOT / "status.tsv", "w", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(COLUMNS) + "\n")
        f.writelines("\t".join(r.get(c, "") for c in COLUMNS) + "\n" for r in out)
    counts = {}
    for r in out:
        counts[r["state"]] = counts.get(r["state"], 0) + 1
    print(f"status.tsv: {len(out)} puzzles", counts)


if __name__ == "__main__":
    main()
