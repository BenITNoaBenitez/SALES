# =============================================================================
# CONFIGURATION AGENT SALES — PLUTON CONSULTING
# Stack : Pappers + Firecrawl + Unipile + Lusha/Kaspr + Groq → Excel
# Modifie ces paramètres avant de lancer.
# =============================================================================

import os

# =============================================================================
# SOURCE DE LEADS — d'où viennent les entreprises à traiter
# "pappers"  : recherche Pappers par code APE + départements (donne le SIREN)
# "apify"    : Google Maps via Apify (TPE/PME locales avec site web)
# "linkedin" : recherche d'entreprises LinkedIn via Unipile
# "manual"   : liste COMPANIES ci-dessous (saisie à la main)
# Pour apify/linkedin, le SIREN manquant est résolu automatiquement via Pappers.
# =============================================================================
SOURCE = "pappers"

# Paramètres de la source "pappers"
SEARCH = {
    "codes_ape": ["4120A", "4120B", "8121Z", "8122Z", "8129A", "6920Z"],
    # Pappers filtre par DÉPARTEMENT (pas par nom de région).
    # Île-de-France = 75,77,78,91,92,93,94,95. Réduis la liste pour cibler.
    "departements": ["75", "92", "93", "94"],
    "effectif_min": 10,        # écarte micro-entreprises (ICP Pluton : PME)
    "personne_morale": True,   # écarte les auto-entrepreneurs
    "max_results": 20,
}

# Paramètres de la source "apify" (Google Maps)
APIFY = {
    "sector": "société de nettoyage",
    "location": "Paris",
    "max_results": 20,
}

# Paramètres de la source "linkedin" (Unipile)
LINKEDIN_SEARCH = {
    "keywords": "nettoyage facilities Paris",
    "max_results": 20,
}

# Liste manuelle (utilisée seulement si SOURCE = "manual").
# Chaque entrée : siren, nom, url (site), linkedin_url.
COMPANIES = [
    {
        "siren": "",
        "nom": "Entreprise Exemple BTP",
        "url": "https://www.exemple-btp.fr",
        "linkedin_url": "",
    },
]

# Identifiant du compte LinkedIn connecté côté Unipile (requis pour Unipile).
UNIPILE_ACCOUNT_ID = os.getenv("UNIPILE_ACCOUNT_ID", "D99WeT4lRSiiTlwIsz9OVA")

# DSN (host:port) attribué à ton compte Unipile — visible dans le dashboard / les curl.
UNIPILE_DSN = os.getenv("UNIPILE_DSN", "https://api44.unipile.com:17474")

# =============================================================================
# CLÉS API
# Firecrawl et Groq sont récupérées du projet BenIT existant (réutilisables).
# Unipile / Pappers / Dropcontact : à créer (placeholders pour l'instant).
# Tu peux aussi les définir en variables d'environnement (priorité à l'env).
# =============================================================================

API_KEYS = {
    # Firecrawl — réutilisé du projet BenIT (plan gratuit : 500 crédits/mois)
    "firecrawl": os.getenv("FIRECRAWL_API_KEY", "fc-e5beffe7ff0444aba2bc6ac44f03cce4"),

    # Groq — réutilisé du projet BenIT (gratuit)
    "groq": os.getenv("GROQ_API_KEY", "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"),

    # Pappers — https://www.pappers.fr/api (données légales FR)
    "pappers": os.getenv("PAPPERS_API_KEY", "6605a1da5389857bb871e69a470f09ac64c6d5fb82d1c639"),

    # Apify — réutilisé du projet BenIT (source Google Maps + recherche d'entreprises)
    "apify": os.getenv("APIFY_API_KEY", "apify_api_tPds4WHVVKxt8PHWxD6RxtDLAtcOSf0z0OLT"),

    # Unipile — https://www.unipile.com (LinkedIn sans Sales Navigator)
    "unipile": os.getenv("UNIPILE_API_KEY", "EmZXV/u4.5cRunL+e7WwOB8EgjV9YabwYnXeQQn6FLBmTImSPDn4="),

    # Kaspr — https://app.kaspr.io/settings/api (email + téléphone via LinkedIn)
    # Accès API à partir du plan Starter (essai gratuit).
    "kaspr": os.getenv("KASPR_API_KEY", ""),

    # Lusha — https://dashboard.lusha.com (email + téléphone, 5 crédits gratuits/mois)
    # Pour tester le workflow complet avant d'acheter Kaspr.
    "lusha": os.getenv("LUSHA_API_KEY", "d3e386ab-fcc4-47aa-a9c0-252117b1ad97"),
}

# Service d'enrichissement contact actif : "lusha" | "kaspr" | "none".
# Bascule sur "kaspr" une fois ton plan Kaspr acheté.
ENRICHER = "lusha"

# Nb de décideurs enrichis (email/tél) par entreprise. Lusha gratuit = 5 crédits/mois,
# donc 1 permet d'étaler sur ~5 entreprises. Monte-le avec un plan payant.
MAX_ENRICH_PER_COMPANY = 1

# =============================================================================
# PARAMÈTRES LLM (Groq)
# =============================================================================

LLM = {
    # "llama-3.1-8b-instant" (volume, gros quota journalier gratuit) ou
    # "llama-3.3-70b-versatile" (meilleure qualité, mais quota 100k tokens/jour
    # vite épuisé : ~4-5 entreprises seulement en gratuit).
    "model": "llama-3.1-8b-instant",
    "temperature": 0.2,
    "max_tokens": 2000,
}

# Postes à cibler en priorité côté décideurs (ordre = priorité).
TARGET_TITLES = [
    "Directeur général",
    "Directeur des opérations",
    "Responsable innovation",
    "Directeur commercial",
]
