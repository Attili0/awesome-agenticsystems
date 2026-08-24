"""scripts/arxiv.py — id parsing and the API response shape.

The network is mocked throughout. Besides the usual reason, the real API
answers repeated calls with a 429, which is exactly what a test suite does.
"""
import io
import urllib.error

import pytest

import arxiv


# --- extract_id / is_arxiv_link -------------------------------------------
# These decide whether the issue form may skip BibTeX, so a wrong answer here
# either demands BibTeX needlessly or tries to fetch a non-arXiv link.

@pytest.mark.parametrize(
    "raw, expected",
    [
        ("2210.03629", "2210.03629"),
        ("2210.03629v3", "2210.03629"),
        ("https://arxiv.org/abs/2303.11366", "2303.11366"),
        ("https://arxiv.org/abs/2303.11366v2", "2303.11366"),
        ("https://arxiv.org/pdf/2305.10601", "2305.10601"),
        ("http://ARXIV.ORG/abs/2406.12045", "2406.12045"),
        # Five-digit sequence numbers exist and must not be truncated.
        ("https://arxiv.org/abs/2608.19741", "2608.19741"),
        ("https://aclanthology.org/2023.emnlp-main.123/", None),
        ("", None),
        (None, None),
    ],
)
def test_extract_id(raw, expected):
    assert arxiv.extract_id(raw) == expected


@pytest.mark.parametrize(
    "link, expected",
    [
        ("https://arxiv.org/abs/2210.03629", True),
        ("https://ARXIV.org/abs/2210.03629", True),
        # arXiv host but no parseable id: BibTeX is still required.
        ("https://arxiv.org/list/cs.AI/recent", False),
        ("https://openreview.net/forum?id=abc", False),
        ("", False),
        (None, False),
    ],
)
def test_is_arxiv_link(link, expected):
    assert arxiv.is_arxiv_link(link) is expected


# --- fetch -----------------------------------------------------------------

ENTRY = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/2210.03629v3</id>
    <published>2022-10-06T00:00:00Z</published>
    <title>ReAct: Synergizing Reasoning
      and Acting in Language Models</title>
    <author><name>Shunyu Yao</name></author>
    <author><name>Jeffrey Zhao</name></author>
    {journal_ref}
  </entry>
</feed>"""

# A bad id still returns HTTP 200; the entry title is the only signal.
ERROR_FEED = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/api/errors</id>
    <title>Error</title>
    <summary>incorrect id format</summary>
  </entry>
</feed>"""

EMPTY_FEED = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"></feed>"""


def serve(monkeypatch, payload):
    class Response(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            self.close()

    monkeypatch.setattr(
        arxiv.urllib.request, "urlopen",
        lambda url, timeout=None: Response(payload.encode("utf-8")),
    )


def test_fetch_parses_entry(monkeypatch):
    serve(monkeypatch, ENTRY.format(journal_ref=""))
    title, authors, year, venue = arxiv.fetch("2210.03629")

    # Whitespace in the XML must not survive into the record: the title is
    # written straight into the .yml.
    assert title == "ReAct: Synergizing Reasoning and Acting in Language Models"
    assert authors == ["Shunyu Yao", "Jeffrey Zhao"]
    assert year == 2022
    # A preprint has no journal_ref, and the schema rejects an empty venue, so
    # the caller needs an empty string to know to omit the key.
    assert venue == ""


def test_fetch_reads_journal_ref_as_venue(monkeypatch):
    serve(monkeypatch, ENTRY.format(
        journal_ref="<arxiv:journal_ref>ICLR 2023</arxiv:journal_ref>"))
    assert arxiv.fetch("2210.03629")[3] == "ICLR 2023"


def test_fetch_rejects_error_entry(monkeypatch):
    serve(monkeypatch, ERROR_FEED)
    with pytest.raises(arxiv.ArxivError, match="returned nothing"):
        arxiv.fetch("9999.99999")


def test_fetch_rejects_empty_feed(monkeypatch):
    serve(monkeypatch, EMPTY_FEED)
    with pytest.raises(arxiv.ArxivError, match="returned nothing"):
        arxiv.fetch("9999.99999")


def test_fetch_wraps_network_failure(monkeypatch):
    def boom(url, timeout=None):
        raise urllib.error.URLError("no route to host")

    monkeypatch.setattr(arxiv.urllib.request, "urlopen", boom)
    # ArxivError and not URLError: process_issue turns this into an issue
    # comment telling the contributor to paste BibTeX instead.
    with pytest.raises(arxiv.ArxivError, match="could not reach"):
        arxiv.fetch("2210.03629")
