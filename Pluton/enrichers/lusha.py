"""
Enrichissement des contacts (email + téléphone) via Lusha (Person API V2).
→ GET https://api.lusha.com/v2/person
   header: api_key: <clé>
   params: firstName, lastName, linkedinUrl, companyName, companyDomain
Pour tester le workflow complet avant d'acheter Kaspr (plan gratuit : 5 crédits/mois).
Dégrade proprement si la clé n'est pas configurée.
"""

import time
import requests
from urllib.parse import urlparse
from config import API_KEYS

URL = "https://api.lusha.com/v2/person"


def _has_key() -> bool:
    return bool(API_KEYS.get("lusha"))


def _linkedin_url(contact: dict) -> str:
    """Reconstruit une URL LinkedIn complète depuis le slug/URL fourni par Unipile."""
    raw = (contact.get("profil_linkedin_url") or "").strip()
    if not raw:
        return ""
    if raw.startswith("http"):
        return raw
    slug = raw.strip("/").split("?")[0]
    return f"https://www.linkedin.com/in/{slug}"


def _domain(contact: dict) -> str:
    """Extrait le domaine du site entreprise (pour le fallback nom + société)."""
    site = (contact.get("_company_website") or "").strip()
    if not site:
        return ""
    if not site.startswith("http"):
        site = "https://" + site
    return urlparse(site).netloc.replace("www.", "")


def _pick_email(data: dict) -> str:
    """1er email parmi emailAddresses[] / emails[] (sous-champ email/value)."""
    for key in ("emailAddresses", "emails"):
        for item in data.get(key) or []:
            if isinstance(item, str) and item:
                return item
            if isinstance(item, dict):
                v = item.get("email") or item.get("value") or item.get("address")
                if v:
                    return v
    return ""


def _pick_phone(data: dict) -> str:
    """1er téléphone parmi phoneNumbers[] / phones[] (sous-champ number/internationalNumber)."""
    for key in ("phoneNumbers", "phones"):
        for item in data.get(key) or []:
            if isinstance(item, str) and item:
                return item
            if isinstance(item, dict):
                v = (item.get("internationalNumber") or item.get("number")
                     or item.get("localNumber") or item.get("value"))
                if v:
                    return v
    return ""


def enrich(contacts: list) -> list:
    """Ajoute email/téléphone à chaque contact identifiable."""
    if not _has_key():
        return contacts
    headers = {"api_key": API_KEYS["lusha"], "Content-Type": "application/json"}
    for contact in contacts:
        params = {
            "firstName": contact.get("prenom", ""),
            "lastName": contact.get("nom", ""),
            "linkedinUrl": _linkedin_url(contact),
            "companyName": contact.get("_company_name", ""),
            "companyDomain": _domain(contact),
        }
        params = {k: v for k, v in params.items() if v}
        # Il faut au moins le profil LinkedIn, ou nom + société/domaine.
        has_li = "linkedinUrl" in params
        has_name_co = "lastName" in params and ("companyName" in params or "companyDomain" in params)
        if not (has_li or has_name_co):
            continue
        name = f"{contact.get('prenom', '')} {contact.get('nom', '')}".strip()
        try:
            r = requests.get(URL, headers=headers, params=params, timeout=25)
            if r.status_code != 200:
                print(f"  [Lusha] {name}: HTTP {r.status_code}")
                continue
            body = r.json()
            # Structure V2 : {"contact": {"error": ..., "data": {...} | null}}
            contact = body.get("contact") or body
            data = contact.get("data") or {}
            if not data:
                continue
            email = _pick_email(data)
            phone = _pick_phone(data)
            if email:
                contact["email"] = email
            if phone:
                contact["telephone"] = phone
        except Exception as e:
            print(f"  [Lusha] erreur {name}: {e}")
        time.sleep(0.5)  # rate limiting
    return contacts
