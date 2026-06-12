"""
Source de leads : recherche d'entreprises LinkedIn via Unipile.
Avantage : capte les sociétés actives sur LinkedIn (+ leur URL LinkedIn, utile
pour les signaux et l'enrichissement). Inconvénient : pas de SIREN → résolu
ensuite via Pappers. Renvoie [{siren, nom, url, linkedin_url}].
"""

from collectors import unipile
from config import LINKEDIN_SEARCH


def fetch() -> list:
    ls = LINKEDIN_SEARCH
    print(f"[Source: LinkedIn/Unipile] '{ls['keywords']}' (max {ls['max_results']})")
    companies = unipile.search_companies(ls["keywords"], ls["max_results"])
    print(f"[Source: LinkedIn] {len(companies)} entreprises trouvées")
    return companies
