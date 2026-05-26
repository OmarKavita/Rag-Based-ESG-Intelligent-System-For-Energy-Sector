import os
from langchain_community.document_loaders import PyPDFLoader


def load_pdfs_with_metadata(base_path):
    documents = []

    # Load Company Reports 
    company_path = os.path.join(base_path, "reports")

    for file in os.listdir(company_path):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(company_path, file))
            docs = loader.load()

            for doc in docs:
                doc.metadata["source_type"] = "company"
                doc.metadata["file_name"] = file

            documents.extend(docs)

    # Load GRI Frameworks 
    framework_path = os.path.join(base_path, "frameworks")

    for file in os.listdir(framework_path):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(framework_path, file))
            docs = loader.load()

            for doc in docs:
                doc.metadata["source_type"] = "framework"
                doc.metadata["file_name"] = file

            documents.extend(docs)

    return documents

# docss = load_pdfs_with_metadata("data")
# company_docss = [doc for doc in docss if doc.metadata.get("source_type") =="company"]
# print(company_docss[1])