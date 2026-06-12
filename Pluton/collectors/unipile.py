"""
Collecte des signaux LinkedIn via Unipile (sans Sales Navigator) :
décideurs, offres d'emploi, publications — via l'endpoint unique
POST /api/v1/linkedin/search?account_id=<id>  body {api, category, keywords}.
Dégrade proprement si la clé / l'account_id ne sont pas configurés.
"""

import requests
from config import API_KEYS, UNIPILE_ACCOUNT_ID, UNIPILE_DSN

BASE = f"{UNIPILE_DSN.rstrip('/')}/api/v1"


def _ready() -> bool:
    return bool(API_KEYS.get("unipile")) and bool(UNIPILE_ACCOUNT_ID) \
        and UNIPILE_ACCOUNT_ID != "votre_account_id_unipile"


def _headers() -> dict:
    return {
        "X-API-KEY": API_KEYS["unipile"],
        "accept": "application/json",
        "content-type": "application/json",
    }


def _search(category: str, keywords: str, limit: int = 5) -> list:
    """Appel générique à l'endpoint de recherche LinkedIn classic."""
    if not _ready():
        return []
    url = f"{BASE}/linkedin/search"
    params = {"account_id": UNIPILE_ACCOUNT_ID, "limit": limit}
    payload = {"api": "classic", "category": category, "keywords": keywords}
    try:
        r = requests.post(url, headers=_headers(), params=params, json=payload, timeout=40)
        if r.status_code != 200:
            print(f"  [Unipile] {category} '{keywords}': HTTP {r.status_code}")
            return []
        return r.json().get("items", []) or []
    except Exception as e:
        print(f"  [Unipile] erreur {category}: {e}")
        return []


def _split_name(full: str) -> tuple:
    """'Jean Baptiste RIBA' → ('Jean', 'Baptiste RIBA')."""
    parts = (full or "").strip().split()
    if not parts:
        return "", ""
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], " ".join(parts[1:])


def get_jobs(company_name: str) -> list:
    """Offres d'emploi LinkedIn pour l'entreprise (signaux de recrutement)."""
    items = _search("jobs", company_name, limit=10)
    titles = []
    for j in items:
        t = j.get("title") or j.get("name") or ""
        if t:
            titles.append(t)
    return titles


def get_company_posts(company_linkedin_url: str, company_name: str = "") -> list:
    """Publications LinkedIn récentes liées à l'entreprise (signaux d'activité)."""
    kw = company_name or company_linkedin_url
    items = _search("posts", kw, limit=5)
    posts = []
    for p in items:
        text = p.get("text") or p.get("commentary") or p.get("name") or ""
        if text:
            posts.append(text[:200])
    return posts


def search_companies(keywords: str, limit: int = 20) -> list:
    """Recherche d'ENTREPRISES sur LinkedIn (source de leads). Renvoie la structure
    normalisée {siren, nom, url, linkedin_url} — le SIREN est résolu ensuite via Pappers."""
    items = _search("companies", keywords, min(limit, 50))
    out = []
    for c in items:
        nom = c.get("name", "")
        if nom:
            out.append({
                "siren": "",
                "nom": nom,
                "url": c.get("website", ""),
                "linkedin_url": c.get("profile_url", ""),
            })
    return out[:limit]


def search_decision_makers(company_name: str, target_titles: list) -> list:
    """Recherche des décideurs LinkedIn pour l'entreprise (1 requête, mots-clés combinés)."""
    if not _ready():
        return []
    # 1 seule requête par entreprise pour ménager le compte LinkedIn :
    # on combine le 1er titre cible + le nom de l'entreprise.
    top_title = target_titles[0] if target_titles else "directeur"
    items = _search("people", f"{top_title} {company_name}", limit=5)
    if not items:
        items = _search("people", company_name, limit=5)

    results = []
    for p in items:
        prenom, nom = _split_name(p.get("name", ""))
        results.append({
            "prenom": prenom,
            "nom": nom,
            "poste": p.get("headline", ""),
            "profil_linkedin_url": p.get("public_profile_url") or p.get("profile_url")
                                   or p.get("public_identifier", ""),
            "anciennete_mois": None,
            "email": "",
            "telephone": "",
            "publications": [],
        })
    return results
