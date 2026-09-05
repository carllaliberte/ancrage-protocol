#!/usr/bin/env python3
"""ANCRAGE v0 — re-mesurer avant date. Physique ≠ crypto."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

FORMAT = "ANCRAGE-v0"
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

try:
    import fcntl
except ImportError:
    fcntl = None  # type: ignore


def _parse_day(s: str) -> date:
    if not DATE.match(s):
        raise SystemExit("refus: date")
    y, m, d = map(int, s.split("-"))
    return date(y, m, d)


def _lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = path.with_suffix(path.suffix + ".lock")
    fh = open(lock_path, "a+", encoding="utf-8")
    if fcntl is not None:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
    return fh


def _unlock(fh) -> None:
    if fcntl is not None:
        fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
    fh.close()


def ecrire(objet: str, avant: str, dest: Path) -> dict:
    fh = _lock(dest)
    try:
        day = _parse_day(avant)
        if day <= date.today():
            raise SystemExit("refus: horizon deja passe")
        if dest.exists():
            raise SystemExit("refus: nouvel acte requis")
        card = {"format": FORMAT, "objet": objet, "avant": avant}
        dest.write_text(json.dumps(card, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return card
    finally:
        _unlock(fh)


def verifier(path: Path, today: date | None = None) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("format") != FORMAT:
        raise SystemExit("refus: format")
    day = _parse_day(str(data.get("avant", "")))
    now = today or date.today()
    if day <= now:
        raise SystemExit("refus: a re-mesurer")
    return data


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="ancrage")
    sub = p.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("ecrire")
    e.add_argument("--objet", required=True)
    e.add_argument("--avant", required=True)
    e.add_argument("--vers", default="carte.ancrage.json")
    v = sub.add_parser("verifier")
    v.add_argument("carte")
    r = sub.add_parser("lire")
    r.add_argument("carte")
    args = p.parse_args(argv)
    if args.cmd == "ecrire":
        print(json.dumps(ecrire(args.objet, args.avant, Path(args.vers)), ensure_ascii=False))
        return 0
    if args.cmd == "verifier":
        print(json.dumps(verifier(Path(args.carte)), ensure_ascii=False))
        return 0
    print(Path(args.carte).read_text(encoding="utf-8"), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
