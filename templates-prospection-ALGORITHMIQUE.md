# BIBLIOTHÈQUE ALGORITHMIQUE — 150 templates de prospection LinkedIn

> Version structurée pour agent IA. Chaque template a un ID unique, des conditions d'usage, un ton et des variables à remplir. L'agent DOIT passer par l'ALGORITHME DE SÉLECTION avant de choisir un template.

---

## 0. ALGORITHME DE SÉLECTION

```
ENTRÉE : contexte_prospect {
  étape_conversation : PREMIER_MESSAGE | RELANCE | RÉPONSE_REÇUE
  signal_détecté     : VISITE_PROFIL | DEMANDE_CONNEXION | LIKE_COMMENT_MON_POST |
                       RÉPONSE_SONDAGE | LIKE_COMMENT_CONCURRENT | ÉVÉNEMENT_CONCURRENT | AUCUN
  historique         : jamais_répondu | a_répondu_puis_silence | en_conversation
  attitude_prospect  : réceptif | non_réceptif | objection | null
  niveau_qualification : non_qualifié | qualifié | a_reçu_ressource | rdv_accepté
  registre           : tu | vous   (détecté sur le profil/les réponses du prospect)
}

ALGORITHME :
1. SI étape == PREMIER_MESSAGE :
   a. SI signal_détecté != AUCUN → branche PM-S-[SIGNAL] (section 1)
      - Choisir l'approche : CONVERSATIONNELLE (défaut, crée du dialogue)
        ou DIRECTE (si on a une ressource gratuite pertinente à offrir)
      - Choisir le ton via la MATRICE DE TON (section 0.1)
   b. SI signal == AUCUN → branche PM-F (section 2)
      - Choisir la tactique via la TABLE DES TACTIQUES FROIDES (section 2.0)

2. SI étape == RELANCE :
   a. SI historique == jamais_répondu → branche RL-N (section 3.1)
      - Relance 1-2 : apport de valeur (RL-N-01 à RL-N-08)
      - Relance 3 : douce ou directe (RL-N-09 à RL-N-16)
      - Dernière relance : porte de sortie (RL-N-17 à RL-N-19)
   b. SI historique == a_répondu_puis_silence → branche RL-G (section 3.2)
      - Privilégier les relances empathiques qui rebondissent sur
        un élément donné par le prospect (RL-G-05 à RL-G-08)

3. SI étape == RÉPONSE_REÇUE :
   a. Classifier la réponse :
      - non_réceptif (méfiance, agacement, refus flou) → branche RP-NR (section 4.1)
        → identifier le cas exact parmi les 7 et utiliser le template correspondant
      - objection précise → branche RP-OBJ (section 4.2)
        → matcher l'objection exacte parmi les 13 cas
      - réceptif :
        * SI non_qualifié → poser des questions RP-Q (section 4.3)
          → ordre recommandé : BESOIN → URGENCE → ALTERNATIVES → BUDGET/DÉCISION → PROJECTION
        * SI qualifié (besoin + urgence confirmés) → offrir une ressource RP-RES (section 4.4)
        * SI a apprécié la ressource → proposer un call RP-CALL (section 4.5)
        * SI rdv_accepté → envoyer le créneau RP-RDV (section 4.6)

RÈGLE TRANSVERSE : toujours adapter [tu/vous] au registre du prospect
(voir section 0.2) et remplacer TOUTES les variables [entre crochets]
par des éléments réels du profil. Ne JAMAIS envoyer un template avec
un crochet non rempli.
```

### 0.1 Matrice de choix du ton (signaux d'intérêt)

| Ton | Code | Quand l'utiliser | Quand l'éviter |
|---|---|---|---|
| Chaleureux | CHA | Défaut sûr. Profil souriant, secteur relationnel, prospect actif sur LinkedIn | Jamais contre-indiqué |
| Empathique | EMP | Prospect qui exprime une douleur, profil discret, secteur sous pression | Prospect très direct/pressé |
| Humoristique | HUM | Prospect avec posts/bio décontractés, emojis, secteur créatif/jeune | Dirigeant formel, secteur conservateur (banque, juridique, BTP traditionnel) |
| Provocateur | PRO | Prospect au profil affirmé, commercial, entrepreneur aguerri | Prospect senior/formel, premier contact fragile |
| Sérieux | SER | Dirigeant formel, grande PME, secteur conservateur, registre "vous" | Profil très décontracté |
| Direct/Ressource | DIR | On dispose d'une ressource gratuite réellement pertinente pour CE profil | Pas de ressource adaptée → ne pas forcer |

### 0.2 Règle de registre (tu/vous)

- Défaut premier contact dirigeant TPE/PME : **vous**
- Passer au **tu** si : le prospect tutoie en premier, OU profil très décontracté (emojis, ton casual dans ses posts)
- Ne jamais mélanger tu/vous dans un même message — adapter le template choisi.

### 0.3 Glossaire des variables

| Variable | Contenu attendu |
|---|---|
| [prénom] | Prénom du prospect |
| [poste] | Titre exact du prospect (gérant, fondateur…) |
| [secteur] | Secteur d'activité du prospect |
| [domaine] / [ton domaine] | Ton domaine d'expertise (ex : automatisation IA) |
| [douleur] / [problème] / [problématique] | Pain point identifié ou supposé du prospect |
| [bénéfice] | Résultat concret obtenu (gain de temps, CA, etc.) |
| [ressource] / [ressource gratuite] | Lead magnet réel : PDF, vidéo, audit, checklist… |
| [solution] | Ton offre ou méthode |
| [client] / [référence client] | Client réel citable en preuve sociale |
| [concurrent] / [créateur] | Concurrent du prospect OU créateur de contenu du secteur |
| [thématique] / [sujet] | Sujet précis du post/sondage/événement concerné |
| [actualité du secteur] | Fait d'actualité vérifiable du secteur du prospect |
| [lien] | URL réelle (ressource, vidéo, agenda) |

---

# SECTION 1 — PREMIER MESSAGE AVEC SIGNAL (PM-S)

> Condition d'entrée : le prospect a émis un signal d'intérêt identifiable.
> Format ID : `PM-S-[SIGNAL]-[TON]`

## 1.1 Signal : le prospect a visité mon profil (PM-S-VIS)

### PM-S-VIS-CHA — conversationnel · chaleureux
**Quand :** visite de profil détectée, on veut ouvrir un dialogue léger.
> Hello [prénom],
>
> Très flatté de voir que tu as pris le temps de passer sur mon profil 😄
>
> Je suis curieux : qu'est-ce qui t'a donné envie de faire un tour par ici ?

### PM-S-VIS-EMP — conversationnel · empathique
**Quand :** visite de profil, prospect discret, on veut désamorcer toute pression.
> Hello [Prénom],
>
> Merci pour ta visite !
>
> Peut-être que tu es passé ici par simple curiosité, ou même sans raison précise.
>
> De mon côté, j'avais juste envie de te tendre la main et d'ouvrir la discussion.
>
> Si tu veux, raconte-moi : qu'est-ce qui t'a amené jusqu'à moi ?

