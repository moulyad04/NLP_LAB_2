# ==========================================
# INFORMATION RETRIEVAL SYSTEM
# ==========================================

import re
from collections import Counter


# ==========================================
# DOCUMENT COLLECTION / KNOWLEDGE BASE
# ==========================================

DOCUMENTS = [
    {
        "id": 1,
        "title": "India",
        "text": """
        India is a country in South Asia.
        Its capital is New Delhi.
        India is located in Asia.
        The currency of India is the Indian Rupee.
        """
    },
    {
        "id": 2,
        "title": "France",
        "text": """
        France is a country in Western Europe.
        Its capital is Paris.
        The currency of France is the Euro.
        """
    },
    {
        "id": 3,
        "title": "Germany",
        "text": """
        Germany is a country in Central Europe.
        Its capital city is Berlin.
        Germany uses the Euro as its currency.
        """
    },
    {
        "id": 4,
        "title": "Italy",
        "text": """
        Italy is a country in Southern Europe.
        Its capital is Rome.
        Italy uses the Euro as its currency.
        """
    },
    {
        "id": 5,
        "title": "Japan",
        "text": """
        Japan is an island country in East Asia.
        Its capital city is Tokyo.
        The currency of Japan is the Yen.
        """
    },
    {
        "id": 6,
        "title": "Python Programming",
        "text": """
        Python is a high-level programming language created by Guido van Rossum.
        It was first released in 1991.
        Python emphasizes code readability and simplicity.
        """
    }
]


def tokenize(text):
    """Clean and tokenize text into lowercase word tokens."""
    return re.findall(r"\b\w+\b", text.lower())


def calculate_jaccard_similarity(query_tokens, doc_tokens):
    """Compute Jaccard overlap between query and document tokens."""
    query_set = set(query_tokens)
    doc_set = set(doc_tokens)
    if not query_set or not doc_set:
        return 0.0
    intersection = query_set.intersection(doc_set)
    union = query_set.union(doc_set)
    return len(intersection) / len(query_set)


def retrieve_documents(query, top_k=3):
    """Retrieve top-k relevant documents based on lexical similarity score."""
    query_tokens = tokenize(query)
    scored_docs = []

    for doc in DOCUMENTS:
        doc_tokens = tokenize(doc["text"])
        score = calculate_jaccard_similarity(query_tokens, doc_tokens)
        scored_docs.append({
            "title": doc["title"],
            "score": round(score, 4),
            "text": doc["text"].strip()
        })

    # Sort descending by score
    scored_docs.sort(key=lambda x: x["score"], reverse=True)
    return scored_docs[:top_k]


if __name__ == "__main__":
    query = "capital currency of Germany and India"
    results = retrieve_documents(query, top_k=3)
    for res in results:
        print(f"Document: {res['title']}")
        print(f"Score: {res['score']}")
        print(f"Text: {res['text'][:120]}...\n")
