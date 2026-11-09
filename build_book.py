#!/usr/bin/env python3
"""Build the French Communalis field-book PDF from its editable text sources."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Flowable,
    Frame,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.flowables import DocIf
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parent
PRODUCT_SOURCES = (
    "Livre_Introduction.txt",
    "Livre_Parcours_Produit.txt",
)
TECHNICAL_SOURCES = (
    "Livre_Partie_A.txt",
    "Livre_Partie_B.txt",
    "Livre_Partie_C.txt",
    "Livre_Partie_D.txt",
    "Livre_Partie_E.txt",
    "Livre_Partie_F.txt",
)
ANNEX_SOURCES = (
    "Livre_Annexes.txt",
)
SOURCES = PRODUCT_SOURCES + TECHNICAL_SOURCES + ANNEX_SOURCES
PLACEHOLDER = re.compile(
    r"\[(?:À ACTUALISER|À CONFIRMER|RÉSULTATS TOGO À INSÉRER|"
    r"à compléter|à remplir|à désigner)[^]]*\]",
    re.IGNORECASE,
)
HINT = re.compile(r"\[[^]]*\]")
HEADING = re.compile(
    r"^(?:PARTIE [A-F]\b|PARCOURS PRODUIT\b|CHAPITRE (?:P\d+|\d+)\b|ANNEXE [A-H]\b|"
    r"INTRODUCTION\b|AVANT-PROPOS\b|MODE D'EMPLOI\b|"
    r"ANNEXES\b|REGISTRE DE SUIVI\b|STATUT ET MODE D'EMPLOI\b|"
    r"PLAN DU LIVRE\b|POUR ALLER PLUS LOIN\b|AVANT DE PASSER AU PROTOTYPE\b)"
)
PART_HEADING = re.compile(r"^(PARTIE [A-F]\b|PARCOURS PRODUIT\b|ANNEXES\b)")
CHAPTER_HEADING = re.compile(r"^(CHAPITRE (?:P\d+|\d+)\b|ANNEXE [A-H]\b)")
UNNUMBERED_CHAPTER = re.compile(
    r"^(INTRODUCTION\b|AVANT-PROPOS\b|MODE D'EMPLOI\b|"
    r"STATUT ET MODE D'EMPLOI\b|REGISTRE DE SUIVI\b)"
)
NUMBERED_SECTION = re.compile(r"^(P?\d+(?:\.\d+)+)\s*(?:[—–-]\s*|\s)(\S.*)$")
CAPTION = re.compile(
    r"^(TABLEAU|Tableau|SCHÉMA|Schéma|FIGURE|Figure)\s+([\w.]+)\s*[—–-]\s*(.+)$"
)
BOX_CAPTION = re.compile(r"^(?:Encadré|ENCADRÉ)(?:\s+[\w.]+)?\s*[—–-]\s*(.+)$")
FORM_LINE = re.compile(r"^([A-ZÀ-ÖØ-Ý][^:|•□\[\]]{1,70}?) : (.+)$")
LIST_ITEM = re.compile(r"^(?:[•□]|\d+\.\s)")
DIAGRAM_CHARS = "→←↑↓↔↕┌┐└┘├┤┬┴─│"
EDITORIAL_NOTES = ("Texte de travail",)

FONT_DIR = Path("/usr/share/fonts/truetype/freefont")
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_X = 20 * mm
MARGIN_TOP = 24 * mm
MARGIN_BOTTOM = 22 * mm
TEXT_WIDTH = PAGE_WIDTH - 2 * MARGIN_X

INK = colors.HexColor("#1F292E")
TEAL = colors.HexColor("#164A57")
TEAL_MID = colors.HexColor("#2C6A78")
TEAL_SOFT = colors.HexColor("#E7F0F1")
TEAL_FAINT = colors.HexColor("#F4F8F8")
ACCENT = colors.HexColor("#C2622A")
ACCENT_SOFT = colors.HexColor("#F3B58C")
MUTED = colors.HexColor("#5F6E74")
RULE = colors.HexColor("#C5D3D6")
NOTE_BG = colors.HexColor("#FCF3E6")
NOTE_BORDER = colors.HexColor("#E4B57E")
NOTE_TEXT = "#8A4512"


def register_fonts() -> None:
    fonts = {
        "Communalis": "FreeSerif.ttf",
        "Communalis-Bold": "FreeSerifBold.ttf",
        "Communalis-Italic": "FreeSerifItalic.ttf",
        "Communalis-BoldItalic": "FreeSerifBoldItalic.ttf",
        "Communalis-Sans": "FreeSans.ttf",
        "Communalis-SansBold": "FreeSansBold.ttf",
        "Communalis-SansItalic": "FreeSansOblique.ttf",
        "Communalis-SansBoldItalic": "FreeSansBoldOblique.ttf",
        "Communalis-Mono": "FreeMono.ttf",
    }
    for name, filename in fonts.items():
        pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / filename)))
    pdfmetrics.registerFontFamily(
        "Communalis",
        normal="Communalis",
        bold="Communalis-Bold",
        italic="Communalis-Italic",
        boldItalic="Communalis-BoldItalic",
    )
    pdfmetrics.registerFontFamily(
        "Communalis-Sans",
        normal="Communalis-Sans",
        bold="Communalis-SansBold",
        italic="Communalis-SansItalic",
        boldItalic="Communalis-SansBoldItalic",
    )


def hyphenation_language() -> str:
    try:
        import pyphen  # noqa: F401
    except ImportError:
        return ""
    return "fr"


def styles() -> dict[str, ParagraphStyle]:
    hyphenation = hyphenation_language()
    body = ParagraphStyle(
        "BookBody",
        fontName="Communalis",
        fontSize=10.8,
        leading=15.2,
        textColor=INK,
        alignment=TA_JUSTIFY,
        spaceAfter=6.5,
        allowWidows=0,
        allowOrphans=0,
        hyphenationLang=hyphenation,
        embeddedHyphenation=1,
        uriWasteReduce=0.3,
    )
    return {
        "body": body,
        "lead": ParagraphStyle(
            "BodyLead", parent=body, keepWithNext=True, alignment=TA_LEFT
        ),
        "bullet": ParagraphStyle(
            "BookBullet",
            parent=body,
            leftIndent=15,
            bulletIndent=4,
            spaceAfter=3.5,
            bulletFontName="Communalis-SansBold",
            bulletFontSize=9.5,
            bulletColor=ACCENT,
        ),
        "check": ParagraphStyle(
            "BookCheck",
            parent=body,
            leftIndent=19,
            bulletIndent=2,
            spaceAfter=4,
            bulletFontName="Communalis-Sans",
            bulletFontSize=13,
            bulletColor=TEAL,
            alignment=TA_LEFT,
        ),
        "numbered": ParagraphStyle(
            "BookNumbered",
            parent=body,
            leftIndent=19,
            bulletIndent=0,
            spaceAfter=4,
            bulletFontName="Communalis-SansBold",
            bulletFontSize=9.8,
            bulletColor=ACCENT,
        ),
        "title": ParagraphStyle(
            "BookTitle",
            fontName="Communalis-SansBold",
            fontSize=40,
            leading=46,
            textColor=colors.white,
        ),
        "subtitle": ParagraphStyle(
            "BookSubtitle",
            fontName="Communalis-Sans",
            fontSize=17,
            leading=23,
            textColor=colors.white,
        ),
        "part": ParagraphStyle(
            "PartHeading",
            fontName="Communalis-SansBold",
            fontSize=25,
            leading=31,
            textColor=colors.white,
            spaceAfter=10 * mm,
            keepWithNext=True,
        ),
        "chapter": ParagraphStyle(
            "ChapterHeading",
            fontName="Communalis-SansBold",
            fontSize=18.5,
            leading=24,
            textColor=TEAL,
            spaceBefore=4,
            spaceAfter=9 * mm,
            keepWithNext=True,
        ),
        "subheading": ParagraphStyle(
            "SubHeading",
            fontName="Communalis-SansBold",
            fontSize=12.6,
            leading=16.5,
            textColor=TEAL,
            spaceBefore=12,
            spaceAfter=6,
            keepWithNext=True,
        ),
        "label": ParagraphStyle(
            "Label",
            fontName="Communalis-SansBold",
            fontSize=10.2,
            leading=13.5,
            textColor=TEAL_MID,
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "caption": ParagraphStyle(
            "Caption",
            fontName="Communalis-SansBold",
            fontSize=9.6,
            leading=12.5,
            textColor=TEAL,
            spaceBefore=8,
            spaceAfter=5,
            keepWithNext=True,
        ),
        "note": ParagraphStyle(
            "Placeholder",
            parent=body,
            fontSize=10.2,
            leading=14,
            alignment=TA_LEFT,
            textColor=colors.HexColor(NOTE_TEXT),
            backColor=NOTE_BG,
            borderColor=NOTE_BORDER,
            borderWidth=0.5,
            borderPadding=(5, 7, 6, 7),
            leftIndent=7,
            rightIndent=7,
            spaceBefore=6,
            spaceAfter=11,
        ),
        "box": ParagraphStyle(
            "BoxBody", parent=body, fontSize=10.3, leading=14.4, spaceAfter=4
        ),
        "small": ParagraphStyle(
            "SmallNote",
            fontName="Communalis-Sans",
            fontSize=9,
            leading=12.5,
            textColor=MUTED,
            alignment=TA_LEFT,
        ),
        "cell": ParagraphStyle(
            "TableCell",
            fontName="Communalis",
            fontSize=9.6,
            leading=12.6,
            textColor=INK,
            hyphenationLang=hyphenation,
            embeddedHyphenation=1,
        ),
        "cell_head": ParagraphStyle(
            "TableHead",
            fontName="Communalis-SansBold",
            fontSize=8.8,
            leading=11.5,
            textColor=colors.white,
        ),
        "cell_label": ParagraphStyle(
            "TableLabel",
            fontName="Communalis-SansBold",
            fontSize=8.8,
            leading=11.8,
            textColor=TEAL,
        ),
        "cell_hint": ParagraphStyle(
            "TableHint",
            fontName="Communalis-Italic",
            fontSize=8.6,
            leading=11.2,
            textColor=MUTED,
        ),
    }


def paragraph_markup(text: str) -> str:
    escaped = escape(text).replace("\u00a0", " ").replace(
        "🔴", '<font color="#C0392B">●</font>'
    )
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
    return PLACEHOLDER.sub(
        lambda match: (
            f'<font color="{NOTE_TEXT}" backColor="#FBE9D3">'
            f"<b>{match.group(0)}</b></font>"
        ),
        escaped,
    )


def make_paragraph(text: str, style: dict[str, ParagraphStyle]) -> Paragraph:
    text = text.strip()
    if PLACEHOLDER.match(text):
        markup = escape(text)
        return Paragraph(markup, style["note"])
    if text.endswith(":"):
        return Paragraph(paragraph_markup(text), style["lead"])
    return Paragraph(paragraph_markup(text), style["body"])


def list_paragraph(text: str, style: dict[str, ParagraphStyle]) -> Paragraph:
    if text.startswith("•"):
        return Paragraph(paragraph_markup(text[1:].strip()), style["bullet"],
                         bulletText="•")
    if text.startswith("□"):
        return Paragraph(paragraph_markup(text[1:].strip()), style["check"],
                         bulletText="☐")
    number, rest = text.split(".", 1)
    return Paragraph(paragraph_markup(rest.strip()), style["numbered"],
                     bulletText=f"{number}.")


def is_heading(line: str) -> bool:
    clean = line.strip()
    return bool(
        HEADING.match(clean)
        or re.match(r"^\d+(?:\.\d+)?\s*[—–-]", clean)
        or NUMBERED_SECTION.match(clean)
        or (clean.isupper() and 4 <= len(clean) <= 90 and "|" not in clean)
    )


def is_label(line: str, next_line: str) -> bool:
    """Detect short standalone labels such as « Objectif » or « Fiche de test »."""
    if line.startswith(" ") or not line.strip():
        return False
    clean = line.strip()
    following = next_line.strip()
    if (
        len(clean) > 80
        or not clean[0].isupper()
        or "|" in clean
        or LIST_ITEM.match(clean)
        or FORM_LINE.match(clean)
        or PLACEHOLDER.search(clean)
        or re.search(r"[.;,!»)\]]$", clean)
    ):
        return False
    if clean.endswith(":") and len(clean.split()) > 5:
        return False
    if not following:
        return not clean.endswith(":") or len(clean.split()) <= 4
    return bool(
        LIST_ITEM.match(following)
        or "|" in following
        or FORM_LINE.match(following)
    )


def split_title(text: str) -> tuple[str, str]:
    parts = re.split(r"\s+[—–-]\s+", text, maxsplit=1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return "", text.strip()


class BookHeading(Paragraph):
    """Heading paragraph carrying table-of-contents and running-head metadata."""

    def __init__(self, text: str, style: ParagraphStyle, kind: str,
                 toc_level: int | None = None, label: str = "",
                 title: str = "", subtitle: str = "") -> None:
        self.kind = kind
        self.label = label
        self.title = title or text
        self.subtitle = subtitle
        self.toc_text = text
        if toc_level is not None:
            self.toc_level = toc_level
        super().__init__(self._markup(), style)

    def _markup(self) -> str:
        title = paragraph_markup(self.title)
        if self.kind == "part":
            markup = ""
            if self.label:
                markup += (
                    f'<font name="Communalis-SansBold" size="11" '
                    f'color="#F3B58C">{escape(self.label)}</font><br/>'
                )
            markup += title
            if self.subtitle:
                markup += (
                    f'<br/><font name="Communalis-SansItalic" size="13" '
                    f'color="#D6E6E9">{escape(self.subtitle)}</font>'
                )
            return markup
        if self.kind == "chapter" and self.label:
            return (
                f'<font name="Communalis-SansBold" size="10.5" color="#C2622A">'
                f"{escape(self.label)}</font><br/>{title}"
            )
        if self.kind == "subheading":
            number = NUMBERED_SECTION.match(self.title)
            if number:
                return (
                    f'<font color="#C2622A">{escape(number.group(1))}</font>'
                    f"&nbsp;&nbsp;{paragraph_markup(number.group(2))}"
                )
        return title

    def split(self, availWidth: float, availHeight: float) -> list[Flowable]:
        return []

    def wrap(self, availWidth: float, availHeight: float) -> tuple[float, float]:
        if self.kind == "part":
            width, height = super().wrap(availWidth - 20 * mm, availHeight)
            self._band_height = height + 34 * mm
            return availWidth, self._band_height
        width, height = super().wrap(availWidth, availHeight)
        if self.kind == "chapter":
            return width, height + 7
        return width, height

    def drawOn(self, canvas: Canvas, x: float, y: float, _sW: float = 0) -> None:
        if self.kind == "part":
            canvas.saveState()
            canvas.setFillColor(TEAL)
            canvas.rect(0, y, PAGE_WIDTH, PAGE_HEIGHT - y, stroke=0, fill=1)
            canvas.setFillColor(ACCENT)
            canvas.rect(0, y, PAGE_WIDTH, 2.2 * mm, stroke=0, fill=1)
            letter = re.search(r"PARTIE ([A-F])", self.label)
            if letter:
                canvas.setFillColor(colors.HexColor("#1F5C6A"))
                canvas.setFont("Communalis-SansBold", 150)
                canvas.drawRightString(PAGE_WIDTH - 12 * mm, y + 10 * mm,
                                       letter.group(1))
            canvas.restoreState()
            super().drawOn(canvas, x, y + 16 * mm, _sW)
            return
        if self.kind == "chapter":
            super().drawOn(canvas, x, y + 7, _sW)
            canvas.saveState()
            canvas.setStrokeColor(ACCENT)
            canvas.setLineWidth(1.6)
            canvas.line(x, y + 1, x + 22 * mm, y + 1)
            canvas.setStrokeColor(RULE)
            canvas.setLineWidth(0.5)
            canvas.line(x + 22 * mm, y + 1, x + TEXT_WIDTH, y + 1)
            canvas.restoreState()
            return
        super().drawOn(canvas, x, y, _sW)


def make_heading(stripped: str, style: dict[str, ParagraphStyle],
                 subtitle: str = "") -> BookHeading:
    text = re.sub(r"^COMMUNALIS\s+[—–-]\s+", "", stripped)
    if PART_HEADING.match(text):
        label, title = split_title(text)
        if text.startswith("ANNEXES"):
            label, title = "ANNEXES", text
        return BookHeading(text, style["part"], "part", 0, label, title, subtitle)
    if CHAPTER_HEADING.match(text):
        label, title = split_title(text)
        return BookHeading(text, style["chapter"], "chapter", 1, label, title)
    if UNNUMBERED_CHAPTER.match(text):
        label, title = split_title(text)
        if not label:
            label, title = "", text
        return BookHeading(text, style["chapter"], "chapter", 0, label, title)
    return BookHeading(text, style["subheading"], "subheading")


def cell_content(text: str, style: dict[str, ParagraphStyle],
                 cell_style: str = "cell") -> Paragraph | str:
    text = text.strip()
    if not text or re.fullmatch(r"\[\s*\]", text):
        return ""
    return Paragraph(paragraph_markup(text), style[cell_style])


def column_widths(rows: list[list[str]], available_width: float) -> list[float]:
    col_count = len(rows[0])
    weights = []
    for column in range(col_count):
        longest = max(len(row[column]) for row in rows)
        weights.append(min(max(longest, 8), 60) ** 0.75)
    total = sum(weights)
    minimum = available_width * 0.16
    widths = [max(available_width * weight / total, minimum) for weight in weights]
    scale = available_width / sum(widths)
    return [width * scale for width in widths]


def build_table(lines: list[str], available_width: float) -> Table:
    style = styles()
    rows: list[list[str]] = []
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
    commands: list[tuple] = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    row_heights: list[float | None] = []
    blank_grid = col_count > 3 and len(rows) > 1 and all(
        not re.sub(r"[\[\]\s]", "", cell) for row in rows[1:] for cell in row[1:]
    )
    if col_count > 3 and not blank_grid:
        headers, *data = rows
        # Wide source tables become labelled records instead of tiny columns.
        rendered: list[list[Paragraph | str]] = []
        records = data or [[""] * col_count]
        for number, row in enumerate(records):
            start = len(rendered)
            for header, cell in zip(headers, row):
                rendered.append([
                    Paragraph(paragraph_markup(header), style["cell_label"]),
                    cell_content(cell, style),
                ])
                row_heights.append(None if cell_content(cell, style) else 8 * mm)
            end = len(rendered) - 1
            commands.extend([
                ("BACKGROUND", (0, start), (0, end), TEAL_SOFT),
                ("BOX", (0, start), (-1, end), 0.6, TEAL_MID),
                ("LINEBELOW", (0, start), (-1, end - 1), 0.35, RULE),
                ("LINEAFTER", (0, start), (0, end), 0.35, RULE),
                ("LINEABOVE", (0, start), (-1, start), 1.4, TEAL_MID),
                ("NOSPLIT", (0, start), (-1, end)),
            ])
            if number < len(records) - 1:
                rendered.append(["", ""])
                row_heights.append(3 * mm)
        widths = [available_width * 0.32, available_width * 0.68]
        repeat_rows = 0
    else:
        header, *data = rows
        rendered = [[cell_content(cell, style, "cell_head") for cell in header]]
        row_heights.append(None)
        for row in data:
            cells = [cell_content(cell, style) for cell in row]
            rendered.append(cells)
            row_heights.append(10 * mm if not any(cells[1:]) else None)
        widths = column_widths(rows, available_width)
        if blank_grid:
            first = available_width * 0.24
            other = (available_width - first) / (col_count - 1)
            widths = [first] + [other] * (col_count - 1)
            commands.extend([
                ("GRID", (0, 1), (-1, -1), 0.35, RULE),
                ("BOX", (0, 0), (-1, -1), 0.6, TEAL_MID),
            ])
        repeat_rows = 1
        commands.extend([
            ("BACKGROUND", (0, 0), (-1, 0), TEAL),
            ("LINEBELOW", (0, 1), (-1, -1), 0.35, RULE),
            ("LINEBELOW", (0, -1), (-1, -1), 0.8, TEAL_MID),
            ("TOPPADDING", (0, 0), (-1, 0), 5),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
        ])
        for index in range(2, len(rendered), 2):
            commands.append(("BACKGROUND", (0, index), (-1, index), TEAL_FAINT))
    table = Table(rendered, colWidths=widths, rowHeights=row_heights,
                  repeatRows=repeat_rows, hAlign="LEFT")
    table.setStyle(TableStyle(commands))
    return table


def build_form(fields: list[tuple[str, str]], width: float,
               style: dict[str, ParagraphStyle]) -> Table:
    """Render « Champ : [indication] » lines as a printable fill-in form."""
    rows = []
    heights = []
    for label, value in fields:
        hint_only = not HINT.sub("", value).strip(" ;.,—-")
        markup = paragraph_markup(value)
        rows.append([
            Paragraph(escape(label), style["cell_label"]),
            Paragraph(escape(value) if hint_only else markup,
                      style["cell_hint"] if hint_only else style["cell"]),
        ])
        heights.append(12 * mm if hint_only else None)
    table = Table(rows, colWidths=[width * 0.34, width * 0.66],
                  rowHeights=heights, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, -1), TEAL_SOFT),
        ("BOX", (0, 0), (-1, -1), 0.6, TEAL_MID),
        ("LINEBELOW", (0, 0), (-1, -2), 0.35, RULE),
        ("LINEAFTER", (0, 0), (0, -1), 0.35, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


def build_box(title: str, content: list[Flowable], width: float) -> Table:
    caption = ParagraphStyle(
        "BoxTitle", fontName="Communalis-SansBold", fontSize=9.8, leading=13,
        textColor=TEAL, spaceAfter=4,
    )
    table = Table([[[Paragraph(paragraph_markup(title), caption), *content]]],
                  colWidths=[width], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), TEAL_FAINT),
        ("LINEBEFORE", (0, 0), (0, -1), 2.4, ACCENT),
        ("BOX", (0, 0), (-1, -1), 0.4, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


def build_diagram(lines: list[str], width: float) -> list[Flowable]:
    indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    diagram = [line[indent:].rstrip() for line in lines]
    longest = max(map(len, diagram))
    font_size = min(9, max(6, (width - 20) / (longest * 0.6)))
    leading = font_size * 1.35
    return [
        CondPageBreak(len(diagram) * leading + 40),
        Preformatted(
            "\n".join(diagram),
            ParagraphStyle(
                "Diagram",
                fontName="Communalis-Mono",
                fontSize=font_size,
                leading=leading,
                leftIndent=8,
                rightIndent=8,
                textColor=colors.HexColor("#21434C"),
                backColor=TEAL_FAINT,
                borderColor=RULE,
                borderWidth=0.5,
                borderPadding=(7, 8, 7, 8),
                spaceBefore=4,
            ),
        ),
        Spacer(1, 12),
    ]


def caption_paragraph(match: re.Match[str], style: dict[str, ParagraphStyle]) -> Paragraph:
    kind = match.group(1).capitalize()
    return Paragraph(
        f'<font color="#C2622A">{escape(kind)} {escape(match.group(2))}</font>'
        f"&nbsp;&nbsp;{paragraph_markup(match.group(3))}",
        style["caption"],
    )


def strip_preamble(lines: list[str]) -> list[str]:
    """Drop the repeated manuscript title block at the start of a source file."""
    first = next((line.strip() for line in lines if line.strip()), "")
    if first != "COMMUNALIS":
        return lines
    for index, line in enumerate(lines):
        if HEADING.match(line.strip()):
            return lines[index:]
    return lines


def take_block(lines: list[str], index: int) -> tuple[list[str], int]:
    while index < len(lines) and not lines[index].strip():
        index += 1
    block = []
    while index < len(lines) and lines[index].strip():
        block.append(lines[index])
        index += 1
    return block, index


def skip_blank_and_rules(lines: list[str], index: int) -> int:
    while index < len(lines) and (
        not lines[index].strip() or re.fullmatch(r"[-=]{3,}", lines[index].strip())
    ):
        index += 1
    return index


def part_subtitle(lines: list[str], index: int) -> tuple[str, int]:
    """Return the short tagline following a part heading, if any."""
    look = skip_blank_and_rules(lines, index)
    if look < len(lines) and lines[look].strip().startswith(EDITORIAL_NOTES):
        look = skip_blank_and_rules(lines, look + 1)
    candidate = lines[look].strip() if look < len(lines) else ""
    after = lines[look + 1].strip() if look + 1 < len(lines) else ""
    if (
        candidate
        and len(candidate) <= 90
        and not candidate.isupper()
        and not is_heading(candidate)
        and "|" not in candidate
        and not re.search(r"[.;:]$", candidate)
        and (not after or re.fullmatch(r"[-=]{3,}", after))
    ):
        return candidate, look + 1
    return "", index


def parse_lines(lines: list[str], style: dict[str, ParagraphStyle],
                width: float) -> list[Flowable]:
    story: list[Flowable] = []
    paragraph: list[str] = []
    index = 0

    def flush_paragraph() -> None:
        if paragraph:
            text = " ".join(part.strip() for part in paragraph).strip()
            if text:
                story.append(make_paragraph(text, style))
            paragraph.clear()

    def next_line(position: int) -> str:
        return lines[position + 1] if position + 1 < len(lines) else ""

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            index += 1
            continue
        if re.fullmatch(r"[-=]{3,}", stripped):
            flush_paragraph()
            index += 1
            continue
        if not paragraph and stripped.startswith(EDITORIAL_NOTES):
            index += 1
            continue
        if not paragraph and (match := CAPTION.match(stripped)):
            caption = caption_paragraph(match, style)
            index += 1
            if match.group(1).upper() in {"SCHÉMA", "FIGURE"}:
                block, index = take_block(lines, index)
                if block and "|" in block[0] and not any(
                    c in "".join(block) for c in DIAGRAM_CHARS + "+v"
                ):
                    story.extend([caption, build_table(block, width), Spacer(1, 10)])
                elif block:
                    keep, *diagram = build_diagram(block, width)
                    story.extend([keep, caption, *diagram])
                else:
                    story.append(caption)
            else:
                story.extend([CondPageBreak(40 * mm), caption])
            continue
        if not paragraph and (match := BOX_CAPTION.match(stripped)):
            block, index = take_block(lines, index + 1)
            content = parse_lines(block, style, width - 24)
            for flowable in content:
                if isinstance(flowable, Paragraph) and flowable.style.name == "BookBody":
                    flowable.style = style["box"]
            story.append(CondPageBreak(30 * mm))
            story.append(build_box(match.group(1), content, width))
            story.append(Spacer(1, 10))
            continue
        if line.startswith("  ") and not paragraph:
            end = index
            while end < len(lines) and lines[end].startswith("  ") and lines[end].strip():
                end += 1
            block = lines[index:end]
            if any(c in "".join(block) for c in DIAGRAM_CHARS):
                story.extend(build_diagram(block, width))
                index = end
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
            story.append(Spacer(1, 10))
            continue
        if not paragraph and FORM_LINE.match(stripped) and FORM_LINE.match(
            next_line(index).strip()
        ) and not next_line(index).startswith(" "):
            fields: list[tuple[str, str]] = []
            while index < len(lines) and lines[index].strip():
                current = lines[index]
                match = FORM_LINE.match(current.strip())
                if match and not current.startswith(" "):
                    fields.append((match.group(1), match.group(2)))
                elif current.startswith(" ") and fields:
                    label, value = fields[-1]
                    fields[-1] = (label, f"{value} {current.strip()}")
                else:
                    break
                index += 1
            story.append(build_form(fields, width, style))
            story.append(Spacer(1, 10))
            continue
        underlined = bool(re.fullmatch(r"[-=]{3,}", next_line(index).strip()))
        if not paragraph and (is_heading(stripped) or underlined):
            text = re.sub(r"^COMMUNALIS\s+[—–-]\s+", "", stripped)
            subtitle, consumed = "", index + 1
            if PART_HEADING.match(text):
                subtitle, consumed = part_subtitle(lines, consumed)
            heading = make_heading(stripped, style, subtitle)
            if heading.kind == "part":
                story.extend([PageBreak(), DocIf("doc.page % 2 == 0", [PageBreak()])])
            elif heading.kind == "chapter":
                follows_part = (
                    story
                    and isinstance(story[-1], BookHeading)
                    and story[-1].kind == "part"
                )
                if not follows_part:
                    story.extend([PageBreak(), Spacer(1, 8 * mm)])
            story.append(heading)
            index = consumed
            continue
        if not paragraph and is_label(line, next_line(index)):
            story.append(Paragraph(paragraph_markup(stripped), style["label"]))
            index += 1
            continue
        if LIST_ITEM.match(stripped):
            flush_paragraph()
            item = [stripped]
            index += 1
            while index < len(lines) and lines[index].startswith("  ") and lines[index].strip():
                item.append(lines[index].strip())
                index += 1
            story.append(list_paragraph(" ".join(item), style))
            continue
        paragraph.append(line)
        index += 1

    flush_paragraph()
    return story


def parse_source(path: Path, style: dict[str, ParagraphStyle], width: float) -> list[Flowable]:
    lines = strip_preamble(path.read_text(encoding="utf-8").splitlines())
    return parse_lines(lines, style, width)


class BookDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, cover: dict[str, str], **kwargs: object) -> None:
        super().__init__(filename, **kwargs)
        self.cover = cover
        self.current_part = ""
        self.current_chapter = ""
        self._opening_page = False
        self._page_has_content = False
        self._outline_keys = 0
        body = Frame(MARGIN_X, MARGIN_BOTTOM, TEXT_WIDTH,
                     PAGE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM,
                     leftPadding=0, rightPadding=0, topPadding=0,
                     bottomPadding=0, id="body")
        cover_frame = Frame(0, 0, PAGE_WIDTH, PAGE_HEIGHT, id="cover")
        self.addPageTemplates([
            PageTemplate(id="cover", frames=cover_frame, onPage=draw_cover),
            PageTemplate(id="body", frames=body, onPage=begin_page,
                         onPageEnd=finish_page),
        ])

    def beforeDocument(self) -> None:
        self.current_part = ""
        self.current_chapter = ""
        self.current_segment = 0
        self.page_usage: list[tuple[int, int, float]] = []
        self._outline_keys = 0

    def afterFlowable(self, flowable: Flowable) -> None:
        if isinstance(flowable, (Paragraph, Table, Preformatted, TableOfContents)):
            self._page_has_content = True
        if not isinstance(flowable, BookHeading):
            return
        if hasattr(flowable, "segment"):
            self.current_segment = flowable.segment
        if flowable.kind == "part":
            self.current_part = flowable.toc_text
            self.current_chapter = ""
            self._opening_page = True
        elif flowable.kind == "chapter":
            if getattr(flowable, "toc_level", None) == 0:
                self.current_part = ""
            self.current_chapter = flowable.toc_text
            self._opening_page = True
        if hasattr(flowable, "toc_level"):
            self._outline_keys += 1
            key = f"heading-{self._outline_keys}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(flowable.toc_text, key,
                                      level=flowable.toc_level, closed=True)
            self.notify("TOCEntry", (flowable.toc_level, flowable.toc_text,
                                     self.page, key))


def draw_cover(canvas: Canvas, doc: BookDocTemplate) -> None:
    cover = doc.cover
    style = styles()
    canvas.saveState()
    canvas.setFillColor(TEAL)
    canvas.rect(0, PAGE_HEIGHT * 0.36, PAGE_WIDTH, PAGE_HEIGHT * 0.64, stroke=0, fill=1)
    canvas.setFillColor(ACCENT)
    canvas.rect(0, PAGE_HEIGHT * 0.36, PAGE_WIDTH, 3 * mm, stroke=0, fill=1)
    canvas.setStrokeColor(colors.HexColor("#245F6D"))
    canvas.setLineWidth(0.8)
    for step in range(9):
        radius = (30 + step * 14) * mm
        canvas.circle(PAGE_WIDTH + 5 * mm, PAGE_HEIGHT - 10 * mm, radius, stroke=1, fill=0)
    canvas.setFillColor(ACCENT_SOFT)
    canvas.setFont("Communalis-SansBold", 10)
    canvas.drawString(24 * mm, PAGE_HEIGHT - 34 * mm, cover["label"])
    y = PAGE_HEIGHT - 70 * mm
    for key in ("title", "subtitle"):
        paragraph = Paragraph(cover[key], style[key])
        _, height = paragraph.wrap(PAGE_WIDTH - 48 * mm, PAGE_HEIGHT)
        paragraph.drawOn(canvas, 24 * mm, y - height)
        y -= height + 8 * mm
    canvas.setFillColor(TEAL)
    canvas.setFont("Communalis-SansBold", 13)
    canvas.drawString(24 * mm, PAGE_HEIGHT * 0.36 - 20 * mm, cover["place"])
    note = Paragraph(cover["note"], ParagraphStyle(
        "CoverNote", parent=style["small"], fontSize=10, leading=14.5,
    ))
    _, height = note.wrap(PAGE_WIDTH - 48 * mm, PAGE_HEIGHT)
    note.drawOn(canvas, 24 * mm, PAGE_HEIGHT * 0.36 - 26 * mm - height)
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(24 * mm, 26 * mm, PAGE_WIDTH - 24 * mm, 26 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Communalis-Sans", 9)
    canvas.drawString(24 * mm, 19 * mm, "Projet Communalis")
    canvas.drawRightString(PAGE_WIDTH - 24 * mm, 19 * mm, cover["edition"])
    canvas.restoreState()


def begin_page(canvas: Canvas, doc: BookDocTemplate) -> None:
    doc._opening_page = False
    doc._page_has_content = False


def shorten(canvas: Canvas, text: str, font: str, size: float, width: float) -> str:
    if canvas.stringWidth(text, font, size) <= width:
        return text
    while text and canvas.stringWidth(text + "…", font, size) > width:
        text = text[:-1]
    return text.rstrip() + "…"


def finish_page(canvas: Canvas, doc: BookDocTemplate) -> None:
    if not doc._page_has_content:
        return
    used = doc.frame._y2 - doc.frame._y
    doc.page_usage.append((doc.page, doc.current_segment, used))
    canvas.saveState()
    odd = doc.page % 2 == 1
    if not doc._opening_page and (doc.current_part or doc.current_chapter):
        font, size = "Communalis-Sans", 7.6
        canvas.setFont(font, size)
        canvas.setFillColor(MUTED)
        header_y = PAGE_HEIGHT - 14 * mm
        if odd:
            text = doc.current_chapter or doc.current_part
            canvas.drawRightString(PAGE_WIDTH - MARGIN_X, header_y,
                                   shorten(canvas, text, font, size, TEXT_WIDTH))
        else:
            text = doc.current_part or doc.current_chapter
            canvas.drawString(MARGIN_X, header_y,
                              shorten(canvas, text, font, size, TEXT_WIDTH))
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.4)
        canvas.line(MARGIN_X, header_y - 2.6 * mm, PAGE_WIDTH - MARGIN_X,
                    header_y - 2.6 * mm)
    footer_y = 11 * mm
    canvas.setFont("Communalis-SansBold", 9)
    canvas.setFillColor(TEAL)
    title_font = "Communalis-Sans"
    if odd:
        canvas.drawRightString(PAGE_WIDTH - MARGIN_X, footer_y, str(doc.page))
        canvas.setFont(title_font, 7.6)
        canvas.setFillColor(MUTED)
        canvas.drawString(MARGIN_X, footer_y, doc.cover["running"])
    else:
        canvas.drawString(MARGIN_X, footer_y, str(doc.page))
        canvas.setFont(title_font, 7.6)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(PAGE_WIDTH - MARGIN_X, footer_y, doc.cover["running"])
    canvas.setFillColor(ACCENT)
    page_x = PAGE_WIDTH - MARGIN_X if odd else MARGIN_X
    canvas.rect(page_x - (6 * mm if odd else 0), footer_y + 4 * mm, 6 * mm, 0.9 * mm,
                stroke=0, fill=1)
    canvas.restoreState()


def front_matter(style: dict[str, ParagraphStyle]) -> list[Flowable]:
    legend = [
        ("[RÉSULTATS TOGO À INSÉRER]",
         "Observations, mesures, dates, lieux autorisés, protocole, effectifs, "
         "limites et preuve de publication à fournir par l'équipe du projet."),
        ("[À ACTUALISER]",
         "Information datée à vérifier : prix, droit, version, disponibilité, "
         "contacts ou statut d'un partenaire."),
        ("[À CONFIRMER]",
         "Hypothèse ou décision qui exige une validation explicite des personnes "
         "responsables et concernées."),
        ("[à compléter] / [à remplir] / [à désigner]",
         "Champ de fiche à renseigner avec une information réelle, un responsable "
         "ou une décision. Ne pas remplacer un champ par une estimation présentée "
         "comme un fait."),
    ]
    rows = [[Paragraph(paragraph_markup(mark), style["cell"]),
             Paragraph(escape(text), style["cell"])] for mark, text in legend]
    legend_table = Table(rows, colWidths=[TEXT_WIDTH * 0.36, TEXT_WIDTH * 0.64],
                         hAlign="LEFT")
    legend_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -2), 0.35, RULE),
        ("BOX", (0, 0), (-1, -1), 0.6, TEAL_MID),
        ("BACKGROUND", (0, 0), (0, -1), NOTE_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    situation = [
        ("Nom retenu et périmètre exact", "[à compléter — intitulé et sites]"),
        ("Période couverte et date d'arrêt des informations",
         "[à compléter — dates vérifiées]"),
        ("État réel de chaque activité",
         "[à compléter — réalisé, en cours, prévu, suspendu ou non engagé, avec preuve]"),
        ("Partenaires, rôles confirmés et autorisation de les nommer",
         "[à compléter — validation des personnes concernées]"),
        ("Langues, variantes et personnes habilitées à relire",
         "[à compléter — noms seulement avec accord]"),
        ("Sources de terrain, protocoles et droits de publication",
         "[à compléter — référence, date, consentements et restrictions]"),
        ("Matériel effectivement utilisé et versions",
         "[à compléter — inventaire vérifié, pas la liste envisagée]"),
        ("Résultats, échecs et limites autorisés à publier",
         "[à compléter — données, dénominateurs et validation]"),
        ("Budget réellement dépensé et monnaie",
         "[à compléter — pièces vérifiées et période]"),
        ("Responsable de validation éditoriale et date",
         "[à compléter — accord avant diffusion]"),
    ]
    return [
        Spacer(1, 10 * mm),
        BookHeading("LIRE LES ANNOTATIONS", style["chapter"], "chapter",
                    label="MODE D'EMPLOI", title="LIRE LES ANNOTATIONS"),
        Paragraph(
            "Ce cahier signale clairement ce qui reste à établir sur le terrain. "
            "Les repères suivants apparaissent surlignés dans le texte ; ils "
            "invitent à agir, pas à deviner.", style["body"]),
        Spacer(1, 4),
        legend_table,
        Spacer(1, 12),
        build_box("Règle de mise à jour", [Paragraph(
            "Pour chaque ajout, conserver la date, la source ou la preuve, les "
            "conditions de collecte, les incertitudes, les droits et la personne "
            "ayant validé la publication. Si l'information n'existe pas encore, "
            "garder le repère et expliquer pourquoi.", style["box"])], TEXT_WIDTH),
        PageBreak(),
        Spacer(1, 10 * mm),
        BookHeading("FICHE DE SITUATION DU PROJET", style["chapter"], "chapter",
                    label="À REMPLIR AVANT DIFFUSION",
                    title="FICHE DE SITUATION DU PROJET"),
        Paragraph(
            "À valider par l'équipe avant toute diffusion comme récit du projet. "
            "Cette fiche n'affirme aucun fait à sa place.", style["body"]),
        Spacer(1, 4),
        build_form(situation, TEXT_WIDTH, style),
    ]


TIGHT_STYLES = {
    "BookBody", "BodyLead", "BookBullet", "BookCheck", "BookNumbered",
    "Placeholder", "BoxBody",
}


def tighten(story: list[Flowable], segments: set[int]) -> None:
    """Slightly reduce spacing in chapters that would end with a near-empty page."""
    segment = 0
    cache: dict[str, ParagraphStyle] = {}
    for flowable in story:
        if isinstance(flowable, BookHeading) and hasattr(flowable, "segment"):
            segment = flowable.segment
            continue
        if segment not in segments:
            continue
        if isinstance(flowable, Spacer) and flowable.height <= 14:
            flowable.height *= 0.6
        if isinstance(flowable, Paragraph) and flowable.style.name in TIGHT_STYLES:
            name = flowable.style.name
            if name not in cache:
                cache[name] = ParagraphStyle(
                    f"{name}Tight",
                    parent=flowable.style,
                    leading=flowable.style.leading - 0.7,
                    spaceAfter=flowable.style.spaceAfter * 0.55,
                    spaceBefore=flowable.style.spaceBefore * 0.55,
                )
            flowable.style = cache[name]


def short_endings(usage: list[tuple[int, int, float]]) -> set[int]:
    short = set()
    for (page, segment, used), following in zip(usage, usage[1:] + [(0, -1, 0)]):
        if segment and following[1] != segment and used < 55 * mm:
            short.add(segment)
    return short


def build(
    output: Path,
    sources: tuple[str, ...] = SOURCES,
    technical: bool = False,
) -> int:
    register_fonts()
    style = styles()
    cover = {
        "label": (
            "DOSSIERS TECHNIQUES — RESSOURCE COMPLÉMENTAIRE"
            if technical else
            "CAHIER DE TERRAIN — INSTITUTIONS ET ACTEURS LOCAUX"
        ),
        "title": "COMMUNALIS",
        "subtitle": (
            "Dossiers techniques<br/>Énergie, langues, capteurs, données et sécurité"
            if technical else
            "Cahier produit et terrain<br/>Des services territoriaux utiles, "
            "adoptés et maintenables"
        ),
        "place": "Pilote proposé à Baguida, Togo",
        "note": (
            "Chapitres de conception à consulter selon le cas d'usage. Ils "
            "complètent le parcours produit et ne remplacent pas les validations "
            "locales ou professionnelles."
            if technical else
            "Parcours produit, adoption par le public, bootcamp et outils de "
            "déploiement. Les résultats et décisions de terrain restent à valider "
            "par les personnes et institutions concernées."
        ),
        "edition": "Édition de référence",
        "running": (
            "Communalis — Dossiers techniques"
            if technical else
            "Communalis — Cahier produit et terrain"
        ),
    }
    title = (
        "Communalis — Dossiers techniques"
        if technical else
        "Communalis — Cahier produit et terrain pour le Togo"
    )
    tight: set[int] = set()
    for _attempt in range(3):
        story = assemble_story(style, sources, technical)
        tighten(story, tight)
        doc = make_doc(output, cover, title, technical)
        output.parent.mkdir(parents=True, exist_ok=True)
        doc.multiBuild(story)
        short = short_endings(doc.page_usage) - tight
        if not short:
            break
        tight |= short
    data = output.read_bytes()
    return len(re.findall(rb"/Type\s*/Page\b", data))


def make_doc(output: Path, cover: dict[str, str], title: str,
             technical: bool) -> BookDocTemplate:
    return BookDocTemplate(
        str(output),
        cover,
        pagesize=A4,
        title=title,
        author="Projet Communalis",
        subject=(
            "Dossiers de conception technique"
            if technical else
            "Guide institutionnel et support de bootcamp — pilote proposé à Baguida"
        ),
        leftMargin=MARGIN_X,
        rightMargin=MARGIN_X,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
    )


def assemble_story(style: dict[str, ParagraphStyle], sources: tuple[str, ...],
                   technical: bool) -> list[Flowable]:
    story: list[Flowable] = [
        Spacer(1, 1),
        NextPageTemplate("body"),
        PageBreak(),
    ]
    if not technical:
        story.extend(front_matter(style))
        story.append(PageBreak())
    toc = TableOfContents(dotsMinLevel=1)
    toc.levelStyles = [
        ParagraphStyle("ContentsPart", fontName="Communalis-SansBold", fontSize=10.5,
                       leading=14, spaceBefore=9, textColor=TEAL,
                       leftIndent=0, firstLineIndent=0, rightIndent=24),
        ParagraphStyle("ContentsChapter", fontName="Communalis", fontSize=10.2,
                       leading=14.5, leftIndent=14, firstLineIndent=0,
                       rightIndent=24, textColor=INK),
    ]
    story.extend([
        Spacer(1, 10 * mm),
        BookHeading("SOMMAIRE", ParagraphStyle("ContentsHeading", parent=style["chapter"],
                    keepWithNext=False), "chapter", title="SOMMAIRE"),
        toc,
    ])
    for filename in sources:
        story.extend(parse_source(ROOT / filename, style, TEXT_WIDTH))
    segment = 0
    for flowable in story:
        if isinstance(flowable, BookHeading) and flowable.kind in {"part", "chapter"}:
            segment += 1
            flowable.segment = segment
    return story


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
