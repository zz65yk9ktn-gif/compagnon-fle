#!/usr/bin/env python3
"""Création sécurisée du premier compte administrateur."""
from __future__ import annotations

import getpass
import sys

from database import create_admin, init_db


def main() -> int:
    init_db()
    login = input("Identifiant administrateur : ").strip()
    if not login:
        print("Erreur : identifiant vide.", file=sys.stderr)
        return 1
    password = getpass.getpass("Mot de passe : ")
    confirmation = getpass.getpass("Confirmer le mot de passe : ")
    if password != confirmation:
        print("Erreur : les mots de passe ne correspondent pas.", file=sys.stderr)
        return 1
    if len(password) < 10:
        print("Erreur : utilisez au moins 10 caractères.", file=sys.stderr)
        return 1
    try:
        admin_id = create_admin(login, password)
    except Exception as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    print(f"Compte administrateur créé (id={admin_id}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
