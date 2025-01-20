import json
from collections import defaultdict

# Load the JSON file
with open("pah_wikp_combo_pro.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Create an inverted index
inverted_index = defaultdict(list)

for idx, record in enumerate(data):
    city = record["City"]
    state = record["State"]
    location_key = f"{record['Date']} - {city}, {state}"

    # Add to the inverted index
    inverted_index[city].append({
        "state": state,
        "date": record["Date"],
        "area_type": record["AreaType"],
        "school": record["School"],
        "fatalities": record["Fatalities"],
        "wounded": record["Wounded"],
        "duplicate": record["Dupe"],
        "source": record["Source"],
        "description": record["Desc"]
    })

# Save the inverted index to a file
with open("inverted_index_geo.json", "w", encoding="utf-8") as outfile:
    json.dump(inverted_index, outfile, ensure_ascii=False, indent=4)

print("The inverted index has been created and saved to inverted_index_geo.json.")
