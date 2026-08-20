#!/usr/bin/env python3

import getpass
import os
from pathlib import Path

from database import (
    authenticate_admin,
    backup_database,
    database_health_report,
    database_timestamp,
    initialize_database,
    reset_admin_password,
)


def main() -> None:
    initialize_database()
    login = os.environ.get("ADMIN_LOGIN") or input("Identifiant administrateur : ").strip()
    new_password = os.environ.get("ADMIN_NEW_PASSWORD") or getpass.getpass(
        "Nouveau mot de passe (14 caractères minimum) : "
    )
    if "ADMIN_NEW_PASSWORD" not in os.environ:
        confirmation = getpass.getpass("Confirmez le nouveau mot de passe : ")
        if new_password != confirmation:
            raise SystemExit("Les mots de passe ne correspondent pas.")

    backup_dir = Path(os.environ.get("ADMIN_BACKUP_DIR", "backups/admin-password-reset"))
    backup_path = backup_database(backup_dir / f"compagnon_fle-{database_timestamp()}.sqlite3")
    if not reset_admin_password(login=login, new_password=new_password):
        raise SystemExit("Réinitialisation refusée : administrateur actif introuvable ou mot de passe insuffisant.")
    if not authenticate_admin(login, new_password):
        raise SystemExit("Échec de vérification après réinitialisation. Restaurer la sauvegarde.")
    if not database_health_report()["ok"]:
        raise SystemExit("La base ne passe plus le contrôle d’intégrité. Restaurer la sauvegarde.")
    print(f"Mot de passe administrateur réinitialisé. Sauvegarde : {backup_path}")


if __name__ == "__main__":
    main()
