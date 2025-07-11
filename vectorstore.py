import os
import chromadb
from typing import List, Dict, Any, Optional
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = chromadb.PersistentClient("./data")
embedding_function = OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY, model_name="text-embedding-3-small")

def vectorize_documents(collection_name: str, documents: List[str]) -> None:
    final_documents = []
    for doc in documents:
        final_documents.append({"content": doc, "source": doc})

        normalized_doc = doc.strip().lower()
        final_documents.append({"content": normalized_doc, "source": doc})

        stop_words = {"of", "and", "the", "for", "in", "on", "at", "to", "a", "an"}
        important_words = [w for w in normalized_doc.split() if w not in stop_words]
        important_words = " ".join(important_words)

        final_documents.append({"content": important_words, "source": doc})

    collection = client.get_or_create_collection(
        name=f"{collection_name}__vectorized",
        embedding_function=embedding_function
    )
    collection.add(
        documents=[final_documents[i]["content"] for i in range(len(final_documents))],
        metadatas=[{"source": doc["source"]} for doc in final_documents],
        ids=[str(i) for i in range(len(final_documents))],
    )


def query(
    collection_name: str, query_text: str, limit: int = 5
) -> List[Dict[str, Any]]:
    collection = client.get_collection(name=f"{collection_name}__vectorized", embedding_function=embedding_function)
    results = collection.query(query_texts=query_text, n_results=limit)
    filtered_results = [
        (metadata["source"], dist)
        for doc, dist, metadata in zip(
            results["documents"][0], results["distances"][0], results["metadatas"][0]
        )
    ]
    return filtered_results
