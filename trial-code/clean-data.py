import json

# Load the annotations
with open("annotations.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Remove duplicate entities
for item in data:
    unique_entities = []
    seen = set()
    for entity in item["entities"]:
        entity_tuple = (entity["start"], entity["end"], entity["label"])
        if entity_tuple not in seen:
            unique_entities.append(entity)
            seen.add(entity_tuple)
    item["entities"] = unique_entities

# Save the cleaned annotations
with open("annotations_cleaned.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print("Duplicates removed. Cleaned data saved to 'annotations_cleaned.json'.")