# rag/retriever.py

def get_relevant_docs(company_db, query, k=12):
    """
    Runs multiple searches and merges results.
    dict keyed by page_content = automatic deduplication.
    """
    results = {}

    # Search 1: the full question as typed by user
    for doc in company_db.similarity_search(query, k=k):
        results[doc.page_content] = doc

    # Search 2,3,4...: smaller targeted sub-terms
    sub_terms = extract_key_terms(query)
    for term in sub_terms:
        for doc in company_db.similarity_search(term, k=6):
            results[doc.page_content] = doc  # duplicates are overwritten, not added again

    return list(results.values())


def extract_key_terms(query):
    """
    Looks at the user's question and pulls out related ESG phrases
    to use as extra search queries.
    No extra libraries needed — just string matching.
    """
    q = query.lower()
    terms = []

    # Emissions related
    if "scope 3" in q:
        terms += ["scope 3 emissions", "value chain emissions", "supply chain carbon"]
    if "scope 2" in q:
        terms += ["scope 2 emissions", "indirect emissions", "purchased electricity"]
    if "scope 1" in q:
        terms += ["scope 1 emissions", "direct emissions", "combustion"]
    if "emission" in q or "carbon" in q or "ghg" in q:
        terms += ["greenhouse gas", "CO2 equivalent", "tCO2e", "net zero target"]

    # Energy
    if "energy" in q:
        terms += ["energy consumption", "renewable energy", "energy intensity", "gigajoule"]

    # Water
    if "water" in q:
        terms += ["water withdrawal", "water consumption", "water discharge", "water stress"]

    # Social / workforce
    if "employee" in q or "workforce" in q or "staff" in q:
        terms += ["headcount", "employee turnover", "new hires", "workforce diversity"]
    if "safety" in q or "health" in q:
        terms += ["injury rate", "lost time", "fatality", "TRIR", "occupational health"]
    if "diversity" in q or "gender" in q:
        terms += ["gender diversity", "women in leadership", "equal pay", "inclusion"]

    # Governance
    if "board" in q or "governance" in q:
        terms += ["board composition", "independent directors", "audit committee"]

    # Targets / goals
    if "target" in q or "goal" in q:
        terms += ["2030 target", "2050 target", "net zero", "science-based targets", "SBTi"]
    if "risk" in q:
        terms += ["climate risk", "TCFD", "physical risk", "transition risk"]

    return terms