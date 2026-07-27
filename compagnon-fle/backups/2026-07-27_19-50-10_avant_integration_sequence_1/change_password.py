#!/usr/bin/env python3

import getpass
import sqlite3

from database import connect, hash_password, initialize_database, normalize_login, verify_password


def main() -> None:
    initialize_database()
    login = normalize_login(input("Identifiant du compte : "))
    current_password = getpass.getpass("Mot de passe actuel : ")
    with connect() as database:
        user = database.execute(
            "SELECT id, password_hash FROM users WHERE login = ?", (login,)
        ).fetchone()
        if not user or not verify_password(current_password, user["password_hash"]):
            raise SystemExit("Identifiant ou mot de passe actuel incorrect.")
        new_password = getpass.getpass("Nouveau mot de passe (14 caractères minimum) : ")
        confirmation = getpass.getpass("Confirmez le nouveau mot de passe : ")
        if new_password != confirmation:
            raise SystemExit("Les mots de passe ne correspondent pas.")
        if (
            len(new_password) < 14
            or not any(character.isalpha() for character in new_password)
            or not any(character.isdigit() for character in new_password)
        ):
            raise SystemExit(
                "Le nouveau mot de passe doit contenir au moins 14 caractères, avec des lettres et des chiffres."
            )
        try:
            database.execute(
                """
                UPDATE users
                SET password_hash = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (hash_password(new_password), user["id"]),
            )
        except sqlite3.DatabaseError as error:
            raise SystemExit(f"Modification impossible : {error}") from error
    print("Mot de passe modifié.")


if __name__ == "__main__":
    main()
