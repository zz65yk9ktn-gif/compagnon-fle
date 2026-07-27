"""Contenu pilote. Ce format pourra être réutilisé pour les futures séquences."""

SEQUENCE_1 = {
    "slug": "sequence-1",
    "title": "Séquence 1 — Me présenter dans ma formation",
    "level": "A1",
    "exercises": (
        {
            "id": "presentation",
            "title": "Choisir une présentation adaptée",
            "instruction": "Choisis la phrase adaptée pour te présenter à un formateur.",
            "support": (
                "A. Salut, moi c’est Sam. — "
                "B. Bonjour, je m’appelle Samir et je suis en première année de CAP. — "
                "C. Hé, je suis là."
            ),
            "expected_answer": "B",
            "accepted_answers": ("b",),
            "correction": (
                "La réponse B convient : elle donne le prénom et la formation dans un registre poli."
            ),
        },
        {
            "id": "verbe",
            "title": "Compléter une phrase",
            "instruction": "Complète avec le verbe qui manque.",
            "support": "Bonjour, je ___ Momo et je prépare un CAP.",
            "expected_answer": "m’appelle",
            "accepted_answers": ("m'appelle", "m’appelle"),
            "correction": "On dit : « Je m’appelle Momo. » Le verbe est s’appeler.",
        },
        {
            "id": "information",
            "title": "Comprendre une présentation",
            "instruction": "Indique la formation préparée par Lina.",
            "support": (
                "Lina dit : « Je suis en première année. Je prépare un CAP équipier polyvalent "
                "du commerce et je commence mon stage lundi. »"
            ),
            "expected_answer": "un CAP équipier polyvalent du commerce",
            "accepted_answers": (
                "cap équipier polyvalent du commerce",
                "un cap équipier polyvalent du commerce",
                "cap epc",
            ),
            "correction": (
                "La formation est le CAP équipier polyvalent du commerce. « Première année » "
                "indique l’année et « lundi » indique le début du stage."
            ),
        },
    ),
    "adaptive_exercises": {
        "accessible": {
            "label": "Plus accessible — A1−",
            "title": "Présentation guidée",
            "instruction": "Complète la présentation avec les mots proposés.",
            "support": "Mots : appelle · CAP · première. Bonjour, je m’___ Momo. Je suis en ___ année de ___.",
            "expected_answer": "appelle · première · CAP",
            "correction": "Bonjour, je m’appelle Momo. Je suis en première année de CAP.",
        },
        "equivalent": {
            "label": "Difficulté équivalente — A1",
            "title": "Présentation courte",
            "instruction": "Écris deux phrases pour donner ton prénom et ta formation.",
            "support": "Aide possible : Je m’appelle… / Je prépare…",
            "expected_answer": "Deux phrases comprenant le prénom et la formation.",
            "correction": "Exemple : Je m’appelle Momo. Je prépare un CAP.",
        },
        "demanding": {
            "label": "Plus exigeant — A1+",
            "title": "Présentation enrichie",
            "instruction": "Présente-toi en trois phrases et ajoute une information sur ton stage ou ton projet.",
            "support": "Utilise au moins un connecteur : et, mais ou parce que.",
            "expected_answer": "Trois phrases, une information complémentaire et un connecteur.",
            "correction": "Exemple : Je m’appelle Momo et je prépare un CAP. Je commence mon stage lundi. Je suis motivé parce que je veux découvrir le métier.",
        },
    },
}
