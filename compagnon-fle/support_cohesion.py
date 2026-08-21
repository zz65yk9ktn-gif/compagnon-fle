"""Bloc 04 — Cohésion et liens logiques, banque officielle."""

from exercise_engine import LEVELS

RAW = [
  {
    "code": "L1-01",
    "notion": "REPRISES ET ÉVITER LES RÉPÉTITIONS",
    "question": "Dans « Paul prend sa trousse. Il l’ouvre. », « l’ » remplace :",
    "choices": {
      "A": "Paul",
      "B": "sa trousse",
      "C": "ouvre",
      "D": "prend"
    },
    "correct": "B"
  },
  {
    "code": "L1-02",
    "notion": "REPRISES ET ÉVITER LES RÉPÉTITIONS",
    "question": "Quelle phrase évite correctement une répétition ?",
    "choices": {
      "A": "Le mécanicien prend la clé. Le mécanicien utilise la clé.",
      "B": "Le mécanicien prend la clé. Il l’utilise.",
      "C": "Le mécanicien prend la clé. La clé prend le mécanicien.",
      "D": "Le mécanicien prend la clé. Utilise mécanicien."
    },
    "correct": "B"
  },
  {
    "code": "L1-03",
    "notion": "REPRISES ET ÉVITER LES RÉPÉTITIONS",
    "question": "Dans « Les élèves entrent. Ils s’installent. », « ils » remplace :",
    "choices": {
      "A": "entrent",
      "B": "les élèves",
      "C": "s’installent",
      "D": "la salle"
    },
    "correct": "B"
  },
  {
    "code": "L1-04",
    "notion": "REPRISES ET ÉVITER LES RÉPÉTITIONS",
    "question": "Quel mot peut reprendre « la voiture » ?",
    "choices": {
      "A": "il",
      "B": "elle",
      "C": "ils",
      "D": "eux"
    },
    "correct": "B"
  },
  {
    "code": "L1-05",
    "notion": "REPRISES ET ÉVITER LES RÉPÉTITIONS",
    "question": "Quelle reprise est correcte ? « J’ai acheté des gants. Je ___ range dans mon sac. »",
    "choices": {
      "A": "les",
      "B": "lui",
      "C": "leur",
      "D": "y"
    },
    "correct": "A"
  },
  {
    "code": "L1-06",
    "notion": "REPRISES ET ÉVITER LES RÉPÉTITIONS",
    "question": "Quel groupe évite la répétition de « le formateur » ?",
    "choices": {
      "A": "cet homme",
      "B": "cette machine",
      "C": "ces outils",
      "D": "ce lieu"
    },
    "correct": "A"
  },
  {
    "code": "L1-07",
    "notion": "REPRISES ET ÉVITER LES RÉPÉTITIONS",
    "question": "Dans « Le moteur est neuf. Celui-ci fonctionne bien. », « celui-ci » remplace :",
    "choices": {
      "A": "neuf",
      "B": "fonctionne",
      "C": "le moteur",
      "D": "bien"
    },
    "correct": "C"
  },
  {
    "code": "L1-08",
    "notion": "REPRISES ET ÉVITER LES RÉPÉTITIONS",
    "question": "Pourquoi utilise-t-on des reprises dans un texte ?",
    "choices": {
      "A": "Pour répéter exactement tous les noms",
      "B": "Pour relier les phrases et éviter les répétitions inutiles",
      "C": "Pour supprimer les verbes",
      "D": "Pour allonger toutes les phrases"
    },
    "correct": "B"
  },
  {
    "code": "L2-01",
    "notion": "INDICATEURS DE TEMPS",
    "question": "Quel mot indique une action passée ?",
    "choices": {
      "A": "hier",
      "B": "demain",
      "C": "bientôt",
      "D": "maintenant"
    },
    "correct": "A"
  },
  {
    "code": "L2-02",
    "notion": "INDICATEURS DE TEMPS",
    "question": "Quel mot indique une action future ?",
    "choices": {
      "A": "autrefois",
      "B": "demain",
      "C": "jadis",
      "D": "hier"
    },
    "correct": "B"
  },
  {
    "code": "L2-03",
    "notion": "INDICATEURS DE TEMPS",
    "question": "Quel indicateur correspond au présent ?",
    "choices": {
      "A": "actuellement",
      "B": "la semaine dernière",
      "C": "l’an prochain",
      "D": "autrefois"
    },
    "correct": "A"
  },
  {
    "code": "L2-04",
    "notion": "INDICATEURS DE TEMPS",
    "question": "Complète : « ___, nous avons visité l’entreprise. »",
    "choices": {
      "A": "Demain",
      "B": "Hier",
      "C": "Bientôt",
      "D": "Plus tard"
    },
    "correct": "B"
  },
  {
    "code": "L2-05",
    "notion": "INDICATEURS DE TEMPS",
    "question": "Complète : « ___, je commencerai mon stage. »",
    "choices": {
      "A": "La semaine prochaine",
      "B": "La semaine dernière",
      "C": "Hier",
      "D": "Autrefois"
    },
    "correct": "A"
  },
  {
    "code": "L2-06",
    "notion": "INDICATEURS DE TEMPS",
    "question": "Quel indicateur exprime la fréquence ?",
    "choices": {
      "A": "souvent",
      "B": "hier",
      "C": "demain",
      "D": "ici"
    },
    "correct": "A"
  },
  {
    "code": "L2-07",
    "notion": "INDICATEURS DE TEMPS",
    "question": "Quel indicateur situe une action avant une autre ?",
    "choices": {
      "A": "auparavant",
      "B": "ensuite",
      "C": "bientôt",
      "D": "maintenant"
    },
    "correct": "A"
  },
  {
    "code": "L2-08",
    "notion": "INDICATEURS DE TEMPS",
    "question": "Quel mot permet d’enchaîner deux étapes dans le temps ?",
    "choices": {
      "A": "ensuite",
      "B": "parce que",
      "C": "mais",
      "D": "sous"
    },
    "correct": "A"
  },
  {
    "code": "L3-01",
    "notion": "SITUER DANS L’ESPACE",
    "question": "Complète : « Le sac est ___ la table. »",
    "choices": {
      "A": "sous",
      "B": "hier",
      "C": "parce que",
      "D": "ensuite"
    },
    "correct": "A"
  },
  {
    "code": "L3-02",
    "notion": "SITUER DANS L’ESPACE",
    "question": "Quel mot indique une position supérieure ?",
    "choices": {
      "A": "au-dessus de",
      "B": "derrière",
      "C": "entre",
      "D": "à gauche de"
    },
    "correct": "A"
  },
  {
    "code": "L3-03",
    "notion": "SITUER DANS L’ESPACE",
    "question": "Complète : « L’atelier est ___ le magasin et le bureau. »",
    "choices": {
      "A": "entre",
      "B": "demain",
      "C": "souvent",
      "D": "donc"
    },
    "correct": "A"
  },
  {
    "code": "L3-04",
    "notion": "SITUER DANS L’ESPACE",
    "question": "Quel mot situe un objet sur le côté opposé à la droite ?",
    "choices": {
      "A": "à gauche",
      "B": "devant",
      "C": "dessous",
      "D": "loin"
    },
    "correct": "A"
  },
  {
    "code": "L3-05",
    "notion": "SITUER DANS L’ESPACE",
    "question": "Complète : « Le véhicule est garé ___ le bâtiment. »",
    "choices": {
      "A": "devant",
      "B": "hier",
      "C": "pendant",
      "D": "car"
    },
    "correct": "A"
  },
  {
    "code": "L3-06",
    "notion": "SITUER DANS L’ESPACE",
    "question": "Quel mot exprime l’éloignement ?",
    "choices": {
      "A": "loin de",
      "B": "près de",
      "C": "sur",
      "D": "dans"
    },
    "correct": "A"
  },
  {
    "code": "L3-07",
    "notion": "SITUER DANS L’ESPACE",
    "question": "Quel mot exprime la proximité ?",
    "choices": {
      "A": "près de",
      "B": "derrière",
      "C": "sous",
      "D": "avant"
    },
    "correct": "A"
  },
  {
    "code": "L3-08",
    "notion": "SITUER DANS L’ESPACE",
    "question": "Quelle phrase situe correctement deux objets ?",
    "choices": {
      "A": "La clé est à côté du tournevis.",
      "B": "La clé est hier du tournevis.",
      "C": "La clé est parce que le tournevis.",
      "D": "La clé est ensuite le tournevis."
    },
    "correct": "A"
  },
  {
    "code": "L4-01",
    "notion": "EXPRIMER LA CAUSE",
    "question": "Quel mot introduit une cause ?",
    "choices": {
      "A": "parce que",
      "B": "donc",
      "C": "pourtant",
      "D": "ensuite"
    },
    "correct": "A"
  },
  {
    "code": "L4-02",
    "notion": "EXPRIMER LA CAUSE",
    "question": "Complète : « Il est absent ___ il est malade. »",
    "choices": {
      "A": "parce qu’",
      "B": "donc",
      "C": "pourtant",
      "D": "puis"
    },
    "correct": "A"
  },
  {
    "code": "L4-03",
    "notion": "EXPRIMER LA CAUSE",
    "question": "Quelle phrase exprime une cause ?",
    "choices": {
      "A": "Je suis en retard parce que le bus n’est pas passé.",
      "B": "Je suis en retard donc je cours.",
      "C": "Je suis en retard mais je viens.",
      "D": "Je suis en retard puis je téléphone."
    },
    "correct": "A"
  },
  {
    "code": "L4-04",
    "notion": "EXPRIMER LA CAUSE",
    "question": "Quel connecteur peut remplacer « parce que » dans un registre courant ?",
    "choices": {
      "A": "car",
      "B": "donc",
      "C": "mais",
      "D": "ensuite"
    },
    "correct": "A"
  },
  {
    "code": "L4-05",
    "notion": "EXPRIMER LA CAUSE",
    "question": "Dans « Le sol est mouillé parce qu’il a plu », la cause est :",
    "choices": {
      "A": "le sol est mouillé",
      "B": "il a plu",
      "C": "le sol",
      "D": "mouillé"
    },
    "correct": "B"
  },
  {
    "code": "L4-06",
    "notion": "EXPRIMER LA CAUSE",
    "question": "Quelle question aide à trouver la cause ?",
    "choices": {
      "A": "Pourquoi ?",
      "B": "Où ?",
      "C": "Combien ?",
      "D": "Quand exactement ?"
    },
    "correct": "A"
  },
  {
    "code": "L4-07",
    "notion": "EXPRIMER LA CAUSE",
    "question": "Complète : « La machine s’est arrêtée ___ une panne électrique. »",
    "choices": {
      "A": "à cause d’",
      "B": "donc",
      "C": "pourtant",
      "D": "ensuite"
    },
    "correct": "A"
  },
  {
    "code": "L4-08",
    "notion": "EXPRIMER LA CAUSE",
    "question": "Quelle phrase est logique ?",
    "choices": {
      "A": "Il porte des gants parce qu’il manipule un produit dangereux.",
      "B": "Il porte des gants donc le produit est hier.",
      "C": "Il porte des gants mais parce que demain.",
      "D": "Il porte des gants ensuite dangereux."
    },
    "correct": "A"
  },
  {
    "code": "L5-01",
    "notion": "EXPRIMER LA CONSÉQUENCE",
    "question": "Quel mot introduit souvent une conséquence ?",
    "choices": {
      "A": "donc",
      "B": "parce que",
      "C": "car",
      "D": "puisque"
    },
    "correct": "A"
  },
  {
    "code": "L5-02",
    "notion": "EXPRIMER LA CONSÉQUENCE",
    "question": "Complète : « Il pleut, ___ je prends un parapluie. »",
    "choices": {
      "A": "donc",
      "B": "parce que",
      "C": "car",
      "D": "avant"
    },
    "correct": "A"
  },
  {
    "code": "L5-03",
    "notion": "EXPRIMER LA CONSÉQUENCE",
    "question": "Dans « La route est fermée, donc nous changeons d’itinéraire », la conséquence est :",
    "choices": {
      "A": "la route est fermée",
      "B": "nous changeons d’itinéraire",
      "C": "la route",
      "D": "fermée"
    },
    "correct": "B"
  },
  {
    "code": "L5-04",
    "notion": "EXPRIMER LA CONSÉQUENCE",
    "question": "Quelle phrase exprime une conséquence ?",
    "choices": {
      "A": "Il a oublié son réveil, donc il est arrivé en retard.",
      "B": "Il est arrivé en retard parce qu’il a oublié son réveil.",
      "C": "Il est arrivé mais son réveil.",
      "D": "Il est arrivé avant son réveil."
    },
    "correct": "A"
  },
  {
    "code": "L5-05",
    "notion": "EXPRIMER LA CONSÉQUENCE",
    "question": "Quel connecteur peut marquer une conséquence ?",
    "choices": {
      "A": "c’est pourquoi",
      "B": "puisque",
      "C": "car",
      "D": "parce que"
    },
    "correct": "A"
  },
  {
    "code": "L5-06",
    "notion": "EXPRIMER LA CONSÉQUENCE",
    "question": "Quelle relation y a-t-il dans « Le moteur chauffe, alors on l’arrête » ?",
    "choices": {
      "A": "conséquence",
      "B": "lieu",
      "C": "opposition",
      "D": "addition"
    },
    "correct": "A"
  },
  {
    "code": "L5-07",
    "notion": "EXPRIMER LA CONSÉQUENCE",
    "question": "Complète : « Le travail est terminé ; ___, nous rangeons les outils. »",
    "choices": {
      "A": "par conséquent",
      "B": "parce que",
      "C": "pourtant",
      "D": "avant"
    },
    "correct": "A"
  },
  {
    "code": "L5-08",
    "notion": "EXPRIMER LA CONSÉQUENCE",
    "question": "Quelle phrase est logique ?",
    "choices": {
      "A": "Il n’a pas de casque, donc il ne peut pas entrer sur le chantier.",
      "B": "Il n’a pas de casque parce que il ne peut pas demain.",
      "C": "Il n’a pas de casque mais donc hier.",
      "D": "Il n’a pas de casque sous le chantier."
    },
    "correct": "A"
  },
  {
    "code": "L6-01",
    "notion": "ADDITION ET OPPOSITION",
    "question": "Quel mot ajoute une information ?",
    "choices": {
      "A": "et",
      "B": "mais",
      "C": "pourtant",
      "D": "cependant"
    },
    "correct": "A"
  },
  {
    "code": "L6-02",
    "notion": "ADDITION ET OPPOSITION",
    "question": "Quel mot marque une opposition ?",
    "choices": {
      "A": "mais",
      "B": "et",
      "C": "aussi",
      "D": "de plus"
    },
    "correct": "A"
  },
  {
    "code": "L6-03",
    "notion": "ADDITION ET OPPOSITION",
    "question": "Complète : « Il est sérieux ___ ponctuel. »",
    "choices": {
      "A": "et",
      "B": "mais",
      "C": "pourtant",
      "D": "cependant"
    },
    "correct": "A"
  },
  {
    "code": "L6-04",
    "notion": "ADDITION ET OPPOSITION",
    "question": "Complète : « Il a beaucoup travaillé, ___ il n’a pas terminé. »",
    "choices": {
      "A": "mais",
      "B": "et",
      "C": "aussi",
      "D": "de plus"
    },
    "correct": "A"
  },
  {
    "code": "L6-05",
    "notion": "ADDITION ET OPPOSITION",
    "question": "Quel connecteur ajoute un argument ?",
    "choices": {
      "A": "de plus",
      "B": "pourtant",
      "C": "cependant",
      "D": "mais"
    },
    "correct": "A"
  },
  {
    "code": "L6-06",
    "notion": "ADDITION ET OPPOSITION",
    "question": "Quel connecteur peut remplacer « mais » ?",
    "choices": {
      "A": "cependant",
      "B": "aussi",
      "C": "et",
      "D": "de plus"
    },
    "correct": "A"
  },
  {
    "code": "L6-07",
    "notion": "ADDITION ET OPPOSITION",
    "question": "Quelle phrase exprime une opposition ?",
    "choices": {
      "A": "Il est fatigué, pourtant il continue.",
      "B": "Il est fatigué et il se repose.",
      "C": "Il est fatigué, de plus il a faim.",
      "D": "Il est fatigué aussi."
    },
    "correct": "A"
  },
  {
    "code": "L6-08",
    "notion": "ADDITION ET OPPOSITION",
    "question": "Quelle phrase ajoute deux qualités ?",
    "choices": {
      "A": "Elle est attentive et organisée.",
      "B": "Elle est attentive mais organisée.",
      "C": "Elle est attentive pourtant organisée.",
      "D": "Elle est attentive cependant organisée."
    },
    "correct": "A"
  },
  {
    "code": "L7-01",
    "notion": "CONSTRUIRE UN PARAGRAPHE",
    "question": "Un paragraphe doit principalement développer :",
    "choices": {
      "A": "une idée principale",
      "B": "quatre sujets sans lien",
      "C": "uniquement une liste de mots",
      "D": "aucune idée précise"
    },
    "correct": "A"
  },
  {
    "code": "L7-02",
    "notion": "CONSTRUIRE UN PARAGRAPHE",
    "question": "Quelle phrase convient le mieux pour commencer un paragraphe ?",
    "choices": {
      "A": "Une phrase qui annonce l’idée principale",
      "B": "Une phrase sans rapport avec le sujet",
      "C": "Une suite de mots isolés",
      "D": "Une conclusion avant toute explication"
    },
    "correct": "A"
  },
  {
    "code": "L7-03",
    "notion": "CONSTRUIRE UN PARAGRAPHE",
    "question": "Quel élément aide à relier les phrases d’un paragraphe ?",
    "choices": {
      "A": "les connecteurs",
      "B": "les fautes volontaires",
      "C": "les répétitions systématiques",
      "D": "les mots au hasard"
    },
    "correct": "A"
  },
  {
    "code": "L7-04",
    "notion": "CONSTRUIRE UN PARAGRAPHE",
    "question": "Quel ordre est le plus logique ?",
    "choices": {
      "A": "idée principale → explication → exemple",
      "B": "exemple → sujet différent → mot isolé",
      "C": "conclusion → aucune idée → titre",
      "D": "mot isolé → répétition → autre sujet"
    },
    "correct": "A"
  },
  {
    "code": "L7-05",
    "notion": "CONSTRUIRE UN PARAGRAPHE",
    "question": "Quelle phrase apporte un exemple ?",
    "choices": {
      "A": "Par exemple, un apprenti peut vérifier son matériel avant de commencer.",
      "B": "Pourtant donc parce que.",
      "C": "Le sujet est ailleurs.",
      "D": "Demain hier maintenant."
    },
    "correct": "A"
  },
  {
    "code": "L7-06",
    "notion": "CONSTRUIRE UN PARAGRAPHE",
    "question": "Pourquoi évite-t-on de changer brutalement de sujet dans un paragraphe ?",
    "choices": {
      "A": "Pour garder une idée cohérente",
      "B": "Pour rendre le texte plus long",
      "C": "Pour supprimer la ponctuation",
      "D": "Pour éviter tous les verbes"
    },
    "correct": "A"
  },
  {
    "code": "L7-07",
    "notion": "CONSTRUIRE UN PARAGRAPHE",
    "question": "Quel connecteur peut introduire une conclusion courte ?",
    "choices": {
      "A": "ainsi",
      "B": "parce que",
      "C": "sous",
      "D": "hier"
    },
    "correct": "A"
  },
  {
    "code": "L7-08",
    "notion": "CONSTRUIRE UN PARAGRAPHE",
    "question": "Quel paragraphe est le plus cohérent ?",
    "choices": {
      "A": "« Le port des EPI est obligatoire. Ils protègent contre plusieurs risques. Par exemple, les gants protègent les mains. »",
      "B": "« Le port des EPI est obligatoire. Demain est bleu. Le moteur mange vite. »",
      "C": "« Les EPI. Pourtant. Une clé. »",
      "D": "« Il protège. Parce que. Ensuite hier. »"
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
        "help": "Relis les deux parties de la phrase et cherche leur relation.",
        "source_group": "soutien_cohesion_v15",
    }

SUPPORT_COHESION_QUESTIONS = tuple(make_question(row) for row in RAW)
SUPPORT_COHESION = {
    "slug": "sequence-soutien-cohesion",
    "title": "Soutien — Cohésion et liens logiques",
    "track": "support",
    "levels": {level: SUPPORT_COHESION_QUESTIONS for level in LEVELS},
}

