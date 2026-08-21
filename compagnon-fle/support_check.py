#!/usr/bin/env python3
"""Contrôle du lot pilote Soutien, de la source au résultat."""

from __future__ import annotations

import http.client
import os
import re
import socket
import subprocess
import sys
import tempfile
import time
from http.cookies import SimpleCookie
from pathlib import Path
from urllib.parse import urlencode


ROOT = Path(__file__).resolve().parent


def request(port, method, path, data=None, cookie=""):
    body = urlencode(data or {}).encode() if data is not None else None
    headers = {"Content-Type": "application/x-www-form-urlencoded"} if body is not None else {}
    if cookie:
        headers["Cookie"] = cookie
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    connection.request(method, path, body=body, headers=headers)
    response = connection.getresponse()
    payload = response.read().decode("utf-8")
    result = response.status, dict(response.getheaders()), payload
    connection.close()
    return result


def value(body, name):
    match = re.search(rf'name="{name}" value="([^"]+)"', body)
    assert match, f"Champ {name} absent"
    return match.group(1)


def main():
    with tempfile.TemporaryDirectory() as temp:
        env = os.environ.copy()
        env.update({"DATABASE_PATH": str(Path(temp) / "support.sqlite3"), "HOST": "127.0.0.1", "APP_ENV": "test"})
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        env["PORT"] = str(port)

        setup = """import database
database.initialize_database()
learner_id = database.create_learner(first_name='Pilote', birth_date='2008-01-01', class_name='Soutien', login='pilote-soutien', password='Compagnon2026')
admin_id = database.create_admin('admin-pilote', 'AdminPilot123')
assert database.assign_level(learner_id=learner_id, level='A0', admin_id=admin_id)
"""
        subprocess.run([sys.executable, "-c", setup], cwd=ROOT, env=env, check=True)
        process = subprocess.Popen([sys.executable, "server.py"], cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            for _ in range(50):
                try:
                    if request(port, "GET", "/health")[0] == 200:
                        break
                except OSError:
                    time.sleep(.1)
            else:
                raise AssertionError("Le serveur de contrôle ne démarre pas")

            status, headers, _ = request(port, "POST", "/connexion/apprenant", {"login": "pilote-soutien", "password": "Compagnon2026"})
            assert status == 303
            morsel = SimpleCookie(headers["Set-Cookie"])["session"]
            cookie = f"session={morsel.value}"
            status, _, dashboard = request(port, "GET", "/espace-apprenant", cookie=cookie)
            assert status == 200 and "Soutien en français" in dashboard
            assert "40 questions" in dashboard and "72 questions" in dashboard
            assert "56 questions" in dashboard
            assert "Cohésion et liens logiques" in dashboard
            assert "64 questions" in dashboard and "Vocabulaire" in dashboard

            start = "/espace-apprenant/sequence-soutien-methodologie/demarrer?nouvelle=1"
            status, _, page = request(port, "GET", start, cookie=cookie)
            assert status == 200 and "Soutien · niveau commun" in page
            for index in range(40):
                question_id = value(page, "question_id")
                run_id = value(page, "run_id")
                csrf = value(page, "csrf_token")
                from support import SUPPORT_QUESTIONS
                question = next(item for item in SUPPORT_QUESTIONS if item["id"] == question_id)
                status, _, feedback = request(port, "POST", "/espace-apprenant/sequence-soutien-methodologie/demarrer", {
                    "csrf_token": csrf, "run_id": run_id, "question_id": question_id,
                    "answer": question["correct_answer"],
                }, cookie)
                assert status == 200 and "Bravo, c’est juste" in feedback
                target = "/espace-apprenant/sequence-soutien-methodologie/resultat" if index == 39 else "/espace-apprenant/sequence-soutien-methodologie/demarrer"
                status, _, page = request(port, "GET", target, cookie=cookie)
                assert status == 200
            assert "100 %" in page and "40 bonne(s) réponse(s)" in page and "Niveau commun" in page

            start = "/espace-apprenant/sequence-soutien-grammaire/demarrer?nouvelle=1"
            status, _, page = request(port, "GET", start, cookie=cookie)
            assert status == 200 and "Soutien · niveau commun" in page
            from support_grammar import SUPPORT_GRAMMAR_QUESTIONS
            for index in range(72):
                question_id = value(page, "question_id")
                run_id = value(page, "run_id")
                csrf = value(page, "csrf_token")
                question = next(item for item in SUPPORT_GRAMMAR_QUESTIONS if item["id"] == question_id)
                status, _, feedback = request(port, "POST", "/espace-apprenant/sequence-soutien-grammaire/demarrer", {
                    "csrf_token": csrf, "run_id": run_id, "question_id": question_id,
                    "answer": question["correct_answer"],
                }, cookie)
                assert status == 200 and "Bravo, c’est juste" in feedback
                target = "/espace-apprenant/sequence-soutien-grammaire/resultat" if index == 71 else "/espace-apprenant/sequence-soutien-grammaire/demarrer"
                status, _, page = request(port, "GET", target, cookie=cookie)
                assert status == 200
            assert "100 %" in page and "72 bonne(s) réponse(s)" in page and "Niveau commun" in page

            start = "/espace-apprenant/sequence-soutien-conjugaison/demarrer?nouvelle=1"
            status, _, page = request(port, "GET", start, cookie=cookie)
            assert status == 200 and "Soutien · niveau commun" in page
            from support_conjugation import SUPPORT_CONJUGATION_QUESTIONS
            for index in range(56):
                question_id = value(page, "question_id")
                run_id = value(page, "run_id")
                csrf = value(page, "csrf_token")
                question = next(item for item in SUPPORT_CONJUGATION_QUESTIONS if item["id"] == question_id)
                status, _, feedback = request(port, "POST", "/espace-apprenant/sequence-soutien-conjugaison/demarrer", {
                    "csrf_token": csrf, "run_id": run_id, "question_id": question_id,
                    "answer": question["correct_answer"],
                }, cookie)
                assert status == 200 and "Bravo, c’est juste" in feedback
                target = "/espace-apprenant/sequence-soutien-conjugaison/resultat" if index == 55 else "/espace-apprenant/sequence-soutien-conjugaison/demarrer"
                status, _, page = request(port, "GET", target, cookie=cookie)
                assert status == 200
            assert "100 %" in page and "56 bonne(s) réponse(s)" in page and "Niveau commun" in page

            start = "/espace-apprenant/sequence-soutien-vocabulaire/demarrer?nouvelle=1"
            status, _, page = request(port, "GET", start, cookie=cookie)
            assert status == 200 and "Soutien · niveau commun" in page
            from support_vocabulary import SUPPORT_VOCABULARY_QUESTIONS
            for index in range(64):
                question_id = value(page, "question_id")
                run_id = value(page, "run_id")
                csrf = value(page, "csrf_token")
                question = next(item for item in SUPPORT_VOCABULARY_QUESTIONS if item["id"] == question_id)
                status, _, feedback = request(port, "POST", "/espace-apprenant/sequence-soutien-vocabulaire/demarrer", {
                    "csrf_token": csrf, "run_id": run_id, "question_id": question_id,
                    "answer": question["correct_answer"],
                }, cookie)
                assert status == 200 and "Bravo, c’est juste" in feedback
                target = "/espace-apprenant/sequence-soutien-vocabulaire/resultat" if index == 63 else "/espace-apprenant/sequence-soutien-vocabulaire/demarrer"
                status, _, page = request(port, "GET", target, cookie=cookie)
                assert status == 200
            assert "100 %" in page and "64 bonne(s) réponse(s)" in page and "Niveau commun" in page

            start = "/espace-apprenant/sequence-soutien-cohesion/demarrer?nouvelle=1"
            status, _, page = request(port, "GET", start, cookie=cookie)
            assert status == 200 and "Soutien · niveau commun" in page
            from support_cohesion import SUPPORT_COHESION_QUESTIONS
            for index in range(56):
                question_id = value(page, "question_id")
                run_id = value(page, "run_id")
                csrf = value(page, "csrf_token")
                question = next(item for item in SUPPORT_COHESION_QUESTIONS if item["id"] == question_id)
                status, _, feedback = request(port, "POST", "/espace-apprenant/sequence-soutien-cohesion/demarrer", {
                    "csrf_token": csrf, "run_id": run_id, "question_id": question_id,
                    "answer": question["correct_answer"],
                }, cookie)
                assert status == 200 and "Bravo, c’est juste" in feedback
                target = "/espace-apprenant/sequence-soutien-cohesion/resultat" if index == 55 else "/espace-apprenant/sequence-soutien-cohesion/demarrer"
                status, _, page = request(port, "GET", target, cookie=cookie)
                assert status == 200
            assert "100 %" in page and "56 bonne(s) réponse(s)" in page and "Niveau commun" in page
        finally:
            process.terminate()
            process.wait(timeout=5)
    print("SUPPORT_CHECK_OK (288 questions)")


if __name__ == "__main__":
    main()
