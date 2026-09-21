"""Transforme le Markdown du rapport en PDF léger et lisible."""
from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def markdown_to_pdf(markdown_path: Path, pdf_path: Path) -> None:
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="ReportTitle", parent=styles["Title"], textColor=HexColor("#143A5C"), spaceAfter=14))
    styles.add(ParagraphStyle(name="ReportH2", parent=styles["Heading2"], textColor=HexColor("#143A5C"), spaceBefore=12, spaceAfter=7))
    styles.add(ParagraphStyle(name="ReportBody", parent=styles["BodyText"], leading=14, spaceAfter=7))
    story = []
    for raw in markdown_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            story.append(Spacer(1, 4)); continue
        if line.startswith("# "):
            story.append(Paragraph(_escape(line[2:]), styles["ReportTitle"]))
        elif line.startswith("## "):
            story.append(Paragraph(_escape(line[3:]), styles["ReportH2"]))
        elif line.startswith("- "):
            story.append(Paragraph("• " + _escape(line[2:]), styles["ReportBody"]))
        else:
            # Le rapport contient du texte provenant de sites externes : l'échapper avant
            # de le passer au mini-langage XML de ReportLab.
            line = _escape(line)
            line = re.sub(r"\[([^]]+)\]\(([^)]+)\)", r'<link href="\2" color="#1A5F8C">\1</link>', line)
            story.append(Paragraph(line, styles["ReportBody"]))
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=1.8*cm, bottomMargin=1.8*cm)
    doc.build(story)
