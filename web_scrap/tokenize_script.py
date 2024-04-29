import nltk
from nltk.tokenize import word_tokenize
import spacy

# Load SpaCy model for English
nlp = spacy.load("en_core_web_sm")

# Read text from file
with open('updated_data.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Tokenize text and perform named entity recognition using SpaCy
doc = nlp(text)

# Extract tokens and named entities
tokens = [token.text for token in doc]
entities = [(ent.text, ent.label_) for ent in doc.ents]

# print("Tokens:", tokens)
# print("Named Entities:", entities)

# Filter and print all PERSON entities
person_entities = [entity[0] for entity in entities if entity[1] == "PERSON"]
print("PERSON Entities:", person_entities)