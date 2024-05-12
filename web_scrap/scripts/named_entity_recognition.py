"""
    In this file NER (Named Entity Recognition) is implemented. For each category, we open the file and read the content. After that, we define patterns 
    that will match the desired text to get annotated as entity. This is implemented mainly based on regular expression, because most of the sentences have a certain 
    format. All NER for each category happens in a seperate function for each category/entity of ontology.
    We are using spacy and entityRuler to make our custom entities.

"""


import spacy
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS
from spacy.pipeline.entityruler import EntityRuler
import re
import urllib.parse


def corner_ner():

    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")


    with open("web_scrap/txt_files/categories/corner_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    sentences = text.split('\n')

    # Define the regex pattern 
    pattern_time = r"\b\d+(?:'\s+\d+)?'"
    pattern_teams = r"\d+'\s+Corner - (.*?)\."
    pattern_players = r"Conceded by ([\w'\-]+(?:\s+[\w'\-]+)*)\."
    
    # Find matches in each sentence based on regexes above.
    matches_teams = re.findall(pattern_teams, text)
    matches_players = re.findall(pattern_players, text)
    matches_time = re.findall(pattern_time, text)

    # EntityRuler patterns
    patterns = [   
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [    
        {"label": "TEAM", "pattern": team} for team in matches_teams
    ] + [
        {"label": "PLAYER", "pattern": player} for player in matches_players
    ]

    # Add patterns to the EntityRuler
    ruler.add_patterns(patterns)
    doc = nlp(text)

    # Define list for each entity in its category
    TEAM = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "TIME"]

    # print(len(TEAM))
    # print(len(PLAYER))
    # print(len(TIME_STAMP))
    # print("\n\n")

    return 1, TEAM, PLAYER, TIME_STAMP



def substitution_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open("web_scrap/txt_files/categories/substitution_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    # Define the regex pattern 
    pattern_time = r"\b\d+(?:'\s+\d+)?'"
    pattern_teams = r"\d+'\s+Substitution - (.*?)\."
    pattern_substitution = r"\.\s*([\w'\-]+(?:\s+[\w'\-]+)*)\s+for\s+([\w'\-]+(?:\s+[\w'\-]+)*)\."

    # Find matches in each sentence based on regexes above.
    matches_teams = re.findall(pattern_teams, text)
    matches_substitutions = re.findall(pattern_substitution, text)
    matches_players_in = [player_in for _, player_in in matches_substitutions]
    matches_players_out = [player_out for player_out, _ in matches_substitutions]
    matches_time = re.findall(pattern_time, text)

    # Define EntityRuler patterns
    patterns = [
        {"label": "TEAM", "pattern": team} for team in matches_teams   
    ] + [    
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [
        {"label": "PLAYER_IN", "pattern": player_in} for player_in in matches_players_in
    ] + [
        {"label": "PLAYER_OUT", "pattern": player_out} for player_out in matches_players_out
    ]

    # Add patterns to the EntityRuler
    ruler.add_patterns(patterns)
    doc = nlp(text)


    TEAM = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "TIME"]
    PLAYER_IN = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "PLAYER_IN"]
    PLAYER_OUT = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "PLAYER_OUT"]


    # print(len(TEAM))
    # print(len(PLAYER_IN))
    # print(len(TIME_STAMP))
    # print(len(PLAYER_OUT))
    # print("\n\n")

    return 1, TEAM, PLAYER_IN, PLAYER_OUT,TIME_STAMP



