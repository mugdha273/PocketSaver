import spacy
import nltk
from nltk.tokenize import word_tokenize

def makeJson(text):
    output = {}
    # Load the spaCy model
    nlp = spacy.load("en_core_web_sm")

    # Process the text
    doc = nlp(text)

    # Tokenize the text
    tokens = word_tokenize(text)

    # POS tag the tokens
    tagged_tokens = nltk.pos_tag(tokens)

    # Extract the price
    price = ""
    for token in doc:
        if token.like_num:
            price = token.text
            break

    # Extract the name
    name = ""
    for token, tag in tagged_tokens:
        if tag == "NNS":
            name = token
            break
        if tag == "NN":
            name = token
            break

    output["name"] = name
    output["price"] = price

    return output
