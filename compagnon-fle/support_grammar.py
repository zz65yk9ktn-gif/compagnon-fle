"""Bloc 02 — Grammaire, importé de la banque Soutien officielle."""

from exercise_engine import LEVELS

RAW = [
  {
    "code": "G1-01",
    "notion": "LA PHRASE : CONSTRUIRE UNE PHRASE QUI A DU SENS",
    "question": "Quelle proposition est une phrase correcte ?",
    "choices": {
      "A": "Le mécanicien vérifie les freins.",
      "B": "Le mécanicien les freins vérifie.",
      "C": "Vérifie mécanicien le freins.",
      "D": "Les freins mécanicien."
    },
    "correct": "A"
  },
  {
    "code": "G1-02",
    "notion": "LA PHRASE : CONSTRUIRE UNE PHRASE QUI A DU SENS",
    "question": "Quelle phrase commence correctement ?",
    "choices": {
      "A": "demain je travaille.",
      "B": "Demain je travaille.",
      "C": "demain Je travaille.",
      "D": "Demain Je Travaille."
    },
    "correct": "B"
  },
  {
    "code": "G1-03",
    "notion": "LA PHRASE : CONSTRUIRE UNE PHRASE QUI A DU SENS",
    "question": "Quelle phrase se termine correctement ?",
    "choices": {
      "A": "L’apprenti range ses outils",
      "B": "L’apprenti range ses outils.",
      "C": "L’apprenti range. ses outils",
      "D": "L’apprenti. range ses outils"
    },
    "correct": "B"
  },
  {
    "code": "G1-04",
    "notion": "LA PHRASE : CONSTRUIRE UNE PHRASE QUI A DU SENS",
    "question": "Quel ordre donne une phrase correcte ?",
    "choices": {
      "A": "prépare / son poste / L’apprenti",
      "B": "L’apprenti / prépare / son poste",
      "C": "son poste / L’apprenti / prépare",
      "D": "prépare / L’apprenti / son poste"
    },
    "correct": "B"
  },
  {
    "code": "G1-05",
    "notion": "LA PHRASE : CONSTRUIRE UNE PHRASE QUI A DU SENS",
    "question": "Quelle phrase a un sens logique ?",
    "choices": {
      "A": "Le client explique la panne au mécanicien.",
      "B": "La panne explique le client au mécanicien.",
      "C": "Le mécanicien panne le client.",
      "D": "Explique la panne client mécanicien."
    },
    "correct": "A"
  },
  {
    "code": "G1-06",
    "notion": "LA PHRASE : CONSTRUIRE UNE PHRASE QUI A DU SENS",
    "question": "Quelle proposition est une phrase complète ?",
    "choices": {
      "A": "Dans l’atelier.",
      "B": "Parce qu’il pleut.",
      "C": "Le chef contrôle le véhicule.",
      "D": "Très rapidement."
    },
    "correct": "C"
  },
  {
    "code": "G1-07",
    "notion": "LA PHRASE : CONSTRUIRE UNE PHRASE QUI A DU SENS",
    "question": "Quelle phrase respecte l’ordre sujet-verbe-complément ?",
    "choices": {
      "A": "Le peintre prépare la surface.",
      "B": "Prépare le peintre la surface.",
      "C": "La surface le peintre prépare.",
      "D": "Le peintre la surface prépare."
    },
    "correct": "A"
  },
  {
    "code": "G1-08",
    "notion": "LA PHRASE : CONSTRUIRE UNE PHRASE QUI A DU SENS",
    "question": "Quelle phrase est correctement ponctuée ?",
    "choices": {
      "A": "Attention la pièce est chaude.",
      "B": "Attention, la pièce est chaude.",
      "C": "Attention la pièce, est chaude.",
      "D": "Attention. la pièce est chaude."
    },
    "correct": "B"
  },
  {
    "code": "G2-01",
    "notion": "LE VERBE : REPÉRER ET CHOISIR UN VERBE PRÉCIS",
    "question": "Quel est le verbe dans « L’apprenti nettoie le poste » ?",
    "choices": {
      "A": "apprenti",
      "B": "nettoie",
      "C": "poste",
      "D": "le"
    },
    "correct": "B"
  },
  {
    "code": "G2-02",
    "notion": "LE VERBE : REPÉRER ET CHOISIR UN VERBE PRÉCIS",
    "question": "Quel mot exprime l’action dans « Le mécanicien démonte la roue » ?",
    "choices": {
      "A": "mécanicien",
      "B": "roue",
      "C": "démonte",
      "D": "la"
    },
    "correct": "C"
  },
  {
    "code": "G2-03",
    "notion": "LE VERBE : REPÉRER ET CHOISIR UN VERBE PRÉCIS",
    "question": "Quel verbe convient le mieux ? « Le coiffeur ___ les cheveux. »",
    "choices": {
      "A": "coupe",
      "B": "roule",
      "C": "peint",
      "D": "pousse"
    },
    "correct": "A"
  },
  {
    "code": "G2-04",
    "notion": "LE VERBE : REPÉRER ET CHOISIR UN VERBE PRÉCIS",
    "question": "Quel verbe est le plus précis ? « Le mécanicien ___ le niveau d’huile. »",
    "choices": {
      "A": "fait",
      "B": "vérifie",
      "C": "met",
      "D": "va"
    },
    "correct": "B"
  },
  {
    "code": "G2-05",
    "notion": "LE VERBE : REPÉRER ET CHOISIR UN VERBE PRÉCIS",
    "question": "Quel mot n’est pas un verbe ?",
    "choices": {
      "A": "réparer",
      "B": "mesurer",
      "C": "outil",
      "D": "nettoyer"
    },
    "correct": "C"
  },
  {
    "code": "G2-06",
    "notion": "LE VERBE : REPÉRER ET CHOISIR UN VERBE PRÉCIS",
    "question": "Dans « Nous préparons le matériel », le verbe est :",
    "choices": {
      "A": "Nous",
      "B": "préparons",
      "C": "le",
      "D": "matériel"
    },
    "correct": "B"
  },
  {
    "code": "G2-07",
    "notion": "LE VERBE : REPÉRER ET CHOISIR UN VERBE PRÉCIS",
    "question": "Quel verbe remplace le mieux « faire » dans « faire un contrôle » ?",
    "choices": {
      "A": "effectuer",
      "B": "dormir",
      "C": "tomber",
      "D": "regarder"
    },
    "correct": "A"
  },
  {
    "code": "G2-08",
    "notion": "LE VERBE : REPÉRER ET CHOISIR UN VERBE PRÉCIS",
    "question": "Quelle phrase contient un verbe d’action précis ?",
    "choices": {
      "A": "Il fait la roue.",
      "B": "Il regarde un truc.",
      "C": "Il serre l’écrou.",
      "D": "Il est dans l’atelier."
    },
    "correct": "C"
  },
  {
    "code": "G3-01",
    "notion": "LE SUJET DU VERBE",
    "question": "Quel est le sujet dans « L’apprenti range les outils » ?",
    "choices": {
      "A": "range",
      "B": "les outils",
      "C": "L’apprenti",
      "D": "outils"
    },
    "correct": "C"
  },
  {
    "code": "G3-02",
    "notion": "LE SUJET DU VERBE",
    "question": "Dans « Les mécaniciens réparent le véhicule », qui fait l’action ?",
    "choices": {
      "A": "le véhicule",
      "B": "Les mécaniciens",
      "C": "réparent",
      "D": "l’action"
    },
    "correct": "B"
  },
  {
    "code": "G3-03",
    "notion": "LE SUJET DU VERBE",
    "question": "Quel est le sujet de « Il nettoie son poste » ?",
    "choices": {
      "A": "Il",
      "B": "nettoie",
      "C": "son",
      "D": "poste"
    },
    "correct": "A"
  },
  {
    "code": "G3-04",
    "notion": "LE SUJET DU VERBE",
    "question": "Quel groupe peut être sujet du verbe « travaillent » ?",
    "choices": {
      "A": "Les apprentis",
      "B": "Le véhicule",
      "C": "Un apprenti",
      "D": "La machine"
    },
    "correct": "A"
  },
  {
    "code": "G3-05",
    "notion": "LE SUJET DU VERBE",
    "question": "Dans « Mon collègue et moi préparons le matériel », le sujet est :",
    "choices": {
      "A": "le matériel",
      "B": "préparons",
      "C": "Mon collègue et moi",
      "D": "moi seulement"
    },
    "correct": "C"
  },
  {
    "code": "G3-06",
    "notion": "LE SUJET DU VERBE",
    "question": "Quelle question aide à trouver le sujet ?",
    "choices": {
      "A": "Où ?",
      "B": "Quand ?",
      "C": "Qui est-ce qui fait l’action ?",
      "D": "Combien ?"
    },
    "correct": "C"
  },
  {
    "code": "G3-07",
    "notion": "LE SUJET DU VERBE",
    "question": "Dans « La voiture démarre difficilement », le sujet est :",
    "choices": {
      "A": "démarre",
      "B": "difficilement",
      "C": "La voiture",
      "D": "voiture démarre"
    },
    "correct": "C"
  },
  {
    "code": "G3-08",
    "notion": "LE SUJET DU VERBE",
    "question": "Quel est le sujet dans « Demain, nous terminons le travail » ?",
    "choices": {
      "A": "Demain",
      "B": "nous",
      "C": "terminons",
      "D": "le travail"
    },
    "correct": "B"
  },
  {
    "code": "G4-01",
    "notion": "LES PRONOMS SUJETS",
    "question": "Quel pronom remplace « Paul » ?",
    "choices": {
      "A": "il",
      "B": "elle",
      "C": "nous",
      "D": "ils"
    },
    "correct": "A"
  },
  {
    "code": "G4-02",
    "notion": "LES PRONOMS SUJETS",
    "question": "Quel pronom remplace « Sarah » ?",
    "choices": {
      "A": "il",
      "B": "elle",
      "C": "ils",
      "D": "nous"
    },
    "correct": "B"
  },
  {
    "code": "G4-03",
    "notion": "LES PRONOMS SUJETS",
    "question": "Quel pronom remplace « Paul et Karim » ?",
    "choices": {
      "A": "il",
      "B": "elle",
      "C": "ils",
      "D": "elles"
    },
    "correct": "C"
  },
  {
    "code": "G4-04",
    "notion": "LES PRONOMS SUJETS",
    "question": "Quel pronom remplace « Léa et Inès » ?",
    "choices": {
      "A": "ils",
      "B": "elles",
      "C": "elle",
      "D": "nous"
    },
    "correct": "B"
  },
  {
    "code": "G4-05",
    "notion": "LES PRONOMS SUJETS",
    "question": "Quel pronom utilise-t-on pour parler de soi ?",
    "choices": {
      "A": "tu",
      "B": "je",
      "C": "il",
      "D": "vous"
    },
    "correct": "B"
  },
  {
    "code": "G4-06",
    "notion": "LES PRONOMS SUJETS",
    "question": "Quel pronom complète « ___ travaillons ensemble » ?",
    "choices": {
      "A": "Nous",
      "B": "Ils",
      "C": "Tu",
      "D": "Elle"
    },
    "correct": "A"
  },
  {
    "code": "G4-07",
    "notion": "LES PRONOMS SUJETS",
    "question": "Quel pronom complète « Monsieur, ___ pouvez entrer » ?",
    "choices": {
      "A": "tu",
      "B": "il",
      "C": "vous",
      "D": "nous"
    },
    "correct": "C"
  },
  {
    "code": "G4-08",
    "notion": "LES PRONOMS SUJETS",
    "question": "Quel pronom remplace « la voiture » ?",
    "choices": {
      "A": "il",
      "B": "elle",
      "C": "ils",
      "D": "nous"
    },
    "correct": "B"
  },
  {
    "code": "G5-01",
    "notion": "LE GROUPE NOMINAL",
    "question": "Quel groupe est un groupe nominal ?",
    "choices": {
      "A": "la clé plate",
      "B": "travaille vite",
      "C": "très doucement",
      "D": "réparer demain"
    },
    "correct": "A"
  },
  {
    "code": "G5-02",
    "notion": "LE GROUPE NOMINAL",
    "question": "Dans « une grande caisse », quel est le nom principal ?",
    "choices": {
      "A": "une",
      "B": "grande",
      "C": "caisse",
      "D": "grand"
    },
    "correct": "C"
  },
  {
    "code": "G5-03",
    "notion": "LE GROUPE NOMINAL",
    "question": "Quel groupe nominal est correctement construit ?",
    "choices": {
      "A": "le outils",
      "B": "les outils",
      "C": "les outil",
      "D": "l’ outils"
    },
    "correct": "B"
  },
  {
    "code": "G5-04",
    "notion": "LE GROUPE NOMINAL",
    "question": "Dans « le jeune apprenti », quel mot est le nom ?",
    "choices": {
      "A": "le",
      "B": "jeune",
      "C": "apprenti",
      "D": "jeune apprenti"
    },
    "correct": "C"
  },
  {
    "code": "G5-05",
    "notion": "LE GROUPE NOMINAL",
    "question": "Quel groupe contient un déterminant et un nom ?",
    "choices": {
      "A": "rapidement",
      "B": "le moteur",
      "C": "travaille",
      "D": "très propre"
    },
    "correct": "B"
  },
  {
    "code": "G5-06",
    "notion": "LE GROUPE NOMINAL",
    "question": "Quel groupe nominal peut compléter « Je prends ___ » ?",
    "choices": {
      "A": "la clé de 12",
      "B": "rapidement",
      "C": "réparer",
      "D": "très bien"
    },
    "correct": "A"
  },
  {
    "code": "G5-07",
    "notion": "LE GROUPE NOMINAL",
    "question": "Quel mot peut enrichir le groupe nominal « une voiture » ?",
    "choices": {
      "A": "rouge",
      "B": "roule",
      "C": "demain",
      "D": "doucement"
    },
    "correct": "A"
  },
  {
    "code": "G5-08",
    "notion": "LE GROUPE NOMINAL",
    "question": "Dans « les nouveaux outils », le noyau du groupe nominal est :",
    "choices": {
      "A": "les",
      "B": "nouveaux",
      "C": "outils",
      "D": "les nouveaux"
    },
    "correct": "C"
  },
  {
    "code": "G6-01",
    "notion": "LES DÉTERMINANTS",
    "question": "Quel déterminant complète « ___ outil est cassé » ?",
    "choices": {
      "A": "Le",
      "B": "Les",
      "C": "Des",
      "D": "Mes"
    },
    "correct": "A"
  },
  {
    "code": "G6-02",
    "notion": "LES DÉTERMINANTS",
    "question": "Quel déterminant convient devant « apprentis » au pluriel ?",
    "choices": {
      "A": "un",
      "B": "le",
      "C": "les",
      "D": "une"
    },
    "correct": "C"
  },
  {
    "code": "G6-03",
    "notion": "LES DÉTERMINANTS",
    "question": "Dans « une clé », le déterminant est :",
    "choices": {
      "A": "clé",
      "B": "une",
      "C": "clé une",
      "D": "aucun"
    },
    "correct": "B"
  },
  {
    "code": "G6-04",
    "notion": "LES DÉTERMINANTS",
    "question": "Quel groupe est correct ?",
    "choices": {
      "A": "un voiture",
      "B": "une voiture",
      "C": "des voiture",
      "D": "le voitures"
    },
    "correct": "B"
  },
  {
    "code": "G6-05",
    "notion": "LES DÉTERMINANTS",
    "question": "Quel déterminant indique la possession ? « ___ outils sont dans ma caisse. »",
    "choices": {
      "A": "Mes",
      "B": "Les",
      "C": "Des",
      "D": "Un"
    },
    "correct": "A"
  },
  {
    "code": "G6-06",
    "notion": "LES DÉTERMINANTS",
    "question": "Quel déterminant complète « ___ moteur de cette voiture » ?",
    "choices": {
      "A": "La",
      "B": "Le",
      "C": "Les",
      "D": "Une"
    },
    "correct": "B"
  },
  {
    "code": "G6-07",
    "notion": "LES DÉTERMINANTS",
    "question": "Quel déterminant est au pluriel ?",
    "choices": {
      "A": "un",
      "B": "une",
      "C": "des",
      "D": "le"
    },
    "correct": "C"
  },
  {
    "code": "G6-08",
    "notion": "LES DÉTERMINANTS",
    "question": "Dans « cette machine », le déterminant est :",
    "choices": {
      "A": "cette",
      "B": "machine",
      "C": "cette machine",
      "D": "aucun"
    },
    "correct": "A"
  },
  {
    "code": "G7-01",
    "notion": "L’ADJECTIF QUALIFICATIF",
    "question": "Dans « une voiture rouge », l’adjectif est :",
    "choices": {
      "A": "une",
      "B": "voiture",
      "C": "rouge",
      "D": "voiture rouge"
    },
    "correct": "C"
  },
  {
    "code": "G7-02",
    "notion": "L’ADJECTIF QUALIFICATIF",
    "question": "Quel adjectif convient pour décrire un outil qui ne coupe plus ?",
    "choices": {
      "A": "usé",
      "B": "courir",
      "C": "atelier",
      "D": "demain"
    },
    "correct": "A"
  },
  {
    "code": "G7-03",
    "notion": "L’ADJECTIF QUALIFICATIF",
    "question": "Quel mot est un adjectif ?",
    "choices": {
      "A": "propre",
      "B": "nettoyer",
      "C": "propreté",
      "D": "atelier"
    },
    "correct": "A"
  },
  {
    "code": "G7-04",
    "notion": "L’ADJECTIF QUALIFICATIF",
    "question": "Dans « un moteur bruyant », que précise « bruyant » ?",
    "choices": {
      "A": "une action",
      "B": "une qualité du moteur",
      "C": "un lieu",
      "D": "un moment"
    },
    "correct": "B"
  },
  {
    "code": "G7-05",
    "notion": "L’ADJECTIF QUALIFICATIF",
    "question": "Quel groupe contient un adjectif qualificatif ?",
    "choices": {
      "A": "la clé neuve",
      "B": "réparer la clé",
      "C": "dans la caisse",
      "D": "très vite"
    },
    "correct": "A"
  },
  {
    "code": "G7-06",
    "notion": "L’ADJECTIF QUALIFICATIF",
    "question": "Quel adjectif peut compléter « une pièce ___ » ?",
    "choices": {
      "A": "défectueuse",
      "B": "réparer",
      "C": "moteur",
      "D": "demain"
    },
    "correct": "A"
  },
  {
    "code": "G7-07",
    "notion": "L’ADJECTIF QUALIFICATIF",
    "question": "Quel adjectif exprime le contraire de « propre » ?",
    "choices": {
      "A": "sale",
      "B": "nettoyer",
      "C": "propreté",
      "D": "lavage"
    },
    "correct": "A"
  },
  {
    "code": "G7-08",
    "notion": "L’ADJECTIF QUALIFICATIF",
    "question": "Dans « des chaussures solides », l’adjectif est :",
    "choices": {
      "A": "des",
      "B": "chaussures",
      "C": "solides",
      "D": "des chaussures"
    },
    "correct": "C"
  },
  {
    "code": "G8-01",
    "notion": "L’ACCORD DU NOM ET DE L’ADJECTIF",
    "question": "Quel groupe est correctement accordé ?",
    "choices": {
      "A": "une voiture rouge",
      "B": "une voiture rouges",
      "C": "un voiture rouge",
      "D": "une voiture rougees"
    },
    "correct": "A"
  },
  {
    "code": "G8-02",
    "notion": "L’ACCORD DU NOM ET DE L’ADJECTIF",
    "question": "Complète : « des outils ___ »",
    "choices": {
      "A": "neuf",
      "B": "neuve",
      "C": "neufs",
      "D": "neuves"
    },
    "correct": "C"
  },
  {
    "code": "G8-03",
    "notion": "L’ACCORD DU NOM ET DE L’ADJECTIF",
    "question": "Complète : « une pièce ___ »",
    "choices": {
      "A": "cassé",
      "B": "cassée",
      "C": "cassés",
      "D": "cassées"
    },
    "correct": "B"
  },
  {
    "code": "G8-04",
    "notion": "L’ACCORD DU NOM ET DE L’ADJECTIF",
    "question": "Quel groupe est correct ?",
    "choices": {
      "A": "des roues usé",
      "B": "des roues usées",
      "C": "des roue usées",
      "D": "une roues usée"
    },
    "correct": "B"
  },
  {
    "code": "G8-05",
    "notion": "L’ACCORD DU NOM ET DE L’ADJECTIF",
    "question": "Complète : « un moteur ___ »",
    "choices": {
      "A": "bruyante",
      "B": "bruyants",
      "C": "bruyant",
      "D": "bruyantes"
    },
    "correct": "C"
  },
  {
    "code": "G8-06",
    "notion": "L’ACCORD DU NOM ET DE L’ADJECTIF",
    "question": "Complète : « les machines ___ »",
    "choices": {
      "A": "propre",
      "B": "propres",
      "C": "proprees",
      "D": "propreses"
    },
    "correct": "B"
  },
  {
    "code": "G8-07",
    "notion": "L’ACCORD DU NOM ET DE L’ADJECTIF",
    "question": "Quel accord est correct ?",
    "choices": {
      "A": "une caisse lourde",
      "B": "une caisse lourd",
      "C": "un caisse lourde",
      "D": "des caisse lourdes"
    },
    "correct": "A"
  },
  {
    "code": "G8-08",
    "notion": "L’ACCORD DU NOM ET DE L’ADJECTIF",
    "question": "Dans « des voitures blanches », pourquoi « blanches » prend-il -es ?",
    "choices": {
      "A": "Parce que « voitures » est féminin pluriel",
      "B": "Parce que le mot est toujours écrit ainsi",
      "C": "Parce que « voitures » est masculin singulier",
      "D": "Parce que la phrase est au passé"
    },
    "correct": "A"
  },
  {
    "code": "G9-01",
    "notion": "L’ACCORD SUJET-VERBE",
    "question": "Complète : « L’apprenti ___ les outils. »",
    "choices": {
      "A": "rangent",
      "B": "range",
      "C": "rangeons",
      "D": "rangez"
    },
    "correct": "B"
  },
  {
    "code": "G9-02",
    "notion": "L’ACCORD SUJET-VERBE",
    "question": "Complète : « Les apprentis ___ les outils. »",
    "choices": {
      "A": "range",
      "B": "ranges",
      "C": "rangent",
      "D": "rangeons"
    },
    "correct": "C"
  },
  {
    "code": "G9-03",
    "notion": "L’ACCORD SUJET-VERBE",
    "question": "Complète : « Nous ___ le véhicule. »",
    "choices": {
      "A": "contrôlons",
      "B": "contrôle",
      "C": "contrôlent",
      "D": "contrôlez"
    },
    "correct": "A"
  },
  {
    "code": "G9-04",
    "notion": "L’ACCORD SUJET-VERBE",
    "question": "Complète : « Vous ___ la pièce. »",
    "choices": {
      "A": "remplace",
      "B": "remplaces",
      "C": "remplacez",
      "D": "remplacent"
    },
    "correct": "C"
  },
  {
    "code": "G9-05",
    "notion": "L’ACCORD SUJET-VERBE",
    "question": "Quelle phrase est correcte ?",
    "choices": {
      "A": "Le mécanicien vérifient les freins.",
      "B": "Les mécaniciens vérifie les freins.",
      "C": "Les mécaniciens vérifient les freins.",
      "D": "Les mécanicien vérifient les freins."
    },
    "correct": "C"
  },
  {
    "code": "G9-06",
    "notion": "L’ACCORD SUJET-VERBE",
    "question": "Complète : « La voiture et la moto ___ dehors. »",
    "choices": {
      "A": "reste",
      "B": "restent",
      "C": "restes",
      "D": "restons"
    },
    "correct": "B"
  },
  {
    "code": "G9-07",
    "notion": "L’ACCORD SUJET-VERBE",
    "question": "Quel élément commande l’accord du verbe ?",
    "choices": {
      "A": "Le sujet",
      "B": "Le complément",
      "C": "La ponctuation",
      "D": "Le dernier mot de la phrase"
    },
    "correct": "A"
  },
  {
    "code": "G9-08",
    "notion": "L’ACCORD SUJET-VERBE",
    "question": "Quelle phrase est correctement accordée ?",
    "choices": {
      "A": "Je préparent le matériel.",
      "B": "Tu prépare le matériel.",
      "C": "Nous préparons le matériel.",
      "D": "Ils prépare le matériel."
    },
    "correct": "C"
  }
]

def make_question(row):
    return {
        "id": f"SUP-{row['code']}",
        "type": "single_choice",
        "instruction": row["question"],
        "support": "",
        "choices": row["choices"],
        "correct_answer": row["correct"],
        "feedback_success": "Bravo, c’est juste.",
        "feedback_error": "Regarde la correction avant de continuer.",
        "competency": row["notion"],
        "difficulty": 1,
        "help": "Relis la phrase et vérifie chaque mot.",
        "source_group": "soutien_grammaire_v15",
    }

SUPPORT_GRAMMAR_QUESTIONS = tuple(make_question(row) for row in RAW)
SUPPORT_GRAMMAR = {
    "slug": "sequence-soutien-grammaire",
    "title": "Soutien — Grammaire",
    "track": "support",
    "levels": {level: SUPPORT_GRAMMAR_QUESTIONS for level in LEVELS},
}

