#!/usr/bin/env python3
"""Create the downloadable CV from the data used by the Jekyll site."""
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, Frame, KeepTogether, PageTemplate, Paragraph, Spacer
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "_data" / "cv.json"
OUTPUT = ROOT / "assets" / "Kieron-Harding-CV.pdf"

INK = colors.HexColor("#10231f")
TEAL = colors.HexColor("#0d6057")
MUTED = colors.HexColor("#587068")
LIME = colors.HexColor("#c8f04c")
LINE = colors.HexColor("#d9e1d9")


def p(text, style):
    return Paragraph(text, style)


def header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(LINE)
    canvas.line(18 * mm, height - 14 * mm, width - 18 * mm, height - 14 * mm)
    canvas.setFont("Helvetica-Bold", 7)
    canvas.setFillColor(TEAL)
    canvas.drawString(18 * mm, height - 10 * mm, "KIERON HARDING  /  LEAD PLATFORM ENGINEER")
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(width - 18 * mm, 11 * mm, f"KIERON.XYZ  ·  {doc.page}")
    canvas.restoreState()


def main():
    cv = json.loads(DATA.read_text())
    OUTPUT.parent.mkdir(exist_ok=True)
    doc = BaseDocTemplate(str(OUTPUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                          topMargin=21 * mm, bottomMargin=17 * mm)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="body")
    doc.addPageTemplates([PageTemplate(id="cv", frames=[frame], onPage=header_footer)])
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Name", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=29,
                              leading=31, textColor=INK, spaceAfter=3))
    styles.add(ParagraphStyle(name="CVTitle", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=11,
                              leading=14, textColor=TEAL, spaceAfter=10))
    styles.add(ParagraphStyle(name="Summary", parent=styles["Normal"], fontSize=10.2, leading=14.5,
                              textColor=INK, spaceAfter=13))
    styles.add(ParagraphStyle(name="Kicker", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=7.2,
                              leading=10, textColor=TEAL, spaceBefore=11, spaceAfter=4, tracking=1.2))
    styles.add(ParagraphStyle(name="Role", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=11,
                              leading=13, textColor=INK))
    styles.add(ParagraphStyle(name="Company", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=8.7,
                              leading=11, textColor=TEAL, alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name="Period", parent=styles["Normal"], fontSize=7.5, leading=10, textColor=MUTED,
                              alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name="Body", parent=styles["Normal"], fontSize=8.2, leading=10.4,
                              textColor=colors.HexColor("#38514a"), leftIndent=8, firstLineIndent=-8, spaceAfter=1))
    styles.add(ParagraphStyle(name="Project", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=10,
                              leading=12, textColor=INK, spaceBefore=5, spaceAfter=2))
    styles.add(ParagraphStyle(name="Small", parent=styles["Normal"], fontSize=8.2, leading=10.4, textColor=MUTED,
                              spaceAfter=2))

    story = [p(cv["name"], styles["Name"]), p(cv["title"], styles["CVTitle"]),
             p(cv["summary"], styles["Summary"]),
             p(f'<b>{cv["location"]}</b>  ·  <b>{cv["contact"]["email"]}</b>  ·  {cv["contact"]["linkedin"]}', styles["Small"]),
             p("EXPERIENCE", styles["Kicker"])]
    for role in cv["roles"]:
        details = [p(f'<b>{item["label"]}.</b> {item["detail"]}', styles["Body"]) for item in role["achievements"]]
        block = [p(role["title"], styles["Role"]), p(f'{role["company"]}  ·  {role["period"]}', styles["Small"])] + details + [Spacer(1, 3)]
        story.append(KeepTogether(block))
    story += [p("SELECTED IMPACT", styles["Kicker"])]
    for project in cv["projects"]:
        outcomes = " · ".join(project["outcomes"])
        story.append(KeepTogether([p(project["name"], styles["Project"]), p(project["description"], styles["Small"]), p(f"<b>Outcomes:</b> {outcomes}", styles["Small"])]))
    skills = "  ·  ".join(skill["name"] for skill in cv["skills"])
    story += [p("CAPABILITIES", styles["Kicker"]), p(skills, styles["Small"])]
    doc.build(story)
    pages = len(PdfReader(str(OUTPUT)).pages)
    if pages != 1:
        raise RuntimeError(f"CV PDF must fit on one page; generated {pages} pages")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
