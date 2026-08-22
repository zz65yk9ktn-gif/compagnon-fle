#!/usr/bin/env python3
from __future__ import annotations

import http.client
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SERVER = ROOT / "server.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def static_checks() -> None:
    text = SERVER.read_text(encoding="utf-8")
    required = [
        "HttpOnly",
        "SameSite=Strict",
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "Cross-Origin-Opener-Policy",
        "MAX_POST_BODY_BYTES",
        "MAX_ACTIVE_SESSIONS",
        "secrets.compare_digest",
        "MAX_LOGIN_FAILURES",
        "invalidate_user_sessions",
        "MAX_PASSWORD_LENGTH",
    ]
    for marker in required:
        require(marker in text, f"Protection absente : {marker}")


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def request(port: int, method: str, path: str, body: bytes | None = None, headers=None):
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    conn.request(method, path, body=body, headers=headers or {})
    response = conn.getresponse()
    payload = response.read()
    result = (response.status, dict(response.getheaders()), payload)
    conn.close()
    return result


def runtime_checks() -> None:
    port = free_port()
    env = os.environ.copy()
    env.update({"HOST": "127.0.0.1", "PORT": str(port), "RENDER": "true", "COMPAGNON_FLE_DB": str(ROOT / "security_check.sqlite3")})
    process = subprocess.Popen([sys.executable, str(SERVER)], cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(50):
            try:
                status, headers, _ = request(port, "GET", "/health")
                if status == 200:
                    break
            except OSError:
                time.sleep(0.1)
        else:
            raise AssertionError("Le serveur de contrôle ne démarre pas")

        require(headers.get("Strict-Transport-Security"), "HSTS absent en production")
        require(headers.get("X-Frame-Options") == "DENY", "Protection anti-frame absente")
        require("object-src 'none'" in headers.get("Content-Security-Policy", ""), "CSP insuffisante")

        status, home_headers, _ = request(port, "GET", "/")
        require(status == 200, "Accueil indisponible")
        require(home_headers.get("Strict-Transport-Security"), "HSTS absent de l’accueil")
        require(home_headers.get("X-Frame-Options") == "DENY", "Protection anti-frame absente de l’accueil")
        require(home_headers.get("Cache-Control") == "no-store", "Cache privé absent de l’accueil")

        status, _, _ = request(port, "POST", "/connexion/apprenant", body=b"{}", headers={"Content-Type": "application/json", "Content-Length": "2"})
        require(status == 400, f"Le JSON inattendu doit être refusé, statut reçu : {status}")

        body = b"x" * 20001
        status, _, _ = request(port, "POST", "/connexion/apprenant", body=body, headers={"Content-Type": "application/x-www-form-urlencoded", "Content-Length": str(len(body))})
        require(status == 413, f"Une requête trop volumineuse doit être refusée, statut reçu : {status}")
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        for suffix in ("", "-wal", "-shm"):
            (ROOT / f"security_check.sqlite3{suffix}").unlink(missing_ok=True)


if __name__ == "__main__":
    static_checks()
    runtime_checks()
    print("SECURITY_CHECK_OK")
