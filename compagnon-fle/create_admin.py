#!/usr/bin/env python3

import getpass
import sqlite3

from database import create_admin, initialize_database


def main() -> None:
    initialize_database()
    login = input("Identifiant administrateur : ").strip()
    password = getpass.getpass("Mot de passe (12 caractères minimum) : ")
    confirmation = getpass.getpass("Confirmez le mot de passe : ")

    if not login:
        raise SystemExit("L’identifiant est obligatoire.")
    if len(password) < 12:
        raise SystemExit("Le mot de passe doit contenir au moins 12 caractères.")
    if password != confirmation:
        raise SystemExit("Les mots de passe ne correspondent pas.")

    try:
        admin_id = create_admin(login, password)
    except sqlite3.IntegrityError:
        raise SystemExit("Cet identifiant existe déjà.")

    print(f"Administrateur créé (identifiant interne : {admin_id}).")


if __name__ == "__main__":
    main()
