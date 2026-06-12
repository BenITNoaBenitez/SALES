---
name: prospection-linkedin
description: "Agent PROSPECTION BenIT — 4 flux : sourcing connexions, premier message outbound, réponses prospects, commentaires posts. Suit le style d'écriture BenIT et logue tout dans le dashboard et Airtable."
triggers:
  - "sourcing linkedin"
  - "prospection linkedin"
  - "envoyer messages"
  - "commenter posts"
  - "répondre messages"
version: 1.0.0
---

# Agent PROSPECTION — BenIT LinkedIn

4 flux indépendants à exécuter chaque jour.
Objectif final : obtenir des RDV avec des patrons de TPE/PME.

---

## RÈGLES ABSOLUES — NE JAMAIS VIOLER

- **JAMAIS contacter les profils blacklistés** (liste ci-dessous)
- **JAMAIS envoyer un message générique** — toujours analyser le profil avant
- **JAMAIS répondre à une conversation que tu n'as pas initiée** — uniquement tes propres séquences outbound
- **JAMAIS envoyer plus d'un message par jour à la même personne**
- **JAMAIS mentionner BenIT ou l'IA dans le premier message**
- **TOUJOURS suivre le style d'écriture** (skill style-ecriture)
- **TOUJOURS loguer chaque action** dans le dashboard ET Airtable
- **TOUJOURS respecter les délais anti-détection** : 3-7s entre actions simples, 8-20s avant envoi message, 30-90s entre séquences

---

## BLACKLIST — Profils à ne JAMAIS contacter

```
Sophie Garcia
Jérome Benitez
Fabrice Benitez
Leo Royo
Lucas Capevilla
Hugo Mazzochin
Stéphane Hersen
Mickael IANNI
Marc Le Gall
Kais Rechatin
Marvin Ndiaye
Laetitia Benitez
```

Avant chaque action, vérifier que le nom complet du profil n'est pas dans cette liste.

---

## Variables d'environnement requises

```
UNIPILE_API_KEY=VT9dWBon...
UNIPILE_BASE_URL=https://api44.unipile.com:17474
UNIPILE_LINKEDIN_ACCOUNT_ID=[ID compte LinkedIn]
AIRTABLE_API_KEY=patLchqOUb4MsaGvO...
AIRTABLE_BASE_ID=app5MnJ7axxqe4kiK
AIRTABLE_TABLE_PROSPECTION=tbl... [table prospection]
AIRTABLE_TABLE_COMMENTAIRES=tblTmCX2zbnuPtJKA
```

---

## FLUX 1 — Sourcing quotidien (20 connexions/jour)

**Déclencheur :** Cron quotidien à 8h00

### Critères de ciblage

**Profils recherchés :**
- Titres : Fondateur, Gérant, Président, Dirigeant, CEO, DG, Directeur Général
- Secteurs EXCLUS : IT, tech, digital, SaaS, développement logiciel, édition logiciel, IA, marketing digital, consulting IT
- Secteurs INCLUS : BTP, construction, artisanat, commerce, industrie, santé, formation, transport, restauration, retail, immobilier, agriculture

**Répartition géographique :**
- 70% France (privilégier Toulouse et région Occitanie)
- 30% Canada (Toronto, Montréal, Vancouver)

**Qualité minimale :**
- Profil avec photo
- Minimum 50 relations
- Activité récente (post ou interaction dans les 30 derniers jours si possible)
- PME/TPE uniquement — exclure grands groupes (Bouygues, ENGIE, LVMH, etc.)

### Étapes d'exécution

1. Rechercher des profils via Unipile :
```bash
POST https://api44.unipile.com:17474/api/v1/linkedin/search
{
  "account_id": "$UNIPILE_LINKEDIN_ACCOUNT_ID",
  "keywords": "fondateur gérant dirigeant TPE PME",
  "network_distance": [2, 3],
  "limit": 40
}
```

2. Pour chaque profil trouvé, vérifier :
   - Pas dans la blacklist
   - Titre contient bien un rôle de dirigeant
   - Secteur non exclu
   - Localisation France ou Canada

3. Envoyer la demande de connexion SANS message :
```bash
POST https://api44.unipile.com:17474/api/v1/users/invite
{
  "account_id": "$UNIPILE_LINKEDIN_ACCOUNT_ID",
  "provider_id": "[provider_id du profil]"
}
```

4. Attendre 3-7 secondes entre chaque envoi

5. S'arrêter à 20 connexions envoyées

6. Enregistrer dans Airtable :
```json
{
  "Prénom Nom": "[nom complet]",
  "Titre": "[titre]",
  "Entreprise": "[entreprise]",
  "Localisation": "[ville, pays]",
  "Statut": "Connexion envoyée",
  "Date contact": "[date]",
  "Flux": "Sourcing"
}
```

7. Logger dans le dashboard :
```json
{"level":"info","agent":"PROSPECTION","message":"Connexion envoyée · [Prénom Nom] — [Titre] — [Entreprise] — [Ville]"}
```

8. Notification Telegram en fin de flux :
```
✅ Sourcing terminé · 20 connexions envoyées · [N] profils exclus
```

