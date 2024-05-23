"""
    In this file NER (Named Entity Recognition) is implemented. For each category, we open the file and read the content. After that, we define patterns 
    that will match the desired text to get annotated as entity. This is implemented mainly based on regular expression, because most of the sentences have a certain 
    format. All NER for each category happens in a seperate function for each category/entity of ontology.
    We are using spacy and entityRuler to make our custom entities.

"""
from rdflib.plugins.sparql import prepareQuery
from owlready2 import get_ontology
from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS, OWL
from urllib.parse import quote 
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
    pattern_time = r"\d+\+?\d*'"
    pattern_teams = r"Corner - (.*?)\."
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
    
    TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    LABELS = []
    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])

    print(len(LABELS))
    print(len(TEAM))
    print(len(PLAYER))
    print(len(TIME_STAMP))
    print("\n\n")

    return LABELS, TEAM, PLAYER, TIME_STAMP



def substitution_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open("web_scrap/txt_files/categories/substitution_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    sentences = text.split('\n')
    # Define the regex pattern 
    pattern_time = r"\d+\+?\d*'"
    pattern_teams = r"Substitution - (.*?)\."
    pattern_substitution = r"\.\s*([\w'\-]+(?:\s+[\w'\-]+)*)\s+for\s+([\w'\ - ]+(?:\s+[\w'\ - ]+)*)(?=\s*[\.-]|\s*$)"



    # Find matches in each sentence based on regexes above.
    matches_teams = re.findall(pattern_teams, text)
    matches_substitutions = re.findall(pattern_substitution, text)
    matches_players_in = [player_in.split(' - ')[0] for _, player_in in matches_substitutions]
    matches_players_out = [player_out.split(' - ')[0]+" for" for player_out, _ in matches_substitutions]
    matches_time = re.findall(pattern_time, text)

    # Define EntityRuler patterns
    patterns = [
        {"label": "PLAYER_OUT", "pattern": player_out} for player_out in matches_players_out

    ] + [    
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [
        {"label": "PLAYER_IN", "pattern": player_in} for player_in in matches_players_in
    ] + [
        {"label": "TEAM", "pattern": team} for team in matches_teams   
    ]

    # Add patterns to the EntityRuler
    ruler.add_patterns(patterns)
    doc = nlp(text)


    TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    PLAYER_IN = [ent.text for ent in doc.ents if ent.label_ == "PLAYER_IN"]
    PLAYER_OUT = [ent.text for ent in doc.ents if ent.label_ == "PLAYER_OUT"]
    PLAYER_OUT = [player[:-4] if player.endswith(" for") else player for player in PLAYER_OUT]

    LABELS = []
    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])

    print(len(TEAM))
    print(len(PLAYER_IN))
    print(len(TIME_STAMP))
    print(len(PLAYER_OUT))
    print(len(LABELS))
    print("\n\n")
      
    return LABELS, TEAM, PLAYER_IN, PLAYER_OUT,TIME_STAMP



def hand_ball_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open("web_scrap/txt_files/categories/hand_ball_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    sentences = text.split('\n')
    # Define the regex pattern 
    pattern_teams = r"- (.*)\n"
    pattern_players = r"by\s+(.*?)\s+-"
    pattern_time = r"\d+\+?\d*'"

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

    TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    LABELS = []
    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])


    print(len(TEAM))
    print(len(PLAYER))
    print(len(TIME_STAMP))
    print("\n\n")

    return LABELS, TEAM, PLAYER, TIME_STAMP


def offside_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open("web_scrap/txt_files/categories/offside_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    sentences = text.split('\n')
    # Define the regex pattern
    pattern_teams = r"- (.*?)\."
    pattern_players = r'(?:(?:.*?\.\s*([^.,]+?)\s*is in offside)|(?:,\s*(?:however\s+)?([^.,]+?)\s*is in offside))'
    pattern_time = r"\d+\+?\d*'"

    # Find matches in each sentence based on regexes above.
    matches_teams = re.findall(pattern_teams, text)
    matches_players = re.findall(pattern_players, text)
    matches_players = [player+" is" for match in matches_players for player in match if player]

    matches_time = re.findall(pattern_time, text)
    print("sasasa -> ", matches_players)
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

    TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    PLAYER = [player.replace("is", "").rstrip() for player in PLAYER]
    TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    
    LABELS = []
    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])
    print(len(TEAM))
    print(len(PLAYER))
    print(len(TIME_STAMP))
    print("\n\n")
    return LABELS, PLAYER, TEAM, TIME_STAMP


def free_kick_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open("web_scrap/txt_files/categories/free kick_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()
    sentences = text.split('\n')
    # Define the regex pattern
    pattern_players = r"'\s+(.*?)\s+-\s+"
    pattern_teams = r"-\s+([^-.]+-)"
    pattern_places = r"kick\s+(.*?)\."
    pattern_time = r"\d+\+?\d*'"

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


    TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
    TEAM = [team.replace(" -", "").rstrip() for team in TEAM] 
    PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    AT_PLACE = [ent.text for ent in doc.ents if ent.label_ == "AT_PLACE"]
    
    LABELS = []
    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])

    print((TEAM))
    print((PLAYER))
    print((TIME_STAMP))
    print((AT_PLACE))
    print("\n\n")

    return LABELS, PLAYER, TEAM, AT_PLACE, TIME_STAMP


def foul_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    
    with open("web_scrap/txt_files/categories/foul_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()
    
    sentences = text.split('\n')
    # Define the regex pattern
    pattern_players = r"by\s+(.*?)\s+-"
    pattern_teams = r"-\s+([A-Za-z\s]+)\s"
    pattern_time = r"\d+\+?\d*'"

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

    TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    
    LABELS = []
    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])
    print(len(TEAM))
    print(len(PLAYER))
    print(len(TIME_STAMP))
    print("\n\n")

    return LABELS, PLAYER, TEAM,  TIME_STAMP


def dangerous_play_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")


    with open("web_scrap/txt_files/categories/dangerous_play_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    sentences = text.split('\n')
    # Define the regex pattern
    pattern_players = r"by\s(.*?)\s-"
    pattern_teams = r"\-\s(.*)"
    pattern_time = r"\d+\+?\d*'"

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

    TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    LABELS = []
    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])

    print(len(TEAM))
    print(len(PLAYER))
    print(len(TIME_STAMP))
    # print(len(DANGEROUS_PLAY))
    print("\n\n")

    return LABELS, PLAYER, TEAM,  TIME_STAMP

def penalty_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    sentences_conceded = []
    sentences_simple = []
    with open('web_scrap/txt_files/categories/penalty_sentences.txt', 'r', encoding='utf-8') as file:
        for line in file:
            if "conceded" in line:
                sentences_conceded.append(line.strip())
            else:
                sentences_simple.append(line.strip())

    print(len(sentences_simple))


    pattern_time = r"\d+\+?\d*'"

    pattern_players_simple = r"\.\s+(.*?)\s+draws"    
    pattern_players_conceded = r"by\s(.*?)\s-"

    matches_players_simple = []
    matches_players_conceded = []    
    matches_time = []

    pattern_teams_simple = r"Penalty\s+([\w\s]+)\."
    pattern_teams_conceded = r"\s-\s(.*?)\s-\s"

    matches_teams_simple = []
    matches_teams_conceded = []

    for sentence in sentences_simple:
        match_player = re.search(pattern_players_simple, sentence)
        match_team = re.search(pattern_teams_simple, sentence)
        match_time = re.search(pattern_time, sentence)
        if match_team:
            matches_teams_simple.append(match_team.group(1))
                
        if match_player: 
            matches_players_simple.append(match_player.group(1))

        if match_time:
            matches_time.append(match_time.group(0))

    for sentence in sentences_conceded:
        match_player = re.search(pattern_players_conceded, sentence)
        match_team = re.search(pattern_teams_conceded, sentence)
        match_time = re.search(pattern_time, sentence)
        if match_team:
            matches_teams_conceded.append(match_team.group(1))
                
        if match_player: 
            matches_players_conceded.append(match_player.group(1))

        if match_time:
            matches_time.append(match_time.group(0))


    patterns = [
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [
        {"label": "TEAM", "pattern": team} for team in matches_teams_conceded + matches_teams_simple
    ] + [
        {"label": "PLAYER", "pattern": player} for player in matches_players_conceded + matches_players_simple
    ]

    # Add patterns to the EntityRuler
    ruler.add_patterns(patterns)
    with open('web_scrap/txt_files/categories/penalty_sentences.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    sentences = text.split('\n')    
    doc = nlp(text)

    TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    LABELS = []
    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])

    print("Number of TEAM entities:", len(TEAM))
    print("Number of PLAYER entities:", len(PLAYER))
    print("Number of TIME entities:", len(TIME_STAMP))
    print("\n\n")

    return LABELS, PLAYER, TEAM,  TIME_STAMP



