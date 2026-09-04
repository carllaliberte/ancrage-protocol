import json
import tempfile
import unittest
from datetime import date
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ancrage


class Physics(unittest.TestCase):
    def test_refuse_passe(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "a.json"
            with self.assertRaises(SystemExit):
                ancrage.ecrire("figure", "2020-01-01", p)

    def test_verifier_futur(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "a.json"
            ancrage.ecrire("figure", "2028-08-31", p)
            out = ancrage.verifier(p, today=date(2026, 9, 4))
            self.assertEqual(out["avant"], "2028-08-31")
            with self.assertRaises(SystemExit):
                ancrage.verifier(p, today=date(2028, 8, 31))

    def test_interdit_physique_crypto(self):
        text = Path("INTERDIT.md").read_text(encoding="utf-8")
        self.assertIn("Physique", text)
        self.assertIn("ε = 0", text)

    def test_example(self):
        card = json.loads(Path("examples/figure.ancrage.json").read_text())
        self.assertEqual(card["format"], "ANCRAGE-v0")


if __name__ == "__main__":
    unittest.main()
