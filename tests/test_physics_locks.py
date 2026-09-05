import json
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import MagicMock
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

    def test_ecrire_sidecar_lock(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "a.json"
            ancrage.ecrire("figure", "2028-08-31", p)
            lock = p.with_suffix(p.suffix + ".lock")
            self.assertTrue(lock.is_file())
            out = ancrage.verifier(p, today=date(2026, 9, 4))
            self.assertEqual(out["objet"], "figure")

    def test_ecrire_calls_flock_ex(self):
        fake = MagicMock()
        fake.LOCK_EX = 2
        fake.LOCK_UN = 8
        orig = ancrage.fcntl
        ancrage.fcntl = fake
        try:
            with tempfile.TemporaryDirectory() as d:
                p = Path(d) / "a.json"
                ancrage.ecrire("figure", "2028-08-31", p)
        finally:
            ancrage.fcntl = orig
        ops = [c.args[1] for c in fake.flock.call_args_list]
        self.assertIn(fake.LOCK_EX, ops)
        self.assertIn(fake.LOCK_UN, ops)
        self.assertEqual(ops[0], fake.LOCK_EX)
        self.assertEqual(ops[-1], fake.LOCK_UN)


if __name__ == "__main__":
    unittest.main()
