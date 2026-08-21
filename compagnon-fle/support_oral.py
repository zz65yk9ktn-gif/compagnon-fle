"""Bloc 08 — Oral, banque officielle."""

from exercise_engine import LEVELS

RAW = [
  {
    "code": "O1-01",
    "notion": "SE PRÉSENTER",
    "question": "Pour commencer une présentation orale, quelle formule convient ?",
    "choices": {
      "A": "Bonjour, je m’appelle Samir.",
      "B": "Voilà.",
      "C": "C’est moi.",
      "D": "Après."
    },
    "correct": "A"
  },
  {
    "code": "O1-02",
    "notion": "SE PRÉSENTER",
    "question": "Quelle information est utile pour se présenter ?",
    "choices": {
      "A": "son prénom",
      "B": "le prix d’un objet sans rapport",
      "C": "la météo d’un autre pays",
      "D": "une phrase sans sujet"
    },
    "correct": "A"
  },
  {
    "code": "O1-03",
    "notion": "SE PRÉSENTER",
    "question": "Quelle présentation est la plus claire ?",
    "choices": {
      "A": "Moi CAP voiture.",
      "B": "Je m’appelle Inès et je prépare un CAP mécanique.",
      "C": "CAP moi oui.",
      "D": "Mécanique après voilà."
    },
    "correct": "B"
  },
  {
    "code": "O1-04",
    "notion": "SE PRÉSENTER",
    "question": "Pour parler de sa formation, on peut dire :",
    "choices": {
      "A": "Je prépare un CAP cuisine.",
      "B": "CAP cuisine moi faire.",
      "C": "Formation truc.",
      "D": "Moi école là."
    },
    "correct": "A"
  },
  {
    "code": "O1-05",
    "notion": "SE PRÉSENTER",
    "question": "Quelle information peut compléter une présentation ?",
    "choices": {
      "A": "son projet professionnel",
      "B": "une liste de mots au hasard",
      "C": "uniquement son âge sans contexte",
      "D": "un autre sujet sans lien"
    },
    "correct": "A"
  },
  {
    "code": "O1-06",
    "notion": "SE PRÉSENTER",
    "question": "À l’oral, il est préférable de :",
    "choices": {
      "A": "parler assez fort et distinctement",
      "B": "tourner le dos à l’auditoire",
      "C": "parler le plus vite possible",
      "D": "ne jamais regarder l’interlocuteur"
    },
    "correct": "A"
  },
  {
    "code": "O1-07",
    "notion": "SE PRÉSENTER",
    "question": "Quelle phrase présente un projet ?",
    "choices": {
      "A": "Plus tard, je voudrais travailler dans l’automobile.",
      "B": "Hier, il pleuvait.",
      "C": "La table est bleue.",
      "D": "J’ai oublié mon stylo."
    },
    "correct": "A"
  },
  {
    "code": "O1-08",
    "notion": "SE PRÉSENTER",
    "question": "Une présentation réussie doit surtout être :",
    "choices": {
      "A": "compréhensible et organisée",
      "B": "très longue obligatoirement",
      "C": "récitée sans comprendre",
      "D": "composée uniquement de mots isolés"
    },
    "correct": "A"
  },
  {
    "code": "O2-01",
    "notion": "RACONTER À L’ORAL",
    "question": "Quel ordre est logique pour raconter une expérience ?",
    "choices": {
      "A": "début → actions → résultat",
      "B": "résultat → début → autre sujet",
      "C": "conclusion → début → milieu",
      "D": "hasard → hasard → hasard"
    },
    "correct": "A"
  },
  {
    "code": "O2-02",
    "notion": "RACONTER À L’ORAL",
    "question": "Quel mot permet de commencer un récit chronologique ?",
    "choices": {
      "A": "D’abord",
      "B": "Pourtant",
      "C": "Donc que",
      "D": "Malgré"
    },
    "correct": "A"
  },
  {
    "code": "O2-03",
    "notion": "RACONTER À L’ORAL",
    "question": "Quel mot permet de poursuivre le récit ?",
    "choices": {
      "A": "Ensuite",
      "B": "Hier que",
      "C": "Parce",
      "D": "Malgré de"
    },
    "correct": "A"
  },
  {
    "code": "O2-04",
    "notion": "RACONTER À L’ORAL",
    "question": "Quel mot permet de terminer le récit ?",
    "choices": {
      "A": "Enfin",
      "B": "D’abord",
      "C": "Pourtant",
      "D": "Puisque mais"
    },
    "correct": "A"
  },
  {
    "code": "O2-05",
    "notion": "RACONTER À L’ORAL",
    "question": "Quelle phrase situe clairement une expérience ?",
    "choices": {
      "A": "Mardi matin, j’étais en stage dans un garage.",
      "B": "C’était là.",
      "C": "Un jour quelque part.",
      "D": "Voilà le truc."
    },
    "correct": "A"
  },
  {
    "code": "O2-06",
    "notion": "RACONTER À L’ORAL",
    "question": "Pour raconter une action passée terminée, quelle phrase convient ?",
    "choices": {
      "A": "J’ai remplacé la batterie.",
      "B": "Je remplacerai la batterie hier.",
      "C": "Je remplace demain la batterie.",
      "D": "Batterie remplacer moi."
    },
    "correct": "A"
  },
  {
    "code": "O2-07",
    "notion": "RACONTER À L’ORAL",
    "question": "Quel récit est le plus compréhensible ?",
    "choices": {
      "A": "D’abord j’ai préparé mes outils, ensuite j’ai contrôlé le véhicule, enfin j’ai rangé mon poste.",
      "B": "Enfin outils hier contrôle d’abord.",
      "C": "Véhicule puis rien garage demain.",
      "D": "Outils outils contrôle."
    },
    "correct": "A"
  },
  {
    "code": "O2-08",
    "notion": "RACONTER À L’ORAL",
    "question": "À l’oral, pour aider l’auditeur à suivre un récit, il faut :",
    "choices": {
      "A": "utiliser des repères chronologiques",
      "B": "changer de sujet sans prévenir",
      "C": "supprimer les verbes",
      "D": "parler sans pause ni organisation"
    },
    "correct": "A"
  },
  {
    "code": "O3-01",
    "notion": "EXPLIQUER UNE ACTIVITÉ",
    "question": "Pour expliquer une activité professionnelle, il faut d’abord :",
    "choices": {
      "A": "préciser ce qu’on doit faire",
      "B": "donner son avis sur un autre sujet",
      "C": "commencer par la conclusion",
      "D": "supprimer les étapes"
    },
    "correct": "A"
  },
  {
    "code": "O3-02",
    "notion": "EXPLIQUER UNE ACTIVITÉ",
    "question": "Quelle phrase explique une première étape ?",
    "choices": {
      "A": "D’abord, je prépare le matériel.",
      "B": "J’aime bien cet atelier.",
      "C": "Peut-être demain.",
      "D": "C’est compliqué."
    },
    "correct": "A"
  },
  {
    "code": "O3-03",
    "notion": "EXPLIQUER UNE ACTIVITÉ",
    "question": "Quelle phrase explique clairement une action ?",
    "choices": {
      "A": "Je desserre les écrous avec la clé adaptée.",
      "B": "Je fais le truc avec ça.",
      "C": "Voilà je fais.",
      "D": "Truc outil après."
    },
    "correct": "A"
  },
  {
    "code": "O3-04",
    "notion": "EXPLIQUER UNE ACTIVITÉ",
    "question": "Pour expliquer correctement une activité, il est utile de préciser :",
    "choices": {
      "A": "les outils et les étapes",
      "B": "uniquement son humeur",
      "C": "des informations sans rapport",
      "D": "seulement le résultat final"
    },
    "correct": "A"
  },
  {
    "code": "O3-05",
    "notion": "EXPLIQUER UNE ACTIVITÉ",
    "question": "Quelle formulation explique une consigne de sécurité ?",
    "choices": {
      "A": "Avant de commencer, je mets mes équipements de protection.",
      "B": "Je fais vite sans regarder.",
      "C": "La sécurité, on verra après.",
      "D": "Je commence puis je cherche les protections."
    },
    "correct": "A"
  },
  {
    "code": "O3-06",
    "notion": "EXPLIQUER UNE ACTIVITÉ",
    "question": "Quelle phrase exprime une conséquence ?",
    "choices": {
      "A": "Je serre correctement la pièce afin qu’elle ne bouge pas.",
      "B": "Je serre la pièce parce que demain.",
      "C": "Pièce donc outil.",
      "D": "Je serre mais bleu."
    },
    "correct": "A"
  },
  {
    "code": "O3-07",
    "notion": "EXPLIQUER UNE ACTIVITÉ",
    "question": "Pour vérifier que l’explication est comprise, on peut :",
    "choices": {
      "A": "demander si l’interlocuteur a des questions",
      "B": "partir immédiatement",
      "C": "changer de sujet",
      "D": "parler encore plus vite"
    },
    "correct": "A"
  },
  {
    "code": "O3-08",
    "notion": "EXPLIQUER UNE ACTIVITÉ",
    "question": "Une bonne explication orale est :",
    "choices": {
      "A": "précise, ordonnée et adaptée à l’interlocuteur",
      "B": "volontairement vague",
      "C": "uniquement composée de termes techniques",
      "D": "sans ordre logique"
    },
    "correct": "A"
  },
  {
    "code": "O4-01",
    "notion": "DONNER UN AVIS À L’ORAL",
    "question": "Quelle formule permet de donner son avis ?",
    "choices": {
      "A": "À mon avis,",
      "B": "Hier,",
      "C": "Ensuite,",
      "D": "Parce que donc"
    },
    "correct": "A"
  },
  {
    "code": "O4-02",
    "notion": "DONNER UN AVIS À L’ORAL",
    "question": "Quelle phrase exprime une opinion ?",
    "choices": {
      "A": "Je pense que cette solution est plus efficace.",
      "B": "La porte mesure deux mètres.",
      "C": "Le cours commence à 8 heures.",
      "D": "Le véhicule est rouge."
    },
    "correct": "A"
  },
  {
    "code": "O4-03",
    "notion": "DONNER UN AVIS À L’ORAL",
    "question": "Pour justifier son avis, on peut utiliser :",
    "choices": {
      "A": "parce que",
      "B": "demain",
      "C": "dessous",
      "D": "ensuite uniquement"
    },
    "correct": "A"
  },
  {
    "code": "O4-04",
    "notion": "DONNER UN AVIS À L’ORAL",
    "question": "Quelle réponse est la mieux argumentée ?",
    "choices": {
      "A": "Je préfère cette méthode parce qu’elle est plus rapide et plus sûre.",
      "B": "Je préfère, voilà.",
      "C": "C’est mieux.",
      "D": "Moi oui."
    },
    "correct": "A"
  },
  {
    "code": "O4-05",
    "notion": "DONNER UN AVIS À L’ORAL",
    "question": "Dans un échange oral, on peut être en désaccord en disant :",
    "choices": {
      "A": "Je comprends ton point de vue, mais je ne suis pas d’accord.",
      "B": "N’importe quoi.",
      "C": "Tais-toi.",
      "D": "C’est faux parce que moi."
    },
    "correct": "A"
  },
  {
    "code": "O4-06",
    "notion": "DONNER UN AVIS À L’ORAL",
    "question": "Quel connecteur permet d’opposer deux idées ?",
    "choices": {
      "A": "mais",
      "B": "ensuite",
      "C": "parce que uniquement",
      "D": "hier"
    },
    "correct": "A"
  },
  {
    "code": "O4-07",
    "notion": "DONNER UN AVIS À L’ORAL",
    "question": "Pour rendre un avis convaincant, il faut :",
    "choices": {
      "A": "donner au moins une raison claire",
      "B": "répéter la même phrase",
      "C": "parler plus fort que les autres",
      "D": "éviter toute justification"
    },
    "correct": "A"
  },
  {
    "code": "O4-08",
    "notion": "DONNER UN AVIS À L’ORAL",
    "question": "Quelle attitude convient dans un échange ?",
    "choices": {
      "A": "écouter l’autre avant de répondre",
      "B": "couper systématiquement la parole",
      "C": "ignorer la question",
      "D": "changer de sujet dès qu’on n’est pas d’accord"
    },
    "correct": "A"
  },
  {
    "code": "O5-01",
    "notion": "PRÉSENTER UN PROJET",
    "question": "Pour présenter un projet, quelle information faut-il donner ?",
    "choices": {
      "A": "l’objectif du projet",
      "B": "uniquement son prénom",
      "C": "une anecdote sans rapport",
      "D": "seulement la date du jour"
    },
    "correct": "A"
  },
  {
    "code": "O5-02",
    "notion": "PRÉSENTER UN PROJET",
    "question": "Quelle phrase annonce clairement un projet ?",
    "choices": {
      "A": "Mon projet est de devenir carrossier après mon CAP.",
      "B": "Voilà après je sais pas.",
      "C": "Peut-être métier.",
      "D": "Mon projet hier était demain."
    },
    "correct": "A"
  },
  {
    "code": "O5-03",
    "notion": "PRÉSENTER UN PROJET",
    "question": "Pour présenter les étapes d’un projet, on peut utiliser :",
    "choices": {
      "A": "d’abord, ensuite, enfin",
      "B": "pourtant, bleu, demain",
      "C": "parce, sous, hier",
      "D": "malgré, table, vite"
    },
    "correct": "A"
  },
  {
    "code": "O5-04",
    "notion": "PRÉSENTER UN PROJET",
    "question": "Quelle information permet d’expliquer pourquoi le projet est important ?",
    "choices": {
      "A": "sa motivation",
      "B": "la couleur de la salle",
      "C": "le prénom du voisin",
      "D": "la météo"
    },
    "correct": "A"
  },
  {
    "code": "O5-05",
    "notion": "PRÉSENTER UN PROJET",
    "question": "Quelle phrase exprime un objectif futur ?",
    "choices": {
      "A": "Après mon CAP, je chercherai un emploi dans ce secteur.",
      "B": "Hier, j’ai pris le bus.",
      "C": "Je range mes outils maintenant.",
      "D": "Avant, j’étais au collège."
    },
    "correct": "A"
  },
  {
    "code": "O5-06",
    "notion": "PRÉSENTER UN PROJET",
    "question": "Pour présenter un projet de façon crédible, il est utile de :",
    "choices": {
      "A": "préciser les étapes prévues",
      "B": "rester volontairement vague",
      "C": "inventer des résultats déjà obtenus",
      "D": "éviter de parler de l’objectif"
    },
    "correct": "A"
  },
  {
    "code": "O5-07",
    "notion": "PRÉSENTER UN PROJET",
    "question": "Quelle conclusion convient à une présentation de projet ?",
    "choices": {
      "A": "Voilà les principales étapes de mon projet et ce que je souhaite atteindre.",
      "B": "Bref voilà.",
      "C": "J’ai fini parce que oui.",
      "D": "Autre chose maintenant."
    },
    "correct": "A"
  },
  {
    "code": "O5-08",
    "notion": "PRÉSENTER UN PROJET",
    "question": "Une présentation de projet réussie doit être :",
    "choices": {
      "A": "organisée, claire et suffisamment précise",
      "B": "uniquement très longue",
      "C": "sans objectif annoncé",
      "D": "composée de réponses isolées"
    },
    "correct": "A"
  }
]

def make_question(row):
    return {
        "id": f"SUP-{row['code']}", "type": "single_choice",
        "instruction": row["question"], "support": "", "choices": row["choices"],
        "correct_answer": row["correct"], "feedback_success": "Bravo, c’est juste.",
        "feedback_error": "Regarde la correction avant de continuer.",
        "competency": row["notion"], "difficulty": 1,
        "help": "Repère la situation, l’interlocuteur et l’information importante.",
        "source_group": "soutien_oral_v15",
    }

SUPPORT_ORAL_QUESTIONS = tuple(make_question(row) for row in RAW)
SUPPORT_ORAL = {
    "slug": "sequence-soutien-oral",
    "title": "Soutien — Oral",
    "track": "support",
    "levels": {level: SUPPORT_ORAL_QUESTIONS for level in LEVELS},
}

