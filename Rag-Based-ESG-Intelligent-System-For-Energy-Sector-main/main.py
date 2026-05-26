# main.py
from ingestion.pdf_loader import load_pdfs_with_metadata
from ingestion.chunking import chunk_documents
from vectorstore.build_index import create_vectorstore
from rag.retriever import get_relevant_docs        # updated retriever
from rag.generator import generate_answer          # updated generator
from esg.rules import check_esg_rules

def main():

    # --- LOAD ONCE ---
    # This is the slow part (embedding all PDFs).
    # We do it once at startup, then reuse the indexes for every question.
    print("Loading and indexing documents... (this takes ~30 seconds)")

    documents = load_pdfs_with_metadata("data")
    chunks = chunk_documents(documents)

    company_chunks   = [c for c in chunks if c.metadata.get("source_type") == "company"]
    framework_chunks = [c for c in chunks if c.metadata.get("source_type") == "framework"]

    company_db   = create_vectorstore(company_chunks)
    framework_db = create_vectorstore(framework_chunks)

    print("Ready. Ask anything about the report. Type 'exit' to quit.\n")

    # --- QUESTION LOOP ---
    # Keeps running until the user types exit/quit/q
    while True:
        query = input("Your question: ").strip()

        if query.lower() in ("exit", "quit", "q"):
            print("Goodbye.")
            break

        if not query:
            print("Please type a question.")
            continue

        # Retrieve — multi-query search from new retriever.py
        company_docs   = get_relevant_docs(company_db, query, k=12)
        framework_docs = framework_db.similarity_search(query, k=3)

        # Generate — Groq + Llama 3.1 with system prompt
        answer = generate_answer(query, company_docs, framework_docs)

        # Print answer
        print("\n" + "─" * 60)
        print(answer)
        print("─" * 60 + "\n")

        # Optional: still run your keyword rules on the answer
        warnings = check_esg_rules(answer)
        if warnings:
            print("ESG flags detected:")
            for w in warnings:
                print(" ", w)
            print()

if __name__ == "__main__":
    main()