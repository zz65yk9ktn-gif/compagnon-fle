"""Bloc 05 — Vocabulaire, banque officielle."""

from exercise_engine import LEVELS

RAW = [
  {
    "code": "V1-01",
    "notion": "FAMILLES DE MOTS",
    "question": "Quel mot appartient à la même famille que « travail » ?",
    "choices": {
      "A": "travailler",
      "B": "table",
      "C": "rapide",
      "D": "route"
    },
    "correct": "A"
  },
  {
    "code": "V1-02",
    "notion": "FAMILLES DE MOTS",
    "question": "Quel mot appartient à la famille de « peinture » ?",
    "choices": {
      "A": "peindre",
      "B": "pente",
      "C": "penser",
      "D": "perdre"
    },
    "correct": "A"
  },
  {
    "code": "V1-03",
    "notion": "FAMILLES DE MOTS",
    "question": "Quel groupe contient des mots de la même famille ?",
    "choices": {
      "A": "lire / lecture / lecteur",
      "B": "lire / livre / ligne",
      "C": "route / rouge / rouler",
      "D": "classe / clair / clé"
    },
    "correct": "A"
  },
  {
    "code": "V1-04",
    "notion": "FAMILLES DE MOTS",
    "question": "Quel mot n’appartient pas à la famille de « mécanique » ?",
    "choices": {
      "A": "mécanicien",
      "B": "mécanique",
      "C": "mécaniquement",
      "D": "mémoire"
    },
    "correct": "D"
  },
  {
    "code": "V1-05",
    "notion": "FAMILLES DE MOTS",
    "question": "« Chanter », « chanson » et « chanteur » :",
    "choices": {
      "A": "sont des synonymes parfaits",
      "B": "appartiennent à la même famille",
      "C": "sont des antonymes",
      "D": "sont trois verbes"
    },
    "correct": "B"
  },
  {
    "code": "V1-06",
    "notion": "FAMILLES DE MOTS",
    "question": "Quel mot complète la famille « former / formation / ... » ?",
    "choices": {
      "A": "formateur",
      "B": "forêt",
      "C": "formule",
      "D": "fort"
    },
    "correct": "A"
  },
  {
    "code": "V1-07",
    "notion": "FAMILLES DE MOTS",
    "question": "Quel mot est de la même famille que « sécurité » ?",
    "choices": {
      "A": "sécuriser",
      "B": "secret",
      "C": "secteur",
      "D": "sérieux"
    },
    "correct": "A"
  },
  {
    "code": "V1-08",
    "notion": "FAMILLES DE MOTS",
    "question": "À quoi sert la famille de mots ?",
    "choices": {
      "A": "À repérer des mots construits autour d’une même idée de base",
      "B": "À classer les mots par longueur",
      "C": "À trouver uniquement des antonymes",
      "D": "À conjuguer les verbes"
    },
    "correct": "A"
  },
  {
    "code": "V2-01",
    "notion": "LE RADICAL",
    "question": "Dans « travailler », quel élément porte l’idée principale du mot ?",
    "choices": {
      "A": "le radical",
      "B": "la ponctuation",
      "C": "l’article",
      "D": "le pronom"
    },
    "correct": "A"
  },
  {
    "code": "V2-02",
    "notion": "LE RADICAL",
    "question": "Quel radical retrouve-t-on dans « chant », « chanter », « chanteur » ?",
    "choices": {
      "A": "chant-",
      "B": "eur-",
      "C": "ter-",
      "D": "an-"
    },
    "correct": "A"
  },
  {
    "code": "V2-03",
    "notion": "LE RADICAL",
    "question": "Dans « relecture », le radical est :",
    "choices": {
      "A": "lect-",
      "B": "re-",
      "C": "-ure",
      "D": "le-"
    },
    "correct": "A"
  },
  {
    "code": "V2-04",
    "notion": "LE RADICAL",
    "question": "Dans « démontage », quel élément renvoie à l’action de monter ?",
    "choices": {
      "A": "mont-",
      "B": "dé-",
      "C": "-age",
      "D": "de-"
    },
    "correct": "A"
  },
  {
    "code": "V2-05",
    "notion": "LE RADICAL",
    "question": "Quel mot contient le radical « form- » ?",
    "choices": {
      "A": "formation",
      "B": "forêt",
      "C": "fermer",
      "D": "force"
    },
    "correct": "A"
  },
  {
    "code": "V2-06",
    "notion": "LE RADICAL",
    "question": "Dans « inutilisable », quel radical exprime l’idée d’utiliser ?",
    "choices": {
      "A": "utilis-",
      "B": "in-",
      "C": "-able",
      "D": "-lis-"
    },
    "correct": "A"
  },
  {
    "code": "V2-07",
    "notion": "LE RADICAL",
    "question": "Repérer le radical aide surtout à :",
    "choices": {
      "A": "comprendre la famille et le sens d’un mot",
      "B": "compter les syllabes uniquement",
      "C": "choisir la ponctuation",
      "D": "conjuguer tous les verbes au futur"
    },
    "correct": "A"
  },
  {
    "code": "V2-08",
    "notion": "LE RADICAL",
    "question": "Quel groupe possède un radical commun évident ?",
    "choices": {
      "A": "réparer / réparation / réparateur",
      "B": "réparer / rapide / repas",
      "C": "outil / utile / huit",
      "D": "classe / casser / calme"
    },
    "correct": "A"
  },
  {
    "code": "V3-01",
    "notion": "LES PRÉFIXES",
    "question": "Un préfixe se place :",
    "choices": {
      "A": "avant le radical",
      "B": "après le radical",
      "C": "toujours à la fin d’une phrase",
      "D": "entre deux verbes"
    },
    "correct": "A"
  },
  {
    "code": "V3-02",
    "notion": "LES PRÉFIXES",
    "question": "Dans « refaire », le préfixe « re- » signifie ici :",
    "choices": {
      "A": "faire à nouveau",
      "B": "ne pas faire",
      "C": "faire moins vite",
      "D": "faire hier"
    },
    "correct": "A"
  },
  {
    "code": "V3-03",
    "notion": "LES PRÉFIXES",
    "question": "Dans « impossible », le préfixe « im- » exprime :",
    "choices": {
      "A": "la négation",
      "B": "le futur",
      "C": "la quantité",
      "D": "le lieu"
    },
    "correct": "A"
  },
  {
    "code": "V3-04",
    "notion": "LES PRÉFIXES",
    "question": "Quel mot contient un préfixe ?",
    "choices": {
      "A": "dévisser",
      "B": "vis",
      "C": "outil",
      "D": "moteur"
    },
    "correct": "A"
  },
  {
    "code": "V3-05",
    "notion": "LES PRÉFIXES",
    "question": "Dans « préchauffer », « pré- » signifie :",
    "choices": {
      "A": "avant",
      "B": "après",
      "C": "contre",
      "D": "sans"
    },
    "correct": "A"
  },
  {
    "code": "V3-06",
    "notion": "LES PRÉFIXES",
    "question": "Quel préfixe peut exprimer l’idée de contraire ou de négation ?",
    "choices": {
      "A": "in-",
      "B": "-ment",
      "C": "-age",
      "D": "-eur"
    },
    "correct": "A"
  },
  {
    "code": "V3-07",
    "notion": "LES PRÉFIXES",
    "question": "Quel mot signifie « brancher de nouveau » ?",
    "choices": {
      "A": "rebrancher",
      "B": "débrancher",
      "C": "branchage",
      "D": "branchement"
    },
    "correct": "A"
  },
  {
    "code": "V3-08",
    "notion": "LES PRÉFIXES",
    "question": "Dans « démonter », le préfixe « dé- » modifie le sens pour indiquer :",
    "choices": {
      "A": "l’action inverse de monter",
      "B": "une personne",
      "C": "une habitude",
      "D": "une couleur"
    },
    "correct": "A"
  },
  {
    "code": "V4-01",
    "notion": "LES SUFFIXES",
    "question": "Un suffixe se place :",
    "choices": {
      "A": "après le radical",
      "B": "avant le radical",
      "C": "avant le sujet",
      "D": "au début de chaque phrase"
    },
    "correct": "A"
  },
  {
    "code": "V4-02",
    "notion": "LES SUFFIXES",
    "question": "Dans « mécanicien », le suffixe « -ien » sert à désigner :",
    "choices": {
      "A": "une personne",
      "B": "une négation",
      "C": "un lieu uniquement",
      "D": "un temps verbal"
    },
    "correct": "A"
  },
  {
    "code": "V4-03",
    "notion": "LES SUFFIXES",
    "question": "Dans « réparation », le suffixe « -tion » forme souvent :",
    "choices": {
      "A": "un nom d’action",
      "B": "un pronom",
      "C": "une préposition",
      "D": "un déterminant"
    },
    "correct": "A"
  },
  {
    "code": "V4-04",
    "notion": "LES SUFFIXES",
    "question": "Quel mot contient le suffixe « -eur » ?",
    "choices": {
      "A": "vendeur",
      "B": "vendre",
      "C": "vente",
      "D": "revendre"
    },
    "correct": "A"
  },
  {
    "code": "V4-05",
    "notion": "LES SUFFIXES",
    "question": "Le suffixe « -able » dans « lavable » signifie :",
    "choices": {
      "A": "qui peut être lavé",
      "B": "qui ne doit jamais être lavé",
      "C": "qui a été lavé hier",
      "D": "qui lave quelqu’un"
    },
    "correct": "A"
  },
  {
    "code": "V4-06",
    "notion": "LES SUFFIXES",
    "question": "Dans « rapidement », le suffixe « -ment » sert à former :",
    "choices": {
      "A": "un adverbe",
      "B": "un nom de personne",
      "C": "un futur",
      "D": "un article"
    },
    "correct": "A"
  },
  {
    "code": "V4-07",
    "notion": "LES SUFFIXES",
    "question": "Quel mot est formé avec un suffixe indiquant un métier ou une personne ?",
    "choices": {
      "A": "formateur",
      "B": "reformer",
      "C": "formation",
      "D": "informe"
    },
    "correct": "A"
  },
  {
    "code": "V4-08",
    "notion": "LES SUFFIXES",
    "question": "Repérer un suffixe peut aider à :",
    "choices": {
      "A": "comprendre la nature ou le sens d’un mot",
      "B": "retrouver uniquement son contraire",
      "C": "supprimer le radical",
      "D": "choisir le sujet du verbe"
    },
    "correct": "A"
  },
  {
    "code": "V5-01",
    "notion": "LES SYNONYMES",
    "question": "Quel est un synonyme de « commencer » ?",
    "choices": {
      "A": "débuter",
      "B": "finir",
      "C": "arrêter",
      "D": "casser"
    },
    "correct": "A"
  },
  {
    "code": "V5-02",
    "notion": "LES SYNONYMES",
    "question": "Quel mot est proche de « rapide » ?",
    "choices": {
      "A": "vite",
      "B": "lent",
      "C": "lourd",
      "D": "tard"
    },
    "correct": "A"
  },
  {
    "code": "V5-03",
    "notion": "LES SYNONYMES",
    "question": "Dans « Ce travail est difficile », quel mot peut remplacer « difficile » sans changer fortement le sens ?",
    "choices": {
      "A": "compliqué",
      "B": "facile",
      "C": "terminé",
      "D": "silencieux"
    },
    "correct": "A"
  },
  {
    "code": "V5-04",
    "notion": "LES SYNONYMES",
    "question": "Quel est un synonyme de « réparer » dans certains contextes ?",
    "choices": {
      "A": "remettre en état",
      "B": "détériorer",
      "C": "abandonner",
      "D": "casser"
    },
    "correct": "A"
  },
  {
    "code": "V5-05",
    "notion": "LES SYNONYMES",
    "question": "Deux synonymes sont :",
    "choices": {
      "A": "deux mots de sens proche",
      "B": "deux mots de sens opposé",
      "C": "deux mots forcément identiques",
      "D": "deux verbes au passé"
    },
    "correct": "A"
  },
  {
    "code": "V5-06",
    "notion": "LES SYNONYMES",
    "question": "Quel mot peut remplacer « vérifier » ?",
    "choices": {
      "A": "contrôler",
      "B": "oublier",
      "C": "salir",
      "D": "fermer"
    },
    "correct": "A"
  },
  {
    "code": "V5-07",
    "notion": "LES SYNONYMES",
    "question": "Quel mot est proche de « choisir » ?",
    "choices": {
      "A": "sélectionner",
      "B": "supprimer",
      "C": "refuser toujours",
      "D": "copier"
    },
    "correct": "A"
  },
  {
    "code": "V5-08",
    "notion": "LES SYNONYMES",
    "question": "Pourquoi utiliser des synonymes dans un texte ?",
    "choices": {
      "A": "Pour éviter les répétitions et préciser le vocabulaire",
      "B": "Pour supprimer tous les verbes",
      "C": "Pour changer le temps des phrases",
      "D": "Pour raccourcir tous les mots"
    },
    "correct": "A"
  },
  {
    "code": "V6-01",
    "notion": "LES ANTONYMES",
    "question": "Quel est l’antonyme de « ouvrir » ?",
    "choices": {
      "A": "fermer",
      "B": "entrer",
      "C": "regarder",
      "D": "tourner"
    },
    "correct": "A"
  },
  {
    "code": "V6-02",
    "notion": "LES ANTONYMES",
    "question": "Quel est le contraire de « propre » ?",
    "choices": {
      "A": "sale",
      "B": "net",
      "C": "rangé",
      "D": "clair"
    },
    "correct": "A"
  },
  {
    "code": "V6-03",
    "notion": "LES ANTONYMES",
    "question": "Quel est l’antonyme de « augmenter » ?",
    "choices": {
      "A": "diminuer",
      "B": "continuer",
      "C": "mesurer",
      "D": "ajouter"
    },
    "correct": "A"
  },
  {
    "code": "V6-04",
    "notion": "LES ANTONYMES",
    "question": "Deux antonymes sont :",
    "choices": {
      "A": "deux mots de sens opposé",
      "B": "deux mots de même famille",
      "C": "deux mots de sens identique",
      "D": "deux noms propres"
    },
    "correct": "A"
  },
  {
    "code": "V6-05",
    "notion": "LES ANTONYMES",
    "question": "Quel est l’antonyme de « possible » ?",
    "choices": {
      "A": "impossible",
      "B": "probable",
      "C": "pratique",
      "D": "précis"
    },
    "correct": "A"
  },
  {
    "code": "V6-06",
    "notion": "LES ANTONYMES",
    "question": "Quel est le contraire de « avant » ?",
    "choices": {
      "A": "après",
      "B": "autour",
      "C": "devant",
      "D": "pendant"
    },
    "correct": "A"
  },
  {
    "code": "V6-07",
    "notion": "LES ANTONYMES",
    "question": "Quel couple contient deux antonymes ?",
    "choices": {
      "A": "chaud / froid",
      "B": "chaud / chaleur",
      "C": "lire / lecture",
      "D": "outil / outillage"
    },
    "correct": "A"
  },
  {
    "code": "V6-08",
    "notion": "LES ANTONYMES",
    "question": "Quel mot s’oppose à « accepter » ?",
    "choices": {
      "A": "refuser",
      "B": "proposer",
      "C": "expliquer",
      "D": "demander"
    },
    "correct": "A"
  },
  {
    "code": "V7-01",
    "notion": "REGISTRES DE LANGUE",
    "question": "Dans un mail professionnel, quelle formule est la plus adaptée ?",
    "choices": {
      "A": "Bonjour Madame,",
      "B": "Wesh ça va ?",
      "C": "Salut toi !",
      "D": "Yo !"
    },
    "correct": "A"
  },
  {
    "code": "V7-02",
    "notion": "REGISTRES DE LANGUE",
    "question": "Quel mot appartient plutôt à un registre familier pour parler d’un travail ?",
    "choices": {
      "A": "boulot",
      "B": "emploi",
      "C": "profession",
      "D": "activité professionnelle"
    },
    "correct": "A"
  },
  {
    "code": "V7-03",
    "notion": "REGISTRES DE LANGUE",
    "question": "Dans une lettre à une entreprise, on écrit plutôt :",
    "choices": {
      "A": "Je vous remercie pour votre réponse.",
      "B": "Merci gros !",
      "C": "Trop cool votre réponse.",
      "D": "Nickel, ça marche."
    },
    "correct": "A"
  },
  {
    "code": "V7-04",
    "notion": "REGISTRES DE LANGUE",
    "question": "Adapter son registre de langue signifie :",
    "choices": {
      "A": "choisir ses mots selon la situation et le destinataire",
      "B": "parler toujours de la même manière",
      "C": "supprimer la politesse",
      "D": "utiliser uniquement des mots compliqués"
    },
    "correct": "A"
  },
  {
    "code": "V7-05",
    "notion": "REGISTRES DE LANGUE",
    "question": "Quel terme est le plus neutre ?",
    "choices": {
      "A": "voiture",
      "B": "bagnole",
      "C": "caisse",
      "D": "bolide de ouf"
    },
    "correct": "A"
  },
  {
    "code": "V7-06",
    "notion": "REGISTRES DE LANGUE",
    "question": "À un responsable que l’on ne connaît pas, quelle demande est la plus adaptée ?",
    "choices": {
      "A": "Pourriez-vous me préciser l’horaire, s’il vous plaît ?",
      "B": "Tu me files l’heure ?",
      "C": "C’est quand ton truc ?",
      "D": "Balance l’horaire."
    },
    "correct": "A"
  },
  {
    "code": "V7-07",
    "notion": "REGISTRES DE LANGUE",
    "question": "Quel registre convient généralement à un entretien d’embauche ?",
    "choices": {
      "A": "courant ou soutenu adapté",
      "B": "uniquement argotique",
      "C": "uniquement familier",
      "D": "langage texto obligatoire"
    },
    "correct": "A"
  },
  {
    "code": "V7-08",
    "notion": "REGISTRES DE LANGUE",
    "question": "« J’ai pas capté » peut être remplacé dans un contexte professionnel par :",
    "choices": {
      "A": "Je n’ai pas compris.",
      "B": "J’ai rien pigé frère.",
      "C": "C’est n’importe quoi.",
      "D": "Ça me saoule."
    },
    "correct": "A"
  },
  {
    "code": "V8-01",
    "notion": "LEXIQUE SCOLAIRE ET PROFESSIONNEL",
    "question": "Dans un cours, « consigne » désigne :",
    "choices": {
      "A": "ce qu’il faut faire",
      "B": "la note obtenue",
      "C": "le nom de l’élève",
      "D": "la date de naissance"
    },
    "correct": "A"
  },
  {
    "code": "V8-02",
    "notion": "LEXIQUE SCOLAIRE ET PROFESSIONNEL",
    "question": "Dans une entreprise, un « tuteur » est généralement :",
    "choices": {
      "A": "la personne qui accompagne l’apprenti",
      "B": "un client",
      "C": "un fournisseur obligatoire",
      "D": "un outil"
    },
    "correct": "A"
  },
  {
    "code": "V8-03",
    "notion": "LEXIQUE SCOLAIRE ET PROFESSIONNEL",
    "question": "Que signifie « échéance » ?",
    "choices": {
      "A": "date limite ou date prévue",
      "B": "pause du matin",
      "C": "nom d’un métier",
      "D": "matériel de sécurité"
    },
    "correct": "A"
  },
  {
    "code": "V8-04",
    "notion": "LEXIQUE SCOLAIRE ET PROFESSIONNEL",
    "question": "Dans un atelier, un EPI est :",
    "choices": {
      "A": "un équipement de protection individuelle",
      "B": "une évaluation de français",
      "C": "un document bancaire",
      "D": "une pause"
    },
    "correct": "A"
  },
  {
    "code": "V8-05",
    "notion": "LEXIQUE SCOLAIRE ET PROFESSIONNEL",
    "question": "« Justificatif » désigne :",
    "choices": {
      "A": "un document qui apporte une preuve",
      "B": "une punition",
      "C": "une note orale",
      "D": "une consigne de sécurité uniquement"
    },
    "correct": "A"
  },
  {
    "code": "V8-06",
    "notion": "LEXIQUE SCOLAIRE ET PROFESSIONNEL",
    "question": "Que signifie « compétence » dans un contexte de formation ?",
    "choices": {
      "A": "capacité à mobiliser des connaissances et savoir-faire dans une situation",
      "B": "nombre d’heures de pause",
      "C": "nom de l’entreprise",
      "D": "salaire mensuel"
    },
    "correct": "A"
  },
  {
    "code": "V8-07",
    "notion": "LEXIQUE SCOLAIRE ET PROFESSIONNEL",
    "question": "Dans un emploi du temps, un « créneau » est :",
    "choices": {
      "A": "une période horaire prévue",
      "B": "une salle uniquement",
      "C": "un examen final",
      "D": "un diplôme"
    },
    "correct": "A"
  },
  {
    "code": "V8-08",
    "notion": "LEXIQUE SCOLAIRE ET PROFESSIONNEL",
    "question": "Quel mot appartient clairement au lexique professionnel ?",
    "choices": {
      "A": "devis",
      "B": "nuage",
      "C": "plage",
      "D": "forêt"
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
        "help": "Observe la construction du mot et le contexte de la phrase.",
        "source_group": "soutien_vocabulaire_v15",
    }

SUPPORT_VOCABULARY_QUESTIONS = tuple(make_question(row) for row in RAW)
SUPPORT_VOCABULARY = {
    "slug": "sequence-soutien-vocabulaire",
    "title": "Soutien — Vocabulaire",
    "track": "support",
    "levels": {level: SUPPORT_VOCABULARY_QUESTIONS for level in LEVELS},
}

