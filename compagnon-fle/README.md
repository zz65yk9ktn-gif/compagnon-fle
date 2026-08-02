# Compagnon FLE

Application web Python avec inscription des apprenants, attribution manuelle des niveaux, exercices par séquence et suivi enseignant.

## Contrôle complet avant lancement

```sh
python3 deployment_check.py
```

Ce contrôle vérifie les fichiers indispensables, la compilation, les imports, la base SQLite, les rôles, le moteur d’exercices, l’interface et les principales routes HTTP.

## Première utilisation : créer un administrateur

```sh
python3 create_admin.py
```

## Lancer en local

```sh
python3 server.py
```

Puis ouvrir `http://localhost:8000`. La route de contrôle est `http://localhost:8000/health`.

## Déploiement Render

Render exécute :

```sh
python3 deployment_check.py
```

puis démarre :

```sh
python3 -u server.py
```

La base persistante est stockée dans `/var/data/compagnon_fle.sqlite3` grâce au disque persistant déclaré dans `render.yaml`.

## Contenu obligatoire du dépôt

`server.py`, `database.py`, `exercise_engine.py`, `sequences.py`, `sequence_1.py`, `sequence_views.py`, `index.html`, `styles.css`, `render.yaml`, les scripts de contrôle et `create_admin.py`.

## Après mise en ligne

```sh
python3 remote_smoke_check.py https://ADRESSE-PUBLIQUE-RENDER
```

La procédure complète figure dans `POST_DEPLOYMENT.md`.