### PM-S-VIS-HUM — conversationnel · humoristique
**Quand :** visite de profil, prospect au profil décontracté.
> Bonjour [prénom],
>
> LinkedIn m'a prévenu que vous avez espionné mon profil récemment 😂
> Blague à part, c'était totalement impromptu ou vous aviez une raison précise d'être dans les parages ?
>
> PS : ma curiosité me rattrape :)

### PM-S-VIS-PRO — conversationnel · provocateur
**Quand :** visite de profil, prospect affirmé, on assume un ton joueur.
> Hello [prénom],
>
> LinkedIn m'a informé que tu as espionné mon profil 🕵️
>
> C'est secret défense ou j'ai le droit de savoir ce qui t'a amené ici ?

### PM-S-VIS-DIR — direct · proposition de ressource
**Quand :** visite de profil ET on possède une ressource pertinente pour ce profil.
> Je viens de voir que vous avez visité mon profil [prénom].
>
> Je profite de l'occasion pour vous proposer [ressource] que j'ai créée récemment pour mes clients 😊
>
> Ça vous dit d'y avoir accès ?

## 1.2 Signal : le prospect m'a envoyé une demande de connexion (PM-S-CNX)

### PM-S-CNX-CHA — conversationnel · chaleureux
**Quand :** demande de connexion entrante, ouverture par question de découverte.
> Hello [Prénom],
>
> J'accepte ton invitation avec plaisir 😊
>
> J'en profite pour te poser une question que je pose à toutes mes nouvelles relations : quelle est ta plus grande difficulté en [ton domaine] ?

### PM-S-CNX-EMP — conversationnel · empathique
**Quand :** demande entrante, on veut comprendre la motivation du prospect.
> Salut 👋
>
> Merci pour ton ajout [prénom] !
>
> J'aime bien aller au-delà du simple bouton "Accepter" : qu'est-ce qui t'a donné envie de rejoindre mon réseau ? Une intuition, un projet, une envie de papoter ?

### PM-S-CNX-HUM — conversationnel · humoristique
**Quand :** demande entrante, prospect décontracté.
> Hello [Prénom],
>
> Merci pour la connexion !
>
> Alors, dis-moi :
>
> 1. Coup de foudre professionnel
> 2. Clic accidentel
> 3. LinkedIn t'a piégé avec son fameux « Personnes que vous pourriez connaître » ?
>
> Je prends toutes les réponses !

### PM-S-CNX-PRO — conversationnel · provocateur
**Quand :** demande entrante, prospect entrepreneur affirmé.
> Connexion acceptée [prénom] ✅
>
> Maintenant, montre-moi que tu fais partie de ceux qui connectent pour construire quelque chose, pas juste pour gonfler leur compteur 😉

### PM-S-CNX-SER — conversationnel · sérieux
**Quand :** demande entrante, dirigeant formel, registre vous.
> Bonjour [Prénom],
>
> Merci pour votre demande.
>
> J'accepte rarement les invitations au hasard.
>
> Votre profil m'a donné envie d'ouvrir la porte, et je serais curieux de savoir ce qui vous a donné envie de venir frapper à la mienne ? 🙂

### PM-S-CNX-DIR — direct · proposition de ressource
**Quand :** demande entrante ET ressource pertinente disponible.
> J'accepte votre invitation avec plaisir [prénom].
>
> Je profite de l'occasion pour vous proposer [ressource] que j'ai créée récemment pour mes clients 😊
>
> Je vous l'envoie ?

## 1.3 Signal : le prospect a liké/commenté l'un de MES posts (PM-S-LIK)

### PM-S-LIK-CHA — conversationnel · chaleureux
**Quand :** like/commentaire sur mon post, ouverture par demande de sujet.
> Salut [Prénom],
>
> Merci pour ton like sous mon dernier post !
>
> Tant qu'à faire, si tu pouvais aussi me souffler LE sujet que tu rêves de voir abordé dans un post, tu auras ma reconnaissance éternelle 😉

### PM-S-LIK-EMP — conversationnel · empathique
**Quand :** like/commentaire, on valorise l'avis du prospect.
> Hello !
>
> Un grand merci pour ton soutien sous mon post [prénom] 🙏
>
> J'essaie d'améliorer mon contenu selon les envies de mon audience donc je voulais simplement savoir : est-ce qu'il y a un prochain sujet de post qui t'intéresserait ?

### PM-S-LIK-HUM — conversationnel · humoristique
**Quand :** like/commentaire, prospect décontracté.
> Merci pour ton like sous mon dernier post [prénom] !
>
> D'ailleurs je suis à court d'idées de posts en ce moment… et n'étant pas mentaliste j'aurais besoin de savoir si certains sujets t'intéresseraient 😅
>
> Une suggestion ?

### PM-S-LIK-PRO — conversationnel · provocateur
**Quand :** like/commentaire, ton complice.
> Merci pour ton like [prénom] !
>
> Si tu as un sujet à me souffler pour un prochain post, ce serait super sympa de ta part.
>
> Promis, si le post cartonne je dirai que c'était mon idée 😂

### PM-S-LIK-SER — conversationnel · sérieux
**Quand :** like/commentaire, dirigeant formel.
> Bonjour [Prénom],
>
> Merci pour ton soutien sous mon dernier post !
>
> D'ailleurs je réfléchis à mes prochains sujets… est-ce qu'il y a une thématique qui t'intéresserait en particulier ?

### PM-S-LIK-DIR — direct · proposition de ressource
**Quand :** like/commentaire ET ressource pertinente disponible.
> Merci pour votre soutien sous mon dernier post [prénom].
>
> Je profite de l'occasion pour vous proposer [ressource] que j'ai créée récemment pour mes clients 😊
>
> Je vous l'envoie ?

## 1.4 Signal : le prospect a répondu à l'un de mes sondages (PM-S-SND)

### PM-S-SND-CHA — conversationnel · chaleureux
**Quand :** réponse à sondage, on creuse la situation.
> Hellooo,
>
> Trop sympa d'avoir répondu à mon sondage [prénom] 😀
>
> Je me suis dit que ça méritait de creuser un peu plus pour comprendre ta situation.
>
> Tu as déjà essayé de [solution] ?

### PM-S-SND-EMP — conversationnel · empathique
**Quand :** réponse à sondage révélant une douleur, on explore l'impact.
> Hello [prénom],
>
> Un grand merci d'avoir pris le temps de répondre à mon sondage sur [thématique].
>
> Tu disais avoir du mal à [douleur], comment ça impacte ton activité en ce moment ?

### PM-S-SND-HUM — conversationnel · humoristique
**Quand :** réponse à sondage, prospect décontracté.
> Hey [prénom],
>
> Ta réponse à mon sondage sur [thématique] m'a faite sourire (bon et un peu grimacer parce que c'est du vécu 😅).
>
> Je voulais creuser un peu avec toi : tu fais comment pour résoudre ce problème actuellement ?
>
> Histoire qu'on confronte un peu nos méthodes.

