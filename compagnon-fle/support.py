"""Lot pilote de soutien commun à tous les élèves."""

from exercise_engine import LEVELS

RAW = (
    ("M1-01", "Verbes de consigne", "Que demande « Entoure le verbe » ?", "Écrire une phrase", "Mettre un cercle autour du verbe", "Barrer le verbe", "Copier le texte", "B"),
    ("M1-02", "Verbes de consigne", "Que signifie « souligne » ?", "Tracer un trait sous le mot", "Effacer le mot", "Recopier le mot trois fois", "Mettre le mot entre parenthèses", "A"),
    ("M1-03", "Verbes de consigne", "« Relie chaque mot à sa définition » signifie :", "Copier les définitions", "Tracer des liens entre les éléments correspondants", "Souligner tous les mots", "Classer par ordre alphabétique", "B"),
    ("M1-04", "Verbes de consigne", "« Cite deux exemples » demande de :", "Donner deux exemples", "Donner une définition", "Faire un dessin", "Expliquer toute la leçon", "A"),
    ("M1-05", "Verbes de consigne", "« Justifie ta réponse » signifie :", "Répondre oui ou non", "Expliquer pourquoi la réponse est correcte", "Copier la question", "Donner un autre sujet", "B"),
    ("M1-06", "Verbes de consigne", "« Compare les deux textes » demande surtout de :", "Dire les points communs et les différences", "Choisir le plus long", "Compter les phrases", "Réécrire les textes", "A"),
    ("M1-07", "Verbes de consigne", "« Classe ces mots dans le tableau » signifie :", "Les recopier au hasard", "Les ranger dans les bonnes catégories", "Les mettre au pluriel", "Les traduire", "B"),
    ("M1-08", "Verbes de consigne", "« Reformule cette phrase » signifie :", "La recopier exactement", "Dire la même idée avec d’autres mots", "La mettre au futur", "Supprimer les verbes", "B"),
    ("M2-01", "Consigne complexe", "« Lis le texte puis souligne deux informations. » Que faire en premier ?", "Souligner", "Lire le texte", "Écrire un résumé", "Répondre au professeur", "B"),
    ("M2-02", "Consigne complexe", "« Observe le document et réponds aux questions 1 à 3. » Combien d’actions principales ?", "Une", "Deux", "Trois", "Quatre", "B"),
    ("M2-03", "Consigne complexe", "Tu dois relever trois mots qui expriment la peur. Que relèves-tu ?", "Trois phrases", "Trois mots liés à la peur", "Trois personnages", "Trois dates", "B"),
    ("M2-04", "Consigne complexe", "Après avoir choisi une réponse, comment la justifier avec le texte ?", "Effacer la question", "Donner une preuve tirée du texte", "Changer de réponse", "Copier tout le texte", "B"),
    ("M2-05", "Consigne complexe", "Classe les phrases puis donne un titre à chaque catégorie. Quelle est la dernière action ?", "Lire", "Classer", "Donner un titre", "Compter les mots", "C"),
    ("M2-06", "Consigne complexe", "Explique en deux phrases pourquoi le personnage refuse. La réponse doit :", "Faire deux phrases et utiliser le document", "Faire un mot", "Être copiée dans le titre", "Être sans lien avec le document", "A"),
    ("M2-07", "Consigne complexe", "Dans une consigne longue, la meilleure méthode est de :", "Répondre avant de lire", "Repérer les verbes d’action et les étapes", "Lire le dernier mot", "Tout recopier", "B"),
    ("M2-08", "Consigne complexe", "Surligne les causes en jaune et les conséquences en bleu. Que distinguer ?", "Titres et paragraphes", "Causes et conséquences", "Noms et verbes", "Mots longs et courts", "B"),
    ("M3-01", "Identifier un document", "Une image prise avec un appareil est :", "Une photographie", "Un article", "Une lettre", "Un tableau", "A"),
    ("M3-02", "Identifier un document", "Où trouve-t-on la source d’un document ?", "Dans les informations sur son origine", "Dans la réponse de l’élève", "Dans le dictionnaire", "Dans le numéro de page seulement", "A"),
    ("M3-03", "Identifier un document", "Le sujet d’un document correspond :", "À ce dont il parle principalement", "À sa couleur", "Au nombre de lignes", "À la taille des lettres", "A"),
    ("M3-04", "Identifier un document", "Titre, date, journaliste et paragraphes : ce document est probablement :", "Une carte", "Un article", "Une photographie", "Un graphique", "B"),
    ("M3-05", "Identifier un document", "Une carte géographique sert principalement à :", "Localiser des espaces", "Conjuguer", "Donner une opinion", "Raconter une fiction", "A"),
    ("M3-06", "Identifier un document", "Une affiche cherche souvent à :", "Informer, convaincre ou annoncer", "Mesurer", "Résoudre une équation", "Remplacer un dictionnaire", "A"),
    ("M3-07", "Identifier un document", "Pour identifier un document, il faut chercher :", "Sa nature, sa source et son sujet", "Sa couleur seulement", "Sa longueur seulement", "Son premier mot seulement", "A"),
    ("M3-08", "Identifier un document", "« Source : INSEE, 2025 » indique :", "L’organisme d’origine et la date", "Le niveau scolaire", "Le nombre de réponses", "Le titre du chapitre", "A"),
    ("M4-01", "Tableau ou graphique", "Dans un tableau, une ligne se lit :", "Horizontalement", "Verticalement", "En diagonale", "De bas en haut seulement", "A"),
    ("M4-02", "Tableau ou graphique", "Dans un tableau, une colonne se lit :", "Horizontalement", "Verticalement", "En cercle", "Au hasard", "B"),
    ("M4-03", "Tableau ou graphique", "Avant de lire un graphique, il faut regarder :", "Son titre et ses axes", "La couleur du fond", "La longueur du titre", "Le nom du professeur", "A"),
    ("M4-04", "Tableau ou graphique", "L’axe vertical d’un graphique peut indiquer :", "Une quantité ou une valeur", "Une règle de grammaire", "Un personnage", "Une consigne", "A"),
    ("M4-05", "Tableau ou graphique", "Si une courbe monte, la valeur :", "Augmente", "Diminue", "Disparaît", "Reste à zéro", "A"),
    ("M4-06", "Tableau ou graphique", "Deux barres de même hauteur ont des valeurs :", "Égales", "Opposées", "Inconnues", "Fausses", "A"),
    ("M4-07", "Tableau ou graphique", "Pour trouver la valeur de 2024 dans un tableau, il faut :", "Repérer 2024 et croiser avec la bonne catégorie", "Lire le titre", "Tout additionner", "Choisir la plus grande valeur", "A"),
    ("M4-08", "Tableau ou graphique", "La légende d’un graphique sert à :", "Expliquer les couleurs ou symboles", "Donner la correction", "Remplacer le titre", "Compter les lignes", "A"),
    ("M5-01", "Croiser des documents", "Croiser deux documents signifie :", "Utiliser les informations des deux", "Les imprimer ensemble", "Choisir le plus court", "Ignorer le second", "A"),
    ("M5-02", "Croiser des documents", "Deux documents donnent la même information. Ils :", "Se confirment", "Se contredisent", "N’ont aucun rapport", "Sont faux", "A"),
    ("M5-03", "Croiser des documents", "Un texte indique une hausse, mais le graphique une baisse. Ils :", "Se contredisent", "Se complètent", "Disent la même chose", "Ne sont pas comparables", "A"),
    ("M5-04", "Croiser des documents", "Un texte explique un phénomène et un graphique montre son évolution. Ils :", "Se complètent", "Sont identiques", "S’annulent", "Ne servent à rien ensemble", "A"),
    ("M5-05", "Croiser des documents", "Pour répondre avec deux documents, il faut d’abord :", "Trouver les informations utiles dans chacun", "Choisir au hasard", "Tout copier", "Lire seulement les titres", "A"),
    ("M5-06", "Croiser des documents", "Quelle phrase croise correctement deux documents ?", "Le document 1 indique une hausse, confirmée par le graphique du document 2.", "J’aime le document 1.", "Le document 2 est plus joli.", "Je n’ai pas lu le document 1.", "A"),
    ("M5-07", "Croiser des documents", "Deux documents sur le même sujet peuvent :", "Donner des informations différentes mais complémentaires", "Être toujours identiques", "Ne jamais être utilisés ensemble", "Avoir le même auteur", "A"),
    ("M5-08", "Croiser des documents", "Si deux documents diffèrent, il faut :", "Vérifier ce que chacun dit avant de conclure", "Supprimer celui qu’on aime moins", "Inventer une information", "Répondre sans lire", "A"),
)


def make_question(row):
    code, notion, text, a, b, c, d, correct = row
    return {"id": f"SUP-{code}", "type": "single_choice", "instruction": text,
            "support": "", "choices": {"A": a, "B": b, "C": c, "D": d},
            "correct_answer": correct, "feedback_success": "Bravo, c’est juste.",
            "feedback_error": "Regarde la correction avant de continuer.",
            "competency": notion, "difficulty": 1,
            "help": "Relis la question et repère le mot important.",
            "source_group": "soutien_methodologie_v15"}


SUPPORT_QUESTIONS = tuple(make_question(row) for row in RAW)
SUPPORT_METHODOLOGY = {"slug": "sequence-soutien-methodologie",
                       "title": "Soutien — Méthodologie", "track": "support",
                       "levels": {level: SUPPORT_QUESTIONS for level in LEVELS}}
