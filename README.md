# Crossword Puzzles in Judge

Judge, the New York humor magazine, ran its first crossword on November 1,
1924. This is the Every Puzzle Project's home for indexing all of them: which
series ran when, where each puzzle survives, and how far it has got in review.

**Status page: https://everypuzzleproject.github.io/judge/**

## How you can help

- **Check puzzles against the scan** on the [review site](https://blitz.xwordapp.com/review/): no account needed.
- **Find missing puzzles.** The status page lists the numbered puzzles that
  aren't in archive.org's scans of Judge.
- **Hunt for Cross Word Funnies.** In 1925 newspapers ran Judge's puzzles as
  "Cross Word Funnies, selected by Judge". Clip any you find and send the
  links in a [blitz request](https://github.com/EveryPuzzleProject/blitz/issues/new?template=request-blitz.yml),
  with the 1-Across clue. Please don't upload page images; requests are public.

Already have puzzles as files (.puz, .ipuz, .jpz, .xd)? Open a request saying
which ones, and we'll arrange how to send them.

## What's here

| File | What it is |
|---|---|
| `series.tsv` | Judge's puzzle series: two numbered runs (Nos. 1–122 from 1924, Nos. 1–415 from 1927), cover puzzles, and the 1925 newspaper feature. |
| `manual.tsv` | Puzzles blitz doesn't list yet, and notes; overrides the state for its rows. |
| `funnies.tsv` | Cross Word Funnies, one row per puzzle (not per newspaper): which Judge puzzle it reprints, if any, and every paper and date it's been found in. Identified by 1-Across and grid shape. |
| `fixes/fixes.toml` | Hand fixes to the harvest: page hints, typed grids, extra pages. |
| `fixes/corrections.jsonl` | The corrections ledger: every accepted change from a review, append-only (who, when, what the OCR read, what it should be). The puzzles are rebuilt from the OCR plus this file. |
| `fixes/corrections.rejected.jsonl` | Changes a maintainer turned down, with the reason. |
| `fixes/tool-notes.jsonl` | Reviewers' notes on what the OCR tools got wrong. |
| `puzzles.tsv` | Every puzzle the tools know of, with its review state (restored, needs-person + reason, missing). Written by the tools' sync after each import; don't edit by hand. |
| `xd/` | The current .xd of every reviewed puzzle (from the OCR plus `fixes/`). |
| `reviews/` | Reviews sent as pull requests (two so far, from the 2026-10-02 trial). |
| `review-notes.md` | What a reviewer needs to know about *Judge*'s pages; `blitz instructions judge` prints it with the general rules. |
| `tools/build_status.py` | Builds `status.tsv` from `puzzles.tsv` plus `manual.tsv`. |
| `tools/render.py` | Builds the status page. |

`status.tsv` isn't committed: CI rebuilds it on every push and daily, and publishes it with the page (`/status.tsv`). States: `missing`,
`need-image`, `need-ocr` (in the scans, not yet harvested), `need-review`,
`in-review`, `needs-person`, `reviewed`, `in-gxd`. Page images live in the private
`judge-scans`; the tools are in [blitz](https://github.com/EveryPuzzleProject/blitz)
and [xword-ocr](https://github.com/EveryPuzzleProject/xword-ocr), which read this
repo's `fixes/` from a checkout beside them. Background, sources and open
questions are in the [catalog entry](https://github.com/EveryPuzzleProject/catalog/blob/main/publications/judge.md).
