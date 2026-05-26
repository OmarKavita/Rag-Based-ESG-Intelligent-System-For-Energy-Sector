# rag/retriever.py

# rag/retriever.py

def get_relevant_docs(company_db, query, k=15):
    results = {}

    # Strategy 1: search with the full question as typed
    for doc in company_db.similarity_search(query, k=k):
        results[doc.page_content] = doc

    # Strategy 2: search with auto-generated paraphrases of the question
    for paraphrase in paraphrase_query(query):
        for doc in company_db.similarity_search(paraphrase, k=6):
            results[doc.page_content] = doc

    # Strategy 3: search for data/numbers related to the topic
    for term in data_focused_queries(query):
        for doc in company_db.similarity_search(term, k=5):
            results[doc.page_content] = doc

    return list(results.values())


def paraphrase_query(query):
    """
    Generates alternative phrasings of the same question.
    Works for ANY topic — no hardcoding needed.

    Logic: ESG reports often use different words than the question.
    Example: user asks "scope 3 emissions" but report says
    "value chain carbon footprint" or "indirect upstream GHG".
    We generate variations automatically.
    """
    q = query.lower().strip()

    paraphrases = []

    # Variation 1: strip question words to get the core topic
    # "what are the scope 3 emissions?" → "scope 3 emissions"
    question_words = ["what are", "what is", "does the company", "does this report",
                      "how much", "how many", "tell me about", "show me",
                      "is there", "are there", "provide", "list", "give me",
                      "mention", "contain", "include", "disclose"]
    core = q
    for word in question_words:
        core = core.replace(word, "").strip()
    core = core.rstrip("?").strip()
    if core and core != q:
        paraphrases.append(core)

    # Variation 2: "X of the company" → "company X disclosure"
    paraphrases.append(f"company {core} disclosure")

    # Variation 3: "X" → "X data figures metrics"
    # Catches tables and numeric sections the question phrasing might miss
    paraphrases.append(f"{core} data figures metrics")

    # Variation 4: "X" → "X report performance"
    paraphrases.append(f"{core} performance report")

    # Variation 5: "X" → "X target reduction initiative"
    # Catches forward-looking sections like targets and action plans
    paraphrases.append(f"{core} target reduction initiative")

    return paraphrases


def data_focused_queries(query):
    """
    Generates number/table focused searches for ANY topic.
    ESG reports store actual figures in tables which use very
    different language from the surrounding text.
    This finds those chunks regardless of topic.
    """
    q = query.lower().strip()

    # Strip question words to get the core noun phrase
    question_words = ["what are", "what is", "does the company", "does this report",
                      "how much", "how many", "tell me about", "show me",
                      "is there", "are there", "provide", "list", "give me",
                      "mention", "contain", "include", "disclose"]
    core = q
    for word in question_words:
        core = core.replace(word, "").strip()
    core = core.rstrip("?").strip()

    # These patterns find tables and numeric disclosures for any topic
    return [
        f"{core} total",                  # e.g. "scope 3 emissions total"
        f"{core} breakdown by year",       # e.g. "water consumption breakdown by year"
        f"{core} FY 2022 FY 2023",        # catches year-wise tables
        f"{core} percentage reduction",    # catches trend data
        f"{core} quantity amount volume",  # generic numeric catch-all
    ]