### PM-S-SND-PRO — conversationnel · provocateur
**Quand :** réponse à sondage, on challenge gentiment le statu quo.
> Hello [prénom],
>
> Ta réponse à mon sondage m'a fait tilter sur un truc : si [douleur] te bloque vraiment, pourquoi ne pas chercher à y remédier tout de suite 😉
>
> Tu as déjà mis des choses en place pour te débloquer ?

### PM-S-SND-SER — conversationnel · sérieux
**Quand :** réponse à sondage, registre formel.
> Bonjour [prénom],
>
> Merci d'avoir répondu à mon dernier sondage sur [thématique].
>
> Comment gérez-vous [douleur] actuellement ?

### PM-S-SND-DIR — direct · proposition de ressource
**Quand :** réponse à sondage révélant une douleur ET ressource qui y répond.
> Un grand merci pour votre réponse à mon sondage sur [thématique].
>
> Tu disais avoir du mal à [problématique spécifique].
>
> Je profite de l'occasion pour vous proposer [ressource] que j'ai créée récemment pour mes clients 😊
>
> Je vous l'envoie ?

## 1.5 Signal : le prospect a liké/commenté le post d'un CONCURRENT (PM-S-CCL)

### PM-S-CCL-CHA — conversationnel · chaleureux
**Quand :** interaction sur post concurrent, approche par la curiosité.
> Hello !!
>
> Tu t'y connais en [ton domaine] [prénom] ?
>
> J'ai vu passer ton commentaire sous un post de [créateur], c'est pour ça que je te demande 😁

### PM-S-CCL-EMP — conversationnel · empathique
**Quand :** interaction sur post concurrent, on demande sincèrement son avis.
> Salut [prénom] 😊
>
> Je prends rarement le temps d'envoyer des messages comme ça, mais là je suis tombé sur un post qui m'a énormément plu… et j'ai vu que t'étais dans les gens qui avaient réagi.
>
> J'me suis dit que ce serait intéressant d'avoir ton point de vue. Bon, tu te rappelles peut-être pas du post mais c'était celui de [créateur] sur [sujet].
>
> Tu as apprécié quoi exactement ? J'essaie de rester au plus proche du terrain.

### PM-S-CCL-HUM — conversationnel · humoristique
**Quand :** interaction sur post concurrent, on désamorce le côté "stalker".
> Hello [prénom],
>
> J'allais te dire "j'ai vu que tu as liké le post de [prénom] au sujet de [sujet du post]" et puis je me suis ravisé en me disant que cette approche était détestable 😂
>
> Mais je voulais quand-même savoir ce que tu as apprécié dans ce post, parce qu'étant dans le même domaine ça m'aide aussi à créer du contenu aligné avec le besoin des gens.

### PM-S-CCL-PRO — conversationnel · provocateur
**Quand :** interaction sur post concurrent, prospect affirmé.
> Yo [prénom],
>
> Jsuis pas du genre à écrire aux gens juste parce qu'ils ont posé un like…
>
> Mais là, j'ai vu ton nom sous un post qui faisait un peu le buzz dans notre petit monde et j'me suis demandé si t'avais liké pour faire ta routine LinkedIn… ou parce que ça t'a vraiment parlé 😏
>
> Ça m'intéressait de savoir ce qui t'a fait lever un sourcil ?

### PM-S-CCL-SER — conversationnel · sérieux
**Quand :** interaction sur post concurrent, registre formel.
> Bonjour [prénom],
>
> Je suis tombé sur le post de [membre] et j'ai vu passer ton nom dans les likes.
>
> [domaine] est un sujet pour toi en ce moment ?

### PM-S-CCL-DIR — direct · proposition de ressource
**Quand :** interaction sur post concurrent ET ressource sur le même sujet.
> Bonjour [prénom],
>
> Un vieux proverbe disait : "celui qui goûte, mérite une seconde part".
>
> Et comme vous avez goûté à [domaine] grâce au post de [créateur], j'aimerais vous offrir [ressource gratuite].
>
> Cette seconde part vous tente ? 😊

## 1.6 Signal : le prospect participe à l'événement d'un concurrent (PM-S-CEV)

### PM-S-CEV-CHA — conversationnel · chaleureux
**Quand :** inscription à un événement concurrent détectée.
> Coucou [prénom] 👋
>
> Quand je m'inscris à un événement, je fais rarement les choses à moitié : j'adore m'impliquer avant même qu'il ne démarre !
>
> Et comme j'ai vu ton inscription à celui de [créateur] sur [sujet], je me suis dit "allez, contacte [prénom]" 😊
>
> Tu as pour projet d'approfondir tes connaissances en [domaine] ?

### PM-S-CEV-EMP — conversationnel · empathique
**Quand :** on participe au MÊME événement que le prospect.
> Hello [prénom],
>
> Tu t'y connais en [domaine] ?
>
> Parce qu'on participe au même événement sur [thématique] et j'aime bien échanger sur le sujet avec des gens qui ont envie d'en apprendre plus, vu que c'est ma zone de génie 😉

### PM-S-CEV-HUM — conversationnel · humoristique
**Quand :** inscription événement concurrent, prospect décontracté.
> Yo [prénom] !
>
> J'allais te dire "j'ai vu que tu assistes à l'événement de [créateur]" mais je me suis rappelé qu'on est beaucoup trop nombreux à s'inscrire à des lives auxquels on n'ira jamais 😂
>
> Du coup je me demandais : si j'en organisais un sur [domaine] aussi, qu'est-ce qui te ferait venir sans hésiter ?

### PM-S-CEV-PRO — conversationnel · provocateur
**Quand :** inscription événement concurrent, ton taquin assumé.
> Hello !
>
> J'ai vu ton nom dans les participants à l'événement de [créateur] sur [sujet].
>
> J'me suis dit : "tiens, si [prénom] a le courage de se pointer à des événements LinkedIn en pleine semaine, c'est que [domaine] doit vraiment être bloquant de son côté" 😂
>
> Bref, tu en es où en ce moment sur [thématique] ?

### PM-S-CEV-SER — conversationnel · sérieux
**Quand :** inscription événement concurrent, registre formel.
> Bonjour [prénom],
>
> Mon tout premier réflexe quand je participe à un événement sur LinkedIn est de regarder qui y participe.
>
> Comme vous êtes dans la liste des participants de celui de [créateur] sur [sujet], je me demandais si vous aviez des difficultés en particulier dans [domaine].
>
> Vous m'en dites plus ?

