import spacy
from spacy.training.example import Example
import random
import json

# Load the annotations from the JSON file
with open("annotations_cleaned.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    print(f"Loaded {len(data)} annotations.")

# Prepare the training data
TRAIN_DATA = []
for item in data:
    text = item["text"]
    entities = [(ent["start"], ent["end"], ent["label"]) for ent in item["entities"]]
    TRAIN_DATA.append((text, {"entities": entities}))
    print(f"Text: {text}")

# Load a blank SpaCy model
nlp = spacy.blank("en")

# Add the NER pipeline if not already present
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")
else:
    ner = nlp.get_pipe("ner")

# Add labels to the NER pipeline
for _, annotations in TRAIN_DATA:
    for ent in annotations["entities"]:
        ner.add_label(ent[2])

# Disable other pipelines during training
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):
    optimizer = nlp.begin_training()
    for i in range(20):  # Number of training iterations
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in TRAIN_DATA:
            example = Example.from_dict(nlp.make_doc(text), annotations)
            nlp.update([example], drop=0.5, losses=losses)
        print(f"Iteration {i + 1}, Losses: {losses}")

# Save the trained model
nlp.to_disk("ner_model")
print("Model training complete. Saved to 'ner_model'.")