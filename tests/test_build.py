"""Tests for the Gentle Accountability Friendship Kit.

Every sheet must build a valid, non-trivial PDF into printables/.
PDFs are checked structurally (header, trailer, page count, size)
using pypdf, with no network access and no signups required.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
SHEETS_DIR = ROOT / "src" / "sheets"
OUT_DIR = ROOT / "printables"

SHEETS = sorted(SHEETS_DIR.glob("*.html"))
SHEET_IDS = [s.stem for s in SHEETS]


def test_sheets_exist():
    assert SHEETS, f"no HTML sheets found in {SHEETS_DIR}"
    assert len(SHEETS) == 7, f"expected 7 sheets, found {len(SHEETS)}: {SHEET_IDS}"


@pytest.fixture(scope="session")
def built_pdfs():
    """Build all sheets once per test session."""
    result = subprocess.run(
        [sys.executable, str(ROOT / "build.py"), "--clean"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert result.returncode == 0, f"build failed:\n{result.stdout}\n{result.stderr}"
    produced = sorted(p for p in OUT_DIR.glob("*.pdf"))
    assert {p.stem for p in produced} == set(SHEET_IDS), (
        f"expected {SHEET_IDS}, built {[p.stem for p in produced]}"
    )
    return {p.stem: p for p in produced}


@pytest.fixture(scope="session")
def pdf_texts(built_pdfs):
    texts = {}
    for stem, path in built_pdfs.items():
        reader = PdfReader(str(path))
        texts[stem] = (reader, "".join(page.extract_text() or "" for page in reader.pages))
    return texts


def _is_valid_pdf(path: Path) -> None:
    data = path.read_bytes()
    assert data.startswith(b"%PDF-"), f"{path.name} missing %PDF header"
    assert b"%%EOF" in data[-256:], f"{path.name} missing %%EOF trailer"
    assert len(data) > 2000, f"{path.name} suspiciously small ({len(data)} bytes)"


@pytest.mark.parametrize("stem", SHEET_IDS)
class TestSheetPdf:
    def test_valid_structure(self, built_pdfs, stem):
        _is_valid_pdf(built_pdfs[stem])

    def test_has_pages(self, built_pdfs, stem):
        reader = PdfReader(str(built_pdfs[stem]))
        assert len(reader.pages) >= 1, f"{stem}.pdf has no pages"

    def test_has_visible_text(self, pdf_texts, stem):
        _, text = pdf_texts[stem]
        assert len(text.strip()) > 100, f"{stem}.pdf has almost no extractable text"

    def test_has_kind_usage_notes(self, pdf_texts, stem):
        _, text = pdf_texts[stem]
        assert "how to use this sheet, kindly" in text.lower(), (
            f"{stem}.pdf is missing its kind usage notes"
        )

    def test_unbranded(self, built_pdfs, pdf_texts, stem):
        """PDFs are unbranded: no company name in metadata or page content."""
        reader, text = pdf_texts[stem]
        meta = reader.metadata or {}
        meta_text = " ".join(str(v) for v in meta.values()).lower()
        assert "asdale" not in meta_text, f"{stem}.pdf leaks branding in metadata"
        assert "asdale" not in text.lower(), f"{stem}.pdf leaks branding in page text"

    def test_no_tracking_urls(self, built_pdfs, stem):
        """No external links: these sheets work offline, forever."""
        reader = PdfReader(str(built_pdfs[stem]))
        for page in reader.pages:
            annots = page.get("/Annots")
            if annots:
                for annot in annots:
                    action = annot.get_object().get("/A", {})
                    uri = action.get("/URI", "")
                    assert not uri, f"{stem}.pdf contains a link: {uri}"


def test_full_build_all_sheets(built_pdfs):
    """The build script ran clean and produced every PDF."""
    for stem, path in built_pdfs.items():
        _is_valid_pdf(path)


def test_no_secrets_in_sources():
    """No API keys or secrets anywhere in the source tree."""
    pattern = re.compile(
        r"(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]{8,}",
        re.IGNORECASE,
    )
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts or "printables" in path.parts:
            continue
        text = path.read_text(errors="ignore")
        assert not pattern.search(text), f"possible secret in {path}"
