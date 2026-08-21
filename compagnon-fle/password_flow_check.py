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
            assert status == 200 and "mot de passe commun donné par votre enseignant" in body
            status, _, body = request(port, "GET", "/mot-de-passe-oublie")
            assert status == 200 and "même pour tous les élèves" in body

            status, _, body = request(port, "GET", "/inscription")
            assert status == 200 and 'name="password"' not in body
            status, _, body = request(port, "POST", "/inscription", {
                "first_name": "Nouveau", "birth_date": "2009-02-03",
                "class_name": "CAP", "login": "nouvel-eleve",
            })
            assert status == 200 and "Inscription enregistrée" in body
            assert "mot de passe commun" in body
            assert database.authenticate_learner("nouvel-eleve", "Compagnon2026")

            status, _, body = request(port, "POST", "/connexion/apprenant", {
                "login": "eleve-test", "password": "A" * 257,
            })
            assert status == 401 and "Identifiant ou mot de passe incorrect" in body
            assert not database.verify_password("A" * 257, database.hash_password("Password1234"))

            # The shared password works even for an existing learner whose stored password differs.
            status, headers, _ = request(port, "POST", "/connexion/apprenant", {
                "login": "eleve-test", "password": "Compagnon2026",
            })
            assert status == 303 and headers["Location"] == "/espace-apprenant"
            morsel = SimpleCookie(headers["Set-Cookie"])["session"]
            cookie = f"session={morsel.value}"
            status, headers, _ = request(port, "GET", "/mot-de-passe", cookie=cookie)
            assert status == 303 and headers["Location"] == "/espace-apprenant"

            marker = 'name="csrf_token" value="'

            # Staff accounts keep their separate protected change flow.
            status, headers, _ = request(port, "POST", "/administration/connexion", {
                "login": "admin-test", "password": "AdminPassword123",
            })
            assert status == 303 and headers["Location"] == "/administration"
            admin_morsel = SimpleCookie(headers["Set-Cookie"])["session"]
            admin_cookie = f"session={admin_morsel.value}"
            status, _, body = request(port, "GET", "/mot-de-passe", cookie=admin_cookie)
            assert status == 200
            admin_csrf = body.split(marker, 1)[1].split('"', 1)[0]

            status, _, body = request(port, "POST", "/mot-de-passe", {
                "csrf_token": admin_csrf, "current_password": "AdminPassword123",
                "new_password": "NewAdminPassword456", "confirmation": "DifferentPassword789",
            }, admin_cookie)
            assert status == 400 and "ne correspondent pas" in body

            status, headers, _ = request(port, "POST", "/mot-de-passe", {
                "csrf_token": admin_csrf, "current_password": "AdminPassword123",
                "new_password": "NewAdminPassword456", "confirmation": "NewAdminPassword456",
            }, admin_cookie)
            assert status == 303 and headers["Location"] == "/administration"
            assert "Max-Age=0" in headers["Set-Cookie"]
            status, _, body = request(port, "GET", "/administration", cookie=admin_cookie)
            assert status == 200 and "Administration des inscriptions" in body
            assert database.authenticate_admin("admin-test", "NewAdminPassword456")
            assert not database.authenticate_admin("admin-test", "AdminPassword123")

            # Login errors remain generic, accessible, and rate-limited.
            for _ in range(5):
                status, _, body = request(port, "POST", "/administration/connexion", {
                    "login": "admin-test", "password": "WrongPassword123",
                })
                assert status == 401 and 'role="alert"' in body
            status, _, body = request(port, "POST", "/administration/connexion", {
                "login": "admin-test", "password": "WrongPassword123",
            })
            assert status == 429 and "Trop de tentatives" in body
        finally:
            process.terminate()
            process.wait(timeout=5)

    print("PASSWORD_FLOW_CHECK_OK")


if __name__ == "__main__":
    main()
