#!/usr/bin/env python3
import sys
import re
import datetime
from pathlib import Path
import bibtexparser

ROOT = Path(__file__).resolve().parent.parent

def slugify(title, year):
    head = re.split(r"[:\-–]", title)[0].lower()
    words = [w for w in re.findall(r"[a-z0-9]+", head) if w not in {"a", "an", "the", "of", "for", "and", "with", "in", "on", "to", "via"}]
    return "-".join(words[:4] or ["paper"]) + (f"-{year}" if year else "")

def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python process_issue.py <issue_body_file>")
        
    issue_body_path = Path(sys.argv[1])
    body = issue_body_path.read_text(encoding='utf-8')
    
    # Extract fields from the issue form body
    link_match = re.search(r'### Link to the paper\s*\n(.*?)\n', body)
    bibtex_match = re.search(r'### BibTeX\s*\n```[a-z]*\n(.*?)\n```', body, re.DOTALL)
    if not bibtex_match:
        bibtex_match = re.search(r'### BibTeX\s*\n(.*?)\n###', body, re.DOTALL)
        
    area_match = re.search(r'### Area\s*\n(.*?)\n', body)
    
    if not bibtex_match:
        sys.exit("Could not find BibTeX in the issue body.")
        
    bibtex_str = bibtex_match.group(1).strip()
    link_str = link_match.group(1).strip() if link_match else ""
    area_str = area_match.group(1).strip() if area_match else ""
    
    # Parse BibTeX
    parser = bibtexparser.bparser.BibTexParser(common_strings=True)
    bib_database = bibtexparser.loads(bibtex_str, parser=parser)
    
    if not bib_database.entries:
        sys.exit("BibTeX parser found no entries.")
        
    entry = bib_database.entries[0]
    
    title = entry.get('title', 'Unknown Title').replace('{', '').replace('}', '').replace('\n', ' ')
    authors_raw = entry.get('author', 'Unknown Author').replace('\n', ' ')
    authors = [a.strip() for a in authors_raw.split(' and ')]
    year = entry.get('year', '')
    venue = entry.get('journal', entry.get('booktitle', entry.get('publisher', '')))
    
    slug = slugify(title, year)
    path = ROOT / "src" / "content" / "papers" / f"{slug}.yml"
    
    if path.exists():
        print(f"File {slug}.yml already exists. Updating might be needed manually.")
        slug = f"{slug}-new"
        path = ROOT / "src" / "content" / "papers" / f"{slug}.yml"

    quoted_authors = [f'"{a}"' if any(c in a for c in ",:") else a for a in authors]
    authors_str = "[" + ", ".join(quoted_authors) + "]"
    
    arxiv_id = ""
    if "arxiv.org" in link_str:
        m = re.search(r"(\d{4}\.\d{4,5})", link_str)
        if m:
            arxiv_id = m.group(1)
            
    content = f"""id: {slug}
title: "{title}"
authors: {authors_str}
year: {year or "null"}
venue: "{venue}"
arxiv: "{arxiv_id}"
links:
  paper: "{link_str}"
area: "{area_str}"
topics: []
capability: []
level: []
type: []
infra: []
domain: [general]
status: triaged
added: {datetime.date.today().isoformat()}
"""
    path.write_text(content, encoding="utf-8")
    print(f"Created {path.relative_to(ROOT)}")
    
    # Save slug for GitHub Action output
    Path("output_slug.txt").write_text(slug)

if __name__ == "__main__":
    main()