### PM-S-CEV-DIR — direct · proposition de ressource
**Quand :** inscription événement concurrent ET ressource complémentaire au sujet de l'événement.
> Bonjour [prénom],
>
> Vous voir inscrit à [nom de l'événement] m'a donné envie de sortir de ma bulle et de connecter avec des personnes qui s'intéressent aux mêmes sujets que moi (ça devient rare).
>
> Si vous voulez prolonger la réflexion, j'ai préparé [ressource offerte] pour un client que je voulais partager autour de moi et qui complétera bien le contenu de cet événement.
>
> Je vous l'envoie ?

---

# SECTION 2 — PREMIER MESSAGE SANS SIGNAL / COLD (PM-F)

> Condition d'entrée : aucun signal d'intérêt détecté (pur outbound).

## 2.0 Table de sélection des tactiques froides

| ID | Tactique | Prérequis | Idéal quand |
|---|---|---|---|
| PM-F-01/02 | Pain killer | Ressource gratuite + douleur typique du persona | La douleur est quasi certaine pour ce poste |
| PM-F-03 | Effet IKEA | Une méthode/outil en cours de développement | On veut flatter l'expertise du prospect |
| PM-F-04 | Biais d'autorité | Un cas client réel et chiffrable | Le prospect ressemble au client cité |
| PM-F-05/06 | FOMO | Doc sur la stratégie d'un concurrent du prospect | Secteur concurrentiel, prospect compétitif |
| PM-F-07 | Quick-tip | Un tip actionnable immédiat | On peut donner de la valeur en 1 phrase |
| PM-F-08 | Out of the box | Aucun | Inbox du prospect probablement saturée |
| PM-F-09 | Question ouverte | Une actualité réelle du secteur | Secteur en mouvement (réglementation, IA…) |
| PM-F-10 | Approche inversée | Aucun | Métier du prospect peu commun, vraie curiosité possible |
| PM-F-11 | Question intriguante | Aucun | Découverte de douleur sans rien offrir |
| PM-F-12/13 | Approche humaine (vidéo/vocal) | Capacité d'envoyer vidéo Loom/vocal | Prospect à forte valeur, on veut se démarquer |
| PM-F-14 | Test offert | Une solution testable gratuitement | Produit/service démontrable |
| PM-F-15 | Recherche d'interlocuteur | Aucun | Entreprise >5 personnes, décideur incertain |
| PM-F-16 | Le constat | Une statistique réelle citée quelque part | Donnée frappante disponible sur le secteur |
| PM-F-17 | Pain-oriented question | Aucun | Variante directe de découverte de douleur |
| PM-F-18 | L'enquête | Avoir vraiment échangé avec des pairs | Effet "vos pairs ont le même problème" |
| PM-F-19 | Humoristique | Prospect décontracté | Profil casual, on assume le fun |
| PM-F-20/21 | Mensonge bienveillant | Crédibilité du prétexte | En dernier recours, prétexte plausible |

### PM-F-01 — Le pain killer (v1)
**Prérequis :** ressource gratuite + douleur typique du poste.
> Hello [prénom],
>
> En tant que [poste], tu fais certainement partie de ceux qui [douleur], dis-moi si je me trompe.
>
> J'ai créé [ressource gratuite] qui te permet de [bénéfice].
>
> Je te l'envoie ?

### PM-F-02 — Le pain killer (v2, preuve sociale)
**Prérequis :** idem v1, avec angle "tes pairs me l'ont dit".
> Hello [prénom],
>
> Plusieurs [poste] comme toi m'ont remonté avoir du mal à [douleur].
>
> Dans le feu de l'action j'ai créé [ressource gratuite] pour [bénéfice].
>
> Ça te dirait d'y avoir accès ?

### PM-F-03 — L'effet IKEA
**Prérequis :** méthode/solution/outil dont on peut demander un avis.
> Bonjour [prénom],
>
> J'ai travaillé sur une méthode/solution/outil pour les [poste] comme vous.
>
> J'aurais besoin de votre avis d'expert du domaine, vous seriez partant pour me faire des retours ?

### PM-F-04 — Le biais d'autorité
**Prérequis :** cas client réel, chiffrable, similaire au prospect.
> Salut [prénom]
>
> J'ai récemment travaillé avec [client] qui avait [douleur] et qui a réussi à [bénéfice] en [durée] grâce à [solution].
>
> Tu veux que je te partage la méthode ?

### PM-F-05 — Le FOMO (v1, stratégie documentée)
**Prérequis :** doc/PDF sur la stratégie d'un concurrent du prospect.
> Bonjour [prénom],
>
> J'ai récemment documenté la stratégie de [domaine] de [concurrent] et je me suis dit que ça pouvait vous intéresser.
>
> Je vous envoie le PDF ?

### PM-F-06 — Le FOMO (v2, deux concurrents)
**Prérequis :** ressource citant deux concurrents du prospect.
> Bonjour [prénom],
>
> J'ai créé [ressource] qui explique comment [concurrent 1] et [concurrent 2] font pour [bénéfice].
>
> Je me suis dit que c'était l'occasion de vous le partager.
>
> Ça vous dit ?

### PM-F-07 — Le quick-tip
**Prérequis :** un conseil actionnable en une phrase pour ce poste.
> Hello [prénom],
>
> Petit tip rapide parce que je vois que tu es [poste] : [tip].
>
> PS : ça fonctionne super bien !

### PM-F-08 — Le message out of the box
**Prérequis :** aucun. Anti-prospection assumée.
> [prénom] tu as sûrement 15 messages de prospection pompeux dans ton inbox donc je vais t'en éviter un 16ème 😅
>
> Je voulais simplement échanger avec toi sur [problème], tu gères ça comment ?

### PM-F-09 — La question ouverte
**Prérequis :** actualité réelle et vérifiable du secteur du prospect.
> Bonjour [prénom],
>
> J'ai remarqué que [sujet] devient un sujet chaud dans le [secteur] en ce moment.
>
> Comment ça impacte votre activité ?

### PM-F-10 — L'approche inversée
**Prérequis :** curiosité crédible pour le métier du prospect.
> Bonjour [prénom],
>
> Je me demandais en quoi consistait ton métier de [poste] ?
>
> Enfin je connais le métier, mais dans les grandes lignes, qu'est-ce que tu fais au quotidien ?

### PM-F-11 — La question intriguante
**Prérequis :** aucun. Découverte de douleur par le temps perdu.
> Salut [prénom],
>
> Je voulais te poser une question comme tu es [poste].
>
> Qu'est-ce qui te prend le plus de temps aujourd'hui sur [domaine] ?
>
> Ça m'intéresserait de savoir comment tu fonctionnes.

### PM-F-12 — L'approche humaine (vidéo)
**Prérequis :** vidéo Loom/Tella/selfie de 3 min max enregistrée pour ce prospect.
> Salut [prénom],
>
> Pour éviter de t'envoyer un méga pavé (que tu n'auras pas envie de lire), je t'ai préparé une courte vidéo pour t'expliquer pourquoi je te contacte : [lien d'une vidéo de 3min max]

### PM-F-13 — L'approche humaine (vocal)
**Prérequis :** possibilité d'envoyer un message vocal LinkedIn.
> Hello [prénom],
>
> Je te fais un vocal pour t'expliquer pourquoi je te contacte :)

### PM-F-14 — Le test offert
**Prérequis :** solution testable gratuitement.
> Bonjour [prénom],
>
> Je cherche des [poste] dans le [secteur] pour tester gratuitement [solution].
>
> Ça vous intéresserait ?

### PM-F-15 — La recherche d'interlocuteur
**Prérequis :** entreprise où le décideur est incertain.
> Bonjour [prénom],
>
> Je cherche à contacter la personne en charge de [sujet spécifique], c'est bien vous ?

### PM-F-16 — Le constat
**Prérequis :** statistique réelle issue d'un post/article.
> Bonjour [prénom],
>
> J'ai récemment lu un [post/article/…] qui disait que [X%] des [cible] rencontre [problème].
>
> Comme le sujet m'intéresse, je mène ma propre enquête.
>
> Est-ce que ton entreprise en fait partie ?

### PM-F-17 — La « pain-oriented question »
**Prérequis :** aucun.
> Hello [prénom],
>
> J'ai l'habitude de poser cette question aux [poste] :
>
> Quelle est ta plus grande difficulté concernant [domaine] ?
>
> Ça m'intéresserait de savoir ce qui te bloque.

### PM-F-18 — L'enquête
**Prérequis :** avoir réellement échangé avec plusieurs pairs du prospect.
> Bonjour [prénom],
>
> J'ai échangé avec une dizaine de [poste] ces dernières semaines qui m'ont tous remonté avoir du mal à gérer [problème].
>
> Est-ce aussi votre cas ?

### PM-F-19 — Le message humoristique
**Prérequis :** prospect décontracté.
> Hellooo,
>
> Ça fait 3x que LinkedIn me recommande ton profil, bon j'ai hésité mais cette fois-ci c'est la bonne : j'ai décidé de m'abonner 😂
>
> J'en profite pour te demander, c'est quoi ta plus grande difficulté en [ton domaine] ?

### PM-F-20 — Le mensonge bienveillant (v1, algorithme)
**Prérequis :** prétexte plausible. À utiliser avec parcimonie.
> Bonjour [Prénom],
>
> Ça fait plusieurs fois que LinkedIn me recommande votre profil, j'ai fini par m'abonner !
> Vous avez déjà croisé le mien ou l'algorithme n'est allé que dans un sens ? 😅

### PM-F-21 — Le mensonge bienveillant (v2, proximité géographique)
**Prérequis :** le siège du prospect est plausiblement sur ton trajet.
> Bonjour [prénom],
>
> Je suis passé devant votre siège ce matin et je voulais vous contacter avant d'oublier.
>
> Qu'est-ce qui vous prend le plus de temps sur [domaine] ?
>
> Je serais curieux de savoir comment vous fonctionnez.

---

# SECTION 3 — RELANCES (RL)

## 3.1 Le prospect ne m'a ENCORE JAMAIS répondu (RL-N)

> Stratégie : relances 1-2 = apporter de la valeur (RL-N-01 à 08). Relance 3 = douce ou directe (RL-N-09 à 16). Dernière = porte de sortie (RL-N-17 à 19). Ne jamais répéter deux fois la même tactique.

### RL-N-01 — La ressource supplémentaire
**Quand :** on a trouvé un contenu tiers utile au prospect.
> Je suis tombé sur [article/ressource] qui pourrait t'aider sur [problème]. Je te mets le lien juste ici : [lien]

### RL-N-02 — L'actualité du secteur
**Quand :** une actualité du secteur permet de relancer naturellement.
> J'ai vu que [actualité du secteur]. Comment ça impacte ton activité ?

### RL-N-03 — La relance FOMO
**Quand :** on a documenté la stratégie d'un concurrent du prospect.
> D'ailleurs j'ai récemment documenté la stratégie de [concurrent] qui lui a permis de [bénéfice/résultat].
>
> Ça vous intéresserait d'y avoir accès ?

### RL-N-04 — Le pied dans la porte
**Quand :** on a une ressource déjà envoyée à un client similaire.
> J'ai repensé à vous aujourd'hui en envoyant [ressource] à un client qui n'arrivait pas à [problématique].
>
> Je me suis dit que ça pourrait aussi vous aider au passage.
>
> Je vous l'envoie ?

### RL-N-05 — La relance immersive
**Quand :** on peut offrir un essai/extrait gratuit sans engagement.
> Je comprendrais que vous puissiez vous dire que c'est un énième message de prospection.
>
> Du coup je vous propose quelque chose : je vous offre [essai gratuit/extrait de prestation gratuite/etc…] pour que vous voyiez ce que ça donnerait de travailler avec moi, sans aucun engagement :)
>
> Dans [X] jours, vous avez le droit de tout plaquer et de me dire : désolé [ton prénom] mais après ce test je ne suis pas intéressé.
>
> Vous êtes partant ?

