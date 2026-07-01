# -*- coding: utf-8 -*-
"""knowledge_updater.py — self-improving knowledge pipeline for the `pcb-design-assistant` skill.

Pattern (per CLAUDE.md):
  1. crawl4ai -> fetch latest papers from ArXiv / domain sources
  2. WebSearch -> latest news/reports from authoritative domain sources
  3. parse  -> title, authors, date, DOI/URL, abstract, key findings
  4. score  -> recency + domain-keyword relevance
  5. append -> scored entries to SECOND-KNOWLEDGE-BRAIN.md (date-stamped)
  6. dedupe -> skip entries already present (URL/DOI hash)

Designed to degrade gracefully: if crawl4ai or network is unavailable it logs and
no-ops rather than corrupting the brain. Recommended schedule: weekly cron.
"""
import os
import re
import sys
import json
import hashlib
import datetime
import urllib.parse
import urllib.request

BRAIN = os.path.join(os.path.dirname(__file__), "..", "SECOND-KNOWLEDGE-BRAIN.md")

ARXIV_CATEGORIES = ['eess.SP']
SEARCH_QUERIES = ['PCB signal integrity return path', 'power distribution network decoupling capacitor placement', 'PCB EMC design guidelines', 'IPC trace width current capacity']
DOMAINS = ['ipc.org', 'ti.com', 'analog.com']
KEYWORDS = [w.lower() for q in SEARCH_QUERIES for w in q.split()]


def _hash(s):
    return hashlib.sha1(s.encode("utf-8", "ignore")).hexdigest()[:12]


def _existing_hashes():
    if not os.path.exists(BRAIN):
        return set()
    with open(BRAIN, encoding="utf-8") as f:
        txt = f.read()
    return set(re.findall(r"<!--h:([0-9a-f]{12})-->", txt))


def fetch_arxiv(category, max_results=15):
    """Query the ArXiv Atom API for a category. Returns list of entry dicts."""
    base = "http://export.arxiv.org/api/query"
    q = "cat:" + category
    url = base + "?" + urllib.parse.urlencode(
        {"search_query": q, "sortBy": "submittedDate", "sortOrder": "descending",
          "max_results": max_results})
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = r.read().decode("utf-8", "ignore")
    except Exception as e:  # graceful degradation
        print("[warn] arxiv fetch failed for %s: %s" % (category, e))
        return []
    entries = []
    for block in re.findall(r"<entry>(.*?)</entry>", data, re.S):
        def g(tag):
            m = re.search(r"<%s>(.*?)</%s>" % (tag, tag), block, re.S)
            return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
        title = g("title")
        summary = g("summary")
        published = g("published")[:10]
        link = ""
        m = re.search(r'<id>(.*?)</id>', block, re.S)
        if m:
            link = m.group(1).strip()
        authors = ", ".join(re.findall(r"<name>(.*?)</name>", block))
        if title:
            entries.append({"title": title, "authors": authors, "date": published,
                            "url": link, "abstract": summary})
    return entries


def relevance(entry):
    """Score = recency weight + keyword-match density."""
    text = (entry["title"] + " " + entry["abstract"]).lower()
    kw = sum(1 for k in set(KEYWORDS) if k in text)
    try:
        d = datetime.date.fromisoformat(entry["date"])
        age_days = (datetime.date.today() - d).days
        rec = max(0.0, 1.0 - age_days / 730.0)  # 2-year decay
    except Exception:
        rec = 0.0
    return kw + 2.0 * rec


def crawl4ai_domains():
    """Optional: use crawl4ai to pull authoritative domain pages. No-op if not installed."""
    try:
        from crawl4ai import WebCrawler  # type: ignore
    except Exception:
        print("[info] crawl4ai not installed; skipping domain crawl (graceful degradation).")
        return []
    out = []
    crawler = WebCrawler()
    crawler.warmup()
    for d in DOMAINS:
        try:
            res = crawler.run(url="https://" + d)
            out.append({"title": "Domain scan: " + d, "authors": "", "date": str(datetime.date.today()),
                         "url": "https://" + d, "abstract": (res.markdown or "")[:400]})
        except Exception as e:
            print("[warn] crawl4ai failed for %s: %s" % (d, e))
    return out


def append_entries(entries):
    existing = _existing_hashes()
    new_rows, log_lines = [], []
    for e in sorted(entries, key=relevance, reverse=True):
        key = _hash(e["url"] or e["title"])
        if key in existing:
            continue
        existing.add(key)
        row = "| {t} | {a} | {y} | ArXiv/Web | {u} | score={s:.2f} <!--h:{h}--> |".format(
            t=e["title"][:90].replace("|", "/"), a=(e["authors"][:40] or "-"),
            y=(e["date"][:4] or "-"), u=e["url"] or "-", s=relevance(e), h=key)
        new_rows.append(row)
        log_lines.append("- %s — added: %s" % (datetime.date.today().isoformat(), e["title"][:90]))
    if not new_rows:
        print("[info] no new entries to append.")
        return
    with open(BRAIN, "a", encoding="utf-8") as f:
        f.write("\n<!-- auto-appended %s -->\n" % datetime.date.today().isoformat())
        f.write("\n".join(new_rows) + "\n")
        f.write("\n".join(log_lines) + "\n")
    print("[ok] appended %d new entries." % len(new_rows))


def main():
    entries = []
    for cat in ARXIV_CATEGORIES:
        entries += fetch_arxiv(cat)
    entries += crawl4ai_domains()
    if not entries:
        print("[info] nothing fetched (offline?). Brain left unchanged.")
        return
    append_entries(entries)


if __name__ == "__main__":
    main()
