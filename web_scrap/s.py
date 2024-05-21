import re
import re
import spacy
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS
from spacy.pipeline.entityruler import EntityRuler
from spacy.tokens import Doc
import re
import urllib.parse
from collections import Counter

matches_assist_list = []
goal_sentences = []
with open('web_scrap/txt_files/categories/goal_sentences.txt', 'r', encoding='utf-8') as file:
        for line in file:
            if "Goal!" in line:
                goal_sentences.append(line.strip())

#print((goal_sentences))


pattern_time = r"\d+\+?\d*'" # for all sentences 
pattern_team = r" - (.+?) - " # for NEW_ATTACKING_ATTEMPT and MISSED_CHANCE 

pattern_assist = r'\. Assist - (.+?)\.$'

matches_time_list_goal = []
matches_team_list_goal = []

for sentence in goal_sentences:
    matches_team = re.findall(pattern_team, sentence)
    matches_time = re.findall(pattern_time, sentence)
    if matches_team and matches_time:
        desired_time = matches_time[0]
        desired_team = matches_team[0]
        matches_time_list_goal.append(desired_time)
        matches_team_list_goal.append(desired_team)
        #print(desired_time, '  ', desired_team)

print(len(matches_time_list_goal))
print(len(matches_team_list_goal))

for ind in range(len(goal_sentences)):
    if "Assist" in goal_sentences[ind]:
        matches_assist = re.findall(pattern_assist, goal_sentences[ind])
        if matches_assist:  # Check if matches_assist is not empty
            assist_text = matches_assist[0]  # Access the first element of the list
            string_to_append = matches_time_list_goal[ind] + " Assist - " + assist_text + ". " +  " - " + matches_team_list_goal[ind] + ". Goal"
            matches_assist_list.append(string_to_append)
        else:
            # If no match found, append an empty string
            matches_assist_list.append("")
print(len(matches_assist_list))            

with open("web_scrap/txt_files/categories/assist_sentences.txt", 'a', encoding='utf-8') as file:
    for ind in range(len(matches_assist_list)):
        file.write(matches_assist_list[ind] + "\n")