### RL-N-06 — L'invitation transversale
**Quand :** on organise un événement ou on a une newsletter.
> Pendant que j'y pense, ça vous dirait de vous inscrire à [événement/newsletter] ?
>
> Promis, aucun blabla vu et revu, que du concret 😊

### RL-N-07 — La ressource gratuite
**Quand :** on envoie directement la ressource sans demander la permission.
> J'en profite pour te transmettre [ressource gratuite] pour t'aider à faire face à [problématique] : [lien]
>
> Tu me diras ce que tu en as pensé 😊

### RL-N-08 — La relance vidéo
**Quand :** on peut montrer la résolution du problème en vidéo.
> Je me suis dit que ce serait plus parlant si je vous montrais en vidéo comment vous pouvez résoudre [problématique].
>
> La vidéo dure [X] minutes : [lien vers la vidéo]

### RL-N-09 — La relance douce (v1)
**Quand :** relance neutre sans pression, 3-5 jours après le message.
> Hello [prénom],
>
> Je voulais m'assurer que mon message n'était pas passé à la trappe :)

### RL-N-10 — La relance douce (v2)
**Quand :** variante de RL-N-09.
> Je fais remonter la conversation dans ta messagerie au cas où elle se serait noyée dans la masse :)

### RL-N-11 — La relance intéressée
**Quand :** on déplace le sujet vers l'activité du prospect.
> Tu peux peut-être m'en dire plus sur ton activité avant, ça m'intéresse de savoir comment tu fonctionnes ?

### RL-N-12 — L'information oubliée
**Quand :** on a réellement une info complémentaire à ajouter.
> J'ai oublié de te préciser que [information supplémentaire]

