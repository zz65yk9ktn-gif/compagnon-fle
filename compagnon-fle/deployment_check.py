#!/usr/bin/env python3
"""Contrôle complet du paquet avant déploiement Render."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

CHECKS = [
    "startup_check.py",
    "database_check.py",
    "user_management_check.py",
    "exercise_framework_check.py",
    "interface_check.py",
    "navigation_check.py",
    "password_flow_check.py",
]


def main() -> int:
    root = Path(__file__).resolve().parent
    missing = [name for name in CHECKS if not (root / name).is_file()]
    if missing:
        print("Contrôles manquants : " + ", ".join(missing), file=sys.stderr)
        return 1

    for name in CHECKS:
        print(f"\n=== {name} ===", flush=True)
        result = subprocess.run([sys.executable, str(root / name)], cwd=root)
        if result.returncode != 0:
            print(f"Échec du contrôle : {name}", file=sys.stderr)
            return result.returncode

    print("\nDEPLOYMENT_CHECK_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
