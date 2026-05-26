def check_esg_rules(answer):
    warnings = []
    ans = answer.lower()

    # Emissions Check (GRI 305)
    if "scope 1" in ans and "scope 2" in ans and "scope 3" not in ans:
        warnings.append("⚠️ Missing Scope 3 emissions disclosure (GRI 305)")

    # Energy Disclosure Check (GRI 302)
    if "energy" not in ans:
        warnings.append("⚠️ Energy consumption details not clearly reported (GRI 302)")

    # Water Disclosure Check (GRI 303)
    if "water" not in ans:
        warnings.append("⚠️ Water usage/discharge not mentioned (GRI 303)")

    # Net Zero Claim Check 
    if "net zero" in ans and ("target" not in ans and "year" not in ans):
        warnings.append("⚠️ Net zero claim without clear timeline (possible greenwashing)")

    # --- Vague Language Check ---
    vague_terms = ["we aim", "we strive", "committed to", "working towards"]

    if any(term in ans for term in vague_terms):
        warnings.append("⚠️ Vague ESG claims detected (non-quantifiable)")

    return warnings