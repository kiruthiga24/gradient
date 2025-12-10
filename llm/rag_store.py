import os
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

CHROMA_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

_embed = None

def embed_model():
    global _embed
    if _embed is None:
        _embed = SentenceTransformer(EMBEDDING_MODEL)
    return _embed

def client():
    return PersistentClient(path=CHROMA_DIR)  # Replaces Settings entirely

def collection():
    c = client()
    try:
        return c.get_collection("rag_docs")
    except:
        return c.create_collection("rag_docs")

def add_documents(docs, metadatas=None):
    col = collection()
    embeddings = embed_model().encode(docs).tolist()
    ids = [str(i) for i in range(len(docs))]
    col.add(ids=ids, documents=docs, metadatas=metadatas, embeddings=embeddings)
    return ids

def query_docs(query, k=4):
    emb = embed_model().encode([query])[0].tolist()
    col = collection()
    result = col.query(query_embeddings=[emb], n_results=k)
    docs = []
    if result["documents"]:
        for d, m in zip(result["documents"][0], result["metadatas"][0]):
            docs.append({"text": d, "metadata": m})
    return docs
