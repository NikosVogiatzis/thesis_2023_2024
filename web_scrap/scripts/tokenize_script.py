# This file implements a simple keyword-based algorithm for categorizing each sentence from commentary.txt file 
# To a certain file for each category. Categories are decided based on the ontology entities on football.ttl (uploaded in github)

import spacy
import re

pattern_match_game = r"MATCH_+\d+"

with open('web_scrap/txt_files/commentary.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Tokenize the text into sentences
sentences = text.split('\n')

categories = {
    'corner' : ['corner -'],
    'penalty_procedure': ['penalty shootout', 'penalty saved', 'penalty missed', "120'\tGoal!"],
    'attacking_attempt' : ['Missed chance', 'attacking attempt', 'shot blocked', 'hits'],
    'goal': ['own goal', 'goal!'],
    'var_decision' : ['VAR '],
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


def assist_making_sentences():
    
    pattern_assist = r'\. Assist - (.+?)\.$'
    matches_assist_list = []
    goal_sentences = []
    with open('web_scrap/txt_files/categories/goal_sentences.txt', 'r', encoding='utf-8') as file:
        for line in file:
            if "Goal!" in line:
                goal_sentences.append(line.strip())

    

    for ind in range(len(goal_sentences)):
        if "Assist" in goal_sentences[ind]:
            matches_assist = re.findall(pattern_assist, goal_sentences[ind])
            match_game = re.findall(pattern_match_game, goal_sentences[ind])
            if matches_assist:  
                assist_text = matches_assist[0]  
                game = match_game[0]
                string_to_append = game + " " + " Assist - " + assist_text + ". Goal_Scored" + str(ind+1)
                matches_assist_list.append(string_to_append)

                

    print(len(matches_assist_list)) # Perfect           
    attacking_attempt_sentences = []
    with open('web_scrap/txt_files/categories/attacking_attempt_sentences.txt', 'r', encoding='utf-8') as file:
        for line in file:
            attacking_attempt_sentences.append(line.strip())

    for ind in range(len(attacking_attempt_sentences)):
        if "Assist" in attacking_attempt_sentences[ind]:
            matches_assist = re.findall(pattern_assist, attacking_attempt_sentences[ind])
            match_game = re.findall(pattern_match_game, attacking_attempt_sentences[ind])
            if matches_assist: 
                assist_text = matches_assist[0]  
                game = match_game[0]
                string_to_append = game+ " " + " Assist - " + assist_text +  ". Attacking_Attempt" + str(ind+1)
                matches_assist_list.append(string_to_append)
  
                        

    with open("web_scrap/txt_files/categories/assist_sentences.txt", 'w', encoding='utf-8') as file:
        for ind in range(len(matches_assist_list)):
            file.write(matches_assist_list[ind] + "\n")

assist_making_sentences()