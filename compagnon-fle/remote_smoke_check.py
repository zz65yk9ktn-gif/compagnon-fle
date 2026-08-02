#!/usr/bin/env python3
"""Contrôle minimal d'une instance Compagnon FLE déjà déployée."""
from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.parse
import urllib.request

CHECKS = [
    ("/health", 200, "OK"),
    ("/", 200, "Compagnon"),
    ("/connexion", 200, "connexion"),
    ("/inscription", 200, "inscription"),
    ("/administration", 200, "administration"),
]


def fetch(url: str) -> tuple[int, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "Compagnon-FLE-Remote-Check/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.status, response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")


def main() -> int:
    parser = argparse.ArgumentParser(description="Teste une version distante de Compagnon FLE.")
    parser.add_argument("base_url", help="Adresse publique, par exemple https://compagnon-fle.onrender.com")
    args = parser.parse_args()

    parsed = urllib.parse.urlparse(args.base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        print("Adresse invalide : utilisez une URL complète en http:// ou https://", file=sys.stderr)
        return 2

    base = args.base_url.rstrip("/")
    failures: list[str] = []
    for path, expected_status, expected_text in CHECKS:
        status, body = fetch(base + path)
        text_ok = expected_text.casefold() in body.casefold()
        ok = status == expected_status and text_ok
        print(f"{'OK' if ok else 'ECHEC'} {path} — HTTP {status}")
        if not ok:
            failures.append(
                f"{path}: statut {status} au lieu de {expected_status}, "
                f"texte attendu absent={not text_ok}"
            )

    if failures:
        print("\nREMOTE_SMOKE_CHECK_FAILED", file=sys.stderr)
        for failure in failures:
            print("- " + failure, file=sys.stderr)
        return 1

    print("\nREMOTE_SMOKE_CHECK_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