def attacking_attempt_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")


    sentences_new_attacking_attempt = [] # 1'	New attacking attempt. Leroy Sané - FC Bayern München - shot with left foot from a diffucult position on the left is saved by goalkeeper in the centre of the goal. Assist - Harry Kane with a through ball.
    sentences_missed_chance = [] # 7'	Missed chance. Leroy Sané - FC Bayern München - shot with left foot from the left side of the box goes high. Assist - Harry Kane following a fast break.
    sentences_shot_blocked = [] # 30'	Shot blocked. Leon Goretzka - FC Bayern München - shot with right foot from the centre of the box is blocked. Assist - Jamal Musiala.
    sentences_hits_bar = [] # 85'	Memphis Depay - Atletico Madrid - hits the left post with a shot with right foot from the centre of the box. Assist - Koke.


    with open('web_scrap/txt_files/categories/attacking_attempt_sentences.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if "New attacking attempt" in line:
                    sentences_new_attacking_attempt.append(line.strip())
                elif "Missed chance" in line:
                    sentences_missed_chance.append(line.strip())
                elif "Shot blocked" in line:
                    sentences_shot_blocked.append(line.strip())
                elif "hits" in line:
                    sentences_hits_bar.append(line.strip())

    matches_time_list_new_attacking_attempt = [] 
    matches_team_list_new_attacking_attempt = []

    matches_time_list_missed_chance = []
    matches_team_list_missed_chance = []


    matches_time_list_shot_blocked = []
    matches_team_list_shot_blocked = []

    matches_time_list_hits_bar = []
    matches_team_list_hits_bar = []


    matches_assist_list = []


    pattern_time = r"\d+\+?\d*'" # for all sentences 
    pattern_team = r"- ([^-]+) -" # for NEW_ATTACKING_ATTEMPT and MISSED_CHANCE 

    pattern_assist = r'\. Assist - (.+?)\.$'


    # -----------------> NEW ATTACKING ATTEMPT <----------------------------

    for sentence in sentences_new_attacking_attempt:
        matches_team = re.findall(pattern_team, sentence)
        matches_time = re.findall(pattern_time, sentence)
        if matches_team and matches_time:
            desired_time = matches_time[0]
            desired_team = matches_team[0]
            matches_time_list_new_attacking_attempt.append(desired_time)
            matches_team_list_new_attacking_attempt.append(desired_team)



    # -----------------> NEW ATTACKING ATTEMPT <----------------------------

    # ----------------> MISSED CHANCE <------------------------------

    for sentence in sentences_missed_chance:
        matches_team = re.findall(pattern_team, sentence)
        matches_time = re.findall(pattern_time, sentence)
        if matches_team and matches_time:
            desired_time = matches_time[0]
            desired_team = matches_team[0]
            matches_time_list_missed_chance.append(desired_time)
            matches_team_list_missed_chance.append(desired_team)



    # ----------------> MISSED CHANCE <------------------------------


    # ---------------> SHOT BLOCKED <----------------------------------

    for sentence in sentences_shot_blocked:
        matches_team = re.findall(pattern_team, sentence)
        matches_time = re.findall(pattern_time, sentence)
        if matches_team and matches_time:
            desired_time = matches_time[0]
            desired_team = matches_team[0]
            matches_time_list_shot_blocked.append(desired_time)
            matches_team_list_shot_blocked.append(desired_team)


    # ---------------> SHOT BLOCKED <----------------------------------



    # ----------------> HITS BAR <---------------------------------------

    for sentence in sentences_hits_bar:
        matches_team = re.findall(pattern_team, sentence)
        matches_time = re.findall(pattern_time, sentence)
        if matches_team and matches_time:
            desired_time = matches_time[0]
            desired_team = matches_team[0]
            matches_time_list_hits_bar.append(desired_time)
            matches_team_list_hits_bar.append(desired_team)

    # ----------------> HITS BAR <---------------------------------------


    # --------------> Από εδώ και κάτω γίνεται το NER για τα Attacking Attempts.         
    with open('web_scrap/txt_files/categories/attacking_attempt_sentences.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Process each line to remove the "Assist - [Player Name]" part
    processed_lines = []
    for line in lines:
        cleaned_line = re.sub(r' Assist - [\w\s]+\.?', '', line)
        cleaned_line2 = re.sub(r'\.\-(\w+)', '', cleaned_line)
        processed_lines.append(cleaned_line2)  

    text = ''.join(processed_lines)
    sentences = text.split('\n')  
    pattern_way_of_attempt = r" - .*? - (.*?)\."
    pattern_player = r"\. (.*?)(?=\s* - \s*)"

    matches_player_no_hits_bar = []
    matches_players_hits_bar = []
    matches_time_list = re.findall(pattern_time, text)

    text_without_hits_bar = sentences_missed_chance + sentences_new_attacking_attempt + sentences_shot_blocked


    for ind in (text_without_hits_bar):
        matches = re.findall(pattern_player, ind)
        if matches:
            player = matches[0]
            matches_player_no_hits_bar.append(player)

    pattern_player_hits_bar = r"\d+'\s+(.*?)(?=\s*-\s*(?![^\s-]+-))"


    for ind in (sentences_hits_bar):
        matches = re.findall(pattern_player_hits_bar, ind)
        if matches:
            player = matches[0]
            matches_players_hits_bar.append(player)

    matches_teams = matches_team_list_new_attacking_attempt + matches_team_list_shot_blocked + matches_team_list_missed_chance + matches_team_list_hits_bar

    all_sentences = text_without_hits_bar + sentences_hits_bar

    matches_way_of_attempt_list = []

    for sentence in processed_lines:
        match = re.search(pattern_way_of_attempt, sentence)
        if match:
            matches_way_of_attempt_list.append(match.group(1).strip())
        else:
            print("No match found")

    patterns = [
        {"label": "TIME", "pattern": time} for time in matches_time_list
    ] + [
        {"label": "TEAM", "pattern": team} for team in matches_teams
    ] + [
        {"label": "PLAYER", "pattern": player} for player in matches_players_hits_bar +   matches_player_no_hits_bar
    ] + [
        {"label": "WAY_OF_ATTEMPT", "pattern": way} for way in matches_way_of_attempt_list        

    ]

    ruler.add_patterns(patterns)
    doc = nlp("\n".join(processed_lines))

    TIME = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    WAY_OF_ATTEMPT = [ent.text for ent in doc.ents if ent.label_ == "WAY_OF_ATTEMPT"]
    LABELS = []
    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])
    print("sssss")
    print(len(TIME))
    print(len(TEAM))
    print(len(PLAYER))
    print(len(WAY_OF_ATTEMPT))
    print("\n\n")


    return LABELS, PLAYER, TEAM,  TIME, WAY_OF_ATTEMPT