### RL-N-13 — La relance vocale
**Quand :** humaniser après un ou deux messages écrits sans réponse.
> *Message vocal :* [reformuler le message précédemment envoyé pour humaniser l'échange]

### RL-N-14 — La relance humoristique
**Quand :** prospect décontracté, après 2+ relances classiques.
> Je suis en train de me demander si tu n'as pas été kidnappé/e par des aliens 👽
>
> Si tu reviens sur Terre, fais-moi signe pour qu'on reprenne la conversation là où on l'a laissée !

### RL-N-15 — Le jeu interactif
**Quand :** dernier essai créatif avant de clore, prospect joueur.
> Bon, faisons un jeu et si vous avez la bonne réponse, je m'engage à ne plus vous relancer 😊
>
> [question difficile]
>
> A - [réponse A]
> B - [réponse B]
> C - [réponse C]
> D - [réponse D]

### RL-N-16 — La relance directe
**Quand :** lever l'ambiguïté franchement après plusieurs silences.
> Est-ce que je dois prendre ton silence pour un "pas le temps", pour un "non" ou "intéressé mais débordé" ?

### RL-N-17 — Le QCM ludique
**Quand :** version structurée de la relance directe, avant-dernière relance.
> Comment je dois interpréter ce silence ?
>
> A - Ce n'est pas le bon timing
> B - Vous êtes déjà équipé
> C - Vous n'êtes pas le bon interlocuteur
> D - Vous n'avez juste pas eu le temps de me répondre

### RL-N-18 — Le bon interlocuteur
**Quand :** on suspecte que le prospect n'est pas le décideur.
> Est-ce que je m'adresse à la bonne personne pour [sujet] ?
>
> Histoire que je ne vous dérange pas plus longtemps si ce n'est pas le cas 🙂

### RL-N-19 — La relance compréhensive
**Quand :** clore en laissant la porte ouverte côté prospect.
> Tiens-moi au courant quand tu auras plus de temps !

### RL-N-20 — La porte de sortie
**Quand :** dernière relance, on planifie un recontact futur.
> Je ne veux pas vous déranger plus longtemps.
>
> Il y a un moment où je peux vous recontacter dans les prochaines semaines/prochains mois et où vous aurez peut-être plus de temps ?

## 3.2 Le prospect m'a DÉJÀ répondu mais ne répond plus / ghosté (RL-G)

> Stratégie : privilégier l'empathie et le rebond sur des éléments que le prospect a déjà partagés. Les relances personnalisées (RL-G-05, RL-G-08) performent mieux que les génériques.

### RL-G-01 — Chaleureuse (v1)
> Hello [prénom],
>
> Je voulais m'assurer que mon message n'est pas passé à la trappe :)

### RL-G-02 — Chaleureuse (v2)
> Hello [prénom],
>
> Je fais remonter la conversation dans ta messagerie au cas où elle se serait noyée dans la masse 😊

### RL-G-03 — Chaleureuse (v3)
> J'ai repensé à nos messages [prénom] si tu es toujours dans les parages !

### RL-G-04 — Chaleureuse (v4, idée oubliée)
> Je viens d'avoir une idée que j'avais oublié de te donner, tu es toujours dans le coin ?

### RL-G-05 — Empathique · rebond personnel ⭐ priorité
**Quand :** le prospect avait mentionné un événement personnel/pro (déménagement, lancement…).
> Hello [prénom],
>
> Je viens aux nouvelles.
>
> [question concernant un élément dont le prospect t'avait parlé]
>
> *Ex : Comment s'est passé ton déménagement ?*

### RL-G-06 — Empathique · timing
> Bonjour [prénom],
>
> Je sais que certains messages peuvent passer entre deux urgences.
>
> Si c'est juste une question de timing, je peux tout à fait attendre un moment plus calme de votre côté 🙂

### RL-G-07 — Empathique · redirection interne
**Quand :** le prospect semble débordé, on cherche un autre interlocuteur.
> Je ne veux pas vous embêter plus longtemps si vous manquez de temps en ce moment 😊
>
> Est-ce qu'il y a une personne qui a votre confiance en interne et vers qui je peux me tourner ?

### RL-G-08 — Empathique · rappel de douleur ⭐ priorité
**Quand :** le prospect avait exprimé une douleur précise.
> Tu m'avais parlé de [douleur].
>
> Tu as avancé dessus depuis ou c'est toujours un sujet bloquant ?

### RL-G-09 — Humoristique
> Je sais pas si t'as été enlevé par des extraterrestres ou juste aspiré par un tunnel de to-dos… mais si t'es de retour sur Terre, je suis toujours là !

### RL-G-10 — Sérieuse · ressource trouvée
> Bonjour [prénom],
>
> J'ai repensé à vous ce matin en tombant sur [article/ressource].
>
> Je me suis dit que ça pourrait vous intéresser d'y jeter un coup d'œil : [lien de la ressource]

### RL-G-11 — Sérieuse · proposition toujours valable
**Quand :** une proposition concrète avait été faite.
> Ma proposition est encore d'actualité [prénom], toujours intéressé ?

### RL-G-12 — Sérieuse · signal détecté
**Quand :** le prospect ghosté vient d'interagir avec un post concurrent.
> J'ai vu ton commentaire sous le post de [concurrent], tu as avancé sur le sujet ou tu es toujours en réflexion ?

### RL-G-13 — Le rappel de valeur
**Quand :** une ressource avait été envoyée et est restée sans retour.
> Alors, tu as pu jeter un coup d'œil à [ressource] ?
>
> Je suis curieux d'avoir ton avis (sincère).

---

# SECTION 4 — RÉPONSES À UN PROSPECT (RP)

## 4.1 Le prospect n'est PAS réceptif (RP-NR)

> Détecter le cas EXACT avant de répondre. Objectif : désamorcer sans se justifier lourdement, puis relancer la conversation par une question.

### RP-NR-01 — Il a ressenti l'automatisation
**Détection :** "c'est un message automatique ?", "t'es un bot ?"
> Tu as raison, j'automatise l'envoi des premiers messages, à vrai dire c'est le seul moyen de contacter des profils pertinents sans bosser 20h par jour 😄
>
> Mais si je prends le temps de te répondre maintenant, c'est que je trouvais ça vraiment intéressant d'échanger avec toi.
>
> [reformuler la question précédente]

### RP-NR-02 — Il dit ne pas être intéressé
**Détection :** "pas intéressé", "non merci".
> J'aurai quand-même tenté le coup 😄
>
> Qu'est-ce qui fait que tu n'es pas intéressé ? Tu es déjà équipé en [ton domaine/activité] ou ce n'est juste pas une priorité pour toi ?

### RP-NR-03 — Il dit recevoir ce genre de messages tous les jours
**Détection :** "j'en reçois 10 par jour", "encore un message de prospection".
> Je comprends et je vois qu'on a la même boîte de réception 😅
>
> Beaucoup envoient des messages copier-coller en masse sans s'intéresser et j'essaie de faire mon max pour ne pas y ressembler.
>
> [reformuler la question précédente]

### RP-NR-04 — Il dit que tu n'as pas consulté son profil
**Détection :** "vous n'avez même pas regardé mon profil".
**⚠ Obligation :** aller VRAIMENT lire le profil avant de répondre, et citer un détail réel.
> Tu as totalement raison, j'avoue ne pas avoir regardé ton profil !
>
> Et j'aurais vraiment dû parce que je vois que [détail de son profil qui joue en ta faveur].
>
> Loin de moi l'envie de te spammer 😊
>
> [reformuler la question précédente]

### RP-NR-05 — Il dit ne pas vouloir acheter quoi que ce soit
**Détection :** "je ne veux rien acheter", "pas de démarchage".
> Tu fais bien de le préciser 😊
>
> En tout cas mon but n'était pas de te vendre quoi que ce soit à tout prix.
>
> J'avais surtout quelques questions pour voir si ça valait le coup d'aller plus loin, sans forcer les choses.
>
> T'es quand-même ok pour y répondre ?

### RP-NR-06 — Il répond avec un pouce en l'air
**Détection :** réaction 👍 seule, sans texte.
> Le fameux pouce en l'air 😅
>
> Est-ce que je dois l'interpréter comme un « dis-m'en plus » ou plutôt « merci mais non merci » ?

### RP-NR-07 — Il répond de manière passive-agressive
**Détection :** "il est où le piège ?", ironie, méfiance hostile.
> J'ai l'impression que mon message t'a un peu hérissé, ce n'était pas le but 😌
>
> Je te clarifie mon intention parce qu'on s'est peut-être mal compris : [reformuler le message précédent de façon plus précise]

## 4.2 Le prospect répond par une OBJECTION (RP-OBJ)

> Matcher l'objection exacte. Quand plusieurs variantes existent (a/b/c), choisir selon le ton de l'échange : (a) = plus offensif, (b/c) = plus doux.

### RP-OBJ-01 — "Je n'ai pas le budget"
**(a) Recadrage ROI :**
> Justement, ce que je propose aide souvent à en libérer. Si je te montre comment rentabiliser l'investissement dès le premier mois, ça t'irait ?

**(b) Adaptation :**
> Je peux m'adapter. L'idée, c'est qu'on construise quelque chose d'accessible et rentable pour toi.
>
> Quel est ton budget actuel ?

### RP-OBJ-02 — "Je suis déjà accompagné"
**(a) Sonder la satisfaction :**
> Ok, et vous êtes satisfait à 100 % ou il y a encore des axes d'amélioration ?

**(b) Second souffle :**
> Top, c'est souvent dans ce cas-là qu'on peut apporter un second souffle ou challenger ce qui existe. Qu'est-ce qui manque à ta solution/ton prestataire actuel pour que tu sois complètement satisfait ?

### RP-OBJ-03 — "Je ne suis pas le bon interlocuteur"
**(a) Demande de redirection :**
> Merci pour ta réponse ! Tu saurais vers qui je devrais me tourner alors ?
> Et si tu veux, je te mets en copie pour que ce soit fluide.

**(b) Mise en relation :**
> Merci pour l'honnêteté. Tu serais ok pour me glisser le nom de la bonne personne ou carrément me mettre en relation ?
> Je ferai simple et rapide.

### RP-OBJ-04 — "Je suis débordé / pas le temps"
**(a) Report planifié :**
> Tu veux que je te recontacte dans 2-3 semaines ? Je bloque une relance si ça te va :)

