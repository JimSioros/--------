import json

def load_inverted_index(file_path):
    """Load and normalize the inverted index from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        raw_index = json.load(file)
    # Normalize keys (city names) to lowercase
    normalized_index = {key.lower(): value for key, value in raw_index.items()}
    return normalized_index

def search_in_index(query, inverted_index):
    """Search the query in the inverted index."""
    query = query.lower().strip()  # Normalize the query
    results = []
    
    # Find matches for the query in the city keys
    for city, documents in inverted_index.items():
        if query in city:  # Partial match against city names
            results.extend(documents)
    return results

def simple_search_engine():
    """Simple user interface for searching the GEO dataset."""
    inverted_index = load_inverted_index('inverted_index_geo.json')  # Load the GEO inverted index

    print("GEO Dataset Search Engine")
    print("Search for anything or type 'exit' to quit.")
    
    while True:
        query = input("\nEnter your search query: ").strip()
        if query.lower() == "exit":
            print("Exiting the search engine...")
            break

        results = search_in_index(query, inverted_index)
        
        if results:
            print(f"Found {len(results)} result(s) for '{query}':")
            for result in results:
                # Display all fields in the result
                print(json.dumps(result, indent=4, ensure_ascii=False))
        else:
            print(f"No results found for '{query}'.")

if __name__ == "__main__":
    simple_search_engine()
