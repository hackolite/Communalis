#!/usr/bin/env python3
"""Build the French Communalis field-book PDF from its editable text sources."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parent
PRODUCT_SOURCES = (
    "Livre_Introduction.txt",
    "Livre_Parcours_Produit.txt",
    "Livre_Annexes.txt",
)
TECHNICAL_SOURCES = (
    "Livre_Partie_A.txt",
    "Livre_Partie_B.txt",
    "Livre_Partie_C.txt",
    "Livre_Partie_D.txt",
    "Livre_Partie_E.txt",
    "Livre_Partie_F.txt",
    "Livre_Annexes.txt",
)
SOURCES = PRODUCT_SOURCES
PLACEHOLDER = re.compile(
    r"\[(?:À ACTUALISER|À CONFIRMER|RÉSULTATS TOGO À INSÉRER|"
    r"à compléter|à remplir|à désigner)[^]]*\]",
    re.IGNORECASE,
)
HEADING = re.compile(
    r"^(?:PARTIE [A-F]\b|PARCOURS PRODUIT\b|CHAPITRE (?:P\d+|\d+)\b|ANNEXE [A-H]\b|"
    r"INTRODUCTION\b|AVANT-PROPOS\b|MODE D'EMPLOI\b|"
    r"ANNEXES\b|REGISTRE DE SUIVI\b|STATUT ET MODE D'EMPLOI\b|"
    r"PLAN DU LIVRE\b|POUR ALLER PLUS LOIN\b|AVANT DE PASSER AU PROTOTYPE\b)"
)
FONT_DIR = Path("/usr/share/fonts/truetype/freefont")


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Communalis", str(FONT_DIR / "FreeSerif.ttf")))
    pdfmetrics.registerFont(
        TTFont("Communalis-Bold", str(FONT_DIR / "FreeSerifBold.ttf"))
    )
    pdfmetrics.registerFont(
        TTFont("Communalis-Italic", str(FONT_DIR / "FreeSerifItalic.ttf"))
    )
    pdfmetrics.registerFont(TTFont("Communalis-Mono", str(FONT_DIR / "FreeMono.ttf")))
    pdfmetrics.registerFontFamily(
        "Communalis",
        normal="Communalis",
        bold="Communalis-Bold",
        italic="Communalis-Italic",
        boldItalic="Communalis-Bold",
    )


class BookDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, **kwargs: object) -> None:
        super().__init__(filename, **kwargs)
        frame = Frame(
            19 * mm,
            18 * mm,
            A4[0] - 38 * mm,
            A4[1] - 36 * mm,
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
            id="book",
        )
        self.addPageTemplates(
            PageTemplate(id="book", frames=frame, onPage=draw_page_number)
        )

    def afterFlowable(self, flowable: Flowable) -> None:
        if isinstance(flowable, Paragraph) and hasattr(flowable, "toc_level"):
            self.notify(
                "TOCEntry",
                (flowable.toc_level, flowable.getPlainText(), self.page),
            )


def draw_page_number(canvas: Canvas, doc: BookDocTemplate) -> None:
    canvas.saveState()
    if doc.page > 1:
        canvas.setFont("Communalis", 8)
        canvas.setFillColor(colors.HexColor("#5D6670"))
        canvas.drawCentredString(A4[0] / 2, 9 * mm, str(doc.page))
        canvas.setStrokeColor(colors.HexColor("#D7DCE0"))
        canvas.setLineWidth(0.35)
        canvas.line(19 * mm, 14 * mm, A4[0] - 19 * mm, 14 * mm)
    canvas.restoreState()


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "body": ParagraphStyle(
            "BookBody",
            parent=base["BodyText"],
            fontName="Communalis",
            fontSize=11.5,
            leading=17,
            textColor=colors.HexColor("#20272E"),
            alignment=TA_LEFT,
            spaceAfter=7.5,
            allowWidows=0,
            allowOrphans=0,
        ),
        "title": ParagraphStyle(
            "BookTitle",
            parent=base["Title"],
            fontName="Communalis-Bold",
            fontSize=26,
            leading=32,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#163D4B"),
            spaceAfter=14,
        ),
        "subtitle": ParagraphStyle(
            "BookSubtitle",
            parent=base["BodyText"],
            fontName="Communalis",
            fontSize=15,
            leading=21,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#40616B"),
            spaceAfter=14,
        ),
        "part": ParagraphStyle(
            "PartHeading",
            parent=base["Heading1"],
            fontName="Communalis-Bold",
            fontSize=18,
            leading=23,
            textColor=colors.HexColor("#163D4B"),
            spaceBefore=15,
            spaceAfter=10,
            keepWithNext=True,
        ),
        "chapter": ParagraphStyle(
            "ChapterHeading",
            parent=base["Heading2"],
            fontName="Communalis-Bold",
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#245B68"),
            spaceBefore=12,
            spaceAfter=7,
            keepWithNext=True,
        ),
        "subheading": ParagraphStyle(
            "SubHeading",
            parent=base["Heading3"],
            fontName="Communalis-Bold",
            fontSize=12.4,
            leading=16,
            textColor=colors.HexColor("#304B54"),
            spaceBefore=9,
            spaceAfter=5,
            keepWithNext=True,
        ),
        "placeholder": ParagraphStyle(
            "Placeholder",
            parent=base["BodyText"],
            fontName="Communalis-Bold",
            fontSize=11.5,
            leading=17,
            textColor=colors.HexColor("#7A3515"),
            backColor=colors.HexColor("#FFF0D7"),
            borderColor=colors.HexColor("#D78735"),
            borderWidth=0.6,
            borderPadding=5,
            leftIndent=5,
            rightIndent=5,
            spaceBefore=3,
            spaceAfter=7,
        ),
        "small": ParagraphStyle(
            "SmallNote",
            parent=base["BodyText"],
            fontName="Communalis",
            fontSize=10.4,
            leading=14,
            textColor=colors.HexColor("#48535B"),
            alignment=TA_CENTER,
        ),
    }


def paragraph_markup(text: str) -> str:
    escaped = escape(text).replace("\u00a0", " ")
    return PLACEHOLDER.sub(
        lambda match: f'<font color="#8C3B16"><b>{match.group(0)}</b></font>',
        escaped,
    )


def make_paragraph(
    text: str, style: dict[str, ParagraphStyle]
) -> Paragraph:
    if PLACEHOLDER.search(text):
        return Paragraph(paragraph_markup(text), style["placeholder"])
    return Paragraph(paragraph_markup(text), style["body"])


def is_heading(line: str) -> bool:
    clean = line.strip()
    return bool(
        HEADING.match(clean)
        or re.match(r"^\d+(?:\.\d+)?\s*[—–-]", clean)
        or clean in {
            "OBJECTIF",
            "MATÉRIEL ET COMPÉTENCES",
            "RÉSULTATS MESURÉS — GABARIT À REMPLIR",
            "RÉSULTATS MESURÉS ET DÉCISION",
            "RÉSULTATS MESURÉS ET RETOUR D'EXPÉRIENCE",
            "RÉSULTATS MESURÉS ET PROTOCOLE D'ÉVALUATION",
            "RÉSULTATS MESURÉS : DISTINGUER PREUVE ET INTENTION",
        }
        or (clean.isupper() and 4 <= len(clean) <= 90 and not "|" in clean)
    )


def build_table(lines: list[str], available_width: float) -> Table:
    rows = []
    for line in lines:
        if line.startswith("  ") and rows:
            continuation = line.strip().split("|")
            rows[-1][-1] += " " + continuation[0].strip()
            rows[-1].extend(cell.strip() for cell in continuation[1:])
            continue
        if "|" not in line:
            if rows:
                rows[-1][-1] += " " + line.strip()
            continue
        text = line.strip()
        if text.startswith("|"):
            text = text[1:]
        if text.endswith("|") and line.strip().startswith("|"):
            text = text[:-1]
        cells = [cell.strip() for cell in text.split("|")]
        if cells and all(re.fullmatch(r":?-{2,}:?", cell) for cell in cells):
            continue
        rows.append(cells)
    if not rows:
        return Table([[""]])
    col_count = max(map(len, rows))
    for row in rows:
        row.extend([""] * (col_count - len(row)))
    cell_style = ParagraphStyle(
        "TableCell",
        fontName="Communalis",
        fontSize=10.2,
        leading=14,
        textColor=colors.HexColor("#24343A"),
    )
    if col_count > 3:
        headers, *data = rows
        # Wide source tables become labelled records instead of tiny columns.
        rendered = []
        for row in data:
            for header, cell in zip(headers, row):
                rendered.append([
                    Paragraph(paragraph_markup(header), cell_style),
                    Paragraph(paragraph_markup(cell), cell_style),
                ])
            rendered.append(["", ""])
        if not rendered:
            rendered = [[Paragraph(paragraph_markup(c), cell_style), ""] for c in headers]
        widths = [available_width * 0.32, available_width * 0.68]
        repeat_rows = 0
    else:
        rendered = [
            [Paragraph(paragraph_markup(cell), cell_style) for cell in row]
            for row in rows
        ]
        widths = [available_width / col_count] * col_count
        repeat_rows = 1
    table = Table(rendered, colWidths=widths, repeatRows=repeat_rows, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6EFF0"))
                if repeat_rows else
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E6EFF0")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#163D4B")),
                ("FONTNAME", (0, 0), (-1, -1), "Communalis"),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B8C6C9")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def parse_source(path: Path, style: dict[str, ParagraphStyle], width: float) -> list[Flowable]:
    story: list[Flowable] = []
    paragraph: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    index = 0

    def flush_paragraph() -> None:
        if paragraph:
            text = " ".join(part.strip() for part in paragraph).strip()
            if text:
                story.append(make_paragraph(text, style))
            paragraph.clear()

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            index += 1
            continue
        if re.fullmatch(r"[-=]{3,}", stripped):
            flush_paragraph()
            story.append(Spacer(1, 5))
            index += 1
            continue
        if line.startswith("  ") and any(c in line for c in "→←↑↓┌└├─│"):
            flush_paragraph()
            diagram = []
            while index < len(lines) and lines[index].startswith("  ") and lines[index].strip():
                diagram.append(lines[index].rstrip())
                index += 1
            diagram_font = min(9, max(6, (width - 20) / (max(map(len, diagram)) * 0.6)))
            story.append(
                Preformatted(
                    "\n".join(diagram),
                    ParagraphStyle(
                        "Diagram",
                        fontName="Communalis-Mono",
                        fontSize=diagram_font,
                        leading=diagram_font * 1.35,
                        leftIndent=6,
                        textColor=colors.HexColor("#2D4B54"),
                        backColor=colors.HexColor("#F2F6F6"),
                        borderColor=colors.HexColor("#CEDADC"),
                        borderWidth=0.4,
                        borderPadding=5,
                    ),
                )
            )
            story.append(Spacer(1, 7))
            continue
        if "|" in stripped:
            flush_paragraph()
            table_lines = []
            while index < len(lines) and lines[index].strip():
                current = lines[index]
                if "|" in current or (current.startswith("  ") and table_lines):
                    table_lines.append(current)
                    index += 1
                else:
                    break
            story.append(build_table(table_lines, width))
            story.append(Spacer(1, 7))
            continue
        if is_heading(stripped):
            flush_paragraph()
            if re.match(r"^(PARTIE [A-F]\b|PARCOURS PRODUIT\b|ANNEXES\b)", stripped):
                level, toc_level = "part", 0
            elif re.match(r"^(CHAPITRE (?:P\d+|\d+)\b|ANNEXE [A-H]\b)", stripped):
                level, toc_level = "chapter", 1
            elif re.match(r"^(INTRODUCTION\b|AVANT-PROPOS\b|MODE D'EMPLOI\b|REGISTRE DE SUIVI\b)", stripped):
                level, toc_level = "chapter", 0
            else:
                level, toc_level = "subheading", None
            heading = Paragraph(paragraph_markup(stripped), style[level])
            if toc_level is not None:
                heading.toc_level = toc_level
            story.append(heading)
            index += 1
            continue
        if stripped.startswith(("•", "□")) or re.match(r"^\d+\.\s", stripped):
            flush_paragraph()
            item = [stripped]
            index += 1
            while index < len(lines) and lines[index].startswith("  ") and lines[index].strip():
                item.append(lines[index].strip())
                index += 1
            story.append(make_paragraph(" ".join(item), style))
            continue
        paragraph.append(line)
        index += 1

    flush_paragraph()
    return story


def build(
    output: Path,
    sources: tuple[str, ...] = SOURCES,
    technical: bool = False,
) -> int:
    register_fonts()
    style = styles()
    width = A4[0] - 38 * mm
    title = (
        "Communalis — Dossiers techniques"
        if technical else
        "Communalis — Cahier produit et terrain pour le Togo"
    )
    subtitle = (
        "Énergie, langues, capteurs,<br/>données et sécurité"
        if technical else
        "Des services territoriaux utiles,<br/>adoptés et maintenables"
    )
    cover_label = (
        "DOSSIERS TECHNIQUES — RESSOURCE COMPLÉMENTAIRE"
        if technical else
        "CAHIER DE RÉFÉRENCE — INSTITUTIONS ET ACTEURS DE TERRAIN"
    )
    cover_note = (
        "Chapitres de conception à consulter selon le cas d'usage. "
        "Ils complètent le parcours produit et ne remplacent pas les "
        "validations locales ou professionnelles."
        if technical else
        "Parcours produit, adoption par le public, bootcamp et outils de "
        "déploiement. Les résultats et décisions de terrain restent à "
        "valider par les personnes et institutions concernées."
    )
    doc = BookDocTemplate(
        str(output),
        pagesize=A4,
        title=title,
        author="Projet Communalis",
        subject=(
            "Dossiers de conception technique"
            if technical else
            "Guide institutionnel et support de bootcamp — pilote proposé à Baguida"
        ),
        leftMargin=19 * mm,
        rightMargin=19 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )
    story: list[Flowable] = [
        Spacer(1, 42 * mm),
        Paragraph("COMMUNALIS", style["title"]),
        Paragraph(subtitle, style["subtitle"]),
        Spacer(1, 14 * mm),
        Paragraph(cover_label, style["chapter"]),
        Paragraph("Pilote proposé à Baguida, Togo", style["small"]),
        Spacer(1, 22 * mm),
        Paragraph(cover_note, style["small"]),
    ]
    story.append(PageBreak())
    if not technical:
        story.extend(
            [
                Paragraph("LIRE LES ANNOTATIONS", style["part"]),
                make_paragraph(
                    "[RÉSULTATS TOGO À INSÉRER] — observations, mesures, dates, "
                    "lieux autorisés, protocole, effectifs, limites et preuve de "
                    "publication à fournir par l'équipe du projet.",
                    style,
                ),
                make_paragraph(
                    "[À ACTUALISER] — information datée à vérifier (prix, droit, "
                    "version, disponibilité, contacts ou statut d'un partenaire).",
                    style,
                ),
                make_paragraph(
                    "[À CONFIRMER] — hypothèse ou décision qui exige une validation "
                    "explicite des personnes responsables et concernées.",
                    style,
                ),
                make_paragraph(
                    "[à compléter] / [à remplir] / [à désigner] — champ de fiche "
                    "à renseigner avec une information réelle, un responsable ou "
                    "une décision. Ne pas remplacer un champ par une estimation "
                    "présentée comme un fait.",
                    style,
                ),
                make_paragraph(
                    "Pour chaque ajout, conserver la date, la source ou la preuve, "
                    "les conditions de collecte, les incertitudes, les droits et "
                    "la personne ayant validé la publication. Si l'information "
                    "n'existe pas encore, garder le repère et expliquer pourquoi.",
                    style,
                ),
                PageBreak(),
                Paragraph("FICHE DE SITUATION DU PROJET", style["part"]),
                make_paragraph(
                    "À valider par l'équipe avant toute diffusion comme récit du "
                    "projet. Cette fiche n'affirme aucun fait à sa place.",
                    style,
                ),
                make_paragraph(
                    "Nom retenu et périmètre exact : [à compléter — intitulé et sites].",
                    style,
                ),
                make_paragraph(
                    "Période couverte et date d'arrêt des informations : "
                    "[à compléter — dates vérifiées].",
                    style,
                ),
                make_paragraph(
                    "État réel de chaque activité : [à compléter — réalisé, en cours, "
                    "prévu, suspendu ou non engagé, avec preuve].",
                    style,
                ),
                make_paragraph(
                    "Partenaires, rôles confirmés et autorisation de les nommer : "
                    "[à compléter — validation des personnes concernées].",
                    style,
                ),
                make_paragraph(
                    "Langues, variantes et personnes habilitées à relire : "
                    "[à compléter — noms seulement avec accord].",
                    style,
                ),
                make_paragraph(
                    "Sources de terrain, protocoles et droits de publication : "
                    "[à compléter — référence, date, consentements et restrictions].",
                    style,
                ),
                make_paragraph(
                    "Matériel effectivement utilisé et versions : "
                    "[à compléter — inventaire vérifié, pas la liste envisagée].",
                    style,
                ),
                make_paragraph(
                    "Résultats, échecs et limites autorisés à publier : "
                    "[à compléter — données, dénominateurs et validation].",
                    style,
                ),
                make_paragraph(
                    "Budget réellement dépensé et monnaie : "
                    "[à compléter — pièces vérifiées et période].",
                    style,
                ),
                make_paragraph(
                    "Responsable de validation éditoriale et date : "
                    "[à compléter — accord avant diffusion].",
                    style,
                ),
                PageBreak(),
            ]
        )
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("ContentsPart", fontName="Communalis-Bold", fontSize=11,
                       leading=16, spaceBefore=5, leftIndent=0, firstLineIndent=0),
        ParagraphStyle("ContentsChapter", fontName="Communalis", fontSize=10.5,
                       leading=15, leftIndent=14, firstLineIndent=0),
    ]
    story.extend([Paragraph("SOMMAIRE", style["part"]), toc, PageBreak()])
    for filename in sources:
        story.extend(parse_source(ROOT / filename, style, width))
        if filename != sources[-1]:
            story.append(PageBreak())
    output.parent.mkdir(parents=True, exist_ok=True)
    doc.multiBuild(story)
    data = output.read_bytes()
    return len(re.findall(rb"/Type\s*/Page\b", data))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "Communalis_Cahier_Terrain.pdf",
    )
    parser.add_argument(
        "--technical-output",
        type=Path,
        default=ROOT / "Communalis_Dossiers_Techniques.pdf",
    )
    args = parser.parse_args()
    page_count = build(args.output)
    print(f"PDF généré : {args.output} ({page_count} pages)")
    technical_pages = build(
        args.technical_output,
        sources=TECHNICAL_SOURCES,
        technical=True,
    )
    print(
        f"PDF généré : {args.technical_output} "
        f"({technical_pages} pages)"
    )


if __name__ == "__main__":
    main()