def card_ner(card_type):
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    if card_type == "yellow":
        with open("web_scrap/txt_files/categories/yellow card_sentences.txt", 'r', encoding='utf-8') as f:
            text = f.read()
            sentences = text.split('\n')
    elif card_type == "red":
        with open("web_scrap/txt_files/categories/red card_sentences.txt", 'r', encoding='utf-8') as f:
            text = f.read()
            sentences = text.split('\n')

    # Define the regex pattern 
    pattern_teams = r"- (.*?)\-"
    pattern_players = r"'(.*?)\-"
    pattern_time = r"\d+\+?\d*'"

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

    TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [ent.text.strip() for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    if card_type == "yellow":
        YELLOW_CARD = ["YELLOW_CARD" + str(i+1) for i in range(len(TEAM))] 
    elif card_type == "red":
        RED_CARD = ["RED_CARD" + str(i+1) for i in range(len(TEAM))] 


    if card_type == "yellow":
        print(len(TEAM))
        print((PLAYER))
        print(len(TIME_STAMP))
        print("\n\n")
        LABELS = []
        for i in range(len(sentences)-1):
            LABELS.append(sentences[i])
        return LABELS, TEAM, PLAYER, TIME_STAMP
    elif card_type == "red":
        print(len(TEAM))
        print((PLAYER))
        print(len(TIME_STAMP))
        print("\n\n")
        LABELS = []
        for i in range(len(sentences)-1):
            LABELS.append(sentences[i])
        return LABELS, TEAM, PLAYER, TIME_STAMP

    

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
            
            if match_time: 
                match_time_no_injury.append(match_time.group(0))


    for sentence in sentences_injury:
            match_team = re.search(pattern_team_injury, sentence)
            match_time = re.search(pattern_time, sentence)
            match_player = re.search(pattern_player_injury, sentence)
            if match_player:
                match_player_injury.append(match_player.group(1))
            if match_team:
                match_team_injury.append(match_team.group(1))

            if match_time: 
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

    LABELS_1 = []
    for i in range(len(sentences_no_injury)):
        LABELS_1.append(sentences_no_injury[i])

    LABELS_2 = []
    for i in range(len(sentences_injury)):
        LABELS_2.append(sentences_injury[i])


    LABELS_3 = []
    for i in range(len(sentences_over)):
        LABELS_3.append(sentences_over[i])        
    print(len(TIME_IN_MATCH))
    print(len(TEAM_IN_MATCH))
    print("-----------------------")

    print(len(TIME_INJURY))
    print(len(TEAM_INJURY))
    print((PLAYER_INJURY))


    print("-----------------------")

    print(len(TIME_OVER))

    return LABELS_1, TIME_IN_MATCH, TIME_INJURY, TIME_OVER, TEAM_IN_MATCH, TEAM_INJURY, PLAYER_INJURY, \
        LABELS_2, LABELS_3
    

def first_half_end_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open("web_scrap/txt_files/categories/first_half_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    sentences = text.split('\n')
    # print(sentences)
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
    LABELS = []
    for i in range(1,len(sentences),2):
        LABELS.append(sentences[i])
    print(len(SCORE))
    print(len(TIME_STAMP))
    print(len(LABELS))
    print("\n\n")

    return LABELS, SCORE, TIME_STAMP

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
    LABELS_1 = []
    for i in range(0,len(sentences_begin)):
        LABELS_1.append(sentences_begin[i])

    SCORE_BEGIN = [ent.text for ent in doc1.ents if ent.label_ == "SCORE"]
    SCORE_END = [ent.text for ent in doc2.ents if ent.label_ == "SCORE"]
    LABELS_2 = []
    for i in range(0,len(sentences_end)):
        LABELS_2.append(sentences_end[i])

    print(len(LABELS_1))
    print(len(TIME_BEGIN))
    print(len(SCORE_BEGIN))
    print("-----------------------")
    print(len(LABELS_2))
    print(len(TIME_END))
    print(len(SCORE_END))

    return LABELS_1, TIME_BEGIN, SCORE_BEGIN, LABELS_2, TIME_END, SCORE_END

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
    LABELS_1 = []
    for i in range(0,len(sentences_begin)):
        LABELS_1.append(sentences_begin[i])

    SCORE_BEGIN = [ent.text for ent in doc1.ents if ent.label_ == "SCORE"]
    SCORE_END = [ent.text for ent in doc2.ents if ent.label_ == "SCORE"]
    LABELS_2 = []
    for i in range(0,len(sentences_end)):
        LABELS_2.append(sentences_end[i])

    print(len(LABELS_1))
    print(len(TIME_BEGIN))
    print(len(SCORE_BEGIN))
    print("-----------------------")
    print(len(LABELS_2))
    print(len(TIME_END))
    print(len(SCORE_END))

    return LABELS_1, TIME_BEGIN, SCORE_BEGIN, LABELS_2, TIME_END, SCORE_END

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
    LABELS_1 = []
    for i in range(0,len(sentences_begin)):
        LABELS_1.append(sentences_begin[i])

    SCORE_BEGIN = [ent.text for ent in doc1.ents if ent.label_ == "SCORE"]
    SCORE_END = [ent.text for ent in doc2.ents if ent.label_ == "SCORE"]
    LABELS_2 = []
    for i in range(0,len(sentences_end)):
        LABELS_2.append(sentences_end[i])


    print(len(TIME_BEGIN))
    print(len(SCORE_BEGIN))
    print("-----------------------")
    print(len(TIME_END))
    print(len(SCORE_END))

    return LABELS_1, TIME_BEGIN, SCORE_BEGIN, LABELS_2, TIME_END, SCORE_END

def end_game_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open('web_scrap/txt_files/categories/end_game_sentences.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    sentences = text.split('\n')
    pattern_score = r" - \s*(.*)"
    matches_score = re.findall(pattern_score, text)

    # Define EntityRuler patterns
    patterns = [
            {"label": "SCORE", "pattern": team} for team in matches_score
    ]

    ruler.add_patterns(patterns)
    doc = nlp(text)

    SCORE = [ent.text for ent in doc.ents if ent.label_ == "SCORE"]
    LABELS = []
    for i in range(1,len(sentences),2):
        LABELS.append(sentences[i])
    print(len(SCORE))

    return LABELS, SCORE

def goal_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    matches_assist_list = []
    goal_sentences = []
    own_goal_sentences = []
    with open('web_scrap/txt_files/categories/goal_sentences.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if "Goal!" in line:
                    goal_sentences.append(line.strip())

                else:
                    own_goal_sentences.append(line.strip())

    # print(own_goal_sentences)
    # print((goal_sentences))


    pattern_time = r"\d+\+?\d*'" # for all sentences 
    pattern_team = r" - (.+?) - " # for NEW_ATTACKING_ATTEMPT and MISSED_CHANCE 
    pattern_player = r'\.\s([^-.]+)'
    pattern_score = r"\!\s([^..]+)"
    pattern_assist = r'\. Assist - (.+?)\.$'
    pattern_way_of_scoring = r"- [^-]* - ([^.]+)\."
    matches_time_list_goal = []
    matches_team_list_goal = []
    matches_player_list_goal = []
    matches_score_list_goal = []
    matches_way_of_scoring = []

    for sentence in goal_sentences:
        matches_team = re.findall(pattern_team, sentence)
        matches_time = re.findall(pattern_time, sentence)
        matches_player = re.findall(pattern_player, sentence)
        matches_score = re.findall(pattern_score, sentence)
        matches_way = re.findall(pattern_way_of_scoring, sentence)

        if matches_team and matches_time and matches_player and matches_score and matches_way:
            desired_time = matches_time[0]
            desired_team = matches_team[0]
            desired_player = matches_player[0]
            desired_score = matches_score[0]
            desired_way = matches_way[0]

            matches_time_list_goal.append(desired_time.strip())
            matches_team_list_goal.append(desired_team.strip())
            matches_player_list_goal.append(desired_player.strip())
            matches_score_list_goal.append(desired_score.strip())
            matches_way_of_scoring.append(desired_way.strip())

    matches_player_list_goal = [player + ' -' for player in matches_player_list_goal]
    matches_team_list_goal = [team + ' -' for team in matches_team_list_goal]


    print(len(matches_way_of_scoring)) # Perfect
    print(len(matches_score_list_goal)) # Perfect
    print(len(matches_time_list_goal)) # Perfect  
    print((matches_team_list_goal)) # Perfect  
    print((matches_player_list_goal)) # Perfect  

    pattern_player_own_goal = r"by ([^,]+),"
    pattern_team_own_goal = r"\,\s([^..]+)"
    pattern_score_own_goal = r"\.\s([^..]+)"

    matches_player_list_own_goal = []
    matches_team_list_own_goal = []
    matches_score_list_own_goal = []
    matches_time_list_own_goal = []

    for sentence in own_goal_sentences:
        matches_player = re.findall(pattern_player_own_goal, sentence)
        matches_team = re.findall(pattern_team_own_goal, sentence)
        matches_score = re.findall(pattern_score_own_goal, sentence)
        matches_time = re.findall(pattern_time, sentence)
        if matches_player and matches_team and matches_score and matches_time:
            desired_player = matches_player[0]
            desired_team = matches_team[0]
            desired_score = matches_score[0]
            desired_time = matches_time[0]

            matches_player_list_own_goal.append(desired_player.strip())
            matches_team_list_own_goal.append(desired_team.strip())
            matches_score_list_own_goal.append(desired_score.strip())
            matches_time_list_own_goal.append(desired_time.strip())

    matches_player_list_own_goal = [player + ',' for player in matches_player_list_own_goal]
    matches_team_list_own_goal = [team + '.' for team in matches_team_list_own_goal]

    # print("-----------------")
    print(matches_player_list_own_goal)  # Perfect
    print(matches_team_list_own_goal) # Perfect
    print(matches_score_list_own_goal)      # Perfect 
    print(matches_time_list_own_goal) # Perfect
    # print("-----------------")


    patterns = [
        {"label": "TIME", "pattern": time} for time in matches_time_list_goal + matches_time_list_own_goal
    ] + [
        {"label": "TEAM", "pattern": team} for team in matches_team_list_goal + matches_team_list_own_goal
    ] + [
        {"label": "PLAYER", "pattern": player} for player in matches_player_list_goal + matches_player_list_own_goal
    ] + [    
        {"label": "SCORE", "pattern": score} for score in matches_score_list_goal + matches_score_list_own_goal
    ] + [    
        {"label": "WAY_OF_SCORING", "pattern": way} for way in matches_way_of_scoring    
    ]


    ruler.add_patterns(patterns)

    text1 = '\n'.join(goal_sentences)
    doc1 = nlp(text1)

    text2 = '\n'.join(own_goal_sentences)
    doc2 = nlp(text2)

    TEAM_GOAL = [ent.text for ent in doc1.ents if ent.label_ == "TEAM"]
    TEAM_OWN_GOAL = [ent.text for ent in doc2.ents if ent.label_ == "TEAM"]

    PLAYER_GOAL = [ent.text for ent in doc1.ents if ent.label_ == "PLAYER"]
    PLAYER_OWN_GOAL = [ent.text for ent in doc2.ents if ent.label_ == "PLAYER"]

    TIME_STAMP_GOAL = [ent.text for ent in doc1.ents if ent.label_ == "TIME"]
    TIME_STAMP_OWN_GOAL = [ent.text for ent in doc2.ents if ent.label_ == "TIME"]

    SCORE_GOAL = [ent.text for ent in doc1.ents if ent.label_ == "SCORE"]
    SCORE_OWN_GOAL = [ent.text for ent in doc2.ents if ent.label_ == "SCORE"]

    WAY_OF_SCORING = [ent.text for ent in doc1.ents if ent.label_ == "WAY_OF_SCORING"]


    PLAYER_GOAL = [player.replace(" -", "").rstrip() for player in PLAYER_GOAL]
    TEAM_GOAL = [team.replace(" -", "").rstrip() for team in TEAM_GOAL]

    PLAYER_OWN_GOAL = [player.replace(",", "").rstrip() for player in PLAYER_OWN_GOAL]
    TEAM_OWN_GOAL = [team.replace(".", "").rstrip() for team in TEAM_OWN_GOAL]

    LABELS_1 = []
    for i in range(len(goal_sentences)):
        LABELS_1.append(goal_sentences[i])

    LABELS_2 = []
    for i in range(len(own_goal_sentences)):
        LABELS_2.append(own_goal_sentences[i])
    

    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print(len(TIME_STAMP_GOAL))
    print(len(TEAM_GOAL))
    print(len(PLAYER_GOAL))
    print(len(SCORE_GOAL))
    print(len(WAY_OF_SCORING))
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print(len(TIME_STAMP_OWN_GOAL))
    print(len(TEAM_OWN_GOAL))
    print(len(PLAYER_OWN_GOAL))
    print(len(SCORE_OWN_GOAL))

    return LABELS_1, TIME_STAMP_GOAL, TEAM_GOAL, PLAYER_GOAL, SCORE_GOAL, WAY_OF_SCORING, LABELS_2, TIME_STAMP_OWN_GOAL, TEAM_OWN_GOAL, PLAYER_OWN_GOAL, SCORE_OWN_GOAL

    
def assist_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open("web_scrap/txt_files/categories/assist_sentences.txt", 'r', encoding='utf-8') as file:
        text = file.read()

    sentences = text.split('\n')

    pattern_assisted_event = r"(Attacking_Attempt|Goal_Scored)(\d+)"
    pattern_player  = r"-\s(.*?)(?=\swith|\sfollowing|\safter|\.\s)"

    matches_assisted_event = []

    matches_players = re.findall(pattern_player, text)

    matches_ = re.findall(pattern_assisted_event, text)

    for match in matches_:
        extracted_match = match[0] + match[1]
        matches_assisted_event.append(extracted_match)

    # print(len(matches_attacking_attempt))
    # print(len(matches_players))

    patterns = [
        {"label": "PLAYER", "pattern": player} for player in matches_players
    ] + [
        {"label": "ASSISTED", "pattern": assisted} for assisted in matches_assisted_event   
    ]

    ruler.add_patterns(patterns)
    doc = nlp(text)

    PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    ASSISTED_EVENT = [ent.text for ent in doc.ents if ent.label_ == "ASSISTED"]
    LABELS = []
    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])

    #print(len(ASSIST))
    print(len(PLAYER))
    print(len(ASSISTED_EVENT ))

    return LABELS, PLAYER, ASSISTED_EVENT

def var_decision_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open("web_scrap/txt_files/categories/var_decision_sentences.txt", 'r', encoding='utf-8') as file:
        text = file.read()

    sentences = text.split('\n')
    pattern_time = r"\d+\+?\d*'"
    pattern_var_decision = r"VAR Decision:\s*(.*)|BY VAR:\s*(.*)"
    matches_var = re.findall(pattern_var_decision, text)
    matche_var_decision = [item for sublist in matches_var for item in sublist if item]
    matches_time = re.findall(pattern_time, text)

    patterns = [
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [
        {"label": "DECISION", "pattern": dec} for dec in matche_var_decision
    ]

    ruler.add_patterns(patterns)
    doc = nlp(text)

    TIME = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    DECISION = [ent.text for ent in doc.ents if ent.label_ == "DECISION"]
    LABELS = []

    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])

    print(TIME)
    print(DECISION)
    # print(VAR)

    return LABELS, TIME, DECISION


def penalty_procedure_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    penalty_goal_sentences = []
    penalty_shootout_begins_sentences = []
    pentalty_shootout_ends_sentences = []
    pentalty_saved_sentences = []
    penalty_missed_sentences = []

    with open("web_scrap/txt_files/categories/penalty_procedure_sentences.txt", 'r', encoding='utf-8') as file:
        for line in file:
            if "Goal!" in line:
                penalty_goal_sentences.append(line)
            elif "Penalty Shootout begins" in line:
                penalty_shootout_begins_sentences.append(line)
            elif "Penalty Shootout ends" in line:
                pentalty_shootout_ends_sentences.append(line)
            elif "Penalty saved" in line:
                pentalty_saved_sentences.append(line)
            elif "Penalty missed" in line:
                penalty_missed_sentences.append(line)

    pattern_time = r"\d+\+?\d*'"

    matches_time_goal = []
    matches_time_begins = []
    matches_time_ends = []
    matches_time_saved = []
    matches_time_missed = []

    pattern_score_begins = r"begins\s(.*)"
    pattern_score_ends = r"ends,\s(.*)"

    matches_score_begins = []
    matches_score_ends = []
    matches_score_goal = []

    pattern_player_saved = r"saved\.\s(.*?)\s-\s"
    pattern_team_saved = r"\s-\s(.*?)\s-\s"
    pattern_way_saved = r"\s-\s.*?\s-\s(.*)"

    matches_player_saved = []
    matches_team_saved = []
    matches_way_saved = []

    for sentence in penalty_shootout_begins_sentences:
        match_time = re.findall(pattern_time, sentence)
        match_score = re.findall(pattern_score_begins, sentence)
        if match_score and match_time:
            desired_time = match_time[0]
            desired_score = match_score[0]

            matches_time_begins.append(desired_time)
            matches_score_begins.append(desired_score)

    for sentence in pentalty_shootout_ends_sentences:
        match_time = re.findall(pattern_time, sentence)
        match_score = re.findall(pattern_score_ends, sentence)
        if match_score and match_time:
            desired_time = match_time[0]
            desired_score = match_score[0]

            matches_time_ends.append(desired_time)
            matches_score_ends.append(desired_score)
    for sentence in pentalty_saved_sentences:
        match_time = re.findall(pattern_time, sentence)
        match_player = re.findall(pattern_player_saved, sentence)
        match_team = re.findall(pattern_team_saved, sentence)
        match_way = re.findall(pattern_way_saved, sentence)

        if match_time and match_player and match_team and match_way:
            desired_time = match_time[0]
            desired_player = match_player[0]
            desired_team = match_team[0]
            desired_way = match_way[0]


            matches_time_saved.append(desired_time)
            matches_player_saved.append(desired_player)
            matches_team_saved.append(desired_team)
            matches_way_saved.append(desired_way)
            
    matches_team_saved = [team+" -" for team in matches_team_saved]

    pattern_player_missed = r"missed\.\s(.*?)\s-\s"


    matches_player_missed = []
    matches_team_missed = []
    matches_way_missed = []


    for sentence in penalty_missed_sentences:
        match_time = re.findall(pattern_time, sentence)
        match_player = re.findall(pattern_player_missed, sentence)
        match_team = re.findall(pattern_team_saved, sentence)
        match_way = re.findall(pattern_way_saved, sentence)

        if match_time and match_player and match_team and match_way:
            desired_time = match_time[0]
            desired_player = match_player[0]
            desired_team = match_team[0]
            desired_way = match_way[0]

            matches_time_missed.append(desired_time)
            matches_player_missed.append(desired_player)
            matches_team_missed.append(desired_team)
            matches_way_missed.append(desired_way)

    matches_team_missed = [team+" -" for team in matches_team_missed]

    pattern_score_goal = r"Goal!\s(.*?)\."
    pattern_player_goal = r"\.\s(.*?)\s-\s"
    pattern_team_goal = r"-\s(.*?)\s-\sconverts\s"
    pattern_way_goal = r"-\s.*?\s-\s(.*)"

    matches_score_goal = []
    matches_player_goal = []
    matches_team_goal = []
    matches_way_goal = []

    for sentence in penalty_goal_sentences:
        timestamp_match = re.search(r'\d+\+?\d*', sentence)
        if timestamp_match:
            timestamp = timestamp_match.group(0)
            matches_time_goal.append(timestamp)
        score_match = re.search(r'[A-Za-z\s]+(?: [\d,\s-]+)?, [A-Za-z\s]+ [\d,\s-]+', sentence)
        if score_match:
            score = score_match.group(0).strip()
            matches_score_goal.append(score)

        player_name_match = re.search(r'((\d+\s-\s\d+\s-\s)|([A-Za-z\s]+\d)), ([A-Za-z\s])+ \d+(\s|[.]?)([\s(\d)]?)+\s(.*?)(?=\s-\s[A-Za-z\s]+-\s)', sentence)
        if player_name_match:
            # Extract the full matched string
            full_match = player_name_match.group(0).strip()
            print(full_match)
            # Split by the last numeric sequence
            parts = re.split(r'\d+,|([\s]-\s]?),\s', full_match)
            if len(parts) > 1:
                player_part = parts[-1]
                player_name = re.split(r'\s-\s|\.', player_part)[-1].strip()
                player_name = player_name.split('-')[0].strip()
                player_name = re.sub(r'^\d+\s*', '', player_name).strip()
                matches_player_goal.append(player_name)
        team_name_match = re.search(r'(?<=-)\s[A-Za-z\s]+(?=\s-\sconverts)', sentence)
        if team_name_match:
            team_name = team_name_match.group(0).strip()
            matches_team_goal.append(team_name)

        way_of_scoring_match = re.search(r'with a (.*?)\.', sentence)
        if way_of_scoring_match:
            way_of_scoring = way_of_scoring_match.group(1).strip()
            matches_way_goal.append(way_of_scoring)


    matches_team_goal = [team+" -" for team in matches_team_goal]

    patterns = [
        {"label": "SCORE", "pattern": score} for score in matches_score_begins + matches_score_ends + matches_score_goal    
    ] + [
        {"label": "TIME", "pattern": time} for time in matches_time_begins + matches_time_ends + matches_time_saved + matches_time_missed + matches_time_goal
    ] + [
        {"label": "TEAM", "pattern": team} for team in matches_team_saved + matches_team_missed + matches_team_goal
    ] + [
        {"label": "PLAYER", "pattern": player} for player in matches_player_goal + matches_player_missed + matches_player_saved
    ] + [
        {"label": "WAY", "pattern": way} for way in matches_way_goal + matches_way_missed + matches_way_saved     
    ]
    # print(patterns)
    ruler.add_patterns(patterns)

    text1 = '\n'.join(penalty_goal_sentences)
    doc1 = nlp(text1)

    text2 = '\n'.join(penalty_shootout_begins_sentences)
    doc2 = nlp(text2)

    text3 = '\n'.join(pentalty_shootout_ends_sentences)
    doc3 = nlp(text3)

    text4 = '\n'.join(pentalty_saved_sentences)
    doc4 = nlp(text4)

    text5 = '\n'.join(penalty_missed_sentences)
    doc5 = nlp(text5)

    TIME_BEGINS = [ent.text for ent in doc2.ents if ent.label_ == "TIME"]
    TIME_ENDS = [ent.text for ent in doc3.ents if ent.label_ == "TIME"]
    TIME_SAVED = [ent.text for ent in doc4.ents if ent.label_ == "TIME"]
    TIME_MISSED = [ent.text for ent in doc5.ents if ent.label_ == "TIME"]
    TIME_GOAL = [ent.text for ent in doc1.ents if ent.label_ == "TIME"]

    SCORE_BEGINS = [ent.text for ent in doc2.ents if ent.label_ == "SCORE"]
    SCORE_ENDS = [ent.text for ent in doc3.ents if ent.label_ == "SCORE"]
    SCORE_GOAL = [ent.text for ent in doc1.ents if ent.label_ == "SCORE"]

    TEAM_SAVED = [ent.text for ent in doc4.ents if ent.label_ == "TEAM"]
    TEAM_SAVED = [team.replace(" -", "").rstrip() for team in TEAM_SAVED]
    TEAM_MISSED = [ent.text for ent in doc5.ents if ent.label_ == "TEAM"]
    TEAM_MISSED = [team.replace(" -", "").rstrip() for team in TEAM_MISSED]
    TEAM_GOAL = [ent.text for ent in doc1.ents if ent.label_ == "TEAM"]
    TEAM_GOAL = [team.replace(" -", "").rstrip() for team in TEAM_GOAL]


    PLAYER_GOAL = [ent.text for ent in doc1.ents if ent.label_ == "PLAYER"]
    PLAYER_SAVED = [ent.text for ent in doc4.ents if ent.label_ == "PLAYER"]
    PLAYER_MISSED = [ent.text for ent in doc5.ents if ent.label_ == "PLAYER"]

    WAY_GOAL = [ent.text for ent in doc1.ents if ent.label_ == "WAY"]
    WAY_SAVED = [ent.text for ent in doc4.ents if ent.label_ == "WAY"]
    WAY_MISSED = [ent.text for ent in doc5.ents if ent.label_ == "WAY"]

    LABELS_1 = []
    for i in range(0,len(penalty_shootout_begins_sentences)):
        LABELS_1.append(penalty_shootout_begins_sentences[i])

    LABELS_2 = []
    for i in range(0,len(pentalty_shootout_ends_sentences)):
        LABELS_2.append(pentalty_shootout_ends_sentences[i]) 

    LABELS_3 = []
    for i in range(0,len(pentalty_saved_sentences)):
        LABELS_3.append(pentalty_saved_sentences[i])

    LABELS_4 = []
    for i in range(0,len(penalty_missed_sentences)):
        LABELS_4.append(penalty_missed_sentences[i])        

    LABELS_5 = []
    for i in range(0,len(penalty_goal_sentences)):
        LABELS_5.append(penalty_goal_sentences[i])

    print(len(TIME_BEGINS))
    print(len(TIME_ENDS))
    print(len(TIME_SAVED))
    print(len(TIME_MISSED))
    print(len(TIME_GOAL))
    print("-----------")
    print(len(SCORE_BEGINS))
    print(len(SCORE_ENDS))
    print(len(SCORE_GOAL))

    print("-----------")
    print(len(TEAM_SAVED))
    print(len(TEAM_MISSED))
    print(len(TEAM_GOAL))

    print("-----------")
    print(len(PLAYER_GOAL))
    print(len(PLAYER_SAVED))
    print(len(PLAYER_MISSED))


    print("-----------")
    print(len(WAY_GOAL))
    print(len(WAY_SAVED))
    print(len(WAY_MISSED))


    return TIME_BEGINS, SCORE_BEGINS, TIME_ENDS, SCORE_ENDS, TIME_SAVED, TEAM_SAVED, PLAYER_SAVED, WAY_SAVED, \
        TIME_MISSED, TEAM_MISSED, PLAYER_MISSED, WAY_MISSED, TIME_GOAL, SCORE_GOAL, TEAM_GOAL, PLAYER_GOAL, WAY_GOAL, \
        LABELS_1, LABELS_2, LABELS_3, LABELS_4, LABELS_5     
    
def create_rdf_graph(events):
    g = Graph()
    # Define namespaces
    ex = Namespace("http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/")
    g.bind("ex", ex)
    
    # Add ontology to the graph
    g.parse("web_scrap/football.ttl")
    print(g)
    for event in events:
        event_type, entities = event[0], event[1:]
        event_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/{event_type.replace(' ', '_')}")

        if event_type == "CORNER":
            for i in range(len(entities[0])):
                corner_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Corner{str(i+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{entities[1][i].replace(' ', '_')}")
                player_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{entities[2][i].replace(' ', '_')}")
                time_uri = Literal(entities[3][i])
                labels = Literal(entities[0][i])

                g.add((corner_uri, RDF.type, ex.Corner))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

                g.add((corner_uri, RDFS.label, labels))

                g.add((corner_uri, ex.corner_won_for, team_uri))
                g.add((corner_uri, ex.conceded_by, player_uri))
                g.add((corner_uri, ex.happened_at, time_uri))

        if event_type == "HANDBALL":
            for i in range(len(entities[0])):
                handball_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Hand_Ball{str(i+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{entities[1][i].replace(' ', '_')}")
                player_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{entities[2][i].replace(' ', '_')}")
                time_uri = Literal(entities[3][i])
                labels = Literal(entities[0][i])

                g.add((handball_uri, RDF.type, ex.Hand_Ball))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))
                
                g.add((handball_uri, RDFS.label, labels))
                g.add((handball_uri, ex.conceded_by, player_uri))
                g.add((handball_uri, ex.happened_at, time_uri))
                g.add((player_uri, ex.playsFor, team_uri))

        if event_type == "OFFSIDE":
            for i in range(len(entities[0])):
                offside_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Offside{str(i+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{entities[2][i].replace(' ', '_')}")
                player_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{entities[1][i].replace(' ', '_')}")
                time_uri = Literal(entities[3][i])
                labels = Literal(entities[0][i])

                g.add((offside_uri, RDF.type, ex.Offside))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

                
                g.add((offside_uri, RDFS.label, labels))

                g.add((offside_uri, ex.offside_for, team_uri))
                g.add((offside_uri, ex.offside_caused_by, player_uri))
                g.add((offside_uri, ex.happened_at, time_uri))
                g.add((player_uri, ex.playsFor, team_uri))

        if event_type == "FOUL":
            for i in range(len(entities[0])):
                foul_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Foul{str(i+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{entities[2][i].replace(' ', '_')}")
                player_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{entities[1][i].replace(' ', '_')}")
                time_uri = Literal(entities[3][i])
                labels = Literal(entities[0][i])


                g.add((foul_uri, RDF.type, ex.Foul))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

                g.add((foul_uri, RDFS.label, labels))

                g.add((foul_uri, ex.foul_from, team_uri))
                g.add((foul_uri, ex.fouled_by, player_uri))
                g.add((foul_uri, ex.happened_at, time_uri))
                g.add((player_uri, ex.playsFor, team_uri))

        if event_type == "DANGEROUS_PLAY":
            for i in range(len(entities[0])):
                dangerous_play_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Dangerous_Play{str(i+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{entities[2][i].replace(' ', '_')}")
                player_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{entities[1][i].replace(' ', '_')}")
                time_uri = Literal(entities[3][i])
                labels = Literal(entities[0][i])

                g.add((dangerous_play_uri, RDF.type, ex.Dangerous_Play))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

                g.add((dangerous_play_uri, RDFS.label, labels))


                g.add((dangerous_play_uri, ex.conceded_by, player_uri))
                g.add((dangerous_play_uri, ex.happened_at, time_uri))
                g.add((player_uri, ex.playsFor, team_uri))

        if event_type == "YELLOW_CARD":
            for i in range(len(entities[0])):
                yellow_card_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Yellow_Card{str(i+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{entities[1][i].replace(' ', '_')}")
                player_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{entities[2][i].replace(' ', '_')}")
                time_uri = Literal(entities[3][i])
                labels = Literal(entities[0][i])

                g.add((yellow_card_uri, RDF.type, ex.Yellow_Card))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

                g.add((yellow_card_uri, RDFS.label, labels))

                g.add((yellow_card_uri, ex.card_counts_for, team_uri))
                g.add((yellow_card_uri, ex.recieved_by, player_uri))
                g.add((yellow_card_uri, ex.happened_at, time_uri))
                g.add((player_uri, ex.playsFor, team_uri))

        if event_type == "RED_CARD":
            for i in range(len(entities[0])):
                red_card_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Red_Card{str(i+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{entities[1][i].replace(' ', '_')}")
                player_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{entities[2][i].replace(' ', '_')}")
                time_uri = Literal(entities[3][i])
                labels = Literal(entities[0][i])

                g.add((red_card_uri, RDF.type, ex.Red_Card))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

                g.add((red_card_uri, RDFS.label, labels))

                g.add((red_card_uri, ex.card_counts_for, team_uri))
                g.add((red_card_uri, ex.recieved_by, player_uri))
                g.add((red_card_uri, ex.happened_at, time_uri))
                g.add((player_uri, ex.playsFor, team_uri))

        if event_type == "FREEKICK":
            for i in range(len(entities[0])):
                free_kick_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Free_Kick{str(i+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{entities[2][i].replace(' ', '_')}")
                player_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{entities[1][i].replace(' ', '_')}")
                at_place_uri = Literal(entities[3][i].replace(' ', '_'))
                time_uri = Literal(entities[4][i])
                labels = Literal(entities[0][i])

                g.add((free_kick_uri, RDF.type, ex.Free_Kick))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

                g.add((free_kick_uri, RDFS.label, labels))

                g.add((free_kick_uri, ex.won_for, team_uri))
                g.add((free_kick_uri, ex.won_at_place, at_place_uri))
                g.add((free_kick_uri, ex.won_by, player_uri))
                g.add((free_kick_uri, ex.happened_at, time_uri))
                g.add((player_uri, ex.playsFor, team_uri))


        if event_type == "ATTACKING_ATTEMPT":
            for i in range(len(entities[0])):
                attacking_attempt_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Attacking_Attempt{str(i+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{entities[2][i].replace(' ', '_')}")
                player_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{entities[1][i].replace(' ', '_')}")
                way_of_attempt = Literal(entities[4][i].replace(' ', '_'))
                time_uri = Literal(entities[3][i].replace(' ', '_'))
                labels = Literal(entities[0][i])

                g.add((attacking_attempt_uri, RDF.type, ex.Attacking_Attempt))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))


                g.add((attacking_attempt_uri, RDFS.label, labels))

                g.add((attacking_attempt_uri, ex.counts_for, team_uri))
                g.add((attacking_attempt_uri, ex.way_of_attempt, way_of_attempt))
                g.add((attacking_attempt_uri, ex.noted_by, player_uri))
                g.add((attacking_attempt_uri, ex.happened_at, time_uri))
                g.add((player_uri, ex.playsFor, team_uri))

        if event_type == "SUBSTITUTION":
            for i in range(len(entities[0])):
                substitution_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Substitution{str(i+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{entities[1][i].replace(' ', '_')}")
                player_in_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{entities[2][i].replace(' ', '_')}")
                player_out_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{entities[3][i].replace(' ', '_')}")
                time_uri = Literal(entities[4][i])
                labels = Literal(entities[0][i])

                g.add((substitution_uri, RDF.type, ex.Substitution))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

                g.add((substitution_uri, RDFS.label, labels))

                g.add((substitution_uri, ex.sub_for, team_uri))
                g.add((substitution_uri, ex.happened_at, time_uri))
                g.add((substitution_uri, ex.sub_player_in, player_in_uri))
                g.add((substitution_uri, ex.sub_player_out, player_out_uri))
                g.add((player_in_uri, ex.playsFor, team_uri))
                g.add((player_out_uri, ex.playsFor, team_uri))

        if event_type == "PENALTY":
            for i in range(len(entities[0])):
                penalty_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Penalty{str(i+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{entities[2][i].replace(' ', '_')}")
                player_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{entities[1][i].replace(' ', '_')}")
                time_uri = Literal(entities[3][i])
                labels = Literal(entities[0][i])

                g.add((penalty_uri, RDF.type, ex.Penalty))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

                g.add((penalty_uri, RDFS.label, labels))

                g.add((penalty_uri, ex.penalty_caused_by, player_uri))
                g.add((penalty_uri, ex.happened_at, time_uri))
                g.add((player_uri, ex.playsFor, team_uri))        
                                                                
                                                        
        if event_type == "DELAY":
            ind = 0
            for i in range(len(entities[1])):
                delay_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Delay{str(ind+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{entities[4][i].replace(' ', '_')}")
                time_uri = Literal(entities[1][i])
                labels = Literal(entities[0][i])

                g.add((delay_uri, RDF.type, ex.Delay))
                g.add((team_uri, RDF.type, ex.Team))

                g.add((delay_uri, RDFS.label, labels))

                g.add((delay_uri, ex.happened_at, time_uri))  
                g.add((delay_uri, ex.delay_caused_from, team_uri))   

                ind += 1
            for i in range(len(entities[2])):
                delay_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Delay{str(ind+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{entities[5][i].replace(' ', '_')}")
                player_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{entities[6][i].replace(' ', '_')}")
                time_uri = Literal(entities[2][i])
                labels = Literal(entities[7][i])

                g.add((delay_uri, RDF.type, ex.Delay))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

                g.add((delay_uri, RDFS.label, labels))

                g.add((delay_uri, ex.player_injured, player_uri))
                g.add((delay_uri, ex.happened_at, time_uri))
                g.add((delay_uri, ex.delay_caused_from, team_uri)) 
                g.add((player_uri, ex.playsFor, team_uri))

                ind += 1
            for i in range(len(entities[3])):
                delay_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Delay{str(ind+1)}")
                time_uri = Literal(entities[3][i])
                labels = Literal(entities[8][i])

                g.add((delay_uri, RDF.type, ex.Delay))

                g.add((delay_uri, RDFS.label, labels))

                g.add((delay_uri, ex.happened_at, time_uri))  

                ind += 1 


        if event_type == "FIRST_HALF_ENDED":
            for i in range(len(entities[0])):
                first_half_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/First_Half{str(i+1)}")
                score_uri = Literal(entities[1][i])
                time_uri = Literal(entities[2][i])
                labels = Literal(entities[0][i])


                g.add((first_half_uri, RDF.type, ex.First_Half))

                g.add((first_half_uri, RDFS.label, labels))

                g.add((first_half_uri, ex.ended_at, time_uri))
                g.add((first_half_uri, ex.ended_with_score, score_uri)) 


        if event_type == "SECOND_HALF":
            for i in range(len(entities[0])):
                second_half_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Second_Half{str(i+1)}")
                score_uri = Literal(entities[2][i])
                time_uri = Literal(entities[1][i])
                labels = Literal(entities[0][i])

                g.add((second_half_uri, RDF.type, ex.Second_Half))

                g.add((second_half_uri, RDFS.label, labels))

                g.add((second_half_uri, ex.started_at, time_uri))
                g.add((second_half_uri, ex.started_with_score, score_uri))   
                

            for i in range(len(entities[3])):
                second_half_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Second_Half{str(i+1)}")
                score_uri = Literal(entities[5][i])
                time_uri = Literal(entities[4][i])
                labels = Literal(entities[3][i])

                g.add((second_half_uri, RDF.type, ex.Second_Half))

                g.add((second_half_uri, RDFS.label, labels))

                g.add((second_half_uri, ex.ended_at, time_uri))
                g.add((second_half_uri, ex.ended_with_score, score_uri))  
                                               

        if event_type == "EXTRA_FIRST":
            for i in range(len(entities[0])):
                extra_time_first_half_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/First_Half_Extra_Time{str(i+1)}")
                score_uri = Literal(entities[2][i])
                time_uri = Literal(entities[1][i])
                labels = Literal(entities[0][i])

                g.add((extra_time_first_half_uri, RDF.type, ex.First_Half_Extra_Time))

                g.add((extra_time_first_half_uri, RDFS.label, labels))

                g.add((extra_time_first_half_uri, ex.started_at, time_uri))
                g.add((extra_time_first_half_uri, ex.started_with_score, score_uri))   

            for i in range(len(entities[3])):
                extra_time_first_half_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/First_Half_Extra_Time{str(i+1)}")
                score_uri = Literal(entities[5][i])
                time_uri = Literal(entities[4][i])
                labels = Literal(entities[3][i])

                g.add((extra_time_first_half_uri, RDF.type, ex.First_Half_Extra_Time))

                g.add((extra_time_first_half_uri, RDFS.label, labels))

                g.add((extra_time_first_half_uri, ex.ended_at, time_uri))
                g.add((extra_time_first_half_uri, ex.ended_with_score, score_uri))  


        if event_type == "EXTRA_SECOND":
            for i in range(len(entities[0])):
                second_half_extra_time_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Second_Half_Extra_Time{str(i+1)}")
                score_uri = Literal(entities[2][i])
                time_uri = Literal(entities[1][i])
                labels = Literal(entities[0][i])

                g.add((second_half_extra_time_uri, RDF.type, ex.Second_Half_Extra_Time))

                g.add((second_half_extra_time_uri, RDFS.label, labels))

                g.add((second_half_extra_time_uri, ex.started_at, time_uri))
                g.add((second_half_extra_time_uri, ex.started_with_score, score_uri))   

        

            for i in range(len(entities[3])):
                second_half_extra_time_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Second_Half_Extra_Time{str(i+1)}")
                score_uri = Literal(entities[5][i])
                time_uri = Literal(entities[4][i])
                labels = Literal(entities[3][i])

                g.add((second_half_extra_time_uri, RDF.type, ex.Second_Half_Extra_Time))

                g.add((second_half_extra_time_uri, RDFS.label, labels))

                g.add((second_half_extra_time_uri, ex.ended_at, time_uri))
                g.add((second_half_extra_time_uri, ex.ended_with_score, score_uri))  


        if event_type == "END_GAME":
            for i in range(len(entities[0])):
                end_game_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/End_Game{str(i+1)}")
                score_uri = Literal(entities[1][i])
                labels = Literal(entities[0][i])

                g.add((end_game_uri, RDF.type, ex.End_Game))

                g.add((end_game_uri, RDFS.label, labels))

                g.add((end_game_uri, ex.ended_with_score, score_uri)) 



        if event_type == "GOAL":
            index_goal = 0
            for i in range(len(entities[0])):
                goal_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Goal_Scored{str(index_goal+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{entities[2][i].replace(' ', '_')}")
                player_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{entities[3][i].replace(' ', '_')}")
                labels = Literal(entities[0][i])

                score_uri = Literal(entities[4][i])
                way_of_scoring_uri = Literal(entities[5][i])
                time_uri = Literal(entities[1][i])

                g.add((goal_uri, RDF.type, ex.Goal_Scored))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

                g.add((goal_uri, RDFS.label, labels))

                g.add((goal_uri, ex.scored_by, player_uri))
                g.add((goal_uri, ex.counts_for, team_uri))
                g.add((goal_uri, ex.scored_with, way_of_scoring_uri)) 
                g.add((goal_uri, ex.makes_score, score_uri))
            
                g.add((goal_uri, ex.happened_at, time_uri))  
                index_goal += 1
            for j in range(len(entities[6])):
                own_goal_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Own_Goal{str(j+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{entities[8][j].replace(' ', '_')}")
                player_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{entities[9][j].replace(' ', '_')}")
                labels = Literal(entities[6][j])
                score_uri = Literal(entities[10][j])
                time_uri = Literal(entities[7][j])

                g.add((own_goal_uri, RDF.type, ex.Own_Goal))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

                g.add((own_goal_uri, RDFS.label, labels))


                g.add((own_goal_uri, ex.scored_by, player_uri))
                g.add((own_goal_uri, ex.makes_score, score_uri))
                g.add((player_uri, ex.playsFor, team_uri))
                g.add((own_goal_uri, ex.happened_at, time_uri))  


        if event_type == "ASSIST":
  
            assisted_event_uri = []
            happened_at_predicate = ex.happened_at  
            for i in range(len(entities[0])):
                assist_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Assist{str(i+1)}")
                player_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{entities[1][i].replace(' ', '_')}")
                assisted_event_uri = Literal(entities[2][i])
                labels = Literal(entities[0][i])
                g.add((assist_uri, RDF.type, ex.Assist))
                g.add((assist_uri, ex.assist_made_by, player_uri))
                
                g.add((assist_uri, RDFS.label, labels))  

                local_name_event = assisted_event_uri.split("/")[-1]
                full_assisted_event_uri = ex[local_name_event]
                
                query_string = f'''
                    PREFIX ex: <http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/>
                    SELECT ?value ?team 
                    WHERE {{
                        <{full_assisted_event_uri}> <{happened_at_predicate}> ?value .
                        <{full_assisted_event_uri}> <{ex.counts_for}> ?team .

                    }}
                '''
                query = prepareQuery(query_string)
                
                for row in g.query(query):
                    value = row.value
                    team = row.team
                
                    team_local_name = team.split("/")[-1]
                    team_uri = ex[team_local_name]
                    g.add((assist_uri, ex.happened_at, value))
                    g.add((player_uri, ex.playsFor, team_uri))
                    g.add((assist_uri, ex.refers_to, full_assisted_event_uri))

        if event_type == "VAR":
            for i in range(len(entities[0])):
                var_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/VAR{str(i+1)}")
                time_uri = Literal(entities[1][i])
                decision_uri = Literal(entities[2][i])
                labels = Literal(entities[0][i])

                g.add((var_uri, RDF.type, ex.VAR))

                g.add((var_uri, RDFS.label, labels)) 

                g.add((var_uri, ex.happened_at, time_uri))
                g.add((var_uri, ex.decision_made, decision_uri))  

        if event_type == "PENALTY_PROCEDURE":
            for i in range(len(entities[0])):
                penalty_procedure_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Penalty_Procedure{str(i+1)}")
                score_uri = Literal(entities[1][i])
                time_uri = Literal(entities[0][i])
                labels = Literal(entities[17][i])
                g.add((penalty_procedure_uri, RDF.type, ex.Penalty_Procedure))


                g.add((penalty_procedure_uri, RDFS.label, labels))   

                g.add((penalty_procedure_uri, ex.happened_at, time_uri))
                g.add((penalty_procedure_uri, ex.started_with_score, score_uri))

            for i in range(len(entities[2])):
                penalty_procedure_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Penalty_Procedure{str(i+1)}")
                score_uri = Literal(entities[3][i])
                time_uri = Literal(entities[2][i])
                labels = Literal(entities[18][i])
                g.add((penalty_procedure_uri, RDF.type, ex.Penalty_Procedure))
                
                g.add((penalty_procedure_uri, RDFS.label, labels))   
                 
                
                g.add((penalty_procedure_uri, ex.ended_with_score, score_uri))
            ind = 0
            for i in range(len(entities[4])):
                penalty_no_goal = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Penalty_No_Goal{str(ind+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{entities[5][i].replace(' ', '_')}")
                player_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{entities[6][i].replace(' ', '_')}")
                way_uri = Literal(entities[7][i])
                time_uri = Literal(entities[4][i])
                labels = Literal(entities[19][i])
                g.add((penalty_no_goal, RDF.type, ex.Penalty_No_Goal))
                
                g.add((penalty_no_goal, RDFS.label, labels))  

                g.add((penalty_no_goal, ex.happened_at, time_uri))
                g.add((penalty_no_goal, ex.missed_by, player_uri))
                g.add((penalty_no_goal, ex.missed_with, way_uri))
                g.add((penalty_no_goal, ex.missed_for, team_uri))
                g.add((player_uri, ex.playsFor, team_uri))

                ind += 1

            for i in range(len(entities[8])):     
                penalty_no_goal = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Penalty_No_Goal{str(ind+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{entities[9][i].replace(' ', '_')}")
                player_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{entities[10][i].replace(' ', '_')}")
                way_uri = Literal(entities[11][i])
                time_uri = Literal(entities[8][i])
                labels = Literal(entities[20][i])
                g.add((penalty_no_goal, RDF.type, ex.Penalty_No_Goal))
                
                g.add((penalty_no_goal, RDFS.label, labels))  

                g.add((penalty_no_goal, ex.happened_at, time_uri))
                g.add((penalty_no_goal, ex.missed_by, player_uri))
                g.add((penalty_no_goal, ex.missed_with, way_uri))
                g.add((penalty_no_goal, ex.missed_for, team_uri))
                g.add((player_uri, ex.playsFor, team_uri))

                ind += 1

            for i in range(len(entities[12])):
                penalty_goal = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Penalty_Scored_Goal{str(i+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{entities[14][i].replace(' ', '_')}")
                player_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{entities[15][i].replace(' ', '_')}")
                score_uri = Literal(entities[13][i])
                way_uri = Literal(entities[16][i])
                time_uri = Literal(entities[12][i])
                labels = Literal(entities[21][i])

                g.add((penalty_goal, RDF.type, ex.Penalty_Scored_Goal))
                
                g.add((penalty_goal, RDFS.label, labels))  

                g.add((penalty_goal, ex.makes_score, score_uri))
                g.add((penalty_goal, ex.happened_at, time_uri))
                g.add((penalty_goal, ex.scored_by, player_uri))
                g.add((penalty_goal, ex.scored_with, way_uri))
                g.add((penalty_goal, ex.counts_for, team_uri))
                g.add((player_uri, ex.playsFor, team_uri))        
    return g


events = [
        ("CORNER", *corner_ner()),
        ("HANDBALL", *hand_ball_ner()),
        ("OFFSIDE", *offside_ner()),
        ("FOUL", *foul_ner()),
        ("DANGEROUS_PLAY", *dangerous_play_ner()),
        ("YELLOW_CARD", *card_ner("yellow")),
        ("RED_CARD", *card_ner("red")),
        ("FREEKICK", *free_kick_ner()),
        ("ATTACKING_ATTEMPT", *attacking_attempt_ner()),
        ("SUBSTITUTION", *substitution_ner()),
        ("PENALTY", *penalty_ner()),
        ("DELAY", *delay_ner()),
        ("FIRST_HALF_ENDED", *first_half_end_ner()),
        ("SECOND_HALF", *second_half_sentences_ner()),        
        ("EXTRA_FIRST", *extra_time_first_half_ner()),
        ("EXTRA_SECOND", *extra_time_second_half_ner()),
        ("END_GAME", *end_game_ner()),
        ("GOAL", *goal_ner()),
        ("ASSIST", *assist_ner()),
        ("VAR", *var_decision_ner()),
        ("PENALTY_PROCEDURE", *penalty_procedure_ner()),
    ]

rdf_graph = create_rdf_graph(events)
rdf_graph.serialize("output_graph.rdf", format="turtle")



# CORNER, TEAM, PLAYER, TIME_STAMP = corner_ner() # Perfect
# print("corner")
# HANDBALL, PLAYER, TEAM, TIME_STAMP = hand_ball_ner() # Perfect
# print("HANDBALL")
# OFFSIDE, PLAYER, TEAM, TIME_STAMP = offside_ner() # Perfect
# print("OFFSIDE")
# FOUL, PLAYER, TEAM, TIME_STAMP = foul_ner() # Perfect
# print("FOUL")
# DANEROUS_PLAY, PLAYER, TEAM, TIME_SAMP = dangerous_play_ner() # Perfect
# print("DANEROUS_PLAY")
# YELLOW_CARD, PLAYER, TEAM,  TIME_STAMP = card_ner("yellow") # Perfect
# print("YELLOW_CARD")
# RED_CARD, PLAYER, TEAM, TIME_STAMP = card_ner("red") # Perfect
# print("RED_CARD")
# SUBSTITUTION, TEAM, PLAYER_IN, PLAYER_OUT, TIME_STAMP = substitution_ner() # Perfect
# print("substitution")
# PENALTY, PLAYER, TEAM, TIME_STAMP = penalty_ner() # Perfect
# print("penalty")
# ATTACKING_ATTEMPT, PLAYER, TEAM, WAY, TIME_STAMP = attacking_attempt_ner() #Perfect
# print("Attacking Attempt")
# DELAY, TIME_IN_MATCH, TIME_INJURY, TIME_OVER, TEAM_IN_MATCH, TEAM_INJURY, PLAYER_INJURY = delay_ner() # Perfect
# print("Delay")
# FIRST_HALF_ENDED, SCORE, TIME_STAMP = first_half_end_ner() # Perfect
# print("FIRST_HALF_ENDED")
# SECOND_HALF_STARTS, TIME_BEGIN, SCORE_BEGIN, SECOND_HALF_ENDS, TIME_END, SCORE_END = second_half_sentences_ner() # Perfect
# print("second_half_sentences_ner")
# a,b,c,d,e,r = extra_time_first_half_ner() # Perfect
# print("extra_time_first_half_ner")
# extra_time_second_half_ner() # Perfect
# print("extra_time_second_half_ner")
# END_GAME, SCORE = end_game_ner() # Perfect
# print("END_GAME")
# print("delay_ner")
# VAR, TIME, DECISION = var_decision_ner()
# a,b,c,b,e = free_kick_ner()
#a,b,c = assist_ner()
# a,b,c,q,w,e,r,t,y,u,i,o,p,l = penalty_procedure_ner()