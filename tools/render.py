#!/usr/bin/env python3
"""Render site/index.html (and copy the TSVs into site/) from status.tsv,
funnies.tsv and series.tsv. Runs in CI after build_status.py."""
import collections
import csv
import datetime as dt
import html
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLITZ = "https://github.com/EveryPuzzleProject/blitz"
BLITZ_JUDGE = "https://github.com/EveryPuzzleProject/blitz/tree/main/publications/judge"
REQUEST = "https://github.com/EveryPuzzleProject/blitz/issues/new?template=request-blitz.yml"
CATALOG = "https://github.com/EveryPuzzleProject/catalog/blob/main/publications/judge.md"
REPO = "https://github.com/EveryPuzzleProject/judge"
STATES = [  # (state, label)
    ("in-gxd", "In the archive"),
    ("reviewed", "Reviewed"),
    ("needs-person", "Needs a person"),
    ("in-review", "In review"),
    ("need-review", "Waiting for review"),
    ("need-ocr", "Found, not yet read"),
    ("need-image", "Scan wanted"),
    ("missing", "Not found yet"),
]
COLORS = {"in-gxd": "#2f6f4f", "reviewed": "#4f9a6f", "needs-person": "#c4572c", "in-review": "#4f8fbf",
          "need-review": "#9db8cf", "need-ocr": "#c9a227", "need-image": "#d98a4f", "missing": "#d9d5cc"}