**(b) Résumé asynchrone :**
> Je comprends !
>
> Si je t'envoie un résumé ultra clair de ce que je peux t'apporter, tu prends 2 minutes pour le lire à tête reposée ?

**(c) Format court :**
> Je comprends. Je peux te proposer un format ultra rapide : 15 minutes, tu vois si ça vaut le coup ou non. Ça t'irait ?

### RP-OBJ-05 — "Ce n'est pas une priorité"
**(a) Report :**
> Pas de soucis, merci pour ta transparence.
>
> On en reparle dans quelques semaines pour faire le point ?

**(b) Découverte de la vraie priorité :**
> Merci pour ta transparence.
>
> Par curiosité, quelle est la priorité du moment ?

### RP-OBJ-06 — "Je suis en vacances"
**(a) Point au retour :**
> Je note, bonnes vacances alors !
>
> Tu veux qu'on cale un point à ton retour ? Promis, ce sera rapide et utile.

**(b) Date de relance :**
> Parfait, profite bien 😀
>
> Je peux te relancer à quelle date sans te déranger ?

**(c) Brief asynchrone :**
> Bonnes vacances alors !
>
> Je t'envoie un petit brief par écrit pendant ce temps, tu regarderas quand tu veux.

### RP-OBJ-07 — "On gère ça en interne"
**(a) Booster l'équipe :**
> Je ne cherche pas à remplacer ton équipe, mais à les booster.
>
> Tu serais ouvert à voir comment je peux les faire gagner en efficacité ?

**(b) Challenger le plein potentiel :**
> Tu penses qu'ils sont à leur plein potentiel ? Ou il y a encore un peu de marge ?

### RP-OBJ-08 — "Envoyez-moi un mail / une plaquette"
**(a) Recadrage appel :**
> Ok, mais en toute transparence, ce qu'on fait se comprend mieux en 10 minutes d'appel qu'en 10 pages. Tu préfères quoi ?

**(b) Engagement de lecture :**
> Pas de soucis !
>
> Quand pensez-vous consulter mon mail/ma plaquette une fois que je vous l'aurai envoyée ?
>
> Pour que je sache à peu près quand revenir vers vous.

### RP-OBJ-09 — "Je vais voir avec mon associé(e)"
**(a) Réunion à trois :**
> Top, tu veux qu'on cale un créneau ensemble avec lui directement ?
>
> Comme ça on gagne du temps et on évite de jouer au téléphone arabe 😅

**(b) Anticiper les blocages :**
> Ok, tu penses qu'il aura quoi comme point de blocage potentiel ?
>
> Qu'on l'anticipe.

**(c) Résumé à transmettre :**
> Tu veux que je te laisse un petit résumé détaillé à lui transmettre ?

### RP-OBJ-10 — "Je suis déjà full niveau clients"
**(a) Monter en gamme :**
> Super, bravo pour ça !
>
> Ça te dirait de passer à l'étape « on choisit les clients avec qui on a envie de travailler » ?

**(b) Anticiper le retournement :**
> Bonne nouvelle alors ! Mais tu sais comme moi que ça peut vite tourner. Tu veux qu'on anticipe ensemble pour rester full sur le long terme ?

### RP-OBJ-11 — "Je garde ton contact au cas où"
> Ça marche !
>
> Et justement dans quels cas tu serais amené à me recontacter/à avoir besoin de moi ?

### RP-OBJ-12 — "Je réfléchis et je reviens vers toi"
**(a) Cadrer la relance :**
> Parfait, je te laisse cogiter.
>
> Tu veux que je te relance dans quelques jours ou tu préfères revenir vers moi quand tu es prêt ?

**(b) Récap d'aide à la décision :**
> Ça marche. Tu veux que je t'envoie un petit récap pour t'aider dans la réflexion ou t'as tout ce qu'il te faut pour décider sereinement ?

