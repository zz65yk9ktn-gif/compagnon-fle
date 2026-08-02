#!/usr/bin/env python3
"""Vérifie le contenu d'un dossier ou d'une archive de livraison Compagnon FLE."""
from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

REQUIRED = {
    "server.py", "database.py", "exercise_engine.py", "sequences.py",
    "sequence_1.py", "sequence_views.py", "index.html", "styles.css",
    "render.yaml", "README.md", "create_admin.py", "deployment_check.py",
    "startup_check.py", "database_check.py", "user_management_check.py",
    "navigation_check.py", "exercise_framework_check.py", "interface_check.py",
    "remote_smoke_check.py", "DEPLOYMENT_MANIFEST.txt",
}
FORBIDDEN_PARTS = {"__pycache__", "backups", "data"}
FORBIDDEN_SUFFIXES = {".sqlite", ".sqlite3", ".db", ".pyc"}


def normalized_names(path: Path) -> set[str]:
    if path.is_dir():
        return {
            file.relative_to(path).as_posix()
            for file in path.rglob("*")
            if file.is_file()
        }
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            return {name.rstrip("/") for name in archive.namelist() if not name.endswith("/")}
    raise ValueError("La cible doit être un dossier ou une archive ZIP.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?", default=".")
    args = parser.parse_args()
    target = Path(args.target).resolve()

    try:
        names = normalized_names(target)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    root_names = {name.split("/", 1)[-1] if "/" in name else name for name in names}
    # Accepte une archive avec ou sans dossier racine unique.
    basenames = {Path(name).name for name in names}
    missing = sorted(REQUIRED - basenames)
    forbidden = sorted(
        name for name in names
        if any(part in FORBIDDEN_PARTS for part in Path(name).parts)
        or Path(name).suffix.lower() in FORBIDDEN_SUFFIXES
        or ".before_" in name
    )

    if missing or forbidden:
        if missing:
            print("Fichiers obligatoires manquants : " + ", ".join(missing), file=sys.stderr)
        if forbidden:
            print("Fichiers interdits dans la livraison :", file=sys.stderr)
            for name in forbidden:
                print("- " + name, file=sys.stderr)
        return 1

    print(f"RELEASE_INTEGRITY_OK ({len(names)} fichiers)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
