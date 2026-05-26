# vectorstore/build_index.py
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

def create_vectorstore(chunks, save_path=None):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # If a saved index exists, load it instead of rebuilding
    if save_path and os.path.exists(save_path):
        print(f"Loading existing index from {save_path}...")
        db = FAISS.load_local(save_path, embeddings, 
                              allow_dangerous_deserialization=True)
        return db

    # Otherwise build fresh and save
    db = FAISS.from_documents(chunks, embeddings)

    if save_path:
        db.save_local(save_path)
        print(f"Index saved to {save_path}")

    return db