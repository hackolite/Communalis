import tempfile
import unittest
from pathlib import Path

from reportlab.platypus import Paragraph, Preformatted, Table

from build_book import build_table, parse_source, register_fonts, styles


class BookLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        register_fonts()

    def parse(self, text):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.txt"
            source.write_text(text, encoding="utf-8")
            return parse_source(source, styles(), 480)

    def test_heading_hierarchy_and_separators(self):
        story = self.parse(
            "PARTIE A — PRÉPARER\n\nCHAPITRE 1 — DIAGNOSTIC\n"
            "=================\n\n1.1 — Méthode\n"
        )
        headings = [item for item in story if isinstance(item, Paragraph)]
        self.assertEqual([item.style.name for item in headings],
                         ["PartHeading", "ChapterHeading", "SubHeading"])
        self.assertEqual(headings[0].toc_level, 0)
        self.assertEqual(headings[1].toc_level, 1)

    def test_box_drawing_is_not_a_table(self):
        story = self.parse("  Début → contrôle\n  │       ↓\n  └── résultat\n")
        self.assertEqual(sum(isinstance(item, Preformatted) for item in story), 1)
        self.assertFalse(any(isinstance(item, Table) for item in story))
        diagram = next(item for item in story if isinstance(item, Preformatted))
        self.assertEqual(diagram.style.fontName, "Communalis-Mono")

    def test_wide_table_keeps_labelled_fields(self):
        table = build_table(["Nom | État | Date | Source", "Lab | Prévu | 2026 | registre"], 480)
        cells = [[cell.getPlainText() if isinstance(cell, Paragraph) else cell
                  for cell in row] for row in table._cellvalues]
        self.assertEqual(cells[:4], [["Nom", "Lab"], ["État", "Prévu"],
                                    ["Date", "2026"], ["Source", "registre"]])
        self.assertEqual(len(table._colWidths), 2)

    def test_wrapped_source_table_preserves_columns(self):
        table = build_table(
            ["Phase | Travail | Livrable | Décision",
             "1 | Écouter | Diagnostic |",
             "    Le besoin est-il défini ?",
             "2 | Vérifier les moyens |",
             "    Budget | Peut-on poursuivre ?"], 480
        )
        values = [cell.getPlainText() for row in table._cellvalues
                  for cell in row if isinstance(cell, Paragraph)]
        self.assertIn("Le besoin est-il défini ?", values)
        self.assertIn("Budget", values)
        self.assertIn("Peut-on poursuivre ?", values)

    def test_markdown_table_drops_separator(self):
        table = build_table(["| Champ | Valeur |", "|---|---|", "| Site | Lomé |"], 480)
        self.assertEqual(len(table._cellvalues), 2)
        self.assertEqual(len(table._colWidths), 2)
        self.assertEqual(table.repeatRows, 1)

    def test_bibliographic_link_stays_with_reference(self):
        story = self.parse("• Lewis et al., RAG :\n  https://arxiv.org/abs/2005.11401\n")
        paragraphs = [item for item in story if isinstance(item, Paragraph)]
        self.assertEqual(len(paragraphs), 1)
        self.assertIn("https://arxiv.org/abs/2005.11401", paragraphs[0].getPlainText())


if __name__ == "__main__":
    unittest.main()
