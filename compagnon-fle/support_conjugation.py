"""Bloc 03 — Conjugaison et temps, importé de la banque officielle."""

from exercise_engine import LEVELS

RAW = [
  {
    "code": "C1-01",
    "notion": "LE PRÉSENT",
    "question": "Complète : « Tous les matins, je ___ à 8 heures. »",
    "choices": {
      "A": "commence",
      "B": "commencerai",
      "C": "commençais",
      "D": "ai commencé"
    },
    "correct": "A"
  },
  {
    "code": "C1-02",
    "notion": "LE PRÉSENT",
    "question": "Quelle phrase exprime une habitude actuelle ?",
    "choices": {
      "A": "Hier, j’ai rangé l’atelier.",
      "B": "Chaque lundi, nous vérifions le matériel.",
      "C": "Demain, nous irons en entreprise.",
      "D": "L’an dernier, je travaillais ici."
    },
    "correct": "B"
  },
  {
    "code": "C1-03",
    "notion": "LE PRÉSENT",
    "question": "Complète : « Nous ___ nos outils après le cours. »",
    "choices": {
      "A": "rangeons",
      "B": "rangera",
      "C": "rangé",
      "D": "rangions"
    },
    "correct": "A"
  },
  {
    "code": "C1-04",
    "notion": "LE PRÉSENT",
    "question": "Quel verbe est correctement conjugué au présent ?",
    "choices": {
      "A": "Vous finissé",
      "B": "Vous finissez",
      "C": "Vous finissiez demain",
      "D": "Vous finir"
    },
    "correct": "B"
  },
  {
    "code": "C1-05",
    "notion": "LE PRÉSENT",
    "question": "Complète : « Il ___ son poste de travail. »",
    "choices": {
      "A": "nettoie",
      "B": "nettoient",
      "C": "nettoyer",
      "D": "nettoieras"
    },
    "correct": "A"
  },
  {
    "code": "C1-06",
    "notion": "LE PRÉSENT",
    "question": "Quelle phrase est au présent ?",
    "choices": {
      "A": "Je préparerai la commande.",
      "B": "J’ai préparé la commande.",
      "C": "Je prépare la commande.",
      "D": "Je préparais la commande."
    },
    "correct": "C"
  },
  {
    "code": "C1-07",
    "notion": "LE PRÉSENT",
    "question": "Complète : « Les apprentis ___ les consignes. »",
    "choices": {
      "A": "écoute",
      "B": "écoutent",
      "C": "écoutera",
      "D": "écoutais"
    },
    "correct": "B"
  },
  {
    "code": "C1-08",
    "notion": "LE PRÉSENT",
    "question": "Quel marqueur convient le mieux au présent d’habitude ?",
    "choices": {
      "A": "hier",
      "B": "demain",
      "C": "souvent",
      "D": "l’année dernière"
    },
    "correct": "C"
  },
  {
    "code": "C2-01",
    "notion": "LE PASSÉ COMPOSÉ",
    "question": "Complète : « Hier, j’___ mon dossier. »",
    "choices": {
      "A": "termine",
      "B": "ai terminé",
      "C": "terminerai",
      "D": "terminais toujours"
    },
    "correct": "B"
  },
  {
    "code": "C2-02",
    "notion": "LE PASSÉ COMPOSÉ",
    "question": "Quelle phrase est au passé composé ?",
    "choices": {
      "A": "Nous réparons le véhicule.",
      "B": "Nous réparerons le véhicule.",
      "C": "Nous avons réparé le véhicule.",
      "D": "Nous réparions le véhicule."
    },
    "correct": "C"
  },
  {
    "code": "C2-03",
    "notion": "LE PASSÉ COMPOSÉ",
    "question": "Complète : « Elle ___ arrivée à l’heure. »",
    "choices": {
      "A": "a",
      "B": "est",
      "C": "va",
      "D": "avait demain"
    },
    "correct": "B"
  },
  {
    "code": "C2-04",
    "notion": "LE PASSÉ COMPOSÉ",
    "question": "Complète : « Ils ___ fini leur travail. »",
    "choices": {
      "A": "ont",
      "B": "sont",
      "C": "vont",
      "D": "avaient demain"
    },
    "correct": "A"
  },
  {
    "code": "C2-05",
    "notion": "LE PASSÉ COMPOSÉ",
    "question": "Quel marqueur temporel appelle naturellement une action passée terminée ?",
    "choices": {
      "A": "hier",
      "B": "demain",
      "C": "en ce moment",
      "D": "chaque semaine"
    },
    "correct": "A"
  },
  {
    "code": "C2-06",
    "notion": "LE PASSÉ COMPOSÉ",
    "question": "Quelle forme est correcte ?",
    "choices": {
      "A": "J’ai prendre le bus.",
      "B": "Je suis pris le bus.",
      "C": "J’ai pris le bus.",
      "D": "Je prends hier le bus."
    },
    "correct": "C"
  },
  {
    "code": "C2-07",
    "notion": "LE PASSÉ COMPOSÉ",
    "question": "Complète : « Nous ___ vu le formateur ce matin. »",
    "choices": {
      "A": "sommes",
      "B": "avons",
      "C": "allons",
      "D": "faisions"
    },
    "correct": "B"
  },
  {
    "code": "C2-08",
    "notion": "LE PASSÉ COMPOSÉ",
    "question": "Quelle phrase raconte une action ponctuelle terminée ?",
    "choices": {
      "A": "Tous les jours, je déjeune à midi.",
      "B": "Quand j’étais petit, je jouais dehors.",
      "C": "Ce matin, j’ai envoyé le document.",
      "D": "Demain, j’enverrai le document."
    },
    "correct": "C"
  },
  {
    "code": "C3-01",
    "notion": "L’IMPARFAIT",
    "question": "Complète : « Avant, nous ___ ensemble. »",
    "choices": {
      "A": "travaillons",
      "B": "avons travaillé une fois",
      "C": "travaillions",
      "D": "travaillerons"
    },
    "correct": "C"
  },
  {
    "code": "C3-02",
    "notion": "L’IMPARFAIT",
    "question": "Quelle phrase décrit une habitude passée ?",
    "choices": {
      "A": "Chaque matin, il arrivait à 8 heures.",
      "B": "Ce matin, il est arrivé à 8 heures.",
      "C": "Demain, il arrivera à 8 heures.",
      "D": "Il arrive maintenant."
    },
    "correct": "A"
  },
  {
    "code": "C3-03",
    "notion": "L’IMPARFAIT",
    "question": "Complète : « L’atelier ___ très bruyant. »",
    "choices": {
      "A": "est demain",
      "B": "était",
      "C": "sera hier",
      "D": "a être"
    },
    "correct": "B"
  },
  {
    "code": "C3-04",
    "notion": "L’IMPARFAIT",
    "question": "Complète : « Vous ___ plus de temps avant. »",
    "choices": {
      "A": "avez",
      "B": "aurez",
      "C": "aviez",
      "D": "avez eu demain"
    },
    "correct": "C"
  },
  {
    "code": "C3-05",
    "notion": "L’IMPARFAIT",
    "question": "Quelle forme est correctement conjuguée à l’imparfait ?",
    "choices": {
      "A": "Nous faisions",
      "B": "Nous faisons hier",
      "C": "Nous feront",
      "D": "Nous avons faire"
    },
    "correct": "A"
  },
  {
    "code": "C3-06",
    "notion": "L’IMPARFAIT",
    "question": "Quel marqueur convient bien à une habitude passée ?",
    "choices": {
      "A": "autrefois",
      "B": "demain matin",
      "C": "maintenant",
      "D": "dans deux jours"
    },
    "correct": "A"
  },
  {
    "code": "C3-07",
    "notion": "L’IMPARFAIT",
    "question": "Complète : « Quand j’étais en première année, je ___ le bus. »",
    "choices": {
      "A": "prends",
      "B": "prendrai",
      "C": "prenais",
      "D": "ai prendre"
    },
    "correct": "C"
  },
  {
    "code": "C3-08",
    "notion": "L’IMPARFAIT",
    "question": "Dans quelle phrase l’imparfait décrit-il une situation ?",
    "choices": {
      "A": "Hier, j’ai cassé une clé.",
      "B": "La salle était calme et les élèves travaillaient.",
      "C": "Demain, la salle sera ouverte.",
      "D": "Je ferme la porte maintenant."
    },
    "correct": "B"
  },
  {
    "code": "C4-01",
    "notion": "PASSÉ COMPOSÉ / IMPARFAIT",
    "question": "Complète : « Je ___ quand le téléphone ___. »",
    "choices": {
      "A": "travaillais / a sonné",
      "B": "ai travaillé / sonnait toujours",
      "C": "travaillerai / sonne",
      "D": "travaille / sonnera"
    },
    "correct": "A"
  },
  {
    "code": "C4-02",
    "notion": "PASSÉ COMPOSÉ / IMPARFAIT",
    "question": "Quelle phrase oppose correctement une situation et une action ponctuelle ?",
    "choices": {
      "A": "Il pleuvait quand je suis sorti.",
      "B": "Il a plu quand je sortais tous les jours.",
      "C": "Il pleuvra quand je suis sorti.",
      "D": "Il pleut quand je sortirai hier."
    },
    "correct": "A"
  },
  {
    "code": "C4-03",
    "notion": "PASSÉ COMPOSÉ / IMPARFAIT",
    "question": "Pour raconter une habitude passée, on utilise généralement :",
    "choices": {
      "A": "le futur simple",
      "B": "l’imparfait",
      "C": "le futur proche",
      "D": "uniquement le présent"
    },
    "correct": "B"
  },
  {
    "code": "C4-04",
    "notion": "PASSÉ COMPOSÉ / IMPARFAIT",
    "question": "Pour raconter une action passée terminée et ponctuelle, on utilise généralement :",
    "choices": {
      "A": "le passé composé",
      "B": "l’imparfait d’habitude",
      "C": "le futur simple",
      "D": "le présent d’habitude"
    },
    "correct": "A"
  },
  {
    "code": "C4-05",
    "notion": "PASSÉ COMPOSÉ / IMPARFAIT",
    "question": "Complète : « Tous les jours, il ___ à pied, mais hier il ___ le bus. »",
    "choices": {
      "A": "allait / a pris",
      "B": "va / prendra",
      "C": "est allé / prenait toujours",
      "D": "ira / prend"
    },
    "correct": "A"
  },
  {
    "code": "C4-06",
    "notion": "PASSÉ COMPOSÉ / IMPARFAIT",
    "question": "Complète : « La machine ___ quand elle ___. »",
    "choices": {
      "A": "fonctionnait / est tombée en panne",
      "B": "a fonctionné / tombait toujours",
      "C": "fonctionnera / est tombée",
      "D": "fonctionne / tombait demain"
    },
    "correct": "A"
  },
  {
    "code": "C4-07",
    "notion": "PASSÉ COMPOSÉ / IMPARFAIT",
    "question": "Quelle phrase est correcte ?",
    "choices": {
      "A": "Quand j’étais enfant, j’ai joué dehors tous les jours.",
      "B": "Quand j’étais enfant, je jouais dehors tous les jours.",
      "C": "Quand je serai enfant, je jouais dehors.",
      "D": "Quand j’étais enfant, je jouerai hier."
    },
    "correct": "B"
  },
  {
    "code": "C4-08",
    "notion": "PASSÉ COMPOSÉ / IMPARFAIT",
    "question": "Dans « Je rangeais l’atelier quand le formateur est arrivé », l’action qui dure est :",
    "choices": {
      "A": "est arrivé",
      "B": "rangeais",
      "C": "formateur",
      "D": "quand"
    },
    "correct": "B"
  },
  {
    "code": "C5-01",
    "notion": "LE FUTUR PROCHE",
    "question": "Complète : « Je ___ faire un stage la semaine prochaine. »",
    "choices": {
      "A": "vais",
      "B": "suis",
      "C": "ai",
      "D": "faisais"
    },
    "correct": "A"
  },
  {
    "code": "C5-02",
    "notion": "LE FUTUR PROCHE",
    "question": "Quelle phrase est au futur proche ?",
    "choices": {
      "A": "Nous avons commencé.",
      "B": "Nous commencions.",
      "C": "Nous allons commencer.",
      "D": "Nous commencerons hier."
    },
    "correct": "C"
  },
  {
    "code": "C5-03",
    "notion": "LE FUTUR PROCHE",
    "question": "Le futur proche se construit avec :",
    "choices": {
      "A": "être + infinitif",
      "B": "avoir + infinitif",
      "C": "aller au présent + infinitif",
      "D": "faire + participe passé"
    },
    "correct": "C"
  },
  {
    "code": "C5-04",
    "notion": "LE FUTUR PROCHE",
    "question": "Complète : « Ils ___ terminer leur exercice. »",
    "choices": {
      "A": "vont",
      "B": "sont",
      "C": "ont",
      "D": "allaient hier"
    },
    "correct": "A"
  },
  {
    "code": "C5-05",
    "notion": "LE FUTUR PROCHE",
    "question": "Quelle forme est correcte ?",
    "choices": {
      "A": "Tu vas travailler.",
      "B": "Tu va travaillé.",
      "C": "Tu es travailler.",
      "D": "Tu as travailler demain."
    },
    "correct": "A"
  },
  {
    "code": "C5-06",
    "notion": "LE FUTUR PROCHE",
    "question": "Quel marqueur convient à un projet proche ?",
    "choices": {
      "A": "tout à l’heure",
      "B": "autrefois",
      "C": "il y a dix ans",
      "D": "jadis"
    },
    "correct": "A"
  },
  {
    "code": "C5-07",
    "notion": "LE FUTUR PROCHE",
    "question": "Complète : « Nous ___ préparer le matériel. »",
    "choices": {
      "A": "allons",
      "B": "avons",
      "C": "sommes",
      "D": "faisions"
    },
    "correct": "A"
  },
  {
    "code": "C5-08",
    "notion": "LE FUTUR PROCHE",
    "question": "Quelle phrase annonce une action à venir ?",
    "choices": {
      "A": "J’ai appelé mon employeur.",
      "B": "J’appelais mon employeur chaque lundi.",
      "C": "Je vais appeler mon employeur.",
      "D": "J’appelle mon employeur hier."
    },
    "correct": "C"
  },
  {
    "code": "C6-01",
    "notion": "LE FUTUR SIMPLE",
    "question": "Complète : « L’année prochaine, je ___ dans une entreprise. »",
    "choices": {
      "A": "travaille hier",
      "B": "travaillerai",
      "C": "travaillais",
      "D": "ai travaillé"
    },
    "correct": "B"
  },
  {
    "code": "C6-02",
    "notion": "LE FUTUR SIMPLE",
    "question": "Complète : « Nous ___ notre formation en juin. »",
    "choices": {
      "A": "finirons",
      "B": "finissions",
      "C": "avons fini hier",
      "D": "finissons hier"
    },
    "correct": "A"
  },
  {
    "code": "C6-03",
    "notion": "LE FUTUR SIMPLE",
    "question": "Quelle phrase est au futur simple ?",
    "choices": {
      "A": "Je vais faire un stage.",
      "B": "J’ai fait un stage.",
      "C": "Je ferai un stage.",
      "D": "Je faisais un stage."
    },
    "correct": "C"
  },
  {
    "code": "C6-04",
    "notion": "LE FUTUR SIMPLE",
    "question": "Complète : « Vous ___ plus d’expérience. »",
    "choices": {
      "A": "aviez",
      "B": "aurez",
      "C": "avez eu hier",
      "D": "avez maintenant"
    },
    "correct": "B"
  },
  {
    "code": "C6-05",
    "notion": "LE FUTUR SIMPLE",
    "question": "Quelle forme est correcte ?",
    "choices": {
      "A": "Ils prendront",
      "B": "Ils prendrons",
      "C": "Ils prendrez",
      "D": "Ils prenaient demain"
    },
    "correct": "A"
  },
  {
    "code": "C6-06",
    "notion": "LE FUTUR SIMPLE",
    "question": "Quel marqueur convient bien au futur simple ?",
    "choices": {
      "A": "l’année prochaine",
      "B": "hier matin",
      "C": "autrefois",
      "D": "la semaine dernière"
    },
    "correct": "A"
  },
  {
    "code": "C6-07",
    "notion": "LE FUTUR SIMPLE",
    "question": "Complète : « Demain, tu ___ le dossier. »",
    "choices": {
      "A": "enverras",
      "B": "envoyais",
      "C": "as envoyé hier",
      "D": "envoies hier"
    },
    "correct": "A"
  },
  {
    "code": "C6-08",
    "notion": "LE FUTUR SIMPLE",
    "question": "Quelle phrase présente un projet à venir ?",
    "choices": {
      "A": "Plus tard, je créerai mon entreprise.",
      "B": "Avant, je travaillais ici.",
      "C": "Hier, j’ai signé mon contrat.",
      "D": "En ce moment, je prépare mon CAP."
    },
    "correct": "A"
  },
  {
    "code": "C7-01",
    "notion": "PASSÉ / PRÉSENT / FUTUR",
    "question": "Classe « hier » dans la bonne catégorie.",
    "choices": {
      "A": "passé",
      "B": "présent",
      "C": "futur",
      "D": "lieu"
    },
    "correct": "A"
  },
  {
    "code": "C7-02",
    "notion": "PASSÉ / PRÉSENT / FUTUR",
    "question": "Classe « demain » dans la bonne catégorie.",
    "choices": {
      "A": "passé",
      "B": "présent",
      "C": "futur",
      "D": "manière"
    },
    "correct": "C"
  },
  {
    "code": "C7-03",
    "notion": "PASSÉ / PRÉSENT / FUTUR",
    "question": "Classe « maintenant » dans la bonne catégorie.",
    "choices": {
      "A": "passé",
      "B": "présent",
      "C": "futur",
      "D": "cause"
    },
    "correct": "B"
  },
  {
    "code": "C7-04",
    "notion": "PASSÉ / PRÉSENT / FUTUR",
    "question": "Quelle phrase respecte la chronologie « passé → présent → futur » ?",
    "choices": {
      "A": "Hier j’ai appris, aujourd’hui je m’entraîne, demain je travaillerai.",
      "B": "Demain je travaillerai, hier j’ai appris, aujourd’hui je m’entraîne.",
      "C": "Aujourd’hui je m’entraîne, demain j’ai appris, hier je travaillerai.",
      "D": "Hier je travaillerai, aujourd’hui j’ai appris demain, demain je m’entraînais."
    },
    "correct": "A"
  },
  {
    "code": "C7-05",
    "notion": "PASSÉ / PRÉSENT / FUTUR",
    "question": "Quel mot indique qu’une action a déjà eu lieu ?",
    "choices": {
      "A": "bientôt",
      "B": "actuellement",
      "C": "auparavant",
      "D": "demain"
    },
    "correct": "C"
  },
  {
    "code": "C7-06",
    "notion": "PASSÉ / PRÉSENT / FUTUR",
    "question": "Quel mot indique qu’une action va avoir lieu ?",
    "choices": {
      "A": "autrefois",
      "B": "bientôt",
      "C": "hier",
      "D": "jadis"
    },
    "correct": "B"
  },
  {
    "code": "C7-07",
    "notion": "PASSÉ / PRÉSENT / FUTUR",
    "question": "Quelle phrase parle du présent ?",
    "choices": {
      "A": "La semaine dernière, j’étais en stage.",
      "B": "Aujourd’hui, je suis au CFA.",
      "C": "La semaine prochaine, je serai en entreprise.",
      "D": "Hier, j’ai travaillé."
    },
    "correct": "B"
  },
  {
    "code": "C7-08",
    "notion": "PASSÉ / PRÉSENT / FUTUR",
    "question": "Quel ordre est chronologiquement correct ?",
    "choices": {
      "A": "demain → hier → aujourd’hui",
      "B": "aujourd’hui → hier → demain",
      "C": "hier → aujourd’hui → demain",
      "D": "demain → aujourd’hui → hier"
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
        "help": "Repère le marqueur de temps et le sujet du verbe.",
        "source_group": "soutien_conjugaison_v15",
    }

SUPPORT_CONJUGATION_QUESTIONS = tuple(make_question(row) for row in RAW)
SUPPORT_CONJUGATION = {
    "slug": "sequence-soutien-conjugaison",
    "title": "Soutien — Conjugaison et temps",
    "track": "support",
    "levels": {level: SUPPORT_CONJUGATION_QUESTIONS for level in LEVELS},
}

