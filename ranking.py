import json
import unicodedata
from collections import defaultdict, Counter
import math

# Load and normalize the inverted index
with open('inverted_index_geo.json', 'r', encoding='utf-8') as f:
    raw_inverted_index = json.load(f)

# Normalize keys and tokenize words
inverted_index = defaultdict(list)
word_to_docs = defaultdict(set)

for city, docs in raw_inverted_index.items():
    normalized_city = unicodedata.normalize('NFKD', city.strip().lower())
    inverted_index[normalized_city] = docs

    for word in normalized_city.split():
        if isinstance(docs, list):
            for doc in docs:
                if isinstance(doc, dict):
                    doc_id = f"{doc['date']} - {city.title()}, {doc['state']}"
                    # Fix: Convert doc to a hashable tuple to avoid TypeError
                    word_to_docs[word].add((doc_id, tuple(doc.items())))
        elif isinstance(docs, dict):
            doc_id = f"{docs['date']} - {city.title()}, {docs['state']}"
            # Fix: Convert docs to a hashable tuple
            word_to_docs[word].add((doc_id, tuple(docs.items())))

# Compute TF-IDF
def compute_tf_idf(query, inverted_index, word_to_docs):
    """Calculate TF-IDF for ranking results."""
    total_docs = len(word_to_docs)
    normalized_query = unicodedata.normalize('NFKD', query.strip().lower())

    scores = defaultdict(float)
    for term in normalized_query.split():
        if term in word_to_docs:
            doc_list = word_to_docs[term]
            doc_frequency = len(doc_list)
            idf = math.log(total_docs / (1 + doc_frequency))

            for doc_id, doc_tuple in doc_list:
                scores[doc_id] += idf

    ranked_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_results

# Vector Space Model (VSM)
def compute_vsm(query, inverted_index, word_to_docs):
    """Calculate VSM for ranking results."""
    query_tokens = query.lower().strip().split()
    query_vector = Counter(query_tokens)

    doc_vectors = defaultdict(Counter)
    for term in query_tokens:
        if term in word_to_docs:
            for doc_id, doc_tuple in word_to_docs[term]:
                doc_vectors[doc_id][term] += 1

    scores = {}
    for doc_id, vector in doc_vectors.items():
        dot_product = sum(query_vector[t] * vector[t] for t in query_tokens)
        query_norm = math.sqrt(sum(q ** 2 for q in query_vector.values()))
        doc_norm = math.sqrt(sum(v ** 2 for v in vector.values()))
        scores[doc_id] = dot_product / (query_norm * doc_norm) if query_norm and doc_norm else 0

    ranked_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_results

# BM25
def compute_bm25(query, inverted_index, word_to_docs, k1=1.5, b=0.75):
    """Calculate BM25 for ranking results."""
    total_docs = len(word_to_docs)
    avg_doc_len = sum(len(docs) for docs in inverted_index.values()) / total_docs

    scores = defaultdict(float)
    query_tokens = query.lower().strip().split()

    for term in query_tokens:
        if term in word_to_docs:
            doc_list = word_to_docs[term]
            doc_frequency = len(doc_list)
            idf = math.log((total_docs - doc_frequency + 0.5) / (doc_frequency + 0.5) + 1)

            for doc_id, doc_tuple in doc_list:
                doc_len = len(doc_list)
                tf = 1
                scores[doc_id] += idf * ((tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_len / avg_doc_len))))

    ranked_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_results

# User interface for querying
def query_interface():
    print("Search Engine with Multiple Ranking Algorithms")
    print("Select Algorithm: 1) TF-IDF  2) VSM  3) BM25")
    while True:
        choice = input("Choice: ")
        if choice not in {"1", "2", "3"}:
            print("Invalid choice. Try again.")
            continue

        query = input("Query: ")
        if query.lower() == "exit":
            break

        if choice == "1":
            ranked_results = compute_tf_idf(query, inverted_index, word_to_docs)
        elif choice == "2":
            ranked_results = compute_vsm(query, inverted_index, word_to_docs)
        elif choice == "3":
            ranked_results = compute_bm25(query, inverted_index, word_to_docs)

        if ranked_results:
            print("Ranked Results:")
            for rank, (doc_id, score) in enumerate(ranked_results, start=1):
                print(f"{rank}. {doc_id} (Score: {score:.4f})")
                doc = next(doc for _id, doc in word_to_docs[query.split()[0]] if _id == doc_id)
                print(json.dumps(dict(doc), indent=4, ensure_ascii=False))
        else:
            print("No results found for your query.")

if __name__ == "__main__":
    query_interface()
