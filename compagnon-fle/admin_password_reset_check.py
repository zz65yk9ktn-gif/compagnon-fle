#!/usr/bin/env python3
from __future__ import annotations

import os
import tempfile
from pathlib import Path


with tempfile.TemporaryDirectory() as tmp:
    os.environ["DATABASE_PATH"] = str(Path(tmp) / "reset-check.sqlite3")
    import database as db

    db.initialize_database()
    admin_id = db.create_admin("admin-test", "AncienMotDePasse123!")
    learner_id = db.create_learner(
        first_name="Élève",
        birth_date="2008-01-01",
        class_name="CAP",
        login="eleve-test",
        password="MotDePasseEleve123!",
    )
    with db.connect() as database:
        before = tuple(database.execute("SELECT * FROM learner_profiles WHERE user_id = ?", (learner_id,)).fetchone())
        learner_hash = database.execute("SELECT password_hash FROM users WHERE id = ?", (learner_id,)).fetchone()[0]

    assert not db.reset_admin_password(login="admin-test", new_password="tropcourt1")
    assert db.authenticate_admin("admin-test", "AncienMotDePasse123!")
    assert db.reset_admin_password(login="admin-test", new_password="NouveauMotDePasse456!")
    assert not db.authenticate_admin("admin-test", "AncienMotDePasse123!")
    assert db.authenticate_admin("admin-test", "NouveauMotDePasse456!")["id"] == admin_id

    with db.connect() as database:
        after = tuple(database.execute("SELECT * FROM learner_profiles WHERE user_id = ?", (learner_id,)).fetchone())
        current_learner_hash = database.execute("SELECT password_hash FROM users WHERE id = ?", (learner_id,)).fetchone()[0]
    assert after == before
    assert current_learner_hash == learner_hash
    assert db.authenticate_learner("eleve-test", "MotDePasseEleve123!")
    assert db.database_health_report()["ok"]

print("Réinitialisation administrateur : OK")
