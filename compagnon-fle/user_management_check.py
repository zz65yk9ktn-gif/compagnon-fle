#!/usr/bin/env python3
from __future__ import annotations
import os, tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    db_path = Path(tmp) / 'users.sqlite3'
    os.environ['DATABASE_PATH'] = str(db_path)
    import database as db
    db.initialize_database()
    admin_id = db.create_admin('admin-test', 'MotDePasseAdmin123!')
    teacher_id = db.create_teacher('prof-test', 'MotDePasseProf123!')
    learner_id = db.create_learner(first_name='Test', birth_date='2008-01-01', class_name='CAP', login='eleve-test', password='MotDePasseEleve123!')
    assert db.authenticate_admin('admin-test', 'MotDePasseAdmin123!')
    assert not db.authenticate_admin('prof-test', 'MotDePasseProf123!')
    assert db.authenticate_teacher('prof-test', 'MotDePasseProf123!')
    assert db.authenticate_staff('prof-test', 'MotDePasseProf123!')
    assert db.authenticate_learner('eleve-test', 'MotDePasseEleve123!')
    assert db.assign_level(learner_id=learner_id, level='A1', admin_id=teacher_id)
    assert not db.set_user_active(user_id=learner_id, active=False, actor_id=teacher_id)
    assert db.set_user_active(user_id=learner_id, active=False, actor_id=admin_id)
    assert not db.authenticate_learner('eleve-test', 'MotDePasseEleve123!')
    assert db.set_user_active(user_id=learner_id, active=True, actor_id=admin_id)
    assert db.authenticate_learner('eleve-test', 'MotDePasseEleve123!')
    assert db.database_health_report()['integrity_check'] == 'ok'
print('Gestion des utilisateurs : OK')
