"""
Collecte du contenu du site de l'entreprise via Firecrawl + détection stack tech.
"""

# firecrawl-py v4 : on passe par la couche de compatibilité v1 (kwargs snake_case).
from firecrawl import V1FirecrawlApp as FirecrawlApp
from config import API_KEYS

_app = None

# Outils courants détectables dans le HTML brut / markdown.
TECH_KEYWORDS = {
    "HubSpot": ["hubspot", "hs-scripts"],
    "Salesforce": ["salesforce", "force.com"],
    "Pipedrive": ["pipedrive"],
    "Zoho": ["zoho"],
    "WordPress": ["wp-content", "wordpress"],
    "Webflow": ["webflow.com"],
    "Wix": ["wix.com", "wixstatic"],
    "Google Analytics": ["gtag", "google-analytics", "googletagmanager"],
    "Intercom": ["intercom"],
    "Zendesk": ["zendesk"],
    "Notion": ["notion.so"],
    "Calendly": ["calendly"],
}

# CRM connus (pour distinguer stack_crm de stack_autres côté analyse).
CRM_TOOLS = {"HubSpot", "Salesforce", "Pipedrive", "Zoho"}


def _get_app() -> FirecrawlApp:
    global _app
    if _app is None:
        _app = FirecrawlApp(api_key=API_KEYS["firecrawl"])
    return _app


def _normalize_url(url: str) -> str:
    if url and not url.startswith("http"):
        return "https://" + url
    return url


def _attr(result, *names) -> str:
    """Lit un champ sur l'objet pydantic v4 OU le dict, en tolérant les alias."""
    for n in names:
        val = getattr(result, n, None)
        if val is None and isinstance(result, dict):
            val = result.get(n)
        if val:
            return val
    return ""


def scrape_site(url: str) -> str:
    """Retourne le contenu principal du site en markdown (tronqué)."""
    url = _normalize_url(url)
    if not url:
        return ""
    try:
        result = _get_app().scrape_url(
            url, formats=["markdown"], only_main_content=True, timeout=15000,
        )
        # Tronqué à 2500 car. pour limiter les tokens envoyés à Groq (quota gratuit).
        return _attr(result, "markdown", "content")[:2500]
    except Exception as e:
        print(f"  [Firecrawl] erreur scrape {url}: {e}")
        return ""


def detect_tech_stack(url: str) -> list:
    """Détecte naïvement les outils présents dans le HTML/markdown du site."""
    url = _normalize_url(url)
    if not url:
        return []
    try:
        result = _get_app().scrape_url(
            url, formats=["rawHtml"], only_main_content=False, timeout=15000,
        )
        html = _attr(result, "rawHtml", "raw_html", "html", "markdown").lower()
    except Exception as e:
        print(f"  [Firecrawl] erreur tech {url}: {e}")
        return []
    if not html:
        return []
    return [tech for tech, kws in TECH_KEYWORDS.items()
            if any(k in html for k in kws)]
