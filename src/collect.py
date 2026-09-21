"""Collecte Inoreader et RSS, puis normalisation des articles."""
from __future__ import annotations

import hashlib
import os
from datetime import UTC, datetime, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path

import feedparser
import requests
import yaml


ROOT = Path(__file__).resolve().parents[1]


def _date(value: str | None) -> datetime:
    if not value:
        return datetime.now(UTC)
    try:
        value_dt = parsedate_to_datetime(value)
        return value_dt.astimezone(UTC) if value_dt.tzinfo else value_dt.replace(tzinfo=UTC)
    except (TypeError, ValueError):
        return datetime.now(UTC)


def _article(title: str, link: str, published: datetime, source: str, content: str) -> dict:
    return {
        "id": hashlib.sha256(f"{link}|{title}".encode()).hexdigest()[:16],
        "title": title.strip(), "url": link.strip(), "published": published.isoformat(),
        "source": source, "content": content.strip()[:12000],
    }


def collect_inoreader(settings: dict, since: datetime) -> list[dict]:
    token = os.getenv("INOREADER_ACCESS_TOKEN")
    if not token:
        return []
    url = f"{settings['base_url'].rstrip('/')}/stream/contents/{settings['stream_id']}"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"}, params={"n": 1000}, timeout=30)
    response.raise_for_status()
    articles = []
    for item in response.json().get("items", []):
        published = datetime.fromtimestamp(float(item.get("crawlTimeMsec", 0)) / 1000, tz=UTC)
        if published < since:
            continue
        alternate = item.get("alternate", [{}])[0]
        articles.append(_article(item.get("title", "Sans titre"), alternate.get("href", ""), published,
                                 item.get("origin", {}).get("title", "Inoreader"), item.get("summary", {}).get("content", "")))
    return articles


def collect_rss(sources: list[dict], since: datetime) -> list[dict]:
    articles = []
    for source in sources:
        feed = feedparser.parse(source["url"])
        for entry in feed.entries:
            published = _date(entry.get("published") or entry.get("updated"))
            if published >= since:
                articles.append(_article(entry.get("title", "Sans titre"), entry.get("link", ""), published,
                                         source["name"], entry.get("summary", "") or entry.get("description", "")))
    return articles


def collect_last_days(days: int = 7) -> list[dict]:
    settings = yaml.safe_load((ROOT / "config" / "sources.yml").read_text(encoding="utf-8"))
    since = datetime.now(UTC) - timedelta(days=days)
    articles = []
    if settings.get("inoreader", {}).get("enabled", False):
        articles.extend(collect_inoreader(settings["inoreader"], since))
    articles.extend(collect_rss(settings.get("rss_fallback", []), since))
    unique = {article["id"]: article for article in articles if article["url"]}
    return sorted(unique.values(), key=lambda item: item["published"], reverse=True)
