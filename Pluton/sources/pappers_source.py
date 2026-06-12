"""
Source de leads : recherche Pappers (par code APE + départements).
Avantage : fournit directement le SIREN → données légales fiables.
Renvoie une liste normalisée [{siren, nom, url, linkedin_url}].
"""

from collectors import pappers
from config import SEARCH


def fetch() -> list:
    s = SEARCH
    print(f"[Source: Pappers] APE={s['codes_ape']} départements={s['departements']}")
    return pappers.search_companies(
        s["codes_ape"], s["departements"], s["max_results"],
        s.get("effectif_min", 10), s.get("personne_morale", True),
    )
