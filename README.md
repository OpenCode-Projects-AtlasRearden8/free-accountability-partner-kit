# Gentle Accountability Friendship Kit

Free printables for starting and keeping a gentle accountability friendship.
No signups, no tracking, no apps &mdash; just paper, a pen, and a friend.

Made by [Asdale Dynamics, LLC](https://dylanasdale.github.io) &mdash; AI explained
"like a friend would": plain English, step by step, never condescending.

## The seven sheets

| Sheet | What it's for |
|---|---|
| **Find-a-Buddy Pitch Script** | A kind, low-pressure way to ask someone to be your accountability friend |
| **First-Call Agenda Card** | Twenty friendly minutes for your very first check-in |
| **Weekly Fifteen-Minute Check-In** | One page per week: two wins, one wobble, one small next thing |
| **Promise-Made-Visible Slips** | Cut-out slips: one small promise each, visible where you'll see it |
| **Restart Without Shame** | For the week everything fell apart (it happens to everyone) |
| **Long-Distance Postcard Prompts** | Six prompts for mailing a monthly check-in to a faraway buddy |
| **Season-End Celebration** | Mark a season of showing up, restarts counted proudly |

Every sheet carries its own **kind usage notes** &mdash; a short box explaining how
to use it gently, printed right on the page.

The PDFs are **unbranded**: no logos, no names, no links. Print them, share them,
hand them to a friend.

## Build it yourself

Requirements: Python 3.10+ and [WeasyPrint](https://weasyprint.org/) (`pip install weasyprint`).

```bash
python3 build.py            # renders src/sheets/*.html -> printables/*.pdf
python3 build.py --clean    # wipes printables/ first
```

Output goes to `printables/` as print-ready PDFs (US Letter, works fine on A4).

## Run the tests

```bash
pip install pytest pypdf
pytest
```

Tests verify that every sheet builds a valid PDF with visible text and its kind
usage notes, that the PDFs are unbranded and link-free, and that no secrets
appear in the sources.

## Layout of this repo

```
build.py                  one build script (WeasyPrint)
src/sheets/*.html         the seven sheets, plain HTML
src/css/kit.css           shared print stylesheet
printables/               built PDFs (unbranded, ready to print)
tests/                    pytest suite
```

## License

MIT &mdash; see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.
Print, copy, and share freely.