def read(name: str) -> list[dict]:
    return list(csv.DictReader(open(ROOT / name, encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE))


def e(s: str) -> str:
    return html.escape(s or "")


def main() -> None:
    rows, funnies, series = read("status.tsv"), read("funnies.tsv"), read("series.tsv")
    label = dict(STATES)
    count = collections.Counter(r["state"] for r in rows)
    by_year = collections.defaultdict(collections.Counter)
    for r in rows:
        by_year[r["date"][:4]][r["state"]] += 1
    done = count["reviewed"] + count["in-gxd"]

    def pill(state: str) -> str:
        return f'<span class="pill" style="background:{COLORS.get(state, "#999")}">{e(label.get(state, state))}</span>'

    def table(rs, cols) -> str:
        head = "".join(f"<th>{c}</th>" for c, _ in cols)
        body = "\n".join("<tr>" + "".join(f"<td>{f(r)}</td>" for _, f in cols) + "</tr>" for r in rs)
        return f'<div class="scroll"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'

    hunt = [r for r in rows if r["state"] in ("missing", "need-image", "need-ocr")]
    hunt_table = table(hunt, [("Date", lambda r: e(r["date"])), ("No.", lambda r: e(r["number"])),
                              ("Run", lambda r: e(r["run"])), ("State", lambda r: pill(r["state"])), ("Notes", lambda r: e(r["note"]))])
    funnies_table = table(funnies, [("Id", lambda r: e(r["id"])), ("1-Across clue", lambda r: e(r["clue_1a"])),
                                    ("Answer", lambda r: e(r["answer_1a"])), ("Judge puzzle", lambda r: e(r["judge"])),
                                    ("Where it ran", lambda r: e(r["appearances"])), ("Notes", lambda r: e(r["note"]))])
    series_table = table(series, [("Series", lambda r: e(r["name"])), ("Schedule", lambda r: e(r["days"])),
                                  ("From", lambda r: e(r["from"])), ("To", lambda r: e(r["to"])), ("Status", lambda r: e(r["status"]))])
    bars = "\n".join(
        '<div class=bar><span class=yr>{y}</span><span class=track>{seg}</span><span class=n>{d}/{t}</span></div>'.format(
            y=y, t=sum(c.values()), d=c["reviewed"] + c["in-gxd"],
            seg="".join(f'<span style="flex:{c[s]};background:{COLORS[s]}" title="{lab}: {c[s]}"></span>' for s, lab in STATES if c[s]))
        for y, c in sorted(by_year.items()))
    legend = "".join(f'<span class=key><span class=sw style="background:{COLORS[s]}"></span>{lab} <span class=muted>({count[s]})</span></span>' for s, lab in STATES if count[s])
    all_rows = "\n".join(
        f'<tr data-state="{e(r["state"])}"><td>{e(r["date"])}</td><td>{e(r["number"])}</td><td>{e(r["run"])}</td><td>{pill(r["state"])}</td><td class=id>{e(r["xdid"])}</td><td>{e(r["note"])}</td></tr>'
        for r in sorted(rows, key=lambda r: r["date"]))

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Crossword Puzzles in Judge</title>
<style>
:root {{ --bg:#fbfaf7; --fg:#1d1d1b; --muted:#6b6a65; --line:#e3e0d8; --card:#ffffff; --accent:#8a1c1c; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#161614; --fg:#ecebe6; --muted:#a3a19a; --line:#34332f; --card:#1f1f1c; --accent:#e07a6a; }} }}
:root[data-theme="dark"] {{ --bg:#161614; --fg:#ecebe6; --muted:#a3a19a; --line:#34332f; --card:#1f1f1c; --accent:#e07a6a; }}
* {{ box-sizing:border-box }}
body {{ margin:0; background:var(--bg); color:var(--fg); font:16px/1.55 Georgia, "Times New Roman", serif }}
main {{ max-width:960px; margin:0 auto; padding:32px 16px 64px }}
h1 {{ font-size:2rem; margin:0 0 4px }} h2 {{ margin:40px 0 8px; font-size:1.35rem; border-bottom:2px solid var(--fg); padding-bottom:4px }}
h3 {{ margin:24px 0 6px; font-size:1.05rem }}
a {{ color:var(--accent) }} .muted {{ color:var(--muted) }} .lede {{ font-size:1.1rem }}
.cta {{ background:var(--card); border:1px solid var(--line); border-left:4px solid var(--accent); padding:16px 20px; margin:20px 0 }}
.cta ol {{ margin:8px 0 0; padding-left:22px }}
table {{ width:100%; border-collapse:collapse; font:14px/1.4 system-ui, sans-serif }}
th, td {{ text-align:left; padding:6px 8px; border-bottom:1px solid var(--line); vertical-align:top }}
th {{ font-weight:600 }} .scroll {{ overflow-x:auto }} td:first-child, td.id {{ white-space:nowrap }}
.bar {{ display:flex; align-items:center; gap:8px; font:12px system-ui, sans-serif; margin:2px 0 }}
.yr {{ width:3em; color:var(--muted) }} .n {{ width:4.5em; text-align:right; color:var(--muted) }}
.track {{ flex:1; display:flex; height:12px; border-radius:2px; overflow:hidden; background:#d9d5cc }}
.legend {{ display:flex; flex-wrap:wrap; gap:14px; font:13px system-ui, sans-serif; margin:8px 0 }}
.key {{ display:inline-flex; align-items:center; gap:6px }} .sw {{ width:12px; height:12px; border-radius:2px; display:inline-block }}
.pill {{ font-size:12px; padding:1px 6px; border-radius:9px; color:#fff; white-space:nowrap }}
.filters {{ display:flex; flex-wrap:wrap; gap:8px; margin:8px 0; font:14px system-ui, sans-serif }}
input, select {{ font:inherit; padding:4px 8px; background:var(--card); color:var(--fg); border:1px solid var(--line); border-radius:4px }}
footer {{ margin-top:48px; font:13px system-ui, sans-serif; color:var(--muted) }}
</style></head><body><main>
<h1>Crossword Puzzles in Judge</h1>
<p class="lede">Judge, the New York humor magazine, ran its first crossword on November 1, 1924, billed as the first of a weekly
series of "Home Destroyers". Two weeks later the whole cover was a crossword. The puzzles kept coming, weekly and then monthly,
until at least 1939: groan-worthy clues, odd-shaped grids, and constructors who were mostly readers.</p>
<p>We're indexing every one: when it ran, where a copy survives, and how far it's got in review. Of {len(rows)} puzzles known so far,
<b>{done}</b> are reviewed. Here's what's left, and how you can help.</p>

<div class="cta"><b>How you can help</b>
<ol>
<li><b>Review puzzles.</b> Most of the work is checking puzzles against the page scans. Point your Claude at the <a href="{BLITZ_JUDGE}">Judge packets in blitz</a>; see <a href="{BLITZ}">blitz</a> for how.</li>
<li><b>Find missing puzzles.</b> The numbered puzzles below aren't in archive.org's scans of Judge. A library copy of the magazine, or a newspaper reprint, would fill them in.</li>
<li><b>Hunt for Cross Word Funnies.</b> In 1925 newspapers ran Judge's puzzles as "Cross Word Funnies, selected by Judge". Clip any you find on Newspapers.com and send the links in a <a href="{REQUEST}">blitz request</a>, with the 1-Across clue.</li>
</ol>
<p style="margin:10px 0 0"><b>Already have puzzles as files?</b> A Judge puzzle typed up or saved as a .puz, .ipuz, .jpz or .xd file is welcome too.
Open a request saying which puzzles you have and we'll arrange how to send them.</p></div>

<h2>Puzzles to find</h2>
<p>Numbered puzzles we know about but don't have a usable copy of. "Found, not yet read" means it's in the scans and just needs harvesting.</p>
{hunt_table}

<h2>Cross Word Funnies, 1925</h2>
<p>From January to May 1925 newspapers across the US and Canada ran puzzles as "Cross Word Funnies, selected by Judge" (copyright 1925),
usually with the solution the next day. The January ones are Judge's own numbered puzzles, reprinted six to twelve weeks later: a second copy
wherever Judge's scans are missing a page. From February they're puzzles that never appeared in Judge, so the newspapers are the only source.
US and Canadian papers ran them in different orders, and at least one paper printed a grid with another puzzle's clues, so check that the clues fit.</p>
{funnies_table}

<h2>Series</h2>
{series_table}

<h2>Progress by year</h2>
<div class="legend">{legend}</div>
{bars}

<h2>Every puzzle</h2>
<div class="filters"><input id="q" type="search" placeholder="Search date, number, notes…">
<select id="st"><option value="">All states</option>{''.join(f'<option value="{s}">{lab}</option>' for s, lab in STATES)}</select></div>
<div class="scroll"><table id="all"><thead><tr><th>Date</th><th>No.</th><th>Run</th><th>State</th><th>Id</th><th>Notes</th></tr></thead><tbody>
{all_rows}
</tbody></table></div>

<footer>Part of the <a href="https://github.com/EveryPuzzleProject">Every Puzzle Project</a>. Data: <a href="{REPO}">{REPO.split('github.com/')[1]}</a>
(<a href="status.tsv">status.tsv</a>, <a href="funnies.tsv">funnies.tsv</a>); review state comes from <a href="{BLITZ}">blitz</a>; history and sources in the
<a href="{CATALOG}">catalog</a>. Puzzles themselves aren't published here. Generated {dt.date.today().isoformat()}.</footer>
</main>
<script>
const q=document.getElementById('q'), st=document.getElementById('st'), rows=[...document.querySelectorAll('#all tbody tr')];
function f(){{const t=q.value.toLowerCase(), s=st.value; for(const r of rows) r.hidden=(s&&r.dataset.state!==s)||(t&&!r.textContent.toLowerCase().includes(t));}}
q.addEventListener('input',f); st.addEventListener('change',f);
</script>
</body></html>
"""
    out = ROOT / "site"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(page, encoding="utf-8")
    for name in ("status.tsv", "funnies.tsv", "series.tsv"):
        shutil.copy(ROOT / name, out / name)
    print(f"site/index.html: {len(rows)} puzzles, {len(hunt)} to find, {len(funnies)} funnies")


if __name__ == "__main__":
    main()
