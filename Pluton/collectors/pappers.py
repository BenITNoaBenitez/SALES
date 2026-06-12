"""
Collecte des données légales françaises via l'API Pappers.
CA, effectifs, dirigeants, établissements, BODACC, marchés publics.
Dégrade proprement (retourne du vide) si la clé n'est pas configurée.
"""

import requests
from config import API_KEYS

BASE = "https://api.pappers.fr/v2"


def _has_key() -> bool:
    return bool(API_KEYS.get("pappers"))


def get_entreprise(siren: str) -> dict:
    """Récupère CA, effectifs, dirigeants, établissements, BODACC via Pappers."""
    if not _has_key():
        print("  [Pappers] clé absente — données légales ignorées")
        return {}
    params = {
        "api_token": API_KEYS["pappers"],
        "siren": siren,
        "chiffres_cles": True,
        "dirigeants": True,
        "etablissements": True,
        "beneficiaires_effectifs": True,
    }
    try:
        r = requests.get(f"{BASE}/entreprise", params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"  [Pappers] erreur entreprise {siren}: {e}")
        return {}


def get_marches_publics(siren: str) -> list:
    """Récupère les marchés publics liés à l'entreprise."""
    if not _has_key():
        return []
    params = {"api_token": API_KEYS["pappers"], "siren": siren}
    try:
        r = requests.get(f"{BASE}/entreprise/marches-publics", params=params, timeout=15)
        return r.json().get("marches", [])
    except Exception:
        return []


def resolve_siren(nom: str, departements: list = None) -> str:
    """Retrouve le SIREN d'une entreprise à partir de son nom (recherche plein texte
    Pappers). Sert quand la source est Apify/LinkedIn (qui ne donnent pas le SIREN)."""
    if not _has_key() or not nom:
        return ""
    params = {"api_token": API_KEYS["pappers"], "q": nom, "par_page": 1}
    if departements:
        params["departement"] = ",".join(str(d) for d in departements)
    try:
        r = requests.get(f"{BASE}/recherche", params=params, timeout=15)
        res = r.json().get("resultats", [])
        return res[0].get("siren", "") if res else ""
    except Exception:
        return ""


def search_companies(codes_ape: list, departements: list, max_results: int = 20,
                     effectif_min: int = 10, personne_morale: bool = True) -> list:
    """Recherche des entreprises cibles par code APE + départements (Pappers filtre
    par département, pas par nom de région). Île-de-France = 75,77,78,91,92,93,94,95.
    effectif_min + personne_morale écartent les auto-entrepreneurs / micro-entreprises."""
    if not _has_key():
        print("  [Pappers] clé absente — recherche impossible")
        return []
    results, page = [], 1
    while len(results) < max_results:
        params = {
            "api_token": API_KEYS["pappers"],
            "code_naf": ",".join(codes_ape),
            "departement": ",".join(str(d) for d in departements),
            "entreprise_cessee": "false",
            "effectif_min": effectif_min,
            "personne_morale": "true" if personne_morale else "false",
            "par_page": 20,
            "page": page,
        }
        try:
            r = requests.get(f"{BASE}/recherche", params=params, timeout=15)
            batch = r.json().get("resultats", [])
        except Exception as e:
            print(f"  [Pappers] erreur recherche: {e}")
            break
        if not batch:
            break
        for e in batch:
            if e.get("siren"):
                siege = e.get("siege") or {}
                results.append({
                    "siren": e.get("siren"),
                    "nom": e.get("nom_entreprise") or e.get("denomination", ""),
                    "url": e.get("site_web") or siege.get("site_web", ""),
                    "linkedin_url": "",
                })
        page += 1
    return results[:max_results]
