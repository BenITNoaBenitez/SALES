"""
Intelligence de l'agent : scoring, signaux, angle d'approche et email
via Groq (Llama 3.3 70B), à partir du prompt système Pluton Consulting.
"""

import json
from datetime import datetime
from groq import Groq
from config import API_KEYS, LLM
from system_prompt import SYSTEM_PROMPT

_client = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=API_KEYS["groq"])
    return _client


def run_agent(input_data: dict) -> dict:
    """Appelle Groq et retourne le dossier complet (dict). Lève en cas d'échec."""
    user_message = (
        "Analyse cette entreprise et produis le dossier complet en JSON.\n\n"
        "DONNÉES ENTRÉE :\n"
        + json.dumps(input_data, ensure_ascii=False, indent=2)
    )

    response = _get_client().chat.completions.create(
        model=LLM["model"],
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=LLM["temperature"],
        max_tokens=LLM["max_tokens"],
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    result = json.loads(raw)

    # Garantit la présence de fiche_excel + horodatage.
    result.setdefault("fiche_excel", {})
    result["fiche_excel"]["date_traitement"] = datetime.now().isoformat(timespec="seconds")
    return result
