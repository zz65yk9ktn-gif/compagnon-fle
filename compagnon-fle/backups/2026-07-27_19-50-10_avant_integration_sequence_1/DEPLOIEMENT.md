# Préparation de la mise en ligne — Compagnon FLE

Ce document prépare un pilote sur Render. Il ne déclenche aucune publication ni dépense.

## Solution proposée

- Un service web Render **Starter**, dans la région de Francfort.
- Une seule instance, car SQLite et le disque persistant ne permettent pas la montée en charge horizontale.
- Un disque persistant de 1 Go monté sur `/var/data`.
- SQLite conservé pour le pilote. Une migration vers PostgreSQL sera à prévoir avant un usage à grande échelle.
- Déploiements automatiques désactivés : chaque nouvelle version devra être lancée manuellement.

## Budget prévisible au 26 juillet 2026

- Espace Render Hobby : 0 $US par mois.
- Service web Starter : environ 7 $US par mois.
- Disque persistant : 0,25 $US par Go et par mois, soit environ 0,25 $US pour 1 Go.
- Total minimal estimé : environ **7,25 $US par mois**, hors dépassement de bande passante, taxes et évolution tarifaire.

Vérifier le montant affiché par Render avant toute validation. Le palier gratuit ne doit pas être utilisé avec cette base SQLite : il ne permet pas d’attacher un disque persistant.

## Étapes sans publication immédiate

1. Changer le mot de passe administrateur actuellement utilisé avec `python3 change_password.py`.
2. Supprimer les faux comptes et données de test avant de copier la base destinée au pilote.
3. Déterminer qui est responsable du traitement, pourquoi la date de naissance est nécessaire et combien de temps les comptes seront conservés.
4. Créer un dépôt Git **privé** et vérifier que le dossier `data/` et les sauvegardes SQLite sont ignorés.
5. Copier uniquement le code dans le dépôt. Ne jamais y déposer la base réelle, des mots de passe ou une sauvegarde.
6. Créer un compte Render et activer l’authentification multifacteur. Cette étape reste gratuite.
7. Depuis Render, sélectionner le dépôt privé et examiner le fichier `render.yaml`.
8. Vérifier avant validation : région `Frankfurt`, plan `Starter`, disque 1 Go, montage `/var/data`, une seule instance et déploiements automatiques désactivés.
9. S’arrêter à l’écran récapitulatif du prix et demander une validation explicite avant de créer le service.
10. Après accord seulement, créer le service, transférer une base nettoyée sur le disque et tester les accès avec des comptes pilotes non réels.
11. Avant d’accueillir de vraies données, rédiger l’information destinée aux apprenants, fixer la durée de conservation et organiser les demandes de suppression ou de rectification.

## Mesures déjà préparées

- Mots de passe hachés avec PBKDF2-SHA256, sel aléatoire et comparaison résistante aux attaques temporelles.
- Nouveaux mots de passe apprenants : 12 caractères minimum, lettres et chiffres.
- Limitation des échecs de connexion et des inscriptions répétées.
- Sessions limitées à huit heures, cookies `HttpOnly`, `SameSite=Strict` et `Secure` en production.
- Protection CSRF des actions administratives et des réponses aux exercices.
- En-têtes contre l’intégration dans une page tierce, la détection de type et l’accès aux capteurs.
- HTTPS fourni par Render et données du disque chiffrées au repos avec snapshots quotidiens.
- Chemin de santé `/health` et déploiements automatiques désactivés.

## Points obligatoires avant un vrai pilote

- Changer le mot de passe administrateur divulgué pendant la mise au point.
- Utiliser un mot de passe distinct et activer le MFA sur Render et sur le fournisseur Git.
- Ne collecter que les données nécessaires. Réexaminer notamment le besoin de conserver la date de naissance complète.
- Définir une durée de conservation et une procédure de suppression.
- Vérifier le contrat de sous-traitance, la région d’hébergement et les engagements de Render avec la personne responsable de la conformité.
- Tester une restauration de sauvegarde, pas seulement la présence d’un snapshot.
- Limiter le pilote à un petit nombre d’utilisateurs : le serveur et SQLite restent une architecture de prototype à instance unique.

## Sauvegarde locale avant déploiement

Arrêter l’application, puis copier le fichier `data/compagnon_fle.sqlite3` vers un emplacement chiffré et daté. Ne jamais envoyer cette sauvegarde par courrier électronique ni la placer dans Git.
