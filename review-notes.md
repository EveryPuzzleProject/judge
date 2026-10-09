# Reviewing *Judge* puzzles

What a reviewer needs to know about *Judge* on top of the general rules in
blitz (`uv run blitz instructions judge` prints both). Add to it when a review
round teaches something: say where to look, not what the answer is.

## About *Judge*
- *Judge* printed each puzzle's answers in a LATER issue. `answers.png`, when
  present, is this puzzle's key cut from that later issue. A missing answer
  grid is expected for some puzzles and isn't a blocker by itself; the
  answer grid printed on this puzzle's own page is usually the previous
  issue's.
- *Judge* was weekly until July 1932 and monthly from August 1932 (dates
  like 1932-08-01). Monthly issues usually have two or three puzzles; their
  ids end in `b` or `c` (judge1934-06-01b). When the page holds more than one
  puzzle, make sure the clues, captions and answer key you check are this
  puzzle's (match the clue numbers and answers to this grid), and remove
  anything that belongs to the other one.
- The magazine's stock notice ("Judge pays $10 for each one printed", "Judge
  will run a Crossword Puzzle every week…") is not part of the puzzle.
- "Submitted by …" under the grid often names the constructor: use it for the
  author and byline when there's no other byline.

## Notes on *Judge* (1920s), from earlier review rounds

What the tools tend to get wrong on these pages. These say where to look,
not what the answer is: check every one on a crop as usual. (Kept short; an
entry comes out once the tools are fixed. Last updated after batch 9,
2026-10-07.)

- **The title is "Judge's Crossword Puzzle No. N".** text.md marks a title
  with anything else in it ("suspect") and `blitz sheets` then adds meta:top,
  the band across the top of the page; the extra words came from an ad, a
  headline or the next column's heading ("Horizontal", "ANSWERS TO"). The
  A1 clue can pick up the same ad text.
- **The last clue of a column** often has the page number or the next
  heading, "Solution of Last Week's Puzzle", run into it, sometimes with a
  garbled repeat of the clue. text.md shows such a clue with that taken off
  and says so; check the crop. A clue the heading replaced entirely has to be
  read from the page.
- **Answer key letters:** the reader often can't read the key's hand-lettered
  A, and sometimes misreads it as another letter. Look at each unreadable
  square; don't assume.
- **Clue type:** c is often read as e ("eall", "Chieago"); type is often
  broken or faint, which is a correction, not "sic".
- **Bylines** are a name and a town ("Chicago, Ill."); the reader slips on
  them (Ilinois, IU., Leuis, Broun for Brown).
- **Clues with no text:** a clue can be printed as symbols (D23 "\* \* \*" for
  ASTERISKS), or sit at the foot of the previous column, above the list.
  Crop its place with box: before deciding. In 1930 the Down list is often
  on another page the packet doesn't have: text.md says "clue list continues
  on another page"; escalate it.
- **Changing the grid:** change a square (grid:rNcM) only when the scan clearly shows
  the OCR got it wrong, and check the numbers printed in the grid itself (grid:all)
  against the numbering you get: the printed numbers are the proof. A fix that
  invents an entry nobody printed a clue for (and "[no clue printed]" to
  cover it) is almost always a wrong grid fix. `finish` compares the numbering
  before and after your fix and warns when it gets worse (1931-05-02 and
  1934-12-01b each got a black square the scan doesn't have).
- **Shapes:** a few puzzles are not rectangles (a heart, a diamond), and some
  1929 grids really are asymmetric. Check the whole grid (grid:all) before
  calling either a reading error.
