from ingestion.pdf_loader import load_pdfs_with_metadata
from ingestion.chunking import chunk_documents
from vectorstore.build_index import create_vectorstore
# from rag.retriever import get_relevant_docs, split_by_source
# from rag.retriever import get_relevant_docs
from rag.generator import generate_answer
from esg.rules import check_esg_rules


def main():
    print("Loading documents...")

    # Load -> Chunk
    documents = load_pdfs_with_metadata("data")
    chunks = chunk_documents(documents)

    # Split
    company_chunks = [c for c in chunks if c.metadata.get("source_type") == "company"]
    framework_chunks = [c for c in chunks if c.metadata.get("source_type") == "framework"]

    # Build DBs
    company_db = create_vectorstore(company_chunks)
    framework_db = create_vectorstore(framework_chunks)

    # Query
    query = input("Ask ESG question: ")

    # Retrieve
    company_docs = company_db.similarity_search(query, k=10)
    framework_docs = framework_db.similarity_search(query, k=5)

    # Generate
    answer = generate_answer(query, company_docs, framework_docs)



    print("\nANSWER:\n")
    print(answer)

    # ESG Rules
    warnings = check_esg_rules(answer)

    if warnings:
        print("\n ESG WARNINGS:\n")
        for w in warnings:
            print("-", w)
    else:
        print("\nNo major ESG issues detected")


if __name__ == "__main__":
    main()