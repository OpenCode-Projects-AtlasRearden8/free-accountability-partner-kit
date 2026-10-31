# STATUS

## What was built

The **Gentle Accountability Friendship Kit**: seven free, unbranded printables for
starting and keeping a gentle accountability friendship, built from HTML/CSS with
one build script (WeasyPrint) and verified by a pytest suite.

Sheets (each carries its own "How to use this sheet, kindly" usage notes printed
on the page):

1. **Find-a-Buddy Pitch Script** — a three-piece, low-pressure ask
2. **First-Call Agenda Card** — twenty friendly minutes, three parts
3. **Weekly Fifteen-Minute Check-In** — two wins, one wobble, one small next thing (with a spare copy page)
4. **Promise-Made-Visible Slips** — cut-out slips, one small promise each
5. **Restart Without Shame** — for the week everything fell apart
6. **Long-Distance Postcard Prompts** — six prompts for mailed check-ins
7. **Season-End Celebration** — mark a season of showing up, restarts counted proudly

All PDFs are unbranded (no logos, names, or links), US Letter, print fine on A4.

## How to run it

```bash
python3 build.py            # build all sheets -> printables/*.pdf
python3 build.py --clean    # wipe printables/ first
pip install pytest pypdf && pytest   # run the test suite
```

Requires Python 3.10+ and WeasyPrint (tests also need pytest + pypdf).

## Verification results

- `python3 build.py --clean` — builds all 7 sheets, exit 0
- `pytest` — **45 passed** (0 failures) as of the commit below
- Tests verify per sheet: valid PDF structure (%PDF header + %%EOF trailer,
  non-trivial size), at least one page, extractable visible text, presence of
  kind usage notes, no branding in metadata or page content, and zero link
  annotations (works fully offline)
- A repo-wide scan confirms no secrets/API keys/personal data in sources

## Known gaps

- PDFs are Letter-sized; no separate A4 variant (A4 printers can "fit to page")
- Text extraction in tests relies on WeasyPrint's text layer; a purely graphical
  redesign would need updated assertions
- No dark/print-ink-saving "compact" variant of the sheets
- No prebuilt PDF verification in CI (no CI configured in this repo)
- Postcard prompts assume standard 4x6 postcards; no cut guides included
