import os
import uuid
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DIR = os.path.join(BASE_DIR, "..", "chroma_db")
CHROMA_DIR = os.path.abspath(CHROMA_DIR)

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
COLLECTION_NAME = "rag_docs"

_embed = None
_client = None

def embed_model():
    global _embed
    if _embed is None:
        _embed = SentenceTransformer(EMBEDDING_MODEL)
    return _embed

def client():
    global _client
    if _client is None:
        print("✅ Using Chroma path:", CHROMA_DIR)
        _client = PersistentClient(path=CHROMA_DIR)
    return _client

def collection():
    c = client()

    # show collections for debugging
    existing = [x.name for x in c.list_collections()]
    print("✅ Existing collections:", existing)

    try:
        return c.get_collection(COLLECTION_NAME)
    except:
        print("✅ Creating collection:", COLLECTION_NAME)
        return c.create_collection(COLLECTION_NAME)

def add_documents(docs, metadatas=None):
    col = collection()

    embeddings = embed_model().encode(docs).tolist()
    ids = [str(uuid.uuid4()) for _ in docs]

    col.add(
        ids=ids,
        documents=docs,
        metadatas=metadatas,
        embeddings=embeddings
    )

    print(f"✅ Inserted {len(docs)} docs")
    return ids

def query_docs(query, k=4, use_case=None):
    col = collection()

    print("✅ TOTAL DOC COUNT:", col.count())

    emb = embed_model().encode([query])[0].tolist()

    where = {"use_case": use_case} if use_case else None

    result = col.query(
        query_embeddings=[emb],
        n_results=k,
        where=where
    )

    docs = []
    if result["documents"]:
        for d, m in zip(result["documents"][0], result["metadatas"][0]):
            docs.append({"text": d, "metadata": m})

    return docs
