# rag/generator.py
import os
from groq import Groq
from dotenv import load_dotenv

# Reads GROQ_API_KEY from environment variable
# Set it by running: export GROQ_API_KEY="your_key_here"  (Mac/Linux)
# Or on Windows:     set GROQ_API_KEY=your_key_here
print(os.getcwd())
load_dotenv()
print(os.getenv("GROQ_API_KEY"))
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------- SYSTEM PROMPT ----------
# This is sent separately from the user's question.
# It defines the model's role and strict rules before it sees any data.
# This is what makes answers sound like a real analyst, not a chatbot.

SYSTEM_PROMPT = """You are a senior ESG analyst who has read the company sustainability report thoroughly.

Your job is to answer questions about the report clearly and professionally.

Rules you must always follow:
1. Answer ONLY from the report excerpts provided. Do not use outside knowledge for facts.
2. If specific figures, percentages, years, or targets are present — include them in your answer.
3. If steps or initiatives are mentioned — summarize them clearly.
4. If information is partially present — share what is there and clearly note what is missing.
5. If information is completely absent — say exactly: "This information is not disclosed in the report."
6. Do not say "based on the context" or "according to the excerpts" — write naturally.
7. Write in flowing paragraphs. Only use bullet points if listing 3 or more distinct items.
8. Keep answers focused — 3 to 5 sentences for simple questions, up to 2 paragraphs for complex ones.
9. If you can see ANY figures or numbers related to the question — always report them. Never say
   data is missing if numbers are visible in the excerpts provided to you.
"""

def generate_answer(query, company_docs, framework_docs=None):

    # If retrieval found nothing, return immediately
    if not company_docs:
        return "No relevant sections were found in the report for this question."

    # Build the context block from retrieved chunks
    # Each chunk is labelled with its source file and page number
    context_parts = []
    for doc in company_docs:
        page = doc.metadata.get("page", "")
        file = doc.metadata.get("file_name", "report")
        label = f"[{file}, page {page}]" if page else f"[{file}]"
        context_parts.append(f"{label}\n{doc.page_content.strip()}")

    # Join all chunks with a separator so the model can tell them apart
    company_context = "\n\n---\n\n".join(context_parts)

    # This is what the user's turn looks like — question + report excerpts
    user_message = f"""Question: {query}

Report excerpts:
{company_context[:5000]}
"""
    # 5000 char limit keeps the request within Groq's free tier token limits
    # You can raise this to 8000 safely with llama-3.1-8b-instant

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",   # free on Groq, fast, good quality
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message}
        ],
        max_tokens=1024,
        temperature=0.2   # 0 = fully deterministic, 1 = creative/random
                          # 0.2 = factual but not robotic
    )

    return response.choices[0].message.content