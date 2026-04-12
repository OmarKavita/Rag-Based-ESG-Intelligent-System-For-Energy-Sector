
# def get_relevant_docs(db, query):
#     retriever = db.as_retriever(search_kwargs={"k": 6})

#     docs = retriever.invoke(query)

#     return docs


# # filtering company and gri dta
# def split_by_source(docs):
#     company_docs = []
#     framework_docs = []

#     for doc in docs:
#         if doc.metadata.get("source_type") == "company":
#             company_docs.append(doc)
#         elif doc.metadata.get("source_type") == "framework":
#             framework_docs.append(doc)

#     return company_docs, framework_docs

def get_relevant_docs(db, query):
    docs = db.similarity_search(query, k=20)  

    company_docs = [d for d in docs if d.metadata.get("source_type") == "company"]
    framework_docs = [d for d in docs if d.metadata.get("source_type") == "framework"]

    return company_docs, framework_docs