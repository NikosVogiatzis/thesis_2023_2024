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
from collections import Counter

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

    print(len(TEAM))
    print(len(PLAYER))
    print((TIME_STAMP))
    print("\n\n")

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


    print(len(TEAM))
    print(len(PLAYER_IN))
    print(len(TIME_STAMP))
    print(len(PLAYER_OUT))
    print("\n\n")

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

    print(len(TEAM))
    print(len(PLAYER))
    print(len(TIME_STAMP))
    print("\n\n")

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

    print(len(TEAM))
    print(len(PLAYER))
    print(len(TIME_STAMP))
    print("\n\n")
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
    
    print(len(TEAM))
    print(len(PLAYER))
    print(len(TIME_STAMP))
    print(len(AT_PLACE))
    print("\n\n")

    return 1, PLAYER, TEAM, AT_PLACE, TIME_STAMP


def foul_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
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

    print(len(TEAM))
    print(len(PLAYER))
    print(len(TIME_STAMP))
    print("\n\n")

    return 1, PLAYER, TEAM,  TIME_STAMP


def dangerous_play_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
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

    print(len(TEAM))
    print(len(PLAYER))
    print(len(TIME_STAMP))
    print("\n\n")

    return 1, PLAYER, TEAM,  TIME_STAMP

def penalty_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")


    with open("web_scrap/txt_files/categories/penalty_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    # Define the regex patterns
    
    
    pattern_players1 = r"\.\s(.*?)(?=\sdraws)"    
    pattern_players2 = r"by\s(.*?)\s-"
    

    pattern_teams1 = r"Penalty\s+(?!conceded)(.*?)\."
    pattern_teams2 = r"\-\s(.*?)\s\-"

    pattern_time = r"\b\d+(?:'\s+\d+)?'"


    # Find matches in each sentence based on regexes above.
    
    matches_teams1 = re.findall(pattern_teams1, text)
    matches_teams2 = re.findall(pattern_teams2, text)
    matches_time = re.findall(pattern_time, text)

    matches_players1 = re.findall(pattern_players1, text)
    matches_players2 = re.findall(pattern_players2, text)


    print(matches_players1)
    print(matches_players2)
    print(matches_teams1)
    print(matches_teams2)
    print(matches_time)
    # Combine teams from both patterns into a single list
    matches_teams = matches_teams1 + matches_teams2
    # print(matches_teams)
    # print("\n\n\n")
    # print(len(matches_teams))
    # print(matches_players1)
    # print("\n\n")
    # print(matches_players2)
    # print("\n\n")
    # print(matches_teams1)
    # print("\n\n")
    # print(matches_teams2)
    # print("\n\n")
    # print(matches_time)
    # print("\n\n")
    # Define EntityRuler patterns
    patterns = [
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [
        {"label": "TEAM", "pattern": team} for team in matches_teams
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



def attacking_attempt_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")


    with open("web_scrap/txt_files/categories/attacking_attempt_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    # Define the regex pattern
    # Define the regex pattern
    pattern_players = r'\.\s*([^-.]+)\s*-\s*'

    matches_players = []
    # Find and print the extracted names for each sentence
    sentences = text.split('\n')
    for sentence in sentences:
        match = re.search(pattern_players, sentence)
        if match:
            name = match.group(1)
            if name.lower() != "assist":  # Exclude "Assist"
                matches_players.append(name.strip())

    print(matches_players)
    

    
    pattern_teams = r'-\s*([^-.]+)\s*-\s*' #se merika teams pou to onoma prin exei dash buggarei
    pattern_time = r"\b\d+(?:'\s+\d+)?'"
    matches_teams = re.findall(pattern_teams, text)
    matches_time = re.findall(pattern_time, text)

    print(len(matches_teams))
    print(len(matches_time))
    with open("sentences.txt", 'w', encoding='utf-8') as f:
        for ent in matches_players:
            f.write(ent + "\n")
    print((len(matches_players)))
    return 1,1,1,1,1
    # Find matches in each sentence based on regexes above.
    
    

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


def yellow_card_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open("web_scrap/txt_files/categories/yellow card_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    # Define the regex pattern 
    pattern_teams = r"- (.*?)\-"
    pattern_players = r"'(.*?)\-"
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

    print(len(TEAM))
    print(len(PLAYER))
    print(len(TIME_STAMP))
    print("\n\n")

    return 1, TEAM, PLAYER,  1,TIME_STAMP

def delay_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    sentences_no_injury = []
    sentences_injury = []
    sentences_over = []
    with open('web_scrap/txt_files/categories/delay_sentences.txt', 'r', encoding='utf-8') as file:
        for line in file:
            if "over" in line:
                sentences_over.append(line.strip())
            elif "injury" in line:
                sentences_injury.append(line.strip())
            else:
                sentences_no_injury.append(line.strip())

    pattern_time = r"\d+\+?\d*'"
    pattern_team_no_injury = r"-\s(.+)"
    pattern_team_injury = r"(?:.*?-){2}\s*(.*)"
    pattern_player_injury = r"-\s+(?:injury\s+)?([^-.]+)"


    match_time_no_injury = []
    match_time_injury = []
    match_time_over = []

    match_team_no_injury = []
    match_team_injury = []

    match_player_injury = []

    for sentence in sentences_no_injury:
            match_team = re.search(pattern_team_no_injury, sentence)
            match_time = re.search(pattern_time, sentence)
            if match_team:
                match_team_no_injury.append(match_team.group(1))
            
            if match_team: 
                match_time_no_injury.append(match_time.group(0))


    for sentence in sentences_injury:
            match_team = re.search(pattern_team_injury, sentence)
            match_time = re.search(pattern_time, sentence)
            match_player = re.search(pattern_player_injury, sentence)
            if match_player:
                match_player_injury.append(match_player.group(1))
            if match_team:
                match_team_injury.append(match_team.group(1))

            if match_team: 
                match_time_injury.append(match_time.group(0))

    for sentence in sentences_over:
        match_time = re.search(pattern_time, sentence)
        if match_time:
            match_time_over.append(match_time.group(0))

    patterns = [
        {"label": "TIME", "pattern": time} for time in match_time_injury + match_time_no_injury + match_time_over
    ] + [
        {"label": "TEAM", "pattern": team} for team in match_team_injury + match_team_no_injury
    ] + [
        {"label": "PLAYER", "pattern": player} for player in match_player_injury 
    ]

    ruler.add_patterns(patterns)

    text1 = '\n'.join(sentences_no_injury)
    doc1 = nlp(text1)

    text2 = '\n'.join(sentences_injury)
    doc2 = nlp(text2)

    text3 = '\n'.join(sentences_over)
    doc3 = nlp(text3)

    TIME_IN_MATCH = [ent.text for ent in doc1.ents if ent.label_ == "TIME"]
    TIME_INJURY = [ent.text for ent in doc2.ents if ent.label_ == "TIME"]
    TIME_OVER = [ent.text for ent in doc3.ents if ent.label_ == "TIME"]

    TEAM_IN_MATCH = [ent.text for ent in doc1.ents if ent.label_ == "TEAM"]
    TEAM_INJURY = [ent.text for ent in doc2.ents if ent.label_ == "TEAM"]

    PLAYER_INJURY = [ent.text for ent in doc2.ents if ent.label_ == "PLAYER"]


    print(len(TIME_IN_MATCH))
    print(len(TEAM_IN_MATCH))
    print("-----------------------")

    print(len(TIME_INJURY))
    print(len(TEAM_INJURY))
    print(len(PLAYER_INJURY))

    print("-----------------------")

    print(len(TIME_OVER))




def first_half_end_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open("web_scrap/txt_files/categories/first_half_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    # Define the regex pattern 
    pattern_score = r"ended\s*-\s*(.+)"
    pattern_time = r"\d+\+?\d*'"

    # Find matches in each sentence based on regexes above.
    matches_score = re.findall(pattern_score, text)
    matches_time = re.findall(pattern_time, text)
    # Define EntityRuler patterns
    patterns = [
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [
        {"label": "SCORE", "pattern": score} for score in matches_score
    ]

    # Add patterns to the EntityRuler
    ruler.add_patterns(patterns)
    doc = nlp(text)

    SCORE = [ent.text for ent in doc.ents if ent.label_ == "SCORE"]
    TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]

    print(len(SCORE))
    print(len(TIME_STAMP))
    print("\n\n")

    return 1, SCORE, TIME_STAMP
def second_half_sentences_ner():
    sentences_begin = []
    sentences_end = []
    with open('web_scrap/txt_files/categories/second_half_sentences.txt', 'r', encoding='utf-8') as file:
        for line in file:
            if "starts" in line:
                sentences_begin.append(line.strip())
            elif "ended" in line:
                sentences_end.append(line.strip())
            

    # Define regex patterns
    pattern_start_score = r"starts\s*(.*)"
    pattern_end_score = r"ended -\s*(.*)"
    pattern_time_begin = r"\d+\+?\d*'"
    pattern_time_end = r"\d+\+?\d*'"

    # Initialize lists to store matches
    matches_score_begin = []
    matches_time_begin = []
    matches_score_end = []
    matches_time_end = []

    # Extract matches for "starts" sentences
    for sentence in sentences_begin:
        match_score = re.search(pattern_start_score, sentence)
        match_time = re.search(pattern_time_begin, sentence)
        if match_score:
            matches_score_begin.append(match_score.group(1))
        if match_time:
            matches_time_begin.append(match_time.group(0))

    # Extract matches for "ended" sentences
    for sentence in sentences_end:
        match_score = re.search(pattern_end_score, sentence)
        match_time = re.search(pattern_time_end, sentence)
        if match_score:
            matches_score_end.append(match_score.group(1))
        if match_time:
            matches_time_end.append(match_time.group(0))


    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")
    # Define EntityRuler patterns
    patterns = [
            {"label": "TIME", "pattern": time} for time in matches_time_end + matches_time_begin
        ] + [
            {"label": "SCORE", "pattern": team} for team in matches_score_begin + matches_score_end
    ]

    ruler.add_patterns(patterns)

    text1 = '\n'.join(sentences_begin)
    doc1 = nlp(text1)

    text2 = '\n'.join(sentences_end)
    doc2 = nlp(text2)

    TIME_BEGIN = [ent.text for ent in doc1.ents if ent.label_ == "TIME"]
    TIME_END = [ent.text for ent in doc2.ents if ent.label_ == "TIME"]
    SCORE_BEGIN = [ent.text for ent in doc1.ents if ent.label_ == "SCORE"]
    SCORE_END = [ent.text for ent in doc2.ents if ent.label_ == "SCORE"]
    # print(len(TIME_BEGIN))
    # print(len(SCORE_BEGIN))
    # print("-----------------------")
    # print(len(TIME_END))
    # print(len(SCORE_END))



def extra_time_first_half_ner():
    sentences_begin = []
    sentences_end = []
    with open('web_scrap/txt_files/categories/extra_time_first_half_sentences.txt', 'r', encoding='utf-8') as file:
        for line in file:
            if "begins" in line:
                sentences_begin.append(line.strip())
            elif "ends" in line:
                sentences_end.append(line.strip())

    # Define regex patterns
    pattern_start_score = r"begins\s*(.*)"
    pattern_end_score = r"ends -\s*(.*)"
    pattern_time_begin = r"\d+\+?\d*'"
    pattern_time_end = r"\d+\+?\d*'"

    # Initialize lists to store matches
    matches_score_begin = []
    matches_time_begin = []
    matches_score_end = []
    matches_time_end = []

    # Extract matches for "starts" sentences
    for sentence in sentences_begin:
        match_score = re.search(pattern_start_score, sentence)
        match_time = re.search(pattern_time_begin, sentence)
        if match_score:
            matches_score_begin.append(match_score.group(1))
        if match_time:
            matches_time_begin.append(match_time.group(0))

    # Extract matches for "ended" sentences
    for sentence in sentences_end:
        match_score = re.search(pattern_end_score, sentence)
        match_time = re.search(pattern_time_end, sentence)
        if match_score:
            matches_score_end.append(match_score.group(1))
        if match_time:
            matches_time_end.append(match_time.group(0))


    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")
    # Define EntityRuler patterns
    patterns = [
            {"label": "TIME", "pattern": time} for time in matches_time_end + matches_time_begin
        ] + [
            {"label": "SCORE", "pattern": team} for team in matches_score_begin + matches_score_end
    ]

    ruler.add_patterns(patterns)

    text1 = '\n'.join(sentences_begin)
    doc1 = nlp(text1)

    text2 = '\n'.join(sentences_end)
    doc2 = nlp(text2)

    TIME_BEGIN = [ent.text for ent in doc1.ents if ent.label_ == "TIME"]
    TIME_END = [ent.text for ent in doc2.ents if ent.label_ == "TIME"]
    SCORE_BEGIN = [ent.text for ent in doc1.ents if ent.label_ == "SCORE"]
    SCORE_END = [ent.text for ent in doc2.ents if ent.label_ == "SCORE"]


    print(len(TIME_BEGIN))
    print(len(SCORE_BEGIN))
    print("-----------------------")
    print(len(TIME_END))
    print(len(SCORE_END))

def extra_time_second_half_ner():
    sentences_begin = []
    sentences_end = []
    with open('web_scrap/txt_files/categories/extra_time_second_half_sentences.txt', 'r', encoding='utf-8') as file:
        for line in file:
            if "begins" in line:
                sentences_begin.append(line.strip())
            elif "ends" in line:
                sentences_end.append(line.strip())

    # Define regex patterns
    pattern_start_score = r"begins\s*(.*)"
    pattern_end_score = r"ends -\s*(.*)"
    pattern_time_begin = r"\d+\+?\d*'"
    pattern_time_end = r"\d+\+?\d*'"

    # Initialize lists to store matches
    matches_score_begin = []
    matches_time_begin = []
    matches_score_end = []
    matches_time_end = []

    # Extract matches for "starts" sentences
    for sentence in sentences_begin:
        match_score = re.search(pattern_start_score, sentence)
        match_time = re.search(pattern_time_begin, sentence)
        if match_score:
            matches_score_begin.append(match_score.group(1))
        if match_time:
            matches_time_begin.append(match_time.group(0))

    # Extract matches for "ended" sentences
    for sentence in sentences_end:
        match_score = re.search(pattern_end_score, sentence)
        match_time = re.search(pattern_time_end, sentence)
        if match_score:
            matches_score_end.append(match_score.group(1))
        if match_time:
            matches_time_end.append(match_time.group(0))


    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")
    # Define EntityRuler patterns
    patterns = [
            {"label": "TIME", "pattern": time} for time in matches_time_end + matches_time_begin
        ] + [
            {"label": "SCORE", "pattern": team} for team in matches_score_begin + matches_score_end
    ]

    ruler.add_patterns(patterns)

    text1 = '\n'.join(sentences_begin)
    doc1 = nlp(text1)

    text2 = '\n'.join(sentences_end)
    doc2 = nlp(text2)

    TIME_BEGIN = [ent.text for ent in doc1.ents if ent.label_ == "TIME"]
    TIME_END = [ent.text for ent in doc2.ents if ent.label_ == "TIME"]
    SCORE_BEGIN = [ent.text for ent in doc1.ents if ent.label_ == "SCORE"]
    SCORE_END = [ent.text for ent in doc2.ents if ent.label_ == "SCORE"]


    print((TIME_BEGIN))
    print((SCORE_BEGIN))
    print("-----------------------")
    print((TIME_END))
    print((SCORE_END))


def end_game_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open('web_scrap/txt_files/categories/end_game_sentences.txt', 'r', encoding='utf-8') as file:
        text = file.read()


    pattern_score = r" - \s*(.*)"
    matches_score = re.findall(pattern_score, text)

    # Define EntityRuler patterns
    patterns = [
            {"label": "SCORE", "pattern": team} for team in matches_score
    ]

    ruler.add_patterns(patterns)
    doc = nlp(text)

    SCORE = [ent.text for ent in doc.ents if ent.label_ == "SCORE"]
    print((SCORE))

    return END_GAME, SCORE


# CORNER, TEAM, PLAYER, TIME_STAMP = corner_ner() # Perfect
# HANDBALL, PLAYER, TEAM, TIME_STAMP = hand_ball_ner() # Perfect
# OFFSIDE, PLAYER, TEAM, TIME_STAMP = offside_ner() # Perfect
# FOUL, PLAYER, TEAM, TIME_STAMP = foul_ner() # Perfect
# DANEROUS_PLAY, PLAYER, TEAM, TIME_SAMP = dangerous_play_ner() # Perfect
# YELLOW_CARD, PLAYER, TEAM, FOR, TIME_STAMP = yellow_card_ner() # Perfect
# RED_CARD, PLAYER, TEAM, FOR, TIME_STAMP = red_card_ner() # Perfect
# FIRST_HALF_ENDED, SCORE, TIME_STAMP = first_half_end_ner() # Perfect
# second_half_sentences_ner() # Perfect
# extra_time_first_half_ner() # Perfect
# extra_time_second_half_ner() # Perfect
# END_GAME, SCORE = end_game_ner() # Perfect
# delay_ner() # Perfect



# These ones dont work correctly so it is TODO 
# --------------- &***&*&*&---------------------
# PENALTY, PLAYER, TEAM, TIME_STAMP = penalty_ner()
# ATTACKING_ATTEMPT, PLAYER, TEAM, WAY, TIME_STAMP = attacking_attempt_ner()
# SUBSTITUTION, TEAM, PLAYER_IN, PLAYER_OUT, TIME_STAMP = substitution_ner() #θελει να το ξαναδω
# GOAL
# --------------- &***&*&*&---------------------



