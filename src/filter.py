"""Filtrage transparent, utile à expliquer dans le portfolio."""
from __future__ import annotations

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def filter_articles(articles: list[dict]) -> list[dict]:
    rules = yaml.safe_load((ROOT / "config" / "keywords.yml").read_text(encoding="utf-8"))
    kept = []
    for article in articles:
        haystack = f"{article['title']} {article['content']}".lower()
        primary_hits = [word for word in rules["primary"] if word.lower() in haystack]
        secondary_hits = [word for word in rules.get("secondary", []) if word.lower() in haystack]
        excluded = any(word.lower() in haystack for word in rules.get("exclude", []))
        if primary_hits and not excluded:
            article["keyword_hits"] = primary_hits + secondary_hits
            kept.append(article)
    return kept
