"""Bloc 07 — Se corriger, banque officielle."""

from exercise_engine import LEVELS

RAW = [
  {
    "code": "SC1-01",
    "notion": "RELECTURE",
    "question": "Après avoir écrit un texte, quelle est la première action utile ?",
    "choices": {
      "A": "L’envoyer immédiatement",
      "B": "Le relire",
      "C": "Supprimer la dernière phrase",
      "D": "Changer de sujet"
    },
    "correct": "B"
  },
  {
    "code": "SC1-02",
    "notion": "RELECTURE",
    "question": "Relire permet surtout de :",
    "choices": {
      "A": "repérer et corriger des erreurs",
      "B": "rendre le texte plus long",
      "C": "remplacer tous les mots",
      "D": "éviter la ponctuation"
    },
    "correct": "A"
  },
  {
    "code": "SC1-03",
    "notion": "RELECTURE",
    "question": "Pour relire efficacement, il vaut mieux :",
    "choices": {
      "A": "vérifier un type d’erreur à la fois",
      "B": "lire le plus vite possible",
      "C": "regarder uniquement le titre",
      "D": "ne vérifier que la longueur"
    },
    "correct": "A"
  },
  {
    "code": "SC1-04",
    "notion": "RELECTURE",
    "question": "Quelle question est utile pendant la relecture ?",
    "choices": {
      "A": "Mon texte répond-il à la consigne ?",
      "B": "Ai-je utilisé exactement 100 mots ?",
      "C": "Ai-je changé de stylo ?",
      "D": "Mon voisin a-t-il fini ?"
    },
    "correct": "A"
  },
  {
    "code": "SC1-05",
    "notion": "RELECTURE",
    "question": "Pour repérer une phrase maladroite, on peut :",
    "choices": {
      "A": "la relire lentement",
      "B": "supprimer tous les verbes",
      "C": "ajouter des mots au hasard",
      "D": "ignorer la phrase"
    },
    "correct": "A"
  },
  {
    "code": "SC1-06",
    "notion": "RELECTURE",
    "question": "Une grille de relecture sert à :",
    "choices": {
      "A": "vérifier toujours les mêmes points importants",
      "B": "donner automatiquement la note",
      "C": "remplacer le texte",
      "D": "choisir le sujet"
    },
    "correct": "A"
  },
  {
    "code": "SC1-07",
    "notion": "RELECTURE",
    "question": "Quel élément doit être vérifié avant de rendre un travail ?",
    "choices": {
      "A": "La consigne et la réponse produite",
      "B": "La météo",
      "C": "Le nombre de pages du manuel",
      "D": "La marque du stylo"
    },
    "correct": "A"
  },
  {
    "code": "SC1-08",
    "notion": "RELECTURE",
    "question": "Après une première correction, il est utile de :",
    "choices": {
      "A": "relire une dernière fois",
      "B": "remettre volontairement les erreurs",
      "C": "supprimer la ponctuation",
      "D": "changer toutes les phrases"
    },
    "correct": "A"
  },
  {
    "code": "SC2-01",
    "notion": "PONCTUATION",
    "question": "Quel signe termine une phrase déclarative ?",
    "choices": {
      "A": ".",
      "B": ",",
      "C": ":",
      "D": ";"
    },
    "correct": "A"
  },
  {
    "code": "SC2-02",
    "notion": "PONCTUATION",
    "question": "Quel signe termine généralement une question ?",
    "choices": {
      "A": "!",
      "B": "?",
      "C": ",",
      "D": ":"
    },
    "correct": "B"
  },
  {
    "code": "SC2-03",
    "notion": "PONCTUATION",
    "question": "Quelle phrase est correctement ponctuée ?",
    "choices": {
      "A": "Bonjour comment allez-vous ?",
      "B": "Bonjour, comment allez-vous ?",
      "C": "Bonjour comment, allez-vous",
      "D": "Bonjour ? comment allez-vous,"
    },
    "correct": "B"
  },
  {
    "code": "SC2-04",
    "notion": "PONCTUATION",
    "question": "Une phrase commence généralement par :",
    "choices": {
      "A": "une majuscule",
      "B": "une virgule",
      "C": "un point",
      "D": "un chiffre"
    },
    "correct": "A"
  },
  {
    "code": "SC2-05",
    "notion": "PONCTUATION",
    "question": "Quelle phrase est correcte ?",
    "choices": {
      "A": "demain je travaille.",
      "B": "Demain je travaille",
      "C": "Demain, je travaille.",
      "D": "demain, Je travaille"
    },
    "correct": "C"
  },
  {
    "code": "SC2-06",
    "notion": "PONCTUATION",
    "question": "Dans une énumération, quel signe sépare souvent les éléments ?",
    "choices": {
      "A": "la virgule",
      "B": "le point d’interrogation",
      "C": "l’apostrophe uniquement",
      "D": "les parenthèses obligatoirement"
    },
    "correct": "A"
  },
  {
    "code": "SC2-07",
    "notion": "PONCTUATION",
    "question": "Quel signe peut annoncer une liste ?",
    "choices": {
      "A": ":",
      "B": "?",
      "C": "’",
      "D": "- uniquement"
    },
    "correct": "A"
  },
  {
    "code": "SC2-08",
    "notion": "PONCTUATION",
    "question": "Quelle correction faut-il apporter à « Je travaille demain matin » ?",
    "choices": {
      "A": "Ajouter un point final",
      "B": "Supprimer le verbe",
      "C": "Mettre une minuscule à Je",
      "D": "Ajouter un point d’interrogation"
    },
    "correct": "A"
  },
  {
    "code": "SC3-01",
    "notion": "SYNTAXE",
    "question": "Quelle phrase est correctement construite ?",
    "choices": {
      "A": "Le mécanicien contrôle le véhicule.",
      "B": "Contrôle véhicule le mécanicien.",
      "C": "Le véhicule mécanicien contrôle.",
      "D": "Mécanicien le véhicule."
    },
    "correct": "A"
  },
  {
    "code": "SC3-02",
    "notion": "SYNTAXE",
    "question": "Dans une phrase simple, quel ordre est fréquent ?",
    "choices": {
      "A": "sujet – verbe – complément",
      "B": "complément – complément – sujet",
      "C": "verbe – point – sujet",
      "D": "adjectif – virgule – déterminant"
    },
    "correct": "A"
  },
  {
    "code": "SC3-03",
    "notion": "SYNTAXE",
    "question": "Quelle phrase a un sens clair ?",
    "choices": {
      "A": "Je prépare mes outils avant de commencer.",
      "B": "Outils je avant préparer commencer.",
      "C": "Avant outils commence je.",
      "D": "Prépare avant mes commencer."
    },
    "correct": "A"
  },
  {
    "code": "SC3-04",
    "notion": "SYNTAXE",
    "question": "Quelle phrase contient un verbe conjugué ?",
    "choices": {
      "A": "Le véhicule démarre.",
      "B": "Le véhicule rouge.",
      "C": "Dans le garage.",
      "D": "Une grande voiture."
    },
    "correct": "A"
  },
  {
    "code": "SC3-05",
    "notion": "SYNTAXE",
    "question": "Quelle correction convient à « Moi travailler demain » ?",
    "choices": {
      "A": "Je travaille demain.",
      "B": "Moi demain travail.",
      "C": "Demain moi travailler.",
      "D": "Je demain travail."
    },
    "correct": "A"
  },
  {
    "code": "SC3-06",
    "notion": "SYNTAXE",
    "question": "Quelle phrase est complète ?",
    "choices": {
      "A": "Parce que le bus.",
      "B": "Dans l’atelier.",
      "C": "Je range les outils dans l’atelier.",
      "D": "Après le travail."
    },
    "correct": "C"
  },
  {
    "code": "SC3-07",
    "notion": "SYNTAXE",
    "question": "Une phrase mal ordonnée peut :",
    "choices": {
      "A": "rendre le message difficile à comprendre",
      "B": "améliorer automatiquement l’orthographe",
      "C": "remplacer la ponctuation",
      "D": "corriger les accords"
    },
    "correct": "A"
  },
  {
    "code": "SC3-08",
    "notion": "SYNTAXE",
    "question": "Quelle phrase faut-il corriger ?",
    "choices": {
      "A": "Nous terminons le travail.",
      "B": "Le professeur explique la consigne.",
      "C": "Les élèves le texte lisent.",
      "D": "Je prends mon cahier."
    },
    "correct": "C"
  },
  {
    "code": "SC4-01",
    "notion": "ACCORD SUJET-VERBE",
    "question": "Choisis la forme correcte : « Les élèves ___ le texte. »",
    "choices": {
      "A": "lit",
      "B": "lis",
      "C": "lisent",
      "D": "lisez"
    },
    "correct": "C"
  },
  {
    "code": "SC4-02",
    "notion": "ACCORD SUJET-VERBE",
    "question": "Choisis la forme correcte : « Le mécanicien ___ la voiture. »",
    "choices": {
      "A": "contrôlent",
      "B": "contrôle",
      "C": "contrôlez",
      "D": "contrôler"
    },
    "correct": "B"
  },
  {
    "code": "SC4-03",
    "notion": "ACCORD SUJET-VERBE",
    "question": "Dans « Nous préparons le matériel », le verbe s’accorde avec :",
    "choices": {
      "A": "nous",
      "B": "matériel",
      "C": "le",
      "D": "préparons"
    },
    "correct": "A"
  },
  {
    "code": "SC4-04",
    "notion": "ACCORD SUJET-VERBE",
    "question": "Quelle phrase est correcte ?",
    "choices": {
      "A": "Ils travaille demain.",
      "B": "Ils travaillent demain.",
      "C": "Ils travailles demain.",
      "D": "Ils travailler demain."
    },
    "correct": "B"
  },
  {
    "code": "SC4-05",
    "notion": "ACCORD SUJET-VERBE",
    "question": "Quelle phrase contient une erreur d’accord sujet-verbe ?",
    "choices": {
      "A": "Tu ranges les outils.",
      "B": "Vous commencez à huit heures.",
      "C": "Les apprentis prépare le véhicule.",
      "D": "Je termine mon exercice."
    },
    "correct": "C"
  },
  {
    "code": "SC4-06",
    "notion": "ACCORD SUJET-VERBE",
    "question": "Corrige : « La voiture et le camion arrive. »",
    "choices": {
      "A": "La voiture et le camion arrivent.",
      "B": "La voiture et le camion arrives.",
      "C": "La voiture et le camion arriver.",
      "D": "La voiture et le camion arrivons."
    },
    "correct": "A"
  },
  {
    "code": "SC4-07",
    "notion": "ACCORD SUJET-VERBE",
    "question": "Pour vérifier l’accord du verbe, il faut d’abord trouver :",
    "choices": {
      "A": "le sujet",
      "B": "la ponctuation",
      "C": "le dernier mot",
      "D": "l’adjectif"
    },
    "correct": "A"
  },
  {
    "code": "SC4-08",
    "notion": "ACCORD SUJET-VERBE",
    "question": "Quelle forme convient ? « Je ___ mon dossier. »",
    "choices": {
      "A": "terminent",
      "B": "terminez",
      "C": "termine",
      "D": "terminons"
    },
    "correct": "C"
  },
  {
    "code": "SC5-01",
    "notion": "ACCORDS ESSENTIELS",
    "question": "Quelle expression est correcte ?",
    "choices": {
      "A": "une voiture rouge",
      "B": "une voiture rouges",
      "C": "un voiture rouge",
      "D": "une voitures rouge"
    },
    "correct": "A"
  },
  {
    "code": "SC5-02",
    "notion": "ACCORDS ESSENTIELS",
    "question": "Quelle expression est correcte ?",
    "choices": {
      "A": "des outil propre",
      "B": "des outils propres",
      "C": "des outils propre",
      "D": "des outil propres"
    },
    "correct": "B"
  },
  {
    "code": "SC5-03",
    "notion": "ACCORDS ESSENTIELS",
    "question": "Dans « une grande machine », l’adjectif « grande » s’accorde avec :",
    "choices": {
      "A": "machine",
      "B": "une",
      "C": "avec",
      "D": "le verbe"
    },
    "correct": "A"
  },
  {
    "code": "SC5-04",
    "notion": "ACCORDS ESSENTIELS",
    "question": "Choisis la forme correcte : « un véhicule ___ »",
    "choices": {
      "A": "neuve",
      "B": "neufs",
      "C": "neuf",
      "D": "neuves"
    },
    "correct": "C"
  },
  {
    "code": "SC5-05",
    "notion": "ACCORDS ESSENTIELS",
    "question": "Choisis la forme correcte : « deux pièces ___ »",
    "choices": {
      "A": "cassé",
      "B": "cassée",
      "C": "cassées",
      "D": "cassés"
    },
    "correct": "C"
  },
  {
    "code": "SC5-06",
    "notion": "ACCORDS ESSENTIELS",
    "question": "Quelle phrase est correcte ?",
    "choices": {
      "A": "Les portes sont ouvert.",
      "B": "Les portes sont ouvertes.",
      "C": "Les porte sont ouvertes.",
      "D": "Les portes est ouvertes."
    },
    "correct": "B"
  },
  {
    "code": "SC5-07",
    "notion": "ACCORDS ESSENTIELS",
    "question": "Pour vérifier un accord dans le groupe nominal, on observe notamment :",
    "choices": {
      "A": "le genre et le nombre",
      "B": "uniquement le temps du verbe",
      "C": "la longueur du mot",
      "D": "la place du paragraphe"
    },
    "correct": "A"
  },
  {
    "code": "SC5-08",
    "notion": "ACCORDS ESSENTIELS",
    "question": "Quelle correction convient à « les nouvelle consignes » ?",
    "choices": {
      "A": "les nouvelles consignes",
      "B": "les nouveaux consignes",
      "C": "les nouvelle consigne",
      "D": "le nouvelles consignes"
    },
    "correct": "A"
  },
  {
    "code": "SC6-01",
    "notion": "CONJUGAISON",
    "question": "Quelle phrase est au présent ?",
    "choices": {
      "A": "Je travaille aujourd’hui.",
      "B": "J’ai travaillé hier.",
      "C": "Je travaillerai demain.",
      "D": "Je vais travailler demain."
    },
    "correct": "A"
  },
  {
    "code": "SC6-02",
    "notion": "CONJUGAISON",
    "question": "Quelle phrase est au passé composé ?",
    "choices": {
      "A": "Je contrôle la voiture.",
      "B": "J’ai contrôlé la voiture.",
      "C": "Je contrôlerai la voiture.",
      "D": "Je contrôlais souvent la voiture."
    },
    "correct": "B"
  },
  {
    "code": "SC6-03",
    "notion": "CONJUGAISON",
    "question": "Quelle phrase est au futur simple ?",
    "choices": {
      "A": "Nous terminons.",
      "B": "Nous avons terminé.",
      "C": "Nous terminerons.",
      "D": "Nous terminions."
    },
    "correct": "C"
  },
  {
    "code": "SC6-04",
    "notion": "CONJUGAISON",
    "question": "Quel temps convient pour une action terminée hier ?",
    "choices": {
      "A": "passé composé",
      "B": "futur simple",
      "C": "présent uniquement",
      "D": "futur proche"
    },
    "correct": "A"
  },
  {
    "code": "SC6-05",
    "notion": "CONJUGAISON",
    "question": "Corrige : « Hier, je range mes outils. » si l’action est terminée.",
    "choices": {
      "A": "Hier, j’ai rangé mes outils.",
      "B": "Hier, je rangerai mes outils.",
      "C": "Hier, je vais ranger mes outils.",
      "D": "Hier, range mes outils."
    },
    "correct": "A"
  },
  {
    "code": "SC6-06",
    "notion": "CONJUGAISON",
    "question": "Quelle phrase utilise correctement l’imparfait pour une habitude passée ?",
    "choices": {
      "A": "Quand j’étais apprenti, je prenais le bus chaque matin.",
      "B": "Quand j’étais apprenti, je prendrai le bus chaque matin.",
      "C": "Quand j’étais apprenti, je prends demain le bus.",
      "D": "Quand j’étais apprenti, prendre le bus."
    },
    "correct": "A"
  },
  {
    "code": "SC6-07",
    "notion": "CONJUGAISON",
    "question": "Pour vérifier la conjugaison, il faut notamment repérer :",
    "choices": {
      "A": "le sujet et le temps voulu",
      "B": "seulement la ponctuation",
      "C": "uniquement le complément",
      "D": "la couleur du texte"
    },
    "correct": "A"
  },
  {
    "code": "SC6-08",
    "notion": "CONJUGAISON",
    "question": "Quelle phrase est cohérente avec « demain » ?",
    "choices": {
      "A": "Demain, je rencontrerai mon tuteur.",
      "B": "Demain, j’ai rencontré mon tuteur hier.",
      "C": "Demain, je rencontrais mon tuteur autrefois.",
      "D": "Demain, rencontrer mon tuteur hier."
    },
    "correct": "A"
  },
  {
    "code": "SC7-01",
    "notion": "ORTHOGRAPHE LEXICALE",
    "question": "Quel mot est correctement écrit ?",
    "choices": {
      "A": "aprenti",
      "B": "apprenti",
      "C": "aprrenti",
      "D": "apprentit"
    },
    "correct": "B"
  },
  {
    "code": "SC7-02",
    "notion": "ORTHOGRAPHE LEXICALE",
    "question": "Quel mot est correctement écrit ?",
    "choices": {
      "A": "matérièl",
      "B": "materiel",
      "C": "matériel",
      "D": "matérriel"
    },
    "correct": "C"
  },
  {
    "code": "SC7-03",
    "notion": "ORTHOGRAPHE LEXICALE",
    "question": "Quel mot est correctement écrit ?",
    "choices": {
      "A": "professionel",
      "B": "professionnel",
      "C": "proffessionnel",
      "D": "professionnell"
    },
    "correct": "B"
  },
  {
    "code": "SC7-04",
    "notion": "ORTHOGRAPHE LEXICALE",
    "question": "Quel mot est correctement écrit ?",
    "choices": {
      "A": "mécanique",
      "B": "méquanique",
      "C": "mécannique",
      "D": "mecanik"
    },
    "correct": "A"
  },
  {
    "code": "SC7-05",
    "notion": "ORTHOGRAPHE LEXICALE",
    "question": "Pour vérifier l’orthographe d’un mot inconnu, on peut :",
    "choices": {
      "A": "utiliser un dictionnaire ou un outil de vérification",
      "B": "choisir au hasard",
      "C": "supprimer le mot systématiquement",
      "D": "écrire toutes les variantes"
    },
    "correct": "A"
  },
  {
    "code": "SC7-06",
    "notion": "ORTHOGRAPHE LEXICALE",
    "question": "Quel mot est correctement écrit ?",
    "choices": {
      "A": "nécessaire",
      "B": "nécéssaire",
      "C": "néssécaire",
      "D": "necessairre"
    },
    "correct": "A"
  },
  {
    "code": "SC7-07",
    "notion": "ORTHOGRAPHE LEXICALE",
    "question": "Quel mot est correctement écrit ?",
    "choices": {
      "A": "sécurité",
      "B": "sécuritée",
      "C": "séqurité",
      "D": "securitè"
    },
    "correct": "A"
  },
  {
    "code": "SC7-08",
    "notion": "ORTHOGRAPHE LEXICALE",
    "question": "Lorsqu’on hésite sur un mot fréquent, il est utile de :",
    "choices": {
      "A": "mémoriser sa forme correcte après vérification",
      "B": "inventer une nouvelle orthographe",
      "C": "retirer toutes les lettres doubles",
      "D": "supprimer les accents de tous les mots"
    },
    "correct": "A"
  },
  {
    "code": "SC8-01",
    "notion": "COHÉRENCE DU TEXTE",
    "question": "Quel texte est le plus cohérent ?",
    "choices": {
      "A": "D’abord, je prépare mes outils. Ensuite, je contrôle le véhicule. Enfin, je range mon poste.",
      "B": "Enfin je commence. Hier demain. Outils parce que.",
      "C": "Je contrôle. Recette. Télévision. Véhicule.",
      "D": "Ensuite. D’abord. Sans action."
    },
    "correct": "A"
  },
  {
    "code": "SC8-02",
    "notion": "COHÉRENCE DU TEXTE",
    "question": "Un texte cohérent doit :",
    "choices": {
      "A": "conserver un sujet compréhensible et organiser les idées",
      "B": "changer de sujet à chaque phrase",
      "C": "supprimer tous les connecteurs",
      "D": "éviter les informations précises"
    },
    "correct": "A"
  },
  {
    "code": "SC8-03",
    "notion": "COHÉRENCE DU TEXTE",
    "question": "Quel connecteur convient ? « J’ai terminé le contrôle. ___, j’ai rangé les outils. »",
    "choices": {
      "A": "Ensuite",
      "B": "Pourtant que",
      "C": "Parce",
      "D": "Malgré de"
    },
    "correct": "A"
  },
  {
    "code": "SC8-04",
    "notion": "COHÉRENCE DU TEXTE",
    "question": "Quelle phrase n’a pas sa place dans un paragraphe sur une journée de stage en garage ?",
    "choices": {
      "A": "J’ai accueilli un client.",
      "B": "J’ai contrôlé les pneus.",
      "C": "Mon animal préféré est le dauphin.",
      "D": "J’ai rangé mon poste de travail."
    },
    "correct": "C"
  },
  {
    "code": "SC8-05",
    "notion": "COHÉRENCE DU TEXTE",
    "question": "Pour éviter les contradictions, il faut :",
    "choices": {
      "A": "vérifier les informations données dans l’ensemble du texte",
      "B": "ne relire que le premier mot",
      "C": "changer les dates au hasard",
      "D": "supprimer les verbes"
    },
    "correct": "A"
  },
  {
    "code": "SC8-06",
    "notion": "COHÉRENCE DU TEXTE",
    "question": "Quel ordre est cohérent ?",
    "choices": {
      "A": "préparation → réalisation → vérification",
      "B": "vérification → préparation → sujet sans rapport",
      "C": "conclusion → préparation → début",
      "D": "résultat → autre sujet → consigne"
    },
    "correct": "A"
  },
  {
    "code": "SC8-07",
    "notion": "COHÉRENCE DU TEXTE",
    "question": "Quelle phrase reprend clairement l’idée précédente ? « Le véhicule ne démarre pas. ___ »",
    "choices": {
      "A": "Je vérifie donc la batterie.",
      "B": "J’aime les vacances.",
      "C": "La recette contient du sucre.",
      "D": "Demain était hier."
    },
    "correct": "A"
  },
  {
    "code": "SC8-08",
    "notion": "COHÉRENCE DU TEXTE",
    "question": "Lors de la relecture finale, vérifier la cohérence signifie :",
    "choices": {
      "A": "s’assurer que les idées s’enchaînent et ne se contredisent pas",
      "B": "compter uniquement les lettres",
      "C": "mettre une virgule après chaque mot",
      "D": "remplacer tous les noms"
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
        "help": "Relis lentement et vérifie un seul type d’erreur à la fois.",
        "source_group": "soutien_correction_v15",
    }

SUPPORT_CORRECTION_QUESTIONS = tuple(make_question(row) for row in RAW)
SUPPORT_CORRECTION = {
    "slug": "sequence-soutien-correction",
    "title": "Soutien — Se corriger",
    "track": "support",
    "levels": {level: SUPPORT_CORRECTION_QUESTIONS for level in LEVELS},
}

