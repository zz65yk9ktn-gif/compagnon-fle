#!/usr/bin/env python3
from __future__ import annotations

import http.client
import os
import socket
import subprocess
import sys
import tempfile
import time
from http.cookies import SimpleCookie
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parent


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def request(port, method, path, data=None, cookie=None):
    body = urlencode(data or {}).encode()
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Content-Length": str(len(body))}
    if cookie:
        headers["Cookie"] = cookie
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    connection.request(method, path, body=body if method == "POST" else None, headers=headers)
    response = connection.getresponse()
    payload = response.read().decode("utf-8", "replace")
    result = response.status, dict(response.getheaders()), payload
    connection.close()
    return result


def main():
    with tempfile.TemporaryDirectory() as temp:
        database_path = Path(temp) / "passwords.sqlite3"
        os.environ["DATABASE_PATH"] = str(database_path)
        import database

        database.initialize_database()
        admin_id = database.create_admin("admin-test", "AdminPassword123")
        learner_id = database.create_learner(
            first_name="Élève", birth_date="2008-01-01", class_name="CAP",
            login="eleve-test", password="LearnerPassword123",
        )
        port = free_port()
        environment = os.environ.copy()
        environment.update({"HOST": "127.0.0.1", "PORT": str(port), "DATABASE_PATH": str(database_path)})
        process = subprocess.Popen([sys.executable, str(ROOT / "server.py")], cwd=ROOT, env=environment)
        try:
            for _ in range(50):
                try:
                    if request(port, "GET", "/health")[0] == 200:
                        break
                except OSError:
                    time.sleep(0.1)
            else:
                raise AssertionError("Le serveur ne démarre pas")

            status, _, body = request(port, "GET", "/connexion")
            assert status == 200 and "Mot de passe oublié ?" in body
            status, _, body = request(port, "POST", "/mot-de-passe-oublie", {"login": "inconnu"})
            assert status == 200 and "Si cet identifiant" in body
            status, _, body = request(port, "POST", "/mot-de-passe-oublie", {"login": "eleve-test"})
            assert status == 200 and "Si cet identifiant" in body
            assert len(database.list_pending_password_resets()) == 1

            temporary = "TemporaryPassword123"
            assert database.reset_learner_password(learner_id=learner_id, new_password=temporary, actor_id=admin_id)
            status, headers, _ = request(port, "POST", "/connexion/apprenant", {"login": "eleve-test", "password": temporary})
            assert status == 303 and headers["Location"] == "/mot-de-passe"
            morsel = SimpleCookie(headers["Set-Cookie"])["session"]
            cookie = f"session={morsel.value}"
            status, _, body = request(port, "GET", "/mot-de-passe", cookie=cookie)
            assert status == 200 and "doit être remplacé" in body
            # Read the CSRF token rendered in the page; it belongs to the subprocess session.
            marker = 'name="csrf_token" value="'
            csrf = body.split(marker, 1)[1].split('"', 1)[0]
            status, _, body = request(port, "POST", "/mot-de-passe", {
                "csrf_token": csrf, "current_password": "incorrect",
                "new_password": "NewLearnerPassword456", "confirmation": "NewLearnerPassword456",
            }, cookie)
            assert status == 401 and "Mot de passe actuel incorrect" in body
            status, headers, _ = request(port, "POST", "/mot-de-passe", {
                "csrf_token": csrf, "current_password": temporary,
                "new_password": "NewLearnerPassword456", "confirmation": "NewLearnerPassword456",
            }, cookie)
            assert status == 303 and headers["Location"] == "/connexion"
            assert "Max-Age=0" in headers["Set-Cookie"]
            status, _, _ = request(port, "GET", "/espace-apprenant", cookie=cookie)
            assert status == 401
            assert database.authenticate_learner("eleve-test", "NewLearnerPassword456")
            assert not database.authenticate_learner("eleve-test", temporary)
        finally:
            process.terminate()
            process.wait(timeout=5)

    print("PASSWORD_FLOW_CHECK_OK")


if __name__ == "__main__":
    main()
