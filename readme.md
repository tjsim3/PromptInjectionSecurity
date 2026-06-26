**How to use**
This is a tool that runs in the CLI. Install numpy, and type commands in the terminal using python <script> <arguments>


**train.py**
Trains the model based on data inputted

Usage: python train.py argument

train.py takes one of 3 inputs:
- clear: deletes generated data, and the currently stored model
- generate: uses riskgenerator.py and benigngenerator.py to generate random samples of prompts to train the neural network
- trainingfile.jsonl: takes in any number of jsonl file and trains on the file. The jsonl format should look like: 
{"text": "prompt", "label": 1 or 0} (1 for a prompt injection attack, 0 for a benign prompt)


**main.py**
Takes in a text input and passes it to the neural network which will predict of the prompt is a prompt injection attack or a benign prompt

Usage: python main.py "prompt"


**Workflow**
First entry point: main.py

- The main() loop reads the arguments provided by the user. It can take in a string in quotes, or it can join arguments to a single string
- Sets model and vectorizer by calling load_resources() from predict.py, which loads SimpleNN and  Vectorizer() objects
- Calls score_text() from predict.py, passing the prompt, and the model and vectorizer which were retrieved in the previous step. 
    score_text():
    - transforms text to vectors using the vectorizer
    - runs the text through the actual neural network which returns an array of probabilities
    - returns the first value in the array as a float
    - scores the prompt based on keywords passed in config.py
    - finally returns risk_score, nn_score and rule_score which is equal to nn_score * weight (set in CONFIG) + rule_score * weight 
- Determines risk level (HIGH, MEDIUM, LOW) based on thresholds provided in CONFIG
- Prints the result in json format


Second entry point: train.py

- The main() loops read arguments provided, and based on those it chooses one of three options:
    1. clear: deletes any datasets generated, and the model files. 
    2. .jsonl file: trains the dataset on the provided file path
    3. generate: generates a randomized jsonl file from the generator scripts and trains the model on those
- Training workflow begins by loading text and labels from the .jsonl file
- Initializes a Vectorizer and an array of labels
- Initializes SimpleNN using parameters provided in CONFIG
- Trains the model on the dataset 
- Saves the model and vocab.json
- Calculates and prints accuracy


Third optional entry point: benigngenerator.py and riskgenerator.py

    These scripts can be run on their own, however they are automated in the training process so it is not recommended