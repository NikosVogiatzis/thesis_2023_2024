# This file implements a simple keyword-based algorithm for categorizing each sentence from commentary.txt file 
# To a certain file for each category. Categories are decided based on the ontology entities on football.ttl (uploaded in github)

import spacy


with open('web_scrap/txt_files/commentary.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Tokenize the text into sentences
sentences = text.split('\n')

categories = {
    'corner' : ['corner -'],
    'penalty_procedure': ['penalty shootout', 'penalty saved', 'penalty missed', 'converts'],
    'attacking_attempt' : ['Missed chance', 'attacking attempt', 'shot blocked', 'hits'],
    'referee' : ['referee', 'VAR '],
    'goal': ['own goal', 'goal!'],
    'yellow card': ['yellow card'],
    'red card': ['red card'],
    'penalty' : ['penalty'],
    'substitution' : ['substitution'],
    'offside' : ['offside'],
    'foul' : ['fouled'],
    'free kick' : ['free kick'],
    'extra_time_first_half' : ['first half extra time'],
    'extra_time_second_half' : ['second half extra time'],
    'first_half' : ['first half'],
    'second_half' : ['second half'],
    'delay' : ['delay'],
    'hand_ball' : ['hand ball'],
    'end_game' : ['game finished'],
    'dangerous_play' : ['dangerous play'],
    'Other': [] 
}

# dictionary to store categorized sentences
categorized_sentences = {category: [] for category in categories}

# Function to categorize sentences
def categorize_sentence(sentence):
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in sentence.lower(): 
                return category
    return 'Other'

# Categorize each sentence
for sentence in sentences:
    category = categorize_sentence(sentence)
    categorized_sentences[category].append(sentence)


# Write the results to a file for each category
for category, sentences in categorized_sentences.items():
    with open(f'web_scrap/txt_files/categories/{category}_sentences.txt', 'w', encoding='utf-8') as output_file:
        for sentence in sentences:
            output_file.write(f"{sentence}\n")
