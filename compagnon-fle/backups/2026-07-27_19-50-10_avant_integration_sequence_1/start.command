#!/bin/zsh

cd "${0:A:h}" || exit 1
echo "Compagnon FLE : http://localhost:8000"
echo "Pour arrêter l’application, appuyez sur Ctrl+C."
python3 server.py
