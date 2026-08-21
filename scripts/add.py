#!/usr/bin/env python3
"""Crea una ficha desde un id o URL de arXiv.

    python scripts/add.py 2210.03629
    python scripts/add.py https://arxiv.org/abs/2303.11366

Baja título, autores y año de la API de arXiv y deja los campos de
clasificación vacíos con status: captured. Vos ponés area, level y type.
"""
import datetime
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NS = {"a": "http://www.w3.org/2005/Atom"}
STOP = {"a", "an", "the", "of", "for", "and", "with", "in", "on", "to", "via"}


def arxiv_id(raw):
    match = re.search(r"(\d{4}\.\d{4,5})(v\d+)?", raw)
    if not match:
        sys.exit(f"No pude extraer un id de arXiv de '{raw}'")
    return match.group(1)


def fetch(aid):
    url = f"http://export.arxiv.org/api/query?id_list={aid}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        entry = ET.fromstring(resp.read()).find("a:entry", NS)
    if entry is None:
        sys.exit(f"arXiv no devolvió nada para {aid}")
    title = " ".join(entry.findtext("a:title", "", NS).split())
    authors = [a.findtext("a:name", "", NS) for a in entry.findall("a:author", NS)]
    published = entry.findtext("a:published", "", NS)
    return title, authors, int(published[:4]) if published else None


def slugify(title, year):
    head = re.split(r"[:\-–]", title)[0].lower()
    words = [w for w in re.findall(r"[a-z0-9]+", head) if w not in STOP]
    return "-".join(words[:4] or ["paper"]) + (f"-{year}" if year else "")


def yaml_list(values):
    return "[" + ", ".join(values) + "]"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    aid = arxiv_id(sys.argv[1])
    title, authors, year = fetch(aid)
    slug = sys.argv[2] if len(sys.argv) > 2 else slugify(title, year)
    path = ROOT / "papers" / f"{slug}.yml"
    if path.exists():
        sys.exit(f"Ya existe {path.relative_to(ROOT)}")

    quoted = [f'"{a}"' if any(c in a for c in ",:") else a for a in authors]
    path.write_text(
        f"id: {slug}\n"
        f'title: "{title}"\n'
        f"authors: {yaml_list(quoted)}\n"
        f"year: {year}\n"
        f'venue: "arXiv preprint"   # completar si tiene venue\n'
        f'arxiv: "{aid}"\n'
        f"links:\n"
        f"  paper: https://arxiv.org/abs/{aid}\n\n"
        f"# --- triage: con estos tres campos ya entra al índice ---\n"
        f"area:            # ver taxonomy.yml\n"
        f"level: []        # single-agent | multi-agent | human-agent\n"
        f"type: []         # survey | method | benchmark | framework | ...\n\n"
        f"# --- al leerlo ---\n"
        f"topics: []\ncapability: []\ninfra: []\ndomain: [general]\n"
        f'tldr: ""\nnotes: ""\nrelates_to: []\nevaluated_on: []\n\n'
        f"status: captured\n"
        f"added: {datetime.date.today().isoformat()}\n",
        encoding="utf-8",
    )
    print(f"creado papers/{slug}.yml — completá area, level y type")


if __name__ == "__main__":
    main()
