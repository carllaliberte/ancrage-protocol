#!/usr/bin/env python3
"""Prove ecrire() calls flock LOCK_EX then LOCK_UN. .lock existing is not enough."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import ancrage  # noqa: E402


class FlockEcrire(unittest.TestCase):
    def test_ecrire_calls_flock_ex(self):
        if ancrage.fcntl is None:
            self.skipTest("fcntl absent")
        mock = MagicMock()
        mock.LOCK_EX = getattr(ancrage.fcntl, "LOCK_EX", 2)
        mock.LOCK_UN = getattr(ancrage.fcntl, "LOCK_UN", 8)
        orig = ancrage.fcntl
        ancrage.fcntl = mock
        try:
            with tempfile.TemporaryDirectory() as d:
                p = Path(d) / "a.json"
                ancrage.ecrire("figure", "2028-08-31", p)
            calls = [c.args[1] for c in mock.flock.call_args_list]
            self.assertGreaterEqual(len(calls), 2)
            self.assertEqual(calls[0], mock.LOCK_EX)
            self.assertEqual(calls[-1], mock.LOCK_UN)
        finally:
            ancrage.fcntl = orig


if __name__ == "__main__":
    unittest.main()
