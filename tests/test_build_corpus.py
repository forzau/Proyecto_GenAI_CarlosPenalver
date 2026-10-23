import unittest

from scripts.build_corpus import markdown_cards


class MarkdownCardsTest(unittest.TestCase):
    def test_preserves_conditions_and_alternatives(self):
        text = "# Fuente\nNota general\n\n## Entry / Oversteer\nLow speed: A OR B.\n\n## Exit / Oversteer\nHigh speed: C.\n"
        self.assertEqual(markdown_cards(text), [
            ("Entry / Oversteer", "Low speed: A OR B."),
            ("Exit / Oversteer", "High speed: C."),
        ])

    def test_rejects_missing_empty_and_duplicate_cards(self):
        for text in ("# Solo título", "\n## Caso\n", "\n## Caso\nA\n## Caso\nB"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                markdown_cards(text)


if __name__ == "__main__":
    unittest.main()