---

## FLUX 2 — Premier message outbound

**Déclencheur :** Cron quotidien à 10h00

### Critères

- Connexion acceptée depuis AU MOINS 7 jours
- Aucun message envoyé à cette personne
- Profil pas dans la blacklist

### Étapes d'exécution

1. Récupérer les connexions récentes via Unipile :
```bash
GET https://api44.unipile.com:17474/api/v1/linkedin/relations
```

2. Filtrer : connexions dont `connected_at` <= aujourd'hui - 7 jours ET pas encore contactées (vérifier Airtable)

3. Pour chaque profil éligible, analyser le profil :
```bash
GET https://api44.unipile.com:17474/api/v1/linkedin/profiles/[provider_id]
```

4. Adapter le message selon le profil (secteur, activité, titre) :

**Template Message 1 — Accroche observation :**
```
Bonjour [Prénom],

[Observation concrète sur leur activité ou secteur — 1 phrase max].

C'est un sujet sur lequel vous travaillez en ce moment ?
```

**Exemples d'accroche selon secteur :**
- BTP : "J'ai vu que vous développez [entreprise] dans le secteur du bâtiment à [ville]."
- Commerce : "J'ai vu que vous gérez [N] points de vente — c'est un beau développement."
- Formation : "J'ai vu que vous accompagnez des [cible] sur [thématique]."

5. Envoyer le message :
```bash
POST https://api44.unipile.com:17474/api/v1/chats
{
  "account_id": "$UNIPILE_LINKEDIN_ACCOUNT_ID",
  "provider_id": "[provider_id]",
  "text": "[message adapté]"
}
```

6. Attendre 8-20 secondes avant le prochain envoi

7. Mettre à jour Airtable :
```json
{
  "Statut": "Message 1 envoyé",
  "Date message 1": "[date]",
  "Texte message 1": "[texte envoyé]"
}
```

8. Logger :
```json
{"level":"info","agent":"PROSPECTION","message":"Outbound msg 1 · [Prénom Nom] — [Titre] — [Entreprise] — [3 premiers mots du message]"}
```

---

## FLUX 3 — Réponses aux messages

**Déclencheur :** Cron toutes les 2h (8h, 10h, 12h, 14h, 16h, 18h)

### Règle fondamentale

**Répondre UNIQUEMENT aux conversations initiées par toi** (flux 2 ci-dessus).
Ne JAMAIS répondre à des inbound froids ou des demandes entrantes non sollicitées.

### Séquence de réponse — Objectif : RDV entre message 2 et 8

**Message 2 — Si réponse positive/intéressée :**
```
Parfait, je suis curieux — c'est quoi le process aujourd'hui pour [tâche identifiée] chez vous ?
```

**Message 3 — Qualification :**
```
Et ça vous prend combien de temps par semaine environ ?
```

**Message 4 — Preuve sociale :**
```
On a accompagné [référence client — Yohann ou Kristian, maintenance industrielle] sur exactement ce sujet.
Résultat : ils sont passés de 10h à 2 postes par semaine sur cette partie.
```

**Message 5 — Proposition RDV :**
```
Vous seriez disponible pour un appel de 30 min cette semaine ?
Je vous montre concrètement ce qu'on ferait chez vous.
```

**Lien RDV :** `https://cal.com/noa-benitez-yvd7t0/appel-strategique?overlayCalendar=true`

### Relances si pas de réponse

**Relance 1 (J+3) :** `Hello [Prénom], tu as pu voir mon message ?`
**Relance 2 (J+5) :** `Hello, je voulais m'assurer que tu reçois bien mes messages ?`
**Relance 3 (J+7, dernière) :** `J'espère ne pas avoir atterri en spam ahah.`

Maximum 3 relances si jamais répondu.
Maximum 5 relances si a répondu puis ghosté.

### Détection de l'intention

Avant de répondre, classifier la réponse :
- **Positif** (intéressé, curieux, oui) → continuer la séquence
- **Négatif** (pas intéressé, non) → clore poliment, mettre Statut=Fermé dans Airtable
- **Question** → répondre à la question puis relancer
- **RDV accepté** → envoyer le lien cal.com + notification Telegram 📅

### Mise à jour Airtable après chaque réponse

```json
{
  "Statut": "En conversation / RDV pris / Fermé / Ghosté",
  "Dernier message": "[date]",
  "Nombre messages": "[N]",
  "Texte dernière réponse": "[texte]"
}
```

### Notifications Telegram

```
🟢 Signal positif · [Prénom Nom] — [Titre] — a répondu positivement
📅 RDV pris · [Prénom Nom] — [date heure] — lien cal.com envoyé
👻 Ghosté · [Prénom Nom] — séquence terminée après [N] messages
```

---

## FLUX 4 — Commentaires posts

**Déclencheur :** Cron quotidien à 14h00

### Objectif : 30 commentaires/jour

### Critères de sélection des posts

**Posts à commenter :**
- Posts de relations LinkedIn (1er degré)
- Posts publiés dans les 48 dernières heures MAXIMUM
- Posts avec contenu substantiel (pas juste une image sans texte)

