"""
Source de leads : Google Maps via Apify (actor compass/crawler-google-places).
Avantage : capte des TPE/PME locales avec site web + téléphone, même absentes
des bases LinkedIn. Inconvénient : pas de SIREN → résolu ensuite via Pappers.
Renvoie une liste normalisée [{siren, nom, url, linkedin_url}].
"""

from config import API_KEYS, APIFY


def fetch() -> list:
    if not API_KEYS.get("apify"):
        print("[Source: Apify] clé absente — aucune entreprise")
        return []
    from apify_client import ApifyClient

    a = APIFY
    query = f"{a['sector']} {a['location']}"
    print(f"[Source: Apify/Google Maps] '{query}' (max {a['max_results']})")
    client = ApifyClient(API_KEYS["apify"])
    run_input = {
        "searchStringsArray": [query],
        "maxCrawledPlacesPerSearch": a["max_results"],
        "language": "fr",
        "countryCode": "fr",
        "includeWebResults": True,
        "scrapeContacts": False,
        "reviewsCount": 0,
    }
    try:
        run = client.actor("compass/crawler-google-places").call(run_input=run_input)
        dataset_id = getattr(run, "default_dataset_id", None) or run["defaultDatasetId"]
    except Exception as e:
        print(f"[Source: Apify] erreur : {e}")
        return []

    out = []
    for item in client.dataset(dataset_id).iterate_items():
        nom = item.get("title", "")
        if nom:
            out.append({
                "siren": "",
                "nom": nom,
                "url": item.get("website", ""),
                "linkedin_url": "",
            })
    print(f"[Source: Apify] {len(out)} entreprises trouvées")
    return out[:a["max_results"]]
