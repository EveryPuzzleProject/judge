# Crossword Puzzles in Judge

Judge, the New York humor magazine, ran its first crossword on November 1,
1924. This is the Every Puzzle Project's home for indexing all of them: which
series ran when, where each puzzle survives, and how far it has got in review.

**Status page: https://everypuzzleproject.github.io/judge/**

## How you can help

- **Review puzzles** in the [Judge packets in blitz](https://github.com/EveryPuzzleProject/blitz/tree/main/publications/judge).
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
| `tools/build_status.py` | Builds `status.tsv` from blitz's `publications/judge/puzzles.tsv` plus `manual.tsv`. |
| `tools/render.py` | Builds the status page. |

`status.tsv` isn't committed: CI rebuilds it from blitz on every push and
daily, and publishes it with the page (`/status.tsv`). States: `missing`,
`need-image`, `need-ocr` (in the scans, not yet harvested), `need-review`,
`in-review`, `needs-person`, `reviewed`, `in-gxd`. This repo holds only
metadata, never puzzles or page images. Background, sources and open
questions are in the [catalog entry](https://github.com/EveryPuzzleProject/catalog/blob/main/publications/judge.md).