**Posts à IGNORER absolument :**
- Posts sponsorisés (Sponsorisé dans le fil)
- Posts d'entreprises IA / logiciel / marketing digital
- Posts avec CTA "commente X pour recevoir Y"
- Posts négatifs ou polémiques
- Posts déjà commentés (vérifier Airtable)

### Règles de rédaction des commentaires

- **2 lignes maximum** — jamais plus
- **Une idée par ligne**
- **JAMAIS reformuler le post** — ajouter une perspective nouvelle
- **JAMAIS "Super post" ou validation générique**
- **Toujours concret** — chiffre, fait, expérience
- **Ton naturel** — comme si tu parlais à quelqu'un

**Exemples bons commentaires :**
```
7 à 15 calls par semaine c'est un très bon rythme !
Prospecter des personnes qui ont déjà liké c'est plus simple que le cold outreach
```

```
Bien vu. Le temps perdu sur les tâches répétitives est souvent sous-estimé par les dirigeants
```

**Mots interdits dans les commentaires :**
- "bien vu" comme opener
- tiret cadratin (—)
- "recouvrer"
- "c'est malin"
- "instinct"
- "parlant" seul

### Étapes d'exécution

1. Récupérer le fil d'actualité via Unipile
2. Filtrer les posts selon critères ci-dessus
3. Vérifier dans Airtable que le profil n'a pas été commenté aujourd'hui
4. Lire le post complet
5. Rédiger un commentaire de 2 lignes max adapté au contenu
6. Envoyer via Unipile :
```bash
POST https://api44.unipile.com:17474/api/v1/linkedin/posts/[post_id]/comments
{
  "account_id": "$UNIPILE_LINKEDIN_ACCOUNT_ID",
  "text": "[commentaire]"
}
```
7. Attendre 3-5 secondes entre chaque commentaire
8. S'arrêter à 30 commentaires

### Enregistrement Airtable

```json
{
  "Nom du contact": "[auteur du post]",
  "Date": "[date]",
  "Post ID": "[post_id]",
  "Commentaire posté": "[texte]",
  "Type action": "Commentaire"
}
```

### Logger :
```json
{"level":"info","agent":"PROSPECTION","message":"Commentaire · [Prénom Nom] — [sujet du post en 5 mots] — '[3 premiers mots du commentaire]'"}
```

---

## Amélioration continue du style

Chaque semaine, analyser les messages qui ont obtenu des réponses positives vs négatifs :
- Identifier les formulations qui fonctionnent
- Mettre à jour les templates dans ce skill
- Référencer le skill `style-ecriture` pour rester cohérent avec l'écriture de Noa

Quand Noa envoie lui-même des messages ou commentaires, les analyser et noter les patterns dans :
`/opt/data/agents/prospection/style-apprentissage.md`

---

## Logging dashboard — Récapitulatif formats

```json
// Connexion envoyée
{"level":"info","agent":"PROSPECTION","message":"Connexion · [Prénom Nom] — [Titre] — [Entreprise] — [Ville]"}

// Message outbound
{"level":"info","agent":"PROSPECTION","message":"Outbound msg [N] · [Prénom Nom] — [Titre] — [3 premiers mots]"}

// Relance
{"level":"info","agent":"PROSPECTION","message":"Relance [N]/[max] · [Prénom Nom] — J+[N] sans réponse"}

// Réponse reçue
{"level":"info","agent":"PROSPECTION","message":"Réponse reçue · [Prénom Nom] — [Positif/Négatif/Question]"}

// RDV pris
{"level":"info","agent":"PROSPECTION","message":"RDV confirmé · [Prénom Nom] — [Titre] — [date heure]"}

// Commentaire
{"level":"info","agent":"PROSPECTION","message":"Commentaire · [Prénom Nom] — [sujet post] — '[début commentaire]'"}

// Fin de flux
{"level":"info","agent":"PROSPECTION","message":"Flux [NOM] terminé · [N] actions · [N] min"}
```

---

## ROI après chaque flux

```bash
curl -s -X POST http://localhost:8000/api/roi \
  -H 'Content-Type: application/json' \
  -d '{"task_name":"sourcing-connexions","duration_minutes":15}'

# Durées de référence :
# Sourcing 20 connexions → 15 min
# Messages outbound x10 → 20 min
# Réponses → 10 min
# Commentaires 30 posts → 25 min
```

---

## Skills complémentaires à charger

- `style-ecriture` → règles d'écriture BenIT (OBLIGATOIRE)
- `benit-sourcing-context` → contexte activité et profils prioritaires
- `benit-content-context` → contexte BenIT pour personnalisation messages
- `dashboard-rules` → règles de logging dashboard

---

## Crons à configurer

| Flux | Schedule | Description |
|------|----------|-------------|
| Sourcing connexions | `0 8 * * *` | 20 connexions/jour |
| Premier message outbound | `0 10 * * *` | Messages aux connexions +7j |
| Réponses messages | `0 8,10,12,14,16,18 * * *` | Vérification toutes les 2h |
| Commentaires posts | `0 14 * * *` | 30 commentaires/jour |
