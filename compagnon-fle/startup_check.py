#!/usr/bin/env python3
"""Contrôle de démarrage reproductible pour Compagnon FLE."""

from __future__ import annotations

import importlib
import os
import py_compile
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PYTHON_FILES = (
    "server.py",
    "database.py",
    "exercise_engine.py",
    "sequence_1.py",
    "sequences.py",
    "sequence_views.py",
)
REQUIRED_FILES = PYTHON_FILES + ("index.html", "styles.css")


def main() -> None:
    missing = [name for name in REQUIRED_FILES if not (BASE_DIR / name).is_file()]
    if missing:
        raise SystemExit("Fichiers requis manquants : " + ", ".join(missing))

    for name in PYTHON_FILES:
        py_compile.compile(str(BASE_DIR / name), doraise=True)

    with tempfile.TemporaryDirectory(prefix="compagnon-fle-check-") as tmp:
        os.environ["DATABASE_PATH"] = str(Path(tmp) / "startup-check.sqlite3")
        database = importlib.import_module("database")
        database.initialize_database()
        db_path = Path(os.environ["DATABASE_PATH"])
        if not db_path.is_file() or db_path.stat().st_size == 0:
            raise SystemExit("La base de données de contrôle n'a pas été créée correctement.")

        importlib.import_module("exercise_engine")
        importlib.import_module("sequence_1")
        importlib.import_module("sequences")
        importlib.import_module("sequence_views")
        importlib.import_module("server")

    print("Contrôle de démarrage réussi : fichiers, compilation, imports et base de données valides.")


if __name__ == "__main__":
    main()
