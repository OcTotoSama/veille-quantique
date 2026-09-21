"""Point d'entrée : collecte -> filtre -> analyse -> Markdown -> PDF."""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from src.analyze import analyze_articles
from src.collect import collect_last_days
from src.filter import filter_articles
from src.generate_pdf import markdown_to_pdf

ROOT = Path(__file__).resolve().parents[1]


def create_markdown(articles: list[dict], output: Path, days: int) -> None:
    lines = [f"# Veille informatique quantique - {date.today().isoformat()}", "",
             f"Période analysée : les {days} derniers jours. Articles retenus : {len(articles)}.",
             "", "## Synthèse"]
    if not articles:
        lines.append("Aucun article n'a été retenu pour cette période. Vérifier les sources et les mots-clés.")
    for index, article in enumerate(articles, start=1):
        a = article["analysis"]
        lines += ["", f"## {index}. {article['title']}",
                  f"Source : [{article['source']}]({article['url']}) - publié le {article['published'][:10]}",
                  f"Scores : pertinence {a['relevance']}/100 | nouveauté {a['novelty']}/100 | importance {a['importance']}/100 | score {article['score']}/100.",
                  f"Catégorie : {a['category']} - Qualité de la source : {a['source_quality']}.",
                  "", a["summary"], "", f"Pourquoi c'est important : {a['why_it_matters']}",
                  f"Mots-clés détectés : {', '.join(article['keyword_hits'])}."]
    lines += ["", "## Méthode", "Collecte Inoreader/RSS, filtre lexical documenté, puis analyse assistée par IA. Les liens vers les sources permettent la vérification."]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Génère la veille quantique hebdomadaire.")
    parser.add_argument("--days", type=int, default=7, help="Nombre de jours à analyser (défaut : 7).")
    parser.add_argument("--limit", type=int, default=10, help="Maximum d'articles dans le rapport.")
    parser.add_argument("--model", default="gpt-4o-mini", help="Modèle OpenAI utilisé.")
    args = parser.parse_args()
    reports = ROOT / "reports"; reports.mkdir(exist_ok=True)
    articles = filter_articles(collect_last_days(args.days))
    articles = analyze_articles(articles, args.model)[:args.limit]
    stem = date.today().isoformat()
    md_path, pdf_path = reports / f"{stem}.md", reports / f"{stem}.pdf"
    create_markdown(articles, md_path, args.days)
    markdown_to_pdf(md_path, pdf_path)
    print(f"Rapport créé : {md_path} et {pdf_path}")


if __name__ == "__main__":
    main()
