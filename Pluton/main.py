"""
Agent Sales Pluton Consulting — pipeline complet.
Pappers → Firecrawl → Unipile → Kaspr → Groq → Excel.

Lancer :  python main.py
Configurer les cibles et les clés dans config.py.
"""

import sys
import time
import traceback

# Console Windows en UTF-8 (sinon les caractères → ✓ ✗ plantent en cp1252).
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import config
from collectors import pappers, firecrawl_site, unipile
from sources import pappers_source, apify_source, linkedin_source
from enrichers import kaspr, lusha
from analyzers import groq_agent
from exporters.excel import export_to_excel

# Outils considérés comme CRM (pour ventiler stack_crm / stack_autres en secours).
CRM_TOOLS = firecrawl_site.CRM_TOOLS

# Service d'enrichissement contact actif (cf. config.ENRICHER).
ENRICHERS = {"lusha": lusha, "kaspr": kaspr}
ENRICHER = ENRICHERS.get(getattr(config, "ENRICHER", "none"))


def build_input(company: dict) -> dict:
    """Collecte + enrichissement → objet d'entrée pour l'agent Groq."""
    siren = company.get("siren", "")
    name = company.get("nom", "")
    url = company.get("url", "")
    li_url = company.get("linkedin_url", "")

    print(f"  [1/4] Pappers…")
    pap = pappers.get_entreprise(siren)
    marches = pappers.get_marches_publics(siren)

    print(f"  [2/4] Firecrawl…")
    site_content = firecrawl_site.scrape_site(url)
    tech_stack = firecrawl_site.detect_tech_stack(url)

    print(f"  [3/4] Unipile LinkedIn…")
    jobs = unipile.get_jobs(name)
    posts = unipile.get_company_posts(li_url, name)
    decideurs = unipile.search_decision_makers(name, config.TARGET_TITLES)

    enricher_name = getattr(config, "ENRICHER", "none")
    print(f"  [4/4] Enrichissement ({enricher_name})…")
    for d in decideurs:
        d["_company_name"] = name
        d["_company_website"] = url
    # On enrichit seulement les N premiers décideurs / entreprise (les dicts sont
    # mutés en place → la liste complète reste vue par l'agent). Préserve le quota
    # Lusha (5 crédits) en l'étalant sur plusieurs entreprises.
    if ENRICHER and decideurs:
        max_enrich = getattr(config, "MAX_ENRICH_PER_COMPANY", 1)
        ENRICHER.enrich(decideurs[:max_enrich])

    # Extraction défensive des données Pappers.
    # CA → liste "finances" (vide si comptes non publiés) ; effectif → champ "effectif".
    finances = pap.get("finances") or []
    siege = pap.get("siege") or {}
    ca = finances[0].get("chiffre_affaires", 0) if finances else 0
    eff = pap.get("effectif_max") or pap.get("effectif_min") or 0
    eff_label = pap.get("effectif", "")  # ex: "Entre 10 et 19 salariés"

    return {
        "entreprise": {
            "nom": name,
            "siren": siren,
            "siret": pap.get("siret", ""),
            "code_ape": pap.get("code_naf", ""),
            "adresse": siege.get("adresse_ligne_1", ""),
            "ville": siege.get("ville", ""),
            "region": siege.get("region", ""),
            "ca": ca,
            "effectifs": eff,
            "tranche_effectif": eff_label,
            "evolution_effectifs": "",
            "nb_etablissements": len(pap.get("etablissements", []) or []),
            "filiales": [],
            "groupe": (pap.get("groupe") or {}).get("denomination", ""),
            "date_creation": pap.get("date_creation", ""),
            "site_web": url,
            "donnees_financieres": {
                "ca_n1": finances[0].get("chiffre_affaires", 0) if len(finances) > 0 else 0,
                "ca_n2": finances[1].get("chiffre_affaires", 0) if len(finances) > 1 else 0,
                "resultat_net": finances[0].get("resultat", 0) if finances else 0,
                "evolution_ca": "",
            },
            "bodacc": [a.get("description", "") for a in (pap.get("publications_bodacc") or [])[:5]],
            "marches_publics": [m.get("intitule", "") for m in (marches or [])[:5]],
        },
        "site_contenu": site_content,
        "stack_tech": tech_stack,
        "signaux_linkedin": {
            "offres_emploi": jobs,
            "publications_recentes": posts,
            "croissance_effectifs_li": "",
        },
        "decideurs": decideurs[:5],
    }


def process_company(company: dict) -> dict | None:
    """Traite une entreprise de bout en bout. Retourne le dossier ou None."""
    name = company.get("nom", "?")
    print(f"\n{'=' * 56}\nTraitement : {name} ({company.get('siren', '')})")
    try:
        input_data = build_input(company)
        print("  → Groq analyse…")
        result = groq_agent.run_agent(input_data)

        # Filets de sécurité : compléter la fiche avec les données collectées
        # si l'agent a laissé des champs vides.
        fiche = result.setdefault("fiche_excel", {})
        ent = input_data["entreprise"]
        fiche.setdefault("entreprise_nom", ent["nom"])
        fiche.setdefault("siren", ent["siren"])
        fiche.setdefault("site_web", ent["site_web"])
        if not fiche.get("stack_crm") or not fiche.get("stack_autres"):
            crm = [t for t in input_data["stack_tech"] if t in CRM_TOOLS]
            autres = [t for t in input_data["stack_tech"] if t not in CRM_TOOLS]
            fiche.setdefault("stack_crm", ", ".join(crm))
            fiche.setdefault("stack_autres", ", ".join(autres))

        score = result.get("scoring", {}).get("score_global", "?")
        niveau = result.get("scoring", {}).get("niveau", "?")
        print(f"  ✓ Score : {score}/100 ({niveau})")
        return result
    except Exception as e:
        print(f"  ✗ Erreur : {e}")
        traceback.print_exc()
        return None


def get_companies() -> list:
    """Liste des entreprises selon config.SOURCE (pappers | apify | linkedin | manual).
    Le SIREN manquant (apify/linkedin) est résolu via Pappers pour garder les
    données légales (CA, effectifs, BODACC)."""
    source = getattr(config, "SOURCE", "pappers")
    if source == "pappers":
        companies = pappers_source.fetch()
    elif source == "apify":
        companies = apify_source.fetch()
    elif source == "linkedin":
        companies = linkedin_source.fetch()
    else:  # "manual"
        companies = config.COMPANIES

    if not companies:
        return []

    # Résolution du SIREN pour les sources qui ne le fournissent pas.
    deps = config.SEARCH.get("departements") if source == "apify" else None
    missing = [c for c in companies if not c.get("siren")]
    if missing:
        print(f"  Résolution SIREN via Pappers pour {len(missing)} entreprise(s)…")
        for c in missing:
            c["siren"] = pappers.resolve_siren(c["nom"], deps)
    return companies


def main():
    companies = get_companies()
    if not companies:
        print("Aucune entreprise à traiter. Renseigne config.COMPANIES ou config.SEARCH.")
        return

    print(f"\n{len(companies)} entreprise(s) à traiter.\n")
    results = []
    for company in companies:
        result = process_company(company)
        if result:
            results.append(result)
        time.sleep(2)  # pause entre entreprises

    export_to_excel(results)
    print(f"\n✓ Terminé. {len(results)}/{len(companies)} dossiers produits.")


if __name__ == "__main__":
    main()
