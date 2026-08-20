# Réinitialisation du mot de passe administrateur

## Périmètre de la modification

- Une sauvegarde SQLite cohérente est créée avant toute écriture.
- Une seule ligne de `users` peut être modifiée : le compte actif dont le rôle est `admin` et dont l’identifiant correspond à `ADMIN_LOGIN`.
- Seuls `password_hash` et `updated_at` de ce compte changent.
- Les comptes apprenants, profils, niveaux, tentatives et résultats ne sont ni supprimés ni modifiés.
- Le mot de passe est haché avec PBKDF2-SHA256, un sel aléatoire et 310 000 itérations.

## Procédure contrôlée

1. Ouvrir une console sur l’instance qui monte `/var/data`.
2. Choisir un dossier de sauvegarde chiffré et non versionné.
3. Exécuter `ADMIN_LOGIN='identifiant-admin' ADMIN_BACKUP_DIR='/chemin/sur' python3 change_password.py`.
4. Saisir deux fois un mot de passe inédit d’au moins 14 caractères contenant lettres et chiffres.
5. Conserver le chemin de sauvegarde affiché et vérifier la connexion administrateur.
6. Vérifier séparément la connexion d’un compte apprenant témoin et son historique.

Le script refuse un compte inexistant, inactif ou non administrateur. Après la mise à jour, il vérifie l’authentification et `PRAGMA integrity_check`. En cas d’échec, ne pas redémarrer ni déployer : restaurer la sauvegarde affichée.

## Validation locale

`python3 admin_password_reset_check.py` prouve sur une base temporaire que l’ancien mot de passe est invalidé, que le nouveau fonctionne, et que le profil et le hash du mot de passe apprenant restent strictement identiques.

`python3 deployment_check.py` inclut désormais ce contrôle dans la suite complète.

## Production

Cette branche ne déclenche et n’autorise aucun déploiement. La réinitialisation de la base persistante doit être exécutée seulement après vérification humaine de la sauvegarde, de l’identifiant administrateur cible et du nouveau secret.
