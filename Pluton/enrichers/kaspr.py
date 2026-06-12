"""
Enrichissement des contacts (email + téléphone) via Kaspr.
Kaspr part de l'identifiant LinkedIn (public identifier) + le nom complet.
→ POST https://api.developers.kaspr.io/profile/linkedin
   headers: Authorization: <clé>, accept-version: v2.0, Content-Type: application/json
   body:    {"name": "<prénom nom>", "id": "<public identifier LinkedIn>"}
Coûte 1 crédit Kaspr par requête réussie.
Dégrade proprement si la clé n'est pas configurée.
"""

import time
import requests
from config import API_KEYS

URL = "https://api.developers.kaspr.io/profile/linkedin"


def _has_key() -> bool:
    return bool(API_KEYS.get("kaspr"))


def _headers() -> dict:
    return {
        "Authorization": API_KEYS["kaspr"],
        "accept-version": "v2.0",
        "Content-Type": "application/json",
    }


def _linkedin_id(contact: dict) -> str:
    """Extrait l'identifiant LinkedIn (slug) depuis l'URL/identifiant fourni."""
    raw = (contact.get("profil_linkedin_url") or "").strip()
    if not raw:
        return ""
    if "linkedin.com/in/" in raw:
        raw = raw.split("linkedin.com/in/", 1)[1]
    return raw.strip("/").split("/")[0].split("?")[0]


def _pick_emails(data: dict) -> str:
    """Récupère le 1er email parmi les champs possibles renvoyés par Kaspr."""
    candidates = []
    for key in ("emails", "workEmails", "professionalEmails", "directEmails", "email"):
        val = data.get(key)
        if not val:
            continue
        if isinstance(val, str):
            candidates.append(val)
        elif isinstance(val, list):
            for item in val:
                if isinstance(item, str):
                    candidates.append(item)
                elif isinstance(item, dict):
                    candidates.append(item.get("email") or item.get("value") or "")
    candidates = [c for c in candidates if c]
    return candidates[0] if candidates else ""


def _pick_phones(data: dict) -> str:
    """Récupère le 1er téléphone parmi les champs possibles renvoyés par Kaspr."""
    candidates = []
    for key in ("phones", "phoneNumbers", "mobilePhones", "phone"):
        val = data.get(key)
        if not val:
            continue
        if isinstance(val, str):
            candidates.append(val)
        elif isinstance(val, list):
            for item in val:
                if isinstance(item, str):
                    candidates.append(item)
                elif isinstance(item, dict):
                    candidates.append(item.get("phone") or item.get("number") or item.get("value") or "")
    candidates = [c for c in candidates if c]
    return candidates[0] if candidates else ""


def enrich(contacts: list) -> list:
    """Ajoute email/téléphone à chaque contact disposant d'un profil LinkedIn."""
    if not _has_key():
        return contacts
    for contact in contacts:
        li_id = _linkedin_id(contact)
        name = f"{contact.get('prenom', '')} {contact.get('nom', '')}".strip()
        if not li_id or not name:
            continue
        try:
            r = requests.post(URL, headers=_headers(),
                              json={"name": name, "id": li_id}, timeout=25)
            if r.status_code != 200:
                print(f"  [Kaspr] {name}: HTTP {r.status_code}")
                continue
            body = r.json()
            # La donnée utile peut être à la racine ou sous "data"/"profile".
            data = body.get("data") or body.get("profile") or body
            email = _pick_emails(data)
            phone = _pick_phones(data)
            if email:
                contact["email"] = email
            if phone:
                contact["telephone"] = phone
        except Exception as e:
            print(f"  [Kaspr] erreur {name}: {e}")
        time.sleep(0.5)  # rate limiting
    return contacts
