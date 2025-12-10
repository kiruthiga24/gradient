from chromadb import PersistentClient


client = PersistentClient(path="./chroma_db")
collection = client.get_collection("rag_docs")

print("Total docs:", collection.count())


def debug_rag(query: str):
    from chromadb import PersistentClient

    client = PersistentClient(path="./chroma_db")
    collection = client.get_collection("rag_docs")

    print("📦 Total docs:", collection.count())

    results = collection.query(
        query_texts=[query],
        n_results=5,
        where={'use_case': 'churn'}
    )

    print("🎯 Query:", query)

    print("✅ Results:", results)

# debug_rag("test")


def debug_print_docs():
    from chromadb import PersistentClient

    client = PersistentClient(path="./chroma_db")
    collection = client.get_collection("rag_docs")
    data = collection.get(include=["metadatas", "documents"])
    for i, m in enumerate(data["metadatas"][:]):
        print(i, m)

debug_print_docs()

