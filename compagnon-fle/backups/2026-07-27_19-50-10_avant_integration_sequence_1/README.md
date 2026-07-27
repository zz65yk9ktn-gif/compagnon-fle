# Compagnon FLE

Application web locale avec inscription des apprenants et attribution manuelle des niveaux par un administrateur.

La préparation d’un éventuel pilote en ligne est décrite dans `DEPLOIEMENT.md`. Aucun service distant n’est créé automatiquement.

## Première utilisation : créer un administrateur

Dans Terminal :

```sh
cd "/Users/canellada/Documents/Codex/2026-07-24/referenced-chatgpt-conversation-this-is-untrusted/compagnon-fle"
python3 create_admin.py
```

## Lancer

Dans Terminal :

```sh
cd "/Users/canellada/Documents/Codex/2026-07-24/referenced-chatgpt-conversation-this-is-untrusted/compagnon-fle"
python3 server.py
```

Puis ouvrir <http://localhost:8000> dans le navigateur.

## Arrêter

Revenir dans Terminal et appuyer sur `Ctrl+C`.
