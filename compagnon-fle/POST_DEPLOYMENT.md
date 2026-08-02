# Validation après déploiement — Compagnon FLE

## 1. Déployer

Envoyer au dépôt GitHub uniquement les fichiers énumérés dans `DEPLOYMENT_MANIFEST.txt`, puis déclencher un déploiement manuel dans Render.

Le journal de build doit se terminer par :

```text
DEPLOYMENT_CHECK_OK
```

## 2. Vérifier la version distante

Depuis un terminal :

```sh
python3 remote_smoke_check.py https://ADRESSE-PUBLIQUE-RENDER
```

Le résultat attendu est :

```text
REMOTE_SMOKE_CHECK_OK
```

## 3. Vérification manuelle minimale

1. Ouvrir la page d’accueil depuis un téléphone.
2. Créer un compte apprenant de test.
3. Se connecter comme administrateur ou enseignant.
4. Attribuer un niveau au compte de test.
5. Se connecter comme apprenant.
6. Ouvrir une séquence et répondre à plusieurs questions.
7. Vérifier que les choix A/B/C/D sont grands, mélangés et utilisables d’un clic.
8. Vérifier le résultat et le suivi enseignant.
9. Redémarrer le service Render et confirmer que les comptes et résultats sont toujours présents.

## 4. Critères de validation

La version distante est validée seulement si :

- `/health` répond avec un statut 200 ;
- le build affiche `DEPLOYMENT_CHECK_OK` ;
- le script distant affiche `REMOTE_SMOKE_CHECK_OK` ;
- les trois rôles restent séparés ;
- une réponse peut être enregistrée et retrouvée dans le suivi ;
- les données persistent après redémarrage ;
- aucune base SQLite locale n’est versionnée dans GitHub.
