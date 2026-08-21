"""Bloc 06 — Écriture et communication, banque officielle."""

from exercise_engine import LEVELS

RAW = [
  {
    "code": "E1-01",
    "notion": "RÉPONDRE PAR UNE PHRASE COMPLÈTE",
    "question": "À la question « Où fais-tu ton stage ? », quelle réponse est une phrase complète ?",
    "choices": {
      "A": "Dans un garage.",
      "B": "Garage Bordeaux.",
      "C": "Je fais mon stage dans un garage à Bordeaux.",
      "D": "Bordeaux."
    },
    "correct": "C"
  },
  {
    "code": "E1-02",
    "notion": "RÉPONDRE PAR UNE PHRASE COMPLÈTE",
    "question": "Quelle réponse convient à « Pourquoi es-tu absent ? » ?",
    "choices": {
      "A": "Parce que.",
      "B": "Je suis absent parce que je suis malade.",
      "C": "Malade.",
      "D": "Hier maladie."
    },
    "correct": "B"
  },
  {
    "code": "E1-03",
    "notion": "RÉPONDRE PAR UNE PHRASE COMPLÈTE",
    "question": "Une phrase complète contient au minimum :",
    "choices": {
      "A": "seulement un nom",
      "B": "une idée compréhensible organisée autour d’un verbe",
      "C": "uniquement un adjectif",
      "D": "toujours dix mots"
    },
    "correct": "B"
  },
  {
    "code": "E1-04",
    "notion": "RÉPONDRE PAR UNE PHRASE COMPLÈTE",
    "question": "Quelle phrase répond précisément à « Quand commence le cours ? » ?",
    "choices": {
      "A": "Le cours commence à 8 h 30.",
      "B": "CFA.",
      "C": "Avec le formateur.",
      "D": "Français."
    },
    "correct": "A"
  },
  {
    "code": "E1-05",
    "notion": "RÉPONDRE PAR UNE PHRASE COMPLÈTE",
    "question": "Quelle réponse est la plus claire ?",
    "choices": {
      "A": "Oui travail.",
      "B": "Je travaille demain matin.",
      "C": "Demain.",
      "D": "Travail matin oui."
    },
    "correct": "B"
  },
  {
    "code": "E1-06",
    "notion": "RÉPONDRE PAR UNE PHRASE COMPLÈTE",
    "question": "Pour transformer « atelier » en réponse complète à « Où es-tu ? », on écrit :",
    "choices": {
      "A": "Atelier.",
      "B": "Je suis dans l’atelier.",
      "C": "Dans.",
      "D": "Être atelier."
    },
    "correct": "B"
  },
  {
    "code": "E1-07",
    "notion": "RÉPONDRE PAR UNE PHRASE COMPLÈTE",
    "question": "Quelle phrase est correctement construite ?",
    "choices": {
      "A": "Je mon dossier termine.",
      "B": "Termine dossier je.",
      "C": "Je termine mon dossier.",
      "D": "Mon je termine dossier."
    },
    "correct": "C"
  },
  {
    "code": "E1-08",
    "notion": "RÉPONDRE PAR UNE PHRASE COMPLÈTE",
    "question": "Pour répondre à une question écrite, il faut d’abord :",
    "choices": {
      "A": "recopier toute la question",
      "B": "comprendre ce qui est demandé",
      "C": "choisir la réponse la plus longue",
      "D": "utiliser obligatoirement le futur"
    },
    "correct": "B"
  },
  {
    "code": "E2-01",
    "notion": "ORGANISER LES INFORMATIONS",
    "question": "Quel ordre est le plus logique pour raconter une activité ?",
    "choices": {
      "A": "conclusion → début → action",
      "B": "début → actions → résultat",
      "C": "résultat → titre → début",
      "D": "actions → question → début"
    },
    "correct": "B"
  },
  {
    "code": "E2-02",
    "notion": "ORGANISER LES INFORMATIONS",
    "question": "Quelle phrase doit venir en premier dans un court récit ?",
    "choices": {
      "A": "Enfin, j’ai rangé mon poste.",
      "B": "Ensuite, j’ai démonté la pièce.",
      "C": "D’abord, j’ai préparé mes outils.",
      "D": "Pour finir, j’ai vérifié le travail."
    },
    "correct": "C"
  },
  {
    "code": "E2-03",
    "notion": "ORGANISER LES INFORMATIONS",
    "question": "Quel connecteur permet d’ajouter l’étape suivante ?",
    "choices": {
      "A": "ensuite",
      "B": "pourtant",
      "C": "parce que",
      "D": "malgré"
    },
    "correct": "A"
  },
  {
    "code": "E2-04",
    "notion": "ORGANISER LES INFORMATIONS",
    "question": "Quel ordre rend le message compréhensible ?",
    "choices": {
      "A": "Je serai absent. Bonjour Madame. Merci de votre compréhension.",
      "B": "Bonjour Madame. Je serai absent demain matin. Merci de votre compréhension.",
      "C": "Merci. Absent. Bonjour.",
      "D": "Demain. Compréhension. Madame."
    },
    "correct": "B"
  },
  {
    "code": "E2-05",
    "notion": "ORGANISER LES INFORMATIONS",
    "question": "Dans un paragraphe, les phrases doivent :",
    "choices": {
      "A": "être placées au hasard",
      "B": "suivre une idée et un ordre compréhensibles",
      "C": "commencer toutes par le même mot",
      "D": "avoir exactement la même longueur"
    },
    "correct": "B"
  },
  {
    "code": "E2-06",
    "notion": "ORGANISER LES INFORMATIONS",
    "question": "Quelle suite est chronologique ?",
    "choices": {
      "A": "enfin → d’abord → ensuite",
      "B": "ensuite → enfin → d’abord",
      "C": "d’abord → ensuite → enfin",
      "D": "enfin → ensuite → d’abord"
    },
    "correct": "C"
  },
  {
    "code": "E2-07",
    "notion": "ORGANISER LES INFORMATIONS",
    "question": "Pour éviter un texte désordonné, on peut :",
    "choices": {
      "A": "préparer les idées principales avant d’écrire",
      "B": "supprimer tous les verbes",
      "C": "écrire sans relire",
      "D": "changer de sujet à chaque phrase"
    },
    "correct": "A"
  },
  {
    "code": "E2-08",
    "notion": "ORGANISER LES INFORMATIONS",
    "question": "Quelle phrase annonce clairement le sujet ?",
    "choices": {
      "A": "Je vais présenter mon expérience de stage.",
      "B": "Ensuite.",
      "C": "C’était bien parce que voilà.",
      "D": "Il y avait."
    },
    "correct": "A"
  },
  {
    "code": "E3-01",
    "notion": "ADAPTER UN MESSAGE AU DESTINATAIRE",
    "question": "Tu écris à ton maître d’apprentissage. Quelle formule convient ?",
    "choices": {
      "A": "Wesh ça va ?",
      "B": "Bonjour Monsieur,",
      "C": "Salut frérot,",
      "D": "Yo chef !"
    },
    "correct": "B"
  },
  {
    "code": "E3-02",
    "notion": "ADAPTER UN MESSAGE AU DESTINATAIRE",
    "question": "Quel message convient à un responsable ?",
    "choices": {
      "A": "J’viens pas demain lol.",
      "B": "Bonjour, je vous informe que je serai absent demain matin.",
      "C": "Pas là demain.",
      "D": "Flemme demain."
    },
    "correct": "B"
  },
  {
    "code": "E3-03",
    "notion": "ADAPTER UN MESSAGE AU DESTINATAIRE",
    "question": "Adapter un message au destinataire signifie :",
    "choices": {
      "A": "écrire toujours de la même façon",
      "B": "choisir un ton et des mots adaptés à la personne",
      "C": "utiliser uniquement des mots compliqués",
      "D": "supprimer les formules de politesse"
    },
    "correct": "B"
  },
  {
    "code": "E3-04",
    "notion": "ADAPTER UN MESSAGE AU DESTINATAIRE",
    "question": "À un ami proche, quel message est adapté ?",
    "choices": {
      "A": "Veuillez agréer l’expression de mes salutations distinguées.",
      "B": "Salut, on se retrouve à 18 h ?",
      "C": "Monsieur, je sollicite votre présence.",
      "D": "Je vous prie de bien vouloir comparaître."
    },
    "correct": "B"
  },
  {
    "code": "E3-05",
    "notion": "ADAPTER UN MESSAGE AU DESTINATAIRE",
    "question": "À un professeur, quelle demande est la plus adaptée ?",
    "choices": {
      "A": "Donne-moi le cours.",
      "B": "Bonjour Madame, pourriez-vous me transmettre le cours, s’il vous plaît ?",
      "C": "Le cours stp vite.",
      "D": "Envoie."
    },
    "correct": "B"
  },
  {
    "code": "E3-06",
    "notion": "ADAPTER UN MESSAGE AU DESTINATAIRE",
    "question": "Dans un message professionnel, on évite généralement :",
    "choices": {
      "A": "une formule de politesse",
      "B": "une information précise",
      "C": "les abréviations familières comme « mdr »",
      "D": "une signature"
    },
    "correct": "C"
  },
  {
    "code": "E3-07",
    "notion": "ADAPTER UN MESSAGE AU DESTINATAIRE",
    "question": "Quel élément aide le destinataire à comprendre immédiatement la demande ?",
    "choices": {
      "A": "un objet ou une première phrase précise",
      "B": "dix emojis",
      "C": "une phrase sans verbe",
      "D": "une information sans rapport"
    },
    "correct": "A"
  },
  {
    "code": "E3-08",
    "notion": "ADAPTER UN MESSAGE AU DESTINATAIRE",
    "question": "Pour terminer un message professionnel simple, on peut écrire :",
    "choices": {
      "A": "Cordialement,",
      "B": "Bisous partout,",
      "C": "À plus frérot,",
      "D": "MDR,"
    },
    "correct": "A"
  },
  {
    "code": "E4-01",
    "notion": "ÉCRIRE UN MESSAGE PROFESSIONNEL",
    "question": "Quel objet de mail est le plus précis ?",
    "choices": {
      "A": "Bonjour",
      "B": "Important !!!",
      "C": "Absence du 18 septembre – Christophe Canellada",
      "D": "Question"
    },
    "correct": "C"
  },
  {
    "code": "E4-02",
    "notion": "ÉCRIRE UN MESSAGE PROFESSIONNEL",
    "question": "Dans un mail professionnel, après la formule d’appel, on doit :",
    "choices": {
      "A": "expliquer clairement la raison du message",
      "B": "raconter sa journée entière",
      "C": "écrire uniquement son prénom",
      "D": "mettre plusieurs emojis"
    },
    "correct": "A"
  },
  {
    "code": "E4-03",
    "notion": "ÉCRIRE UN MESSAGE PROFESSIONNEL",
    "question": "Quel message contient une demande claire ?",
    "choices": {
      "A": "Bonjour, pourriez-vous me confirmer l’horaire du rendez-vous de lundi ?",
      "B": "Bonjour, lundi truc heure ?",
      "C": "Rendez-vous.",
      "D": "Je sais pas lundi."
    },
    "correct": "A"
  },
  {
    "code": "E4-04",
    "notion": "ÉCRIRE UN MESSAGE PROFESSIONNEL",
    "question": "Quel élément doit généralement apparaître à la fin d’un mail professionnel ?",
    "choices": {
      "A": "une signature",
      "B": "un nouveau sujet sans rapport",
      "C": "une blague obligatoire",
      "D": "une deuxième formule d’appel"
    },
    "correct": "A"
  },
  {
    "code": "E4-05",
    "notion": "ÉCRIRE UN MESSAGE PROFESSIONNEL",
    "question": "Quel mail est le plus efficace ?",
    "choices": {
      "A": "un message court, précis et poli",
      "B": "un texte très long sans demande claire",
      "C": "une suite d’abréviations",
      "D": "un message sans destinataire identifiable"
    },
    "correct": "A"
  },
  {
    "code": "E4-06",
    "notion": "ÉCRIRE UN MESSAGE PROFESSIONNEL",
    "question": "Pour annoncer une pièce jointe, on peut écrire :",
    "choices": {
      "A": "Ci-joint le document demandé.",
      "B": "Regarde ça.",
      "C": "Y a le truc.",
      "D": "Voilà machin."
    },
    "correct": "A"
  },
  {
    "code": "E4-07",
    "notion": "ÉCRIRE UN MESSAGE PROFESSIONNEL",
    "question": "Quelle formulation est correcte pour demander une réponse ?",
    "choices": {
      "A": "Réponds vite.",
      "B": "Merci par avance pour votre retour.",
      "C": "Tu réponds ou quoi ?",
      "D": "J’attends là."
    },
    "correct": "B"
  },
  {
    "code": "E4-08",
    "notion": "ÉCRIRE UN MESSAGE PROFESSIONNEL",
    "question": "Quel ordre convient pour un mail professionnel simple ?",
    "choices": {
      "A": "signature → demande → bonjour",
      "B": "bonjour → contexte/demande → remerciement → signature",
      "C": "demande → signature → objet → bonjour",
      "D": "remerciement → bonjour → signature → demande"
    },
    "correct": "B"
  },
  {
    "code": "E5-01",
    "notion": "DÉCRIRE UNE SITUATION",
    "question": "Pour décrire une situation professionnelle, quelle information est utile ?",
    "choices": {
      "A": "le lieu",
      "B": "son jeu vidéo préféré",
      "C": "une information sans rapport",
      "D": "uniquement la météo"
    },
    "correct": "A"
  },
  {
    "code": "E5-02",
    "notion": "DÉCRIRE UNE SITUATION",
    "question": "Quelle phrase décrit un fait observable ?",
    "choices": {
      "A": "La voiture est rouge.",
      "B": "Le client doit sûrement être énervé.",
      "C": "Je pense que le mécanicien ment.",
      "D": "Peut-être que tout ira mal."
    },
    "correct": "A"
  },
  {
    "code": "E5-03",
    "notion": "DÉCRIRE UNE SITUATION",
    "question": "Quelle phrase donne une information précise ?",
    "choices": {
      "A": "Il y avait un problème.",
      "B": "Le voyant rouge du tableau de bord était allumé.",
      "C": "C’était un truc bizarre.",
      "D": "Ça faisait machin."
    },
    "correct": "B"
  },
  {
    "code": "E5-04",
    "notion": "DÉCRIRE UNE SITUATION",
    "question": "Pour rendre une description claire, on peut préciser :",
    "choices": {
      "A": "qui, où, quand et ce qui se passe",
      "B": "seulement son opinion",
      "C": "uniquement la dernière phrase",
      "D": "des informations inventées"
    },
    "correct": "A"
  },
  {
    "code": "E5-05",
    "notion": "DÉCRIRE UNE SITUATION",
    "question": "Quelle phrase distingue correctement observation et hypothèse ?",
    "choices": {
      "A": "Le sol est mouillé ; il a peut-être plu.",
      "B": "Il a forcément plu parce que je le décide.",
      "C": "Le sol pense qu’il pleut.",
      "D": "Peut-être est un fait certain."
    },
    "correct": "A"
  },
  {
    "code": "E5-06",
    "notion": "DÉCRIRE UNE SITUATION",
    "question": "Quelle formulation est la plus professionnelle ?",
    "choices": {
      "A": "La machine fait un bruit inhabituel au démarrage.",
      "B": "La machine fait un bruit de ouf.",
      "C": "Le truc déconne grave.",
      "D": "Ça marche chelou."
    },
    "correct": "A"
  },
  {
    "code": "E5-07",
    "notion": "DÉCRIRE UNE SITUATION",
    "question": "Décrire précisément permet surtout :",
    "choices": {
      "A": "au lecteur de comprendre la situation",
      "B": "d’allonger le texte sans raison",
      "C": "de remplacer tous les verbes",
      "D": "d’éviter les informations utiles"
    },
    "correct": "A"
  },
  {
    "code": "E5-08",
    "notion": "DÉCRIRE UNE SITUATION",
    "question": "Quelle phrase situe clairement l’action ?",
    "choices": {
      "A": "Mardi matin, dans l’atelier, j’ai contrôlé les pneus du véhicule.",
      "B": "Là j’ai fait un truc.",
      "C": "Un jour quelque part.",
      "D": "C’était avant ou après."
    },
    "correct": "A"
  },
  {
    "code": "E6-01",
    "notion": "REFORMULER POUR ÊTRE PLUS CLAIR",
    "question": "Quelle reformulation est la plus claire de « Le truc est cassé » ?",
    "choices": {
      "A": "La poignée de la porte est cassée.",
      "B": "Le machin est mort.",
      "C": "Ça là est cassé.",
      "D": "Truc cassé."
    },
    "correct": "A"
  },
  {
    "code": "E6-02",
    "notion": "REFORMULER POUR ÊTRE PLUS CLAIR",
    "question": "Reformuler signifie :",
    "choices": {
      "A": "exprimer la même idée autrement",
      "B": "changer complètement de sujet",
      "C": "supprimer l’information principale",
      "D": "recopier exactement sans réfléchir"
    },
    "correct": "A"
  },
  {
    "code": "E6-03",
    "notion": "REFORMULER POUR ÊTRE PLUS CLAIR",
    "question": "Quelle reformulation précise « Il a fait ça » ?",
    "choices": {
      "A": "Le mécanicien a remplacé la batterie.",
      "B": "Il ça.",
      "C": "Ça a été fait par là.",
      "D": "Le truc a machin."
    },
    "correct": "A"
  },
  {
    "code": "E6-04",
    "notion": "REFORMULER POUR ÊTRE PLUS CLAIR",
    "question": "Pour rendre un message plus clair, il vaut mieux :",
    "choices": {
      "A": "remplacer les mots vagues par des mots précis",
      "B": "ajouter des mots sans rapport",
      "C": "supprimer les informations importantes",
      "D": "utiliser le plus d’abréviations possible"
    },
    "correct": "A"
  },
  {
    "code": "E6-05",
    "notion": "REFORMULER POUR ÊTRE PLUS CLAIR",
    "question": "Quelle phrase est la plus précise ?",
    "choices": {
      "A": "J’ai eu un souci.",
      "B": "Mon bus a été supprimé ce matin, je serai en retard de vingt minutes.",
      "C": "Truc transport.",
      "D": "Je vais être là mais pas là."
    },
    "correct": "B"
  },
  {
    "code": "E6-06",
    "notion": "REFORMULER POUR ÊTRE PLUS CLAIR",
    "question": "Quelle reformulation évite une répétition inutile ?",
    "choices": {
      "A": "J’ai pris les outils. Puis j’ai rangé le matériel.",
      "B": "J’ai pris les outils et les outils étaient les outils que j’ai pris.",
      "C": "Outils outils outils.",
      "D": "J’ai pris pris les outils outils."
    },
    "correct": "A"
  },
  {
    "code": "E6-07",
    "notion": "REFORMULER POUR ÊTRE PLUS CLAIR",
    "question": "Quelle phrase explique clairement une cause ?",
    "choices": {
      "A": "Je suis arrivé en retard parce que mon train a été supprimé.",
      "B": "Retard train voilà.",
      "C": "Je suis arrivé parce que retard.",
      "D": "Train donc mais."
    },
    "correct": "A"
  },
  {
    "code": "E6-08",
    "notion": "REFORMULER POUR ÊTRE PLUS CLAIR",
    "question": "Après avoir reformulé un texte, il faut vérifier :",
    "choices": {
      "A": "que le sens initial est conservé et plus clair",
      "B": "que le sujet a complètement changé",
      "C": "que toutes les phrases sont plus longues",
      "D": "qu’aucun verbe n’est utilisé"
    },
    "correct": "A"
  },
  {
    "code": "E7-01",
    "notion": "RELIRE ET AMÉLIORER UN ÉCRIT",
    "question": "Lors d’une relecture, que vérifie-t-on en priorité ?",
    "choices": {
      "A": "si le message est compréhensible",
      "B": "si toutes les phrases ont dix mots",
      "C": "si le texte contient un emoji",
      "D": "si le titre est en rouge"
    },
    "correct": "A"
  },
  {
    "code": "E7-02",
    "notion": "RELIRE ET AMÉLIORER UN ÉCRIT",
    "question": "Quelle erreur faut-il corriger dans « Les élèves travaille » ?",
    "choices": {
      "A": "l’accord sujet-verbe",
      "B": "le futur proche",
      "C": "le registre de langue",
      "D": "le préfixe"
    },
    "correct": "A"
  },
  {
    "code": "E7-03",
    "notion": "RELIRE ET AMÉLIORER UN ÉCRIT",
    "question": "Dans « une voiture rouge », quel accord peut-on vérifier ?",
    "choices": {
      "A": "nom-adjectif",
      "B": "passé-futur",
      "C": "sujet-complément",
      "D": "préfixe-suffixe"
    },
    "correct": "A"
  },
  {
    "code": "E7-04",
    "notion": "RELIRE ET AMÉLIORER UN ÉCRIT",
    "question": "Pour repérer une phrase trop longue ou mal construite, on peut :",
    "choices": {
      "A": "la relire lentement",
      "B": "supprimer toute la ponctuation",
      "C": "ajouter plusieurs idées",
      "D": "ne jamais la relire"
    },
    "correct": "A"
  },
  {
    "code": "E7-05",
    "notion": "RELIRE ET AMÉLIORER UN ÉCRIT",
    "question": "Quel texte est le plus clair ?",
    "choices": {
      "A": "Je serai absent demain matin car j’ai un rendez-vous médical.",
      "B": "Demain absent rendez-vous truc matin.",
      "C": "Car demain moi absent et voilà.",
      "D": "Rendez-vous donc absence parce que matin oui."
    },
    "correct": "A"
  },
  {
    "code": "E7-06",
    "notion": "RELIRE ET AMÉLIORER UN ÉCRIT",
    "question": "Avant d’envoyer un message professionnel, il est utile de vérifier :",
    "choices": {
      "A": "destinataire, demande, orthographe et formule de politesse",
      "B": "uniquement la couleur de l’écran",
      "C": "seulement le nombre de lignes",
      "D": "uniquement l’heure"
    },
    "correct": "A"
  },
  {
    "code": "E7-07",
    "notion": "RELIRE ET AMÉLIORER UN ÉCRIT",
    "question": "Une relecture efficace sert à :",
    "choices": {
      "A": "améliorer la clarté et corriger les erreurs",
      "B": "rendre systématiquement le texte plus long",
      "C": "changer le destinataire",
      "D": "supprimer l’idée principale"
    },
    "correct": "A"
  },
  {
    "code": "E7-08",
    "notion": "RELIRE ET AMÉLIORER UN ÉCRIT",
    "question": "Après correction, quelle phrase est correcte ?",
    "choices": {
      "A": "Nous avons terminer le travail.",
      "B": "Nous avons terminé le travail.",
      "C": "Nous avons terminés le travail.",
      "D": "Nous terminé avons travail."
    },
    "correct": "B"
  },
  {
    "code": "E8-01",
    "notion": "CHOISIR L’ÉCRIT ADAPTÉ À LA SITUATION",
    "question": "Pour prévenir son employeur d’une absence, quel support est adapté ?",
    "choices": {
      "A": "un message ou un mail professionnel",
      "B": "une recette de cuisine",
      "C": "une affiche publicitaire",
      "D": "un poème obligatoire"
    },
    "correct": "A"
  },
  {
    "code": "E8-02",
    "notion": "CHOISIR L’ÉCRIT ADAPTÉ À LA SITUATION",
    "question": "Pour présenter plusieurs étapes d’une intervention, on privilégie :",
    "choices": {
      "A": "un texte organisé chronologiquement",
      "B": "des mots placés au hasard",
      "C": "uniquement une liste de prénoms",
      "D": "une phrase sans verbe"
    },
    "correct": "A"
  },
  {
    "code": "E8-03",
    "notion": "CHOISIR L’ÉCRIT ADAPTÉ À LA SITUATION",
    "question": "Pour demander officiellement un document, quel ton convient ?",
    "choices": {
      "A": "poli et précis",
      "B": "agressif et vague",
      "C": "familier et incomplet",
      "D": "uniquement humoristique"
    },
    "correct": "A"
  },
  {
    "code": "E8-04",
    "notion": "CHOISIR L’ÉCRIT ADAPTÉ À LA SITUATION",
    "question": "Pour raconter une expérience professionnelle, il faut surtout :",
    "choices": {
      "A": "situer la situation, présenter les actions et leur résultat",
      "B": "donner uniquement son prénom",
      "C": "écrire des informations sans ordre",
      "D": "éviter tous les verbes"
    },
    "correct": "A"
  },
  {
    "code": "E8-05",
    "notion": "CHOISIR L’ÉCRIT ADAPTÉ À LA SITUATION",
    "question": "Pour transmettre une information urgente à son responsable, le message doit être :",
    "choices": {
      "A": "clair et directement compréhensible",
      "B": "volontairement mystérieux",
      "C": "sans information précise",
      "D": "rempli d’abréviations"
    },
    "correct": "A"
  },
  {
    "code": "E8-06",
    "notion": "CHOISIR L’ÉCRIT ADAPTÉ À LA SITUATION",
    "question": "Quel écrit convient pour expliquer une panne observée ?",
    "choices": {
      "A": "une description précise des faits observés",
      "B": "une histoire inventée",
      "C": "une suite d’emojis",
      "D": "une phrase sans rapport"
    },
    "correct": "A"
  },
  {
    "code": "E8-07",
    "notion": "CHOISIR L’ÉCRIT ADAPTÉ À LA SITUATION",
    "question": "Si le destinataire ne connaît pas la situation, il faut :",
    "choices": {
      "A": "donner le contexte nécessaire",
      "B": "supposer qu’il sait tout",
      "C": "supprimer les dates et les lieux",
      "D": "écrire uniquement « voilà »"
    },
    "correct": "A"
  },
  {
    "code": "E8-08",
    "notion": "CHOISIR L’ÉCRIT ADAPTÉ À LA SITUATION",
    "question": "Avant d’écrire, la meilleure question à se poser est :",
    "choices": {
      "A": "À qui j’écris, pourquoi et quelle information dois-je transmettre ?",
      "B": "Combien de mots compliqués puis-je ajouter ?",
      "C": "Puis-je éviter de donner le sujet ?",
      "D": "Puis-je écrire sans lire la consigne ?"
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
        "help": "Cherche la réponse la plus claire, précise et adaptée au destinataire.",
        "source_group": "soutien_ecriture_v15",
    }

SUPPORT_WRITING_QUESTIONS = tuple(make_question(row) for row in RAW)
SUPPORT_WRITING = {
    "slug": "sequence-soutien-ecriture",
    "title": "Soutien — Écriture et communication",
    "track": "support",
    "levels": {level: SUPPORT_WRITING_QUESTIONS for level in LEVELS},
}

