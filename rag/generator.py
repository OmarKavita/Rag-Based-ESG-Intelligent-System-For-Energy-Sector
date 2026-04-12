from transformers import pipeline

# Load model (open-source)
generator = pipeline(
    "text-generation",
    model="google/flan-t5-base",
    max_length=512
)


def generate_answer(query, company_docs, framework_docs):


    if not company_docs:
        return "No relevant company data found. Retrieval failed."

    # Combine context
    company_text = "\n".join([doc.page_content for doc in company_docs])
    framework_text = "\n".join([doc.page_content for doc in framework_docs])

# def generate_answer(query, company_docs, framework_docs):
#     # Combine context

#     # company_text = "\n".join([doc.page_content for doc in company_docs])
#     framework_text = "\n".join([doc.page_content for doc in framework_docs])


    prompt = f"""
    You are an ESG analyst.

    Answer the question STRICTLY using company data.

    Rules:
    - Start with YES or NO
    - Do NOT copy text
    - Summarize in your own words
    - If data missing → clearly say "Not disclosed"
    - Then compare with GRI

    Question:
    {query}

    Company Data:
    {company_text[:2000]}

    GRI Standards:
    {framework_text[:1500]}

    Final Answer Format:
    Answer: <YES/NO + explanation>
    Gap: <what is missing>
    Risk: <ESG risk>
    """

    


    response = generator(prompt, do_sample=False)
    return response[0]["generated_text"]



