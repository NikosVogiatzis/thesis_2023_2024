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


# nlp = spacy.load("en_core_web_lg", disable=["ner"])
# ruler = nlp.add_pipe("entity_ruler")

# with open('web_scrap/txt_files/categories/substitution_sentences.txt', 'r', encoding='utf-8') as f:
#     text = f.read()

# # Define the regex pattern for player going in and out
# pattern = r"\.\s*([\w\s'-]+)\s+for\s+([\w\s'-]+)(?:\s*-\s*injury)?\."

# matches = re.findall(pattern, text)

# substitutions = [(inn.strip(), out.strip()) for inn, out in matches]

# print((substitutions))
# # Define EntityRuler patterns
# patterns = [
#     {"label": "PLAYER_IN", "pattern": player_in} for player_in, player_out in matches
# ] + [
#     {"label": "PLAYER_OUT", "pattern": player_out} for player_in, player_out in matches
# ]

# print(patterns)
#  # Add patterns to the EntityRuler
# ruler.add_patterns(patterns)
# doc = nlp(text)

# # TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
# # TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
# PLAYER_IN = [ent.text for ent in doc.ents if ent.label_ == "PLAYER_IN"]
# PLAYER_OUT = [ent.text for ent in doc.ents if ent.label_ == "PLAYER_OUT"]



# print(len(PLAYER_IN))
# print(len(PLAYER_OUT))


# nlp = spacy.load("en_core_web_lg", disable=["ner"])
# ruler = nlp.add_pipe("entity_ruler")


# sentences_new_attacking_attempt = []
# sentences_missed_chance = []
# sentences_shot_blocked = []
# sentences_hits_bar = []

# with open('web_scrap/txt_files/categories/attacking_attempt_sentences.txt', 'r', encoding='utf-8') as file:
#         for line in file:
#             if "New attacking attempt" in line:
#                 sentences_new_attacking_attempt.append(line.strip())
#             elif "Missed chance" in line:
#                 sentences_missed_chance.append(line.strip())
#             elif "Shot blocked" in line:
#                 sentences_shot_blocked.append(line.strip())
#             elif "hits" in line:
#                 sentences_hits_bar.append(line.strip())

# # ---------> Categorization in 4 type of sentences based on the format <----------
# #                           works fine!
# # print(len(sentences_new_attacking_attempt))
# # print(len(sentences_missed_chance))
# # print(len(sentences_shot_blocked))
# # print(len(sentences_hits_bar))


# pattern_time = r"\d+\+?\d*'"

# pattern_team = r"- ([^-]+) -"

# for sentence in sentences_new_attacking_attempt:
#     matches_team = re.findall(pattern_team, sentence)
#     matches_time = re.findall(pattern_time, sentence)
#     if matches_team and matches_time:
#         print("VOGIAS")
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