def hand_ball_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open("web_scrap/txt_files/categories/hand_ball_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    # Define the regex pattern 
    pattern_teams = r"- (.*)\n"
    pattern_players = r"by\s+(.*?)\s+-"
    pattern_time = r"\b\d+(?:'\s+\d+)?'"

    # Find matches in each sentence based on regexes above.
    matches_teams = re.findall(pattern_teams, text)
    matches_players = re.findall(pattern_players, text)
    matches_time = re.findall(pattern_time, text)

    # Define EntityRuler patterns
    patterns = [
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [
        {"label": "TEAM", "pattern": team} for team in matches_teams
    ] + [
        {"label": "PLAYER", "pattern": player} for player in matches_players
    ]

    # Add patterns to the EntityRuler
    ruler.add_patterns(patterns)
    doc = nlp(text)

    TEAM = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "TIME"]

    # print(len(TEAM))
    # print(len(PLAYER))
    # print(len(TIME_STAMP))
    # print("\n\n")

    return 1, TEAM, PLAYER, TIME_STAMP


def offside_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open("web_scrap/txt_files/categories/offside_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    # Define the regex pattern
    pattern_teams = r"- (.*?)\."
    pattern_players = r"\.\s+(\w+(?:\s+\w+)*)\s+(?:is|with)\b"
    pattern_time = r"\b\d+(?:'\s+\d+)?'"

    # Find matches in each sentence based on regexes above.
    matches_teams = re.findall(pattern_teams, text)
    matches_players = re.findall(pattern_players, text)
    matches_time = re.findall(pattern_time, text)

    # Define EntityRuler patterns
    patterns = [
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [
        {"label": "TEAM", "pattern": team} for team in matches_teams
    ] + [
        {"label": "PLAYER", "pattern": player} for player in matches_players
    ]
 
    # Add patterns to the EntityRuler
    ruler.add_patterns(patterns)
    doc = nlp(text)

    TEAM = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "TIME"]

    # print(len(TEAM))
    # print(len(PLAYER))
    # print(len(TIME_STAMP))
    # print("\n\n")
    return 1, PLAYER, TEAM, TIME_STAMP


def free_kick_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open("web_scrap/txt_files/categories/free kick_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    # Define the regex pattern
    pattern_players = r"\d+'\s+(.*?)\s+-\s+"
    pattern_teams = r"-\s+([^-.]+-)"
    pattern_places = r"kick\s+(.*?)\."
    pattern_time = r"\b\d+(?:'\s+\d+)?'"

    # Find matches in each sentence based on regexes above.
    matches_players = re.findall(pattern_players, text)
    matches_teams = re.findall(pattern_teams, text)
    matches_places = re.findall(pattern_places, text)
    matches_time = re.findall(pattern_time, text)    

    # Define EntityRuler patterns
    patterns = [
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [
        {"label": "TEAM", "pattern": team} for team in matches_teams
    ] + [
        {"label": "PLAYER", "pattern": player} for player in matches_players
    ] + [
        {"label": "AT_PLACE", "pattern": place} for place in matches_places    
    ]

    # Add patterns to the EntityRuler
    ruler.add_patterns(patterns)
    doc = nlp(text)


    TEAM = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "TIME"]
    AT_PLACE = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "AT_PLACE"]
    
    # print(len(TEAM))
    # print(len(PLAYER))
    # print(len(TIME_STAMP))
    # print(len(AT_PLACE))
    # print("\n\n")

    return 1, PLAYER, TEAM, AT_PLACE, TIME_STAMP


def foul_ner():
    nlp = spacy.load("en_core_web_sm", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")


    with open("web_scrap/txt_files/categories/foul_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    # Define the regex pattern
    pattern_players = r"by\s+(.*?)\s+-"
    pattern_teams = r"-\s+([A-Za-z\s]+)\s"
    pattern_time = r"\b\d+(?:'\s+\d+)?'"

    # Find matches in each sentence based on regexes above.
    matches_players = re.findall(pattern_players, text)
    matches_teams = re.findall(pattern_teams, text)
    matches_time = re.findall(pattern_time, text)

    # Define EntityRuler patterns
    patterns = [
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [
        {"label": "TEAM", "pattern": team} for team in matches_teams
    ] + [
        {"label": "PLAYER", "pattern": player} for player in matches_players   
    ]

    # Add patterns to the EntityRuler
    ruler.add_patterns(patterns)
    doc = nlp(text)

    TEAM = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "TIME"]

    # print(len(TEAM))
    # print(len(PLAYER))
    # print(len(TIME_STAMP))
    # print("\n\n")

    return 1, PLAYER, TEAM,  TIME_STAMP


def dangerous_play_ner():
    nlp = spacy.load("en_core_web_sm", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")


    with open("web_scrap/txt_files/categories/dangerous_play_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    # Define the regex pattern
    pattern_players = r"by\s(.*?)\s-"
    pattern_teams = r"\-\s(.*)"
    pattern_time = r"\b\d+(?:'\s+\d+)?'"

    # Find matches in each sentence based on regexes above.
    matches_players = re.findall(pattern_players, text)
    matches_teams = re.findall(pattern_teams, text)
    matches_time = re.findall(pattern_time, text)

    # Define EntityRuler patterns
    patterns = [
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [
        {"label": "TEAM", "pattern": team} for team in matches_teams
    ] + [
        {"label": "PLAYER", "pattern": player} for player in matches_players   
    ]

    # Add patterns to the EntityRuler
    ruler.add_patterns(patterns)
    doc = nlp(text)

    TEAM = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "TIME"]

    # print(len(TEAM))
    # print(len(PLAYER))
    # print(len(TIME_STAMP))
    # print("\n\n")

    return 1, PLAYER, TEAM,  TIME_STAMP

def penalty_ner():
    nlp = spacy.load("en_core_web_sm", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")


    with open("web_scrap/txt_files/categories/penalty_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    # Define the regex patterns
    
    pattern_players2 = r"by\s(.*?)\s-"
    pattern_players1 = r"\.\s(.*?)\sdraws"

    pattern_teams1 = r"Penalty\s+(?!conceded)(.*?)\."
    pattern_teams2 = r"\-\s(.*?)\s\-"

    pattern_time = r"\b\d+(?:'\s+\d+)?'"


    # Find matches in each sentence based on regexes above.
    matches_players1 = re.findall(pattern_players1, text)
    matches_players2 = re.findall(pattern_players2, text)
    matches_teams1 = re.findall(pattern_teams1, text)
    matches_teams2 = re.findall(pattern_teams2, text)
    matches_time = re.findall(pattern_time, text)

    # Combine teams from both patterns into a single list
    matches_teams = matches_teams1 + matches_teams2
    print(matches_teams)
    print("\n\n\n")
    print(len(matches_teams))
    print(matches_players1)
    print("\n\n")
    print(matches_players2)
    print("\n\n")
    print(matches_teams1)
    print("\n\n")
    print(matches_teams2)
    print("\n\n")
    print(matches_time)
    print("\n\n")
    # Define EntityRuler patterns
    patterns = [
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [
        {"label": "TEAM", "pattern": team} for team in matches_teams1 + matches_teams2
    ] + [
        {"label": "PLAYER", "pattern": player} for player in matches_players1 + matches_players2   
    ]

    # Add patterns to the EntityRuler
    ruler.add_patterns(patterns)
    doc = nlp(text)

    TEAM = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [urllib.parse.quote(ent.text.replace(" ", "_")) for ent in doc.ents if ent.label_ == "TIME"]

    print("Number of TEAM entities:", len(TEAM))
    print("Number of PLAYER entities:", len(PLAYER))
    print("Number of TIME entities:", len(TIME_STAMP))
    # print("\n\n")

    return 1, PLAYER, TEAM,  TIME_STAMP

# CORNER, TEAM, PLAYER, TIME_STAMP = corner_ner()
# SUBSTITUTION, TEAM, PLAYER_IN, PLAYER_OUT, TIME_STAMP = substitution_ner() #θελει να το ξαναδω
# HANDBALL, PLAYER, TEAM, TIME_STAMP = hand_ball_ner()
# OFFSIDE, PLAYER, TEAM, TIME_STAMP = offside_ner()
# FREE_KICK, PLAYER, TEAM, AT_PLACE, TIME_STAMP = free_kick_ner()
# FOUL, PLAYER, TEAM, TIME_STAMP = foul_ner()
# DANEROUS_PLAY, PLAYER, TEAM, TIME_SAMP = dangerous_play_ner()



# This one doesnt work correctly so it is TODO 
#PENALTY, PLAYER, TEAM, TIME_STAMP = penalty_ner()



