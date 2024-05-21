"""
    In this file NER (Named Entity Recognition) is implemented. For each category, we open the file and read the content. After that, we define patterns 
    that will match the desired text to get annotated as entity. This is implemented mainly based on regular expression, because most of the sentences have a certain 
    format. All NER for each category happens in a seperate function for each category/entity of ontology.
    We are using spacy and entityRuler to make our custom entities.

"""
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
def encode_entity(entity):
    return quote(entity.replace(' ', '_'))

def corner_ner():

    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open("web_scrap/txt_files/categories/corner_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    

    sentences = text.split('\n')

    # Define the regex pattern 
    pattern_time = r"\d+\+?\d*'"
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
    
    TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    CORNER = ["Corner" + str(i+1) for i in range(len(TEAM))]


    print((CORNER))
    print(len(TEAM))
    print(len(PLAYER))
    print(len(TIME_STAMP))
    print("\n\n")

    return CORNER, TEAM, PLAYER, TIME_STAMP



def substitution_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open("web_scrap/txt_files/categories/substitution_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    # Define the regex pattern 
    pattern_time = r"\d+\+?\d*'"
    pattern_teams = r"\d+'\s+Substitution - (.*?)\."
    pattern_substitution = r"\.\s*([\w'\-]+(?:\s+[\w'\-]+)*)\s+for\s+([\w'\ - ]+(?:\s+[\w'\ - ]+)*)(?=\s*[\.-]|\s*$)"



    # Find matches in each sentence based on regexes above.
    matches_teams = re.findall(pattern_teams, text)
    matches_substitutions = re.findall(pattern_substitution, text)
    matches_players_in = [player_in.split(' - ')[0] for _, player_in in matches_substitutions]
    matches_players_out = [player_out.split(' - ')[0]+" for" for player_out, _ in matches_substitutions]
    matches_time = re.findall(pattern_time, text)
    # print("aaaaa-> ", (matches_players_in))
    # print("------")
    # print("bbbbbbb-> ", (matches_players_out))
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

    SUBSTITUTION = ["SUBSTITUTION" + str(i+1) for i in range(len(TEAM))]


    print(len(TEAM))
    print(len(PLAYER_IN))
    print(len(TIME_STAMP))
    print(len(PLAYER_OUT))
    print(len(SUBSTITUTION))
    print("\n\n")

    # with open("out.txt", 'w', encoding='utf-8') as out_file:
    #     max_len = max(len(PLAYER_OUT), len(PLAYER_IN))
    #     print(max_len)
    #     for i in range(max_len):
    #         player_out = PLAYER_OUT[i] if i < len(PLAYER_OUT) else "N/A"
    #         player_in = PLAYER_IN[i] if i < len(PLAYER_IN) else "N/A"
    #         out_file.write(f"{player_out} -> {player_in}\n")
    # print("VOGID")
    # print(PLAYER_OUT[225])
    # with open("out2.txt", 'w', encoding='utf-8') as out2_file:
    #     for player_in in matches_players_in:
    #         out2_file.write(f"{player_in}\n")        
    return SUBSTITUTION, TEAM, PLAYER_IN, PLAYER_OUT,TIME_STAMP



def hand_ball_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open("web_scrap/txt_files/categories/hand_ball_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

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
    HAND_BALL = ["HAND_BALL" + str(i+1) for i in range(len(TEAM))]



    print(len(TEAM))
    print(len(PLAYER))
    print(len(TIME_STAMP))
    print(len(HAND_BALL))
    print("\n\n")

    return HAND_BALL, TEAM, PLAYER, TIME_STAMP


def offside_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open("web_scrap/txt_files/categories/offside_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

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
    OFFSIDE = ["OFFSIDE" + str(i+1) for i in range(len(TEAM))]
    
    with open("dump.txt", 'w', encoding="utf-8") as f:
        for i in range(len(TEAM)):
            f.write(OFFSIDE[i] + "  " + TIME_STAMP[i] + " " + PLAYER[i] + " " + TEAM[i] + "\n")
    print(len(TEAM))
    print(len(PLAYER))
    print(len(TIME_STAMP))
    print(len(OFFSIDE))
    print("\n\n")
    return OFFSIDE, PLAYER, TEAM, TIME_STAMP


def free_kick_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open("web_scrap/txt_files/categories/free kick_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    # Define the regex pattern
    pattern_players = r"\d+'\s+(.*?)\s+-\s+"
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
    PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    AT_PLACE = [ent.text for ent in doc.ents if ent.label_ == "AT_PLACE"]
    FREE_KICK = ["FREE_KICK" + str(i+1) for i in range(len(TEAM))]
    
    print(len(TEAM))
    print(len(PLAYER))
    print(len(TIME_STAMP))
    print(len(AT_PLACE))
    print(len(FREE_KICK))
    print("\n\n")

    return FREE_KICK, PLAYER, TEAM, AT_PLACE, TIME_STAMP


def foul_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")


    with open("web_scrap/txt_files/categories/foul_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

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
    FOUL = ["FOUL" + str(i+1) for i in range(len(TEAM))]
    print(len(TEAM))
    print(len(PLAYER))
    print(len(TIME_STAMP))
    print(len(FOUL))
    print("\n\n")

    return FOUL, PLAYER, TEAM,  TIME_STAMP


def dangerous_play_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")


    with open("web_scrap/txt_files/categories/dangerous_play_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()

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
    DANGEROUS_PLAY = ["DANGEROUS_PLAY" + str(i+1) for i in range(len(TEAM))] 

    print(len(TEAM))
    print(len(PLAYER))
    print(len(TIME_STAMP))
    print(len(DANGEROUS_PLAY))
    print("\n\n")

    return DANGEROUS_PLAY, PLAYER, TEAM,  TIME_STAMP

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
    doc = nlp(text)

    TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    PENALTY = ["PENALTY" + str(i+1) for i in range(len(TEAM))]

    print("Number of TEAM entities:", len(TEAM))
    print("Number of PLAYER entities:", len(PLAYER))
    print("Number of TIME entities:", len(TIME_STAMP))
    print("\n\n")

    return PENALTY, PLAYER, TEAM,  TIME_STAMP



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


    for ind in range(len(sentences_new_attacking_attempt)):
        if "Assist" in sentences_new_attacking_attempt[ind]:
            matches_assist = re.findall(pattern_assist, sentences_new_attacking_attempt[ind])
            if matches_assist:  # Check if matches_assist is not empty
                assist_text = matches_assist[0]  # Access the first element of the list
                string_to_append = matches_time_list_new_attacking_attempt[ind] + " Assist - " + assist_text + ". " +  " - " + matches_team_list_new_attacking_attempt[ind] + ". Attacking Attempt"
                matches_assist_list.append(string_to_append)
            else:
                matches_assist_list.append("")

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

    for ind in range(len(sentences_missed_chance)):
        if "Assist" in sentences_missed_chance[ind]:
            matches_assist = re.findall(pattern_assist, sentences_missed_chance[ind])
            if matches_assist:  # Check if matches_assist is not empty
                assist_text = matches_assist[0]  # Access the first element of the list
                string_to_append =  matches_time_list_missed_chance[ind] + " Assist - " + assist_text + ". " + " - " + matches_team_list_missed_chance[ind] + ". Attacking Attempt"
                matches_assist_list.append(string_to_append)
            else:
                matches_assist_list.append("")


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

    for ind in range(len(sentences_shot_blocked)):
        if "Assist" in sentences_shot_blocked[ind]:
            matches_assist = re.findall(pattern_assist, sentences_shot_blocked[ind])
            if matches_assist:  # Check if matches_assist is not empty
                assist_text = matches_assist[0]  # Access the first element of the list
                string_to_append = matches_time_list_shot_blocked[ind] + " Assist - " + assist_text + ". " +  " - " + matches_team_list_shot_blocked[ind] + ". Attacking Attempt"
                matches_assist_list.append(string_to_append)
            else:
                matches_assist_list.append("")

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


    for ind in range(len(sentences_hits_bar)):
        if "Assist" in sentences_hits_bar[ind]:
            matches_assist = re.findall(pattern_assist, sentences_hits_bar[ind])
            if matches_assist:  # Check if matches_assist is not empty
                assist_text = matches_assist[0]  # Access the first element of the list
                string_to_append = matches_time_list_hits_bar[ind] + " Assist - " + assist_text + ". " + " - " + matches_team_list_hits_bar[ind] + ". Attacking Attempt"
                matches_assist_list.append(string_to_append)
            else:
                matches_assist_list.append("") 


    # ----------------> HITS BAR <---------------------------------------

    # with open("web_scrap/txt_files/categories/assist_sentences.txt", 'a', encoding='utf-8') as file:
    #     for ind in range(len(matches_assist_list)):
    #         file.write(matches_assist_list[ind] + "\n")



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
    ATTACKING_ATTEMPT = ["ATTACKING_ATTEMPT" + str(i+1) for i in range(len(TEAM))] 
    print("sssss")
    print(len(TIME))
    print(len(TEAM))
    print(len(PLAYER))
    print(len(WAY_OF_ATTEMPT))
    print(len(ATTACKING_ATTEMPT))
    print("\n\n")


    return ATTACKING_ATTEMPT, PLAYER, TEAM,  TIME, WAY_OF_ATTEMPT


def card_ner(card_type):
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    if card_type == "yellow":
        with open("web_scrap/txt_files/categories/yellow card_sentences.txt", 'r', encoding='utf-8') as f:
            text = f.read()
    elif card_type == "red":
        with open("web_scrap/txt_files/categories/red card_sentences.txt", 'r', encoding='utf-8') as f:
            text = f.read()

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

        return YELLOW_CARD, TEAM, PLAYER, TIME_STAMP
    elif card_type == "red":
        print(len(TEAM))
        print((PLAYER))
        print(len(TIME_STAMP))
        print("\n\n")

        return RED_CARD, TEAM, PLAYER, TIME_STAMP

    

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

    DELAY = ["DELAY" + str(i+1) for i in range(len(TIME_INJURY) + len(TIME_IN_MATCH) + len(TIME_OVER))] 

    print(len(TIME_IN_MATCH))
    print(len(TEAM_IN_MATCH))
    print("-----------------------")

    print(len(TIME_INJURY))
    print(len(TEAM_INJURY))
    print((PLAYER_INJURY))
    #print(len(DELAY))

    print("-----------------------")

    print(len(TIME_OVER))

    return DELAY, TIME_IN_MATCH, TIME_INJURY, TIME_OVER, TEAM_IN_MATCH, TEAM_INJURY, PLAYER_INJURY
    

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
    FIRST_HALF = ["FIRST_HALF" + str(i+1) for i in range(len(SCORE))]

    print(len(SCORE))
    print((TIME_STAMP))
    print(len(FIRST_HALF))
    print("\n\n")

    return FIRST_HALF, SCORE, TIME_STAMP

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
    SECOND_HALF_STARTS = ["SECOND_HALF_STARTS" + str(i+1) for i in range(len(TIME_BEGIN))]

    SCORE_BEGIN = [ent.text for ent in doc1.ents if ent.label_ == "SCORE"]
    SCORE_END = [ent.text for ent in doc2.ents if ent.label_ == "SCORE"]
    SECOND_HALF_ENDS = ["SECOND_HALF_ENDS" + str(i+1) for i in range(len(TIME_END))]
    
    print(len(TIME_BEGIN))
    print(len(SCORE_BEGIN))
    print("-----------------------")
    print(len(TIME_END))
    print(len(SCORE_END))

    return SECOND_HALF_STARTS, TIME_BEGIN, SCORE_BEGIN, SECOND_HALF_ENDS, TIME_END, SCORE_END

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
    EXTRA_TIME_FIRST_HALF_STARTS = ["SECOND_HALF_STARTS" + str(i+1) for i in range(len(TIME_BEGIN))]

    SCORE_BEGIN = [ent.text for ent in doc1.ents if ent.label_ == "SCORE"]
    SCORE_END = [ent.text for ent in doc2.ents if ent.label_ == "SCORE"]
    EXTRA_TIME_FIRST_HALF_ENDS = ["SECOND_HALF_ENDS" + str(i+1) for i in range(len(TIME_END))]


    print(len(TIME_BEGIN))
    print(len(SCORE_BEGIN))
    print("-----------------------")
    print(len(TIME_END))
    print(len(SCORE_END))

    return EXTRA_TIME_FIRST_HALF_STARTS, TIME_BEGIN, SCORE_BEGIN, EXTRA_TIME_FIRST_HALF_ENDS, TIME_END, SCORE_END

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
    SECOND_HALF_STARTS = ["SECOND_HALF_STARTS" + str(i+1) for i in range(len(TIME_BEGIN))]

    SCORE_BEGIN = [ent.text for ent in doc1.ents if ent.label_ == "SCORE"]
    SCORE_END = [ent.text for ent in doc2.ents if ent.label_ == "SCORE"]
    SECOND_HALF_ENDS = ["SECOND_HALF_ENDS" + str(i+1) for i in range(len(TIME_END))]


    print(len(TIME_BEGIN))
    print(len(SCORE_BEGIN))
    print("-----------------------")
    print(len(TIME_END))
    print(len(SCORE_END))

    return SECOND_HALF_STARTS, TIME_BEGIN, SCORE_BEGIN, SECOND_HALF_ENDS, TIME_END, SCORE_END

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
    END_GAME = ["END_GAME" + str(i+1) for i in range(len(SCORE))]
    print(len(SCORE))

    return END_GAME, SCORE

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
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{encode_entity(entities[1][i])}")
                player_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{encode_entity(entities[2][i])}")
                time_uri = Literal(entities[3][i])

                g.add((corner_uri, RDF.type, ex.Corner))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

                g.add((corner_uri, ex.corner_won_for, team_uri))
                g.add((corner_uri, ex.conceded_by, player_uri))
                g.add((corner_uri, ex.happened_at, time_uri))

        if event_type == "HANDBALL":
            for i in range(len(entities[0])):
                handball_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Hand_Ball{str(i+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{encode_entity(entities[1][i])}")
                player_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{encode_entity(entities[2][i])}")
                time_uri = Literal(entities[3][i])

                g.add((handball_uri, RDF.type, ex.Hand_Ball))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

                g.add((handball_uri, ex.conceded_by, player_uri))
                g.add((handball_uri, ex.happened_at, time_uri))
                g.add((player_uri, ex.playsFor, team_uri))

        if event_type == "OFFSIDE":
            for i in range(len(entities[0])):
                offside_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Offside{str(i+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{encode_entity(entities[2][i])}")
                player_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{encode_entity(entities[1][i])}")
                time_uri = Literal(entities[3][i])

                g.add((offside_uri, RDF.type, ex.Offside))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

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

                g.add((foul_uri, RDF.type, ex.Foul))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

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

                g.add((dangerous_play_uri, RDF.type, ex.Dangerous_Play))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

                g.add((dangerous_play_uri, ex.conceded_by, player_uri))
                g.add((dangerous_play_uri, ex.happened_at, time_uri))
                g.add((player_uri, ex.playsFor, team_uri))

        if event_type == "YELLOW_CARD":
            for i in range(len(entities[0])):
                yellow_card_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Yellow_Card{str(i+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{entities[1][i].replace(' ', '_')}")
                player_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{entities[2][i].replace(' ', '_')}")
                time_uri = Literal(entities[3][i])

                g.add((yellow_card_uri, RDF.type, ex.Yellow_Card))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

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

                g.add((red_card_uri, RDF.type, ex.Red_Card))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

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

                g.add((free_kick_uri, RDF.type, ex.Free_Kick))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

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

                g.add((attacking_attempt_uri, RDF.type, ex.Attacking_Attempt))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

                g.add((attacking_attempt_uri, ex.attacking_attempt_counts_for, team_uri))
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

                g.add((substitution_uri, RDF.type, ex.Substitution))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

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

                g.add((penalty_uri, RDF.type, ex.Penalty))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

                g.add((penalty_uri, ex.penalty_caused_by, player_uri))
                g.add((penalty_uri, ex.happened_at, time_uri))
                g.add((player_uri, ex.playsFor, team_uri))        
                                                                
                                                        
        if event_type == "DELAY":
            ind = 0
            for i in range(len(entities[1])):
                delay_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Delay{str(ind+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{entities[4][i].replace(' ', '_')}")
                time_uri = Literal(entities[1][i])

                g.add((delay_uri, RDF.type, ex.Delay))
                g.add((team_uri, RDF.type, ex.Team))

                g.add((delay_uri, ex.happened_at, time_uri))  
                g.add((delay_uri, ex.delay_caused_from, team_uri))   

                ind += 1
            for i in range(len(entities[2])):
                delay_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Delay{str(ind+1)}")
                team_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Team{entities[5][i].replace(' ', '_')}")
                player_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Player{entities[6][i].replace(' ', '_')}")
                time_uri = Literal(entities[2][i])

                g.add((delay_uri, RDF.type, ex.Delay))
                g.add((team_uri, RDF.type, ex.Team))
                g.add((player_uri, RDF.type, ex.Player))

                g.add((delay_uri, ex.player_injured, player_uri))
                g.add((delay_uri, ex.happened_at, time_uri))
                g.add((delay_uri, ex.delay_caused_from, team_uri)) 
                g.add((player_uri, ex.playsFor, team_uri))

                ind += 1
            for i in range(len(entities[3])):
                delay_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Delay{str(ind+1)}")
                time_uri = Literal(entities[3][i])

                g.add((delay_uri, RDF.type, ex.Delay))
            
                g.add((delay_uri, ex.happened_at, time_uri))  

                ind += 1 


        if event_type == "FIRST_HALF_ENDED":
            for i in range(len(entities[0])):
                first_half_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/First_Half{str(i+1)}")
                score_uri = Literal(entities[1][i])
                time_uri = Literal(entities[2][i])

                g.add((first_half_uri, RDF.type, ex.First_Half))

                g.add((first_half_uri, ex.ended_at, time_uri))
                g.add((first_half_uri, ex.ended_with_score, score_uri)) 


        if event_type == "SECOND_HALF":
            ind = 0
            for i in range(len(entities[0])):
                second_half_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Second_Half{str(ind+1)}")
                score_uri = Literal(entities[2][i])
                time_uri = Literal(entities[1][i])

                g.add((second_half_uri, RDF.type, ex.Second_Half))

                g.add((second_half_uri, ex.started_at, time_uri))
                g.add((second_half_uri, ex.started_with_score, score_uri))   
                ind += 1

            for i in range(len(entities[3])):
                second_half_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Second_Half{str(ind+1)}")
                score_uri = Literal(entities[5][i])
                time_uri = Literal(entities[4][i])

                g.add((second_half_uri, RDF.type, ex.Second_Half))

                g.add((second_half_uri, ex.ended_at, time_uri))
                g.add((second_half_uri, ex.ended_with_score, score_uri))  
                ind += 1                                   

        if event_type == "EXTRA_FIRST":
            ind = 0
            for i in range(len(entities[0])):
                extra_time_first_half_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/First_Half_Extra_Time{str(ind+1)}")
                score_uri = Literal(entities[2][i])
                time_uri = Literal(entities[1][i])

                g.add((extra_time_first_half_uri, RDF.type, ex.First_Half_Extra_Time))

                g.add((extra_time_first_half_uri, ex.started_at, time_uri))
                g.add((extra_time_first_half_uri, ex.started_with_score, score_uri))   
                ind += 1

            for i in range(len(entities[3])):
                extra_time_first_half_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/First_Half_Extra_Time{str(ind+1)}")
                score_uri = Literal(entities[5][i])
                time_uri = Literal(entities[4][i])

                g.add((extra_time_first_half_uri, RDF.type, ex.First_Half_Extra_Time))

                g.add((extra_time_first_half_uri, ex.ended_at, time_uri))
                g.add((extra_time_first_half_uri, ex.ended_with_score, score_uri))  
                ind += 1     

        if event_type == "EXTRA_SECOND":
            ind = 0
            for i in range(len(entities[0])):
                second_half_extra_time_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Second_Half_Extra_Time{str(ind+1)}")
                score_uri = Literal(entities[2][i])
                time_uri = Literal(entities[1][i])

                g.add((second_half_extra_time_uri, RDF.type, ex.Second_Half_Extra_Time))

                g.add((second_half_extra_time_uri, ex.started_at, time_uri))
                g.add((second_half_extra_time_uri, ex.started_with_score, score_uri))   
                ind += 1

            for i in range(len(entities[3])):
                second_half_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/Second_Half_Extra_Time{str(ind+1)}")
                score_uri = Literal(entities[5][i])
                time_uri = Literal(entities[4][i])

                g.add((second_half_extra_time_uri, RDF.type, ex.Second_Half_Extra_Time))

                g.add((second_half_extra_time_uri, ex.ended_at, time_uri))
                g.add((second_half_extra_time_uri, ex.ended_with_score, score_uri))  
                ind += 1               


        if event_type == "END_GAME":
            for i in range(len(entities[0])):
                end_game_uri = URIRef(f"http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/End_Game{str(i+1)}")
                score_uri = Literal(entities[1][i])

                g.add((end_game_uri, RDF.type, ex.End_Game))
                g.add((end_game_uri, ex.ended_with_score, score_uri)) 


    return g


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

FIRST_HALF_ENDED, SCORE, TIME_STAMP = first_half_end_ner() # Perfect
# print("FIRST_HALF_ENDED")
# SECOND_HALF_STARTS, TIME_BEGIN, SCORE_BEGIN, SECOND_HALF_ENDS, TIME_END, SCORE_END = second_half_sentences_ner() # Perfect
# print("second_half_sentences_ner")
# extra_time_first_half_ner() # Perfect
# print("extra_time_first_half_ner")
# extra_time_second_half_ner() # Perfect
# print("extra_time_second_half_ner")
# END_GAME, SCORE = end_game_ner() # Perfect
# print("END_GAME")

# print("delay_ner")


# a,b,c,b,e = free_kick_ner()
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

    ]

rdf_graph = create_rdf_graph(events)
rdf_graph.serialize("output_graph.rdf", format="turtle")

# These ones dont work correctly so it is TODO 
# --------------- &***&*&*&---------------------
# GOAL
# ASSIST
# Ref
# --------------- &***&*&*&---------------------



