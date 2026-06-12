# Agent Sales — Pluton Consulting

Pipeline de prospection automatisée : pour chaque entreprise cible française, on
collecte les données légales, le contenu du site, les signaux LinkedIn et les
emails des décideurs, puis un agent Groq score le prospect et rédige l'email.
Résultat : un fichier Excel, une ligne par entreprise, colorisé par chaleur.

```
SOURCE ──► [collecte] ──► [enrichissement] ──► Groq ──► Excel
(d'où     Pappers+Firecrawl   Lusha/Kaspr        (IA)
 viennent  +Unipile           (mail+tél)
 les leads)
```

## Source des leads — `config.SOURCE`

Au départ, on choisit **d'où viennent les entreprises** à traiter :

| `SOURCE` | Origine | Donne le SIREN ? | Paramètres |
|---|---|---|---|
| `"pappers"` | Recherche Pappers (code APE + départements) | ✅ oui | `SEARCH` |
| `"apify"` | Google Maps via Apify (TPE/PME locales) | ❌ résolu via Pappers | `APIFY` |
| `"linkedin"` | Recherche d'entreprises LinkedIn (Unipile) | ❌ résolu via Pappers | `LINKEDIN_SEARCH` |
| `"manual"` | Liste écrite à la main | selon saisie | `COMPANIES` |

> Pour `apify` et `linkedin`, le SIREN manquant est **résolu automatiquement** via
> Pappers (recherche par nom), pour garder les données légales (CA, effectifs, BODACC).

Quelle que soit la source, la suite est identique : Pappers (légal) + Firecrawl (site)
+ Unipile (décideurs/signaux) → enrichissement contact → Groq → Excel.

## Installation

```powershell
pip install -r requirements.txt
```

## Configuration — `config.py`

| Paramètre | Rôle |
|---|---|
| `SOURCE` | Origine des leads : `pappers` \| `apify` \| `linkedin` \| `manual` |
| `SEARCH` / `APIFY` / `LINKEDIN_SEARCH` | Paramètres de chaque source |
| `COMPANIES` | Liste manuelle (si `SOURCE="manual"`) |
| `ENRICHER` | Service email/tél : `lusha` \| `kaspr` \| `none` |
| `UNIPILE_ACCOUNT_ID` / `UNIPILE_DSN` | Compte LinkedIn connecté côté Unipile |
| `API_KEYS` | Clés des services |
| `LLM` | Modèle Groq, température, max_tokens |
| `TARGET_TITLES` | Postes décideurs à cibler en priorité |

### Clés API

- **Firecrawl** et **Groq** : déjà renseignées (récupérées du projet BenIT, réutilisables).
- **Pappers**, **Unipile**, **Kaspr** : à créer puis renseigner dans `config.py`
  ou via variables d'environnement (l'env est prioritaire) :

```powershell
$env:PAPPERS_API_KEY = "..."
$env:UNIPILE_API_KEY = "..."
$env:LUSHA_API_KEY   = "..."   # ou KASPR_API_KEY
```

### Enrichissement contact (email + téléphone) — `config.ENRICHER`

Le service actif se choisit avec une seule ligne dans `config.py` :

```python
ENRICHER = "lusha"   # "lusha" | "kaspr" | "none"
```

- **`lusha`** — pour **tester le workflow complet** (plan gratuit : 5 crédits/mois,
  clé sur https://dashboard.lusha.com). Part de l'URL LinkedIn du décideur (Unipile).
- **`kaspr`** — à activer une fois ton plan acheté (accès API dès le plan Starter).
- **`none`** — désactive l'enrichissement (email/téléphone restent vides).

> ⚠️ Les deux dépendent d'**Unipile** : c'est lui qui fournit les profils LinkedIn
> des décideurs à enrichir. Sans Unipile, ces services n'ont personne à traiter.

> Chaque collecteur **dégrade proprement** : si une clé manque, l'étape est sautée
> (champ vide) au lieu de planter. Tu peux donc lancer le pipeline dès maintenant
> avec seulement Firecrawl + Groq, et ajouter les autres services plus tard.

## Lancer

```powershell
python main.py
```

Le fichier `prospects_pluton_AAAAMMJJ_HHMM.xlsx` est créé dans le dossier.

## Coûts mensuels estimés

| Outil | Usage | Coût |
|---|---|---|
| Groq (Llama 3.3 70B) | ~500 analyses | ~5–15 $ |
| Firecrawl | Hobby (~3 000 pages) | 16 $/mois |
| Pappers | données légales | gratuit / crédits |
| Lusha / Kaspr | enrichissement mail+tél | Lusha 5 crédits gratuits ; Kaspr Starter |
| Unipile | 1 compte LinkedIn | 49 €/mois |
| **Total** | | **~100–150 €/mois** |

## Structure

```
Pluton/
├── config.py              clés + cibles + paramètres
├── system_prompt.py       prompt système de l'agent
├── main.py                pipeline (source → collecte → IA → Excel)
├── sources/               D'OÙ viennent les leads (au choix)
│   ├── pappers_source.py  recherche APE + départements
│   ├── apify_source.py    Google Maps
│   └── linkedin_source.py recherche entreprises LinkedIn (Unipile)
├── collectors/
│   ├── pappers.py         données légales FR + recherche cibles
│   ├── firecrawl_site.py  scrape site + détection stack tech
│   └── unipile.py         offres, posts, décideurs LinkedIn
├── enrichers/
│   ├── lusha.py           emails + téléphones (test gratuit)
│   └── kaspr.py           emails + téléphones (prod)
├── analyzers/
│   └── groq_agent.py      scoring + signaux + angle + email
└── exporters/
    └── excel.py           Excel colorisé par chaleur
```
