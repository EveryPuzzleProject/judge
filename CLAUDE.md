# judge: notes for Claude

This repo is Judge magazine's record: the fix file and corrections ledger (fixes/),
every puzzle's state (puzzles.tsv), the reviewed puzzles (xd/), and reviewer notes
(review-notes.md). The tools are in ../xword-ocr and ../blitz; see
../blitz/MAINTAINING.md.

## The goal: a correct xd file, with its proof visible

The xd files must be correct, proven by the OCR, the reviewers' changes and comments, and
the original scans, and the review page (blitz.xwordapp.com/review/) must show everything
in them with its source. So:

- Corrections go in fixes/corrections.jsonl with who and when (append only; the newest
  change to an item wins).
- A hand fix in fixes/fixes.toml is fine, but any judgement it embodies (stacking grids,
  treating marks as blocks, keeping a misprint) goes in the puzzle's `note`, which goes
  into the xd and shows on the review page. A TOML comment alone is hidden from reviewers.
