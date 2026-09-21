"""Analyse des articles par l'API OpenAI avec repli sans IA pour les tests locaux."""
from __future__ import annotations

import json
import os
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]


def _fallback(article: dict) -> dict:
    excerpt = article["content"].replace("\n", " ")[:500]
    return {"relevance": min(100, 55 + 8 * len(article.get("keyword_hits", []))), "novelty": 50,
            "importance": 50, "summary": excerpt or "Résumé indisponible : consulter la source.",
            "why_it_matters": "Article sélectionné par les mots-clés de la veille.",
            "category": "recherche", "source_quality": "secondaire"}


def analyze_articles(articles: list[dict], model: str = "gpt-4o-mini") -> list[dict]:
    prompt = (ROOT / "prompts" / "analyse.txt").read_text(encoding="utf-8")
    client = OpenAI() if os.getenv("OPENAI_API_KEY") else None
    analyzed = []
    for article in articles:
        if client:
            payload = json.dumps({key: article[key] for key in ("title", "source", "url", "published", "content")}, ensure_ascii=False)
            response = client.chat.completions.create(model=model, temperature=0.2,
                response_format={"type": "json_object"}, messages=[{"role": "system", "content": prompt}, {"role": "user", "content": payload}])
            verdict = json.loads(response.choices[0].message.content)
        else:
            verdict = _fallback(article)
        article["analysis"] = verdict
        article["score"] = round(0.45 * verdict["relevance"] + 0.25 * verdict["novelty"] + 0.30 * verdict["importance"])
        analyzed.append(article)
    return sorted(analyzed, key=lambda item: item["score"], reverse=True)