**(c) Identifier le point bloquant :**
> Je te laisse digérer ça tranquillement. Mais juste pour t'aider : c'est quoi selon toi le point principal à éclaircir avant de décider ?
>
> Je peux peut-être t'y aider.

## 4.3 Le prospect est réceptif mais PAS ENCORE QUALIFIÉ (RP-Q)

> Poser 1 question à la fois. Ordre recommandé : BESOIN → URGENCE → ALTERNATIVES → BUDGET/DÉCISION → PROJECTION. Un prospect est "qualifié" quand : douleur identifiée + urgence confirmée + décideur identifié.

### RP-Q-BES — Questions orientées BESOIN (en choisir une)
> Aujourd'hui, comment est-ce que tu gères ton/ta [activité précise : ex. prospection, création de contenu, suivi client] ?

> Qu'est-ce que tu trouves le plus compliqué dans ta gestion de [activité/domaine] ?

> Si tu pouvais améliorer un seul point dans [activité/domaine], ce serait lequel ?

> Quelle est ta plus grande difficulté actuelle concernant [activité/domaine] ?

> Aujourd'hui, qu'est-ce qui te prend le plus de temps et d'énergie concernant [domaine/activité] ?

> Qu'est-ce qui t'empêche d'avoir les résultats que tu voudrais concernant [domaine/activité] ?

> Qu'est-ce qui t'empêche de dormir la nuit concernant [domaine/activité] ?

> Qu'est-ce qui manque selon toi aujourd'hui pour que ton/ta [domaine/activité] tourne parfaitement ?

### RP-Q-URG — Questions orientées URGENCE (en choisir une)
> Cette problématique autour de [domaine/activité], c'est quelque chose que tu envisages de résoudre bientôt ?

> À quel point c'est urgent pour toi de résoudre [activité/domaine] ?

> Combien de temps tu penses pouvoir tenir sans améliorer [domaine/activité] ?

### RP-Q-BUD — Questions orientées BUDGET et DÉCISION (en choisir une)
> C'est bien vous qui gérez [domaine/activité] en interne ?

> Est-ce que d'autres personnes sont en charge de [domaine/activité] avec toi ?

> Quels critères sont les plus importants pour toi si tu décidais d'investir dans une solution à cette problématique ?

### RP-Q-ALT — Questions orientées ALTERNATIVES (en choisir une)
> Est-ce que tu utilises déjà une solution/un outil pour [domaine/activité] ?

> Qu'est-ce que tu as déjà essayé pour résoudre cette problématique ?

> Est-ce que [solution alternative] t'a apporté les résultats que tu attendais ?

> Pourquoi [solution alternative] ne t'a pas rapporté les résultats que tu attendais ?

> Qu'est-ce que [solution alternative] ne t'a pas apporté et que tu aurais aimé ?

> Qu'est-ce qui t'a poussé à utiliser [solution alternative] plutôt qu'une autre pour [activité/domaine] ?

> Es-tu prêt/e à changer la façon dont tu gères [activité/domaine] ?

> Quels seraient les critères les plus importants si tu choisissais une solution pour [domaine/activité] ?

### RP-Q-PRJ — Questions orientées PROJECTION et BÉNÉFICES (en choisir une)
> Qu'est-ce que tu gagnerais à résoudre ce problème ?

> Si on pouvait définitivement résoudre ce problème, qu'est-ce que ça changerait pour toi et pour ton business ?

> Quels résultats te rendraient complètement satisfait/e de ta gestion de [domaine/activité] ?

## 4.4 Le prospect est QUALIFIÉ → offrir une ressource (RP-RES)

> Condition : douleur + urgence confirmées. Objectif : donner de la valeur avant de demander un RDV.

### RP-RES-01 — Ressource créée pour un client similaire
> Je viens de créer [ressource gratuite] pour un client qui [problématique].
>
> Tu serais intéressé d'y avoir accès ?

### RP-RES-02 — Ressource qui débloque
> J'ai créé [ressource gratuite] qui débloque pas mal de monde sur [thématique].
>
> Je te l'envoie ?

### RP-RES-03 — Ressource empathique
> Je sais ce que c'est de galérer sur [thématique], alors j'ai tout synthétisé dans une ressource gratuite.
>
> Tu es partant pour y avoir accès ?

## 4.5 Le prospect a APPRÉCIÉ la ressource → proposer un call (RP-CALL)

> Condition : retour positif sur la ressource envoyée. Objectif : convertir en RDV.

### RP-CALL-01 — Démonstration
> Si ça te tente, je peux te montrer cette semaine comment je [bénéfice]. Ça te dit ?

### RP-CALL-02 — Gain de temps
> Pour t'éviter 3 mois de questionnements, on se fait un call cette semaine ?

### RP-CALL-03 — Méthode personnalisée
> J'ai une idée de méthode à appliquer dans ton cas mais pour éviter de t'envoyer des pavés interminables, ce sera plus simple si je t'explique en visio.
>
> Tu as de la dispo cette semaine ?

### RP-CALL-04 — Micro-engagement 15 min
> Il y a souvent 2-3 petits ajustements qui débloquent tout. On peut voir ça sur un appel de 15 minutes si tu es partant ?

## 4.6 Le prospect a DIT OUI pour un RDV (RP-RDV)

### RP-RDV-01 — Lien agenda
> Super ! Je te laisse prendre un créneau dans mon agenda : [lien de ton agenda]

### RP-RDV-02 — Deux créneaux proposés (tu)
> Je peux te proposer [date 1] à [horaire 1] si ça te va ?
>
> Si ce n'est pas le cas je suis aussi disponible [date 2] à [horaire 2].
>
> Dis-moi et je t'envoie une invitation 🙂

### RP-RDV-03 — Deux créneaux proposés (vous)
> Vous seriez disponible le [date 1] à [horaire 1] ou le [date 2] à [horaire 2] ?

---

# 5. RÈGLES D'OR TRANSVERSES (anti-erreurs)

1. **Jamais de crochet non rempli** — si une variable ne peut pas être remplie avec une info réelle, choisir un autre template.
2. **Jamais deux fois la même tactique** sur le même prospect (tracker les IDs utilisés par prospect).
3. **Un seul CTA par message** — jamais deux questions ou deux propositions.
4. **Personnaliser avant d'envoyer** — chaque template est un squelette : adapter le vocabulaire au secteur du prospect.
5. **Le ton se calque sur le prospect** — s'il est formel, rester sérieux ; s'il met des emojis, on peut en mettre.
6. **Ne pas vendre avant de qualifier** — la séquence est : signal/accroche → conversation → qualification (RP-Q) → ressource (RP-RES) → call (RP-CALL) → RDV (RP-RDV). Ne jamais sauter plus d'une étape.
7. **Une objection traitée = une question relancée** — chaque réponse à objection se termine par une question ouverte.
8. **Prétextes véridiques uniquement** — PM-F-16 (statistique), PM-F-18 (enquête), RL-N-12 (info oubliée) exigent des faits réels. Les "mensonges bienveillants" (PM-F-20/21) restent un dernier recours.
