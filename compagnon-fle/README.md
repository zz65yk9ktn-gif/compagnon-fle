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

## Réinitialiser le mot de passe administrateur

Exécuter la commande sur l’hôte qui possède la base persistante. Le script crée
d’abord une sauvegarde SQLite cohérente, ne cible qu’un compte actif de rôle
`admin`, puis contrôle la nouvelle connexion et l’intégrité de la base.

```sh
ADMIN_LOGIN='identifiant-admin' python3 change_password.py
```

Le mot de passe est demandé sans être affiché. Pour une exécution automatisée,
`ADMIN_NEW_PASSWORD` est accepté temporairement dans l’environnement ; ne jamais
l’inscrire dans Git, dans `render.yaml` ou dans une ligne de commande conservée.

La sauvegarde est placée par défaut dans `backups/admin-password-reset/`. Définir
`ADMIN_BACKUP_DIR` pour utiliser un emplacement chiffré hors du dépôt.

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
