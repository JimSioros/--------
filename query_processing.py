import json
import unicodedata
from collections import defaultdict

# Load and normalize the inverted index
with open('inverted_index_geo.json', 'r', encoding='utf-8') as f:
    raw_inverted_index = json.load(f)

# Normalize keys for the inverted index
inverted_index = {}
for key, docs in raw_inverted_index.items():
    normalized_key = unicodedata.normalize('NFKD', key.strip().lower())
    inverted_index[normalized_key] = docs

# Query processing function
def process_query(query):
    if not any(op in query.lower() for op in ["and", "or", "not"]):
        normalized_query = unicodedata.normalize('NFKD', query.strip().lower())
        return [normalized_query]

    tokens = query.lower().strip().split()
    normalized_tokens = [unicodedata.normalize('NFKD', token.strip()) for token in tokens]
    return normalized_tokens

# Boolean operations
def boolean_and(set1, set2):
    return set1.intersection(set2)

def boolean_or(set1, set2):
    return set1.union(set2)

def boolean_not(set1, all_docs):
    return all_docs - set1

# Boolean query processing for the GEO dataset
def process_boolean_query(query, inverted_index):
    all_docs = set()

    # Collect all unique document identifiers
    for city, docs in inverted_index.items():
        if isinstance(docs, list):
            for doc in docs:
                if isinstance(doc, dict):
                    # Use city and state for unique identifiers
                    doc_id = f"{doc['date']} - {city.title()}, {doc['state']}"
                    all_docs.add(doc_id)

    tokens = process_query(query)

    # Stack for evaluation
    result_stack = []
    operators = []

    for token in tokens:
        if token in {"and", "or", "not"}:
            operators.append(token)
        else:
            # Retrieve postings list for the term
            posting_list = set()
            normalized_token = unicodedata.normalize('NFKD', token.strip().lower())

            # Find matching keys in the normalized inverted index
            for city, docs in inverted_index.items():
                if normalized_token in city:  # Match against the city name
                    for doc in docs:
                        if isinstance(doc, dict):
                            doc_id = f"{doc['date']} - {city.title()}, {doc['state']}"
                            posting_list.add(doc_id)

            result_stack.append(posting_list)

            # Handle the NOT operator immediately
            while operators and operators[-1] == "not":
                operators.pop()
                operand = result_stack.pop()
                result_stack.append(boolean_not(operand, all_docs))

    # Evaluate remaining operators (AND/OR)
    while operators:
        operator = operators.pop(0)
        operand1 = result_stack.pop(0)
        operand2 = result_stack.pop(0)

        if operator == "and":
            result_stack.append(boolean_and(operand1, operand2))
        elif operator == "or":
            result_stack.append(boolean_or(operand1, operand2))

    return result_stack[0] if result_stack else set()

# User interface for search
def query_interface():
    print("Boolean Query Search Engine for GEO Dataset")
    print("Enter your query using AND, OR, NOT (type 'exit' to quit):")
    while True:
        query = input("Query: ")
        if query.lower() == "exit":
            break
        results = process_boolean_query(query, inverted_index)
        print(f"Matching documents: {results}")

if __name__ == "__main__":
    query_interface()
