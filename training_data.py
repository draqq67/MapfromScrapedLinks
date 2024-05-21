from __future__ import unicode_literals, print_function
# import plac
import random
from pathlib import Path
import spacy
from tqdm import tqdm
import os
from spacy.training.example import Example

def product_label():
    product_labels = ["chair", "table", "led","bookcase","stool", "sofa", "bed", "lamp", "desk", "couch", "light", "furniture", "furnishing", ""]
    product_labels += ["shelf", "rug", "mirror", "bookcase", "ottoman", "stool", "bench", "cabinet", "wardrobe"]
    product_labels += ["dining table", "coffee table", "side table", "console table", "end table", "nightstand"]
    product_labels += ["dining chair", "armchair", "lounge chair", "recliner", "rocking chair", "accent chair"]
    product_labels += ["floor lamp", "table lamp", "desk lamp", "chandelier", "pendant light", "sconce", "flush mount"]
    product_labels += ["bed frame", "mattress", "headboard", "bedside table", "dresser", "chest of drawers", "wardrobe"]
    product_labels += ["sectional", "sofa bed", "loveseat", "ottoman", "chaise", "recliner", "sleeper sofa", "futon"]
    product_labels += ["rug", "runner", "area rug", "outdoor rug", "round rug", "shag rug", "wool rug", "jute rug"]
    product_labels += ["mirror", "wall mirror", "floor mirror", "vanity mirror", "round mirror", "oval mirror", "rectangle mirror"]
    product_labels += ["bookcase", "bookshelf", "etagere", "ladder bookcase", "corner bookcase", "wall mounted bookcase"]
    product_labels += ["stool", "counter stool", "bar stool", "adjustable stool", "swivel stool", "backless stool"]
    product_labels += ["bench", "entryway bench", "storage bench", "upholstered bench", "wooden bench", "metal bench"]
    product_labels += ["cabinet", "storage cabinet", "kitchen cabinet", "bathroom cabinet", "pantry cabinet", "bar cabinet"]
    product_labels += ["wardrobe", "closet", "armoire", "wardrobe closet", "wardrobe cabinet", "wardrobe armoire"]
    product_labels += ["dining table", "round dining table", "extendable dining table", "oval dining table", "square dining table"]
    product_labels += ["coffee table", "round coffee table", "oval coffee table", "square coffee table", "rectangle coffee table"]  
    product_labels += ["side table", "round side table", "oval side table", "square side table", "rectangle side table"]
    product_labels += ["console table", "narrow console table", "entryway console table", "hallway console table"]
    product_labels = [label for label in product_labels if label]
    return product_labels

# data_for_training()
def data_for_training():
    directory = "./text_from_links"
    product_labels = product_label()
    count = 0
    nlp = spacy.load("en_core_web_sm")
    train_data = []
    
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            print(f"Reading {file}")
            with open(f"{directory}/{file}", "r") as f: 
                lines = f.readlines()
                for line in lines:
                    words = line.split()
                    if len(words) < 100:
                        # Check if any word in the line is a product label
                        for word in words:
                            if word.lower() in product_labels:
                                train_data.append((line.strip(), {"entities": []}))  # Append the line to training data
                                break  
            count += 1
            if count == 25:
                break
                
    return train_data
def train_ner(train_data):
    # Load the blank English model
    nlp = spacy.blank("en")

    # Add the NER component to the pipeline
    ner = nlp.add_pipe("ner")
    ner.add_label("PRODUCT")

    # Prepare the training examples
    examples = []
    for text, annotations in train_data:
        examples.append(Example.from_dict(nlp.make_doc(text), annotations))

    # Shuffle the training data
    random.shuffle(examples)

    # Train the NER model
    nlp.begin_training()
    for i in range(10):  # You can adjust the number of iterations
        random.shuffle(examples)
        for batch in spacy.util.minibatch(examples, size=4):
            nlp.update(batch)

    return nlp

def main():
    train_data = data_for_training()
    print("Number of training examples:", len(train_data))
    print("Sample training examples:", train_data[:5])

    # Train the NER model
    nlp = train_ner(train_data)

    # Save the trained model
    nlp.to_disk("ner_model")

if __name__ == "__main__":
    #AIzaSyA7HVl51-Q-QWMotQfWU87ZEdCADSkpGU0
    main()