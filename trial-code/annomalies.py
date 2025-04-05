import spacy
from spacy.training import offsets_to_biluo_tags
import json

# Load the SpaCy language model
nlp = spacy.blank("en")

# Load the annotations
with open("annotations.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Check for overlapping or duplicate entities
for item in data:
    text = item["text"]
    entities = [(ent["start"], ent["end"], ent["label"]) for ent in item["entities"]]
    try:
        doc = nlp.make_doc(text)
        biluo_tags = offsets_to_biluo_tags(doc, entities)
    except Exception as e:
        print(f"Error in text: {text}")
        print(f"Entities: {entities}")
        print(f"Error: {e}")