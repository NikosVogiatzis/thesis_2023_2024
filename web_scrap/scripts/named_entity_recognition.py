"""
    In this file NER (Named Entity Recognition) is implemented. For each category, we open the file and read the content. After that, we define patterns 
    that will match the desired text to get annotated as entity. This is implemented mainly based on regular expression, because most of the sentences have a certain 
    format. All NER for each category happens in a seperate function for each category/entity of ontology.
    We are using spacy and entityRuler to make our custom entities.
"""

from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS, OWL
import spacy
from spacy.pipeline.entityruler import EntityRuler
import re


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
    matches_game = re.findall(pattern_match_game, text)

    # EntityRuler patterns
    patterns = [   
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [    
        {"label": "TEAM", "pattern": team} for team in matches_teams
    ] + [
        {"label": "PLAYER", "pattern": player} for player in matches_players
    ] + [
        {"label": "GAME", "pattern": game} for game in matches_game    
    ]

    # Add patterns to the EntityRuler
    ruler.add_patterns(patterns)
    doc = nlp(text)

    # Define list for each entity in its category
    TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    LABELS = []
    GAME_LABELS = [ent.text for ent in doc.ents if ent.label_ == "GAME"]
    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])

    for i in range(len(LABELS)):
        corner_uri = URIRef(ex+f"/Corner{str(i+1)}")
        team_uri = URIRef(ex+f"/{TEAM[i].replace(' ', '_')}")
        player_uri = URIRef(ex+f"/{PLAYER[i].replace(' ', '_')}")
        time_uri = Literal(TIME_STAMP[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS[i]).strip())
        game = (GAME_LABELS[i])

        g.add((corner_uri, RDF.type, ex.Corner))
        g.add((team_uri, RDF.type, ex.Team))
        g.add((team_uri, RDFS.label, Literal(TEAM[i].replace(' ', '_'))))
        g.add((player_uri, RDF.type, ex.Player))
        g.add((player_uri, RDFS.label, Literal(PLAYER[i].replace(' ', '_'))))
        g.add((corner_uri, RDFS.comment, labels))
        g.add((corner_uri, ex.corner_won_for, team_uri))
        g.add((corner_uri, ex.conceded_by, player_uri))
        g.add((corner_uri, ex.happened_at, time_uri))

        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((game, RDF.type, ex.Match))
        g.add((corner_uri, ex.at_game, game))


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
    matches_game = re.findall(pattern_match_game, text)

    # Define EntityRuler patterns
    patterns = [
        {"label": "PLAYER_OUT", "pattern": player_out} for player_out in matches_players_out
    ] + [    
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [
        {"label": "PLAYER_IN", "pattern": player_in} for player_in in matches_players_in
    ] + [
        {"label": "TEAM", "pattern": team} for team in matches_teams   
    ] + [
        {"label": "GAME", "pattern": game} for game in matches_game        
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
    GAME_LABELS = [ent.text for ent in doc.ents if ent.label_ == "GAME"]
    
    LABELS = []
    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])

    for i in range(len(LABELS)):
        substitution_uri = URIRef(ex+f"/Substitution{str(i+1)}")
        team_uri = URIRef(ex+f"/{TEAM[i].replace(' ', '_')}")
        player_in_uri = URIRef(ex+f"/{PLAYER_IN[i].replace(' ', '_')}")
        player_out_uri = URIRef(ex+f"/{PLAYER_OUT[i].replace(' ', '_')}")
        time_uri = Literal(TIME_STAMP[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS[i]).strip())
        game = Literal(GAME_LABELS[i])

        g.add((substitution_uri, RDF.type, ex.Substitution))
        g.add((team_uri, RDF.type, ex.Team))
        g.add((team_uri, RDFS.label, Literal(TEAM[i].replace(' ', '_'))))
        g.add((player_in_uri, RDF.type, ex.Player))
        g.add((player_out_uri, RDF.type, ex.Player))

        g.add((player_in_uri, RDFS.label, Literal(PLAYER_IN[i].replace(' ', '_'))))
        g.add((player_out_uri, RDFS.label, Literal(PLAYER_OUT[i].replace(' ', '_'))))

        g.add((substitution_uri, RDFS.comment, labels))
        g.add((substitution_uri, ex.sub_for, team_uri))
        g.add((substitution_uri, ex.happened_at, time_uri))
        g.add((substitution_uri, ex.sub_player_in, player_in_uri))
        g.add((substitution_uri, ex.sub_player_out, player_out_uri))
        g.add((player_in_uri, ex.playsFor, team_uri))
        g.add((player_out_uri, ex.playsFor, team_uri))

        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((substitution_uri, ex.at_game, game))
        

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
    matches_game = re.findall(pattern_match_game, text)
    
    # Define EntityRuler patterns
    patterns = [
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [
        {"label": "TEAM", "pattern": team} for team in matches_teams
    ] + [
        {"label": "PLAYER", "pattern": player} for player in matches_players
    ] + [
        {"label": "GAME", "pattern": game} for game in matches_game        
    ]

    # Add patterns to the EntityRuler
    ruler.add_patterns(patterns)
    doc = nlp(text)

    TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    GAME_LABELS = [ent.text for ent in doc.ents if ent.label_ == "GAME"]
    LABELS = []
    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])

    for i in range(len(LABELS)):
        handball_uri = URIRef(ex+f"/Hand_Ball{str(i+1)}")
        team_uri = URIRef(ex+f"/{TEAM[i].replace(' ', '_')}")
        player_uri = URIRef(ex+f"/{PLAYER[i].replace(' ', '_')}")
        time_uri = Literal(TIME_STAMP[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS[i]).strip())
        game = Literal(GAME_LABELS[i])

        g.add((handball_uri, RDF.type, ex.Hand_Ball))
        g.add((team_uri, RDF.type, ex.Team))
        g.add((team_uri, RDFS.label, Literal(TEAM[i].replace(' ', '_'))))
        g.add((player_uri, RDF.type, ex.Player)) 
        g.add((player_uri, RDFS.label, Literal(PLAYER[i].replace(' ', '_'))))
        g.add((handball_uri, RDFS.comment, labels))
        g.add((handball_uri, ex.conceded_by, player_uri))
        g.add((handball_uri, ex.happened_at, time_uri))
        g.add((player_uri, ex.playsFor, team_uri))
        
        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((handball_uri, ex.at_game, game))

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
    matches_game = re.findall(pattern_match_game, text)
    # Define EntityRuler patterns
    patterns = [
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [
        {"label": "TEAM", "pattern": team} for team in matches_teams
    ] + [
        {"label": "PLAYER", "pattern": player} for player in matches_players
    ] + [
        {"label": "GAME", "pattern": game} for game in matches_game        
    ]
 
    # Add patterns to the EntityRuler
    ruler.add_patterns(patterns)
    doc = nlp(text)

    TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    PLAYER = [player.replace("is", "").rstrip() for player in PLAYER]
    TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    GAME_LABELS = [ent.text for ent in doc.ents if ent.label_ == "GAME"]
    LABELS = []
    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])

    for i in range(len(LABELS)):
        offside_uri = URIRef(ex+f"/Offside{str(i+1)}")
        team_uri = URIRef(ex+f"/{TEAM[i].replace(' ', '_')}")
        player_uri = URIRef(ex+f"/{PLAYER[i].replace(' ', '_')}")
        time_uri = Literal(TIME_STAMP[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS[i]).strip())
        game = Literal(GAME_LABELS[i])

        g.add((offside_uri, RDF.type, ex.Offside))
        g.add((team_uri, RDF.type, ex.Team))
        g.add((team_uri, RDFS.label, Literal(TEAM[i].replace(' ', '_'))))
        g.add((player_uri, RDF.type, ex.Player))
        g.add((player_uri, RDFS.label, Literal(PLAYER[i].replace(' ', '_'))))
        g.add((offside_uri, RDFS.comment, labels))
        g.add((offside_uri, ex.offside_for, team_uri))
        g.add((offside_uri, ex.offside_caused_by, player_uri))
        g.add((offside_uri, ex.happened_at, time_uri))
        g.add((player_uri, ex.playsFor, team_uri))
    
        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((offside_uri, ex.at_game, game))


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
    matches_game = re.findall(pattern_match_game, text)
    # Define EntityRuler patterns
    patterns = [
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [
        {"label": "TEAM", "pattern": team} for team in matches_teams
    ] + [
        {"label": "PLAYER", "pattern": player} for player in matches_players
    ] + [
        {"label": "AT_PLACE", "pattern": place} for place in matches_places    
    ] + [
        {"label": "GAME", "pattern": game} for game in matches_game        
    ]

    # Add patterns to the EntityRuler
    ruler.add_patterns(patterns)
    doc = nlp(text)

    TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
    TEAM = [team.replace(" -", "").rstrip() for team in TEAM] 
    PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    AT_PLACE = [ent.text for ent in doc.ents if ent.label_ == "AT_PLACE"]
    GAME_LABELS = [ent.text for ent in doc.ents if ent.label_ == "GAME"]
    LABELS = []     
    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])

    for i in range(len(LABELS)):
        free_kick_uri = URIRef(ex+f"/Free_Kick{str(i+1)}")
        team_uri = URIRef(ex+f"/{TEAM[i].replace(' ', '_')}")
        player_uri = URIRef(ex+f"/{PLAYER[i].replace(' ', '_')}")
        at_place_uri = Literal(AT_PLACE[i].replace(' ', '_'))
        time_uri = Literal(TIME_STAMP[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS[i]).strip())
        game = Literal(GAME_LABELS[i])


        g.add((free_kick_uri, RDF.type, ex.Free_Kick))
        g.add((team_uri, RDF.type, ex.Team))
        g.add((team_uri, RDFS.label, Literal(TEAM[i].replace(' ', '_'))))
        g.add((player_uri, RDF.type, ex.Player))
        g.add((player_uri, RDFS.label, Literal(PLAYER[i].replace(' ', '_'))))
        g.add((free_kick_uri, RDFS.comment, labels))
        g.add((free_kick_uri, ex.won_for, team_uri))
        g.add((free_kick_uri, ex.won_at_place, at_place_uri))
        g.add((free_kick_uri, ex.won_by, player_uri))
        g.add((free_kick_uri, ex.happened_at, time_uri))
        g.add((player_uri, ex.playsFor, team_uri))


        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((free_kick_uri, ex.at_game, game))

def foul_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open("web_scrap/txt_files/categories/foul_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()
    sentences = text.split('\n')

    # Define the regex pattern
    pattern_players = r"by\s+(.*?)\s+-"
    pattern_teams = r"-\s+(.*)"
    pattern_time = r"\d+\+?\d*'"

    # Find matches in each sentence based on regexes above.
    matches_players = re.findall(pattern_players, text)
    matches_teams = re.findall(pattern_teams, text)
    matches_time = re.findall(pattern_time, text)
    matches_game = re.findall(pattern_match_game, text)
    # Define EntityRuler patterns
    patterns = [
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [
        {"label": "TEAM", "pattern": team} for team in matches_teams
    ] + [
        {"label": "PLAYER", "pattern": player} for player in matches_players   
    ] + [
        {"label": "GAME", "pattern": game} for game in matches_game        
    ]

    # Add patterns to the EntityRuler
    ruler.add_patterns(patterns)
    doc = nlp(text)

    TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    GAME_LABELS = [ent.text for ent in doc.ents if ent.label_ == "GAME"]
    LABELS = []
    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])

    for i in range(len(LABELS)):
        foul_uri = URIRef(ex+f"/Foul{str(i+1)}")
        team_uri = URIRef(ex+f"/{TEAM[i].replace(' ', '_')}")
        player_uri = URIRef(ex+f"/{PLAYER[i].replace(' ', '_')}")
        time_uri = Literal(TIME_STAMP[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS[i]).strip())
        game = Literal(GAME_LABELS[i])

        g.add((foul_uri, RDF.type, ex.Foul))
        g.add((team_uri, RDF.type, ex.Team))
        g.add((team_uri, RDFS.label, Literal(TEAM[i].replace(' ', '_'))))
        g.add((player_uri, RDF.type, ex.Player))
        g.add((player_uri, RDFS.label, Literal(PLAYER[i].replace(' ', '_'))))
        g.add((foul_uri, RDFS.comment, labels))
        g.add((foul_uri, ex.foul_from, team_uri))
        g.add((foul_uri, ex.fouled_by, player_uri))
        g.add((foul_uri, ex.happened_at, time_uri))
        g.add((player_uri, ex.playsFor, team_uri))

        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((foul_uri, ex.at_game, game))

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
    matches_game = re.findall(pattern_match_game, text)
    # Define EntityRuler patterns
    patterns = [
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [
        {"label": "TEAM", "pattern": team} for team in matches_teams
    ] + [
        {"label": "PLAYER", "pattern": player} for player in matches_players   
    ] + [
        {"label": "GAME", "pattern": game} for game in matches_game        
    ]

    # Add patterns to the EntityRuler
    ruler.add_patterns(patterns)
    doc = nlp(text)

    TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    GAME_LABELS = [ent.text for ent in doc.ents if ent.label_ == "GAME"]

    LABELS = []
    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])

    for i in range(len(LABELS)):
        dangerous_play_uri = URIRef(ex+f"/Dangerous_Play{str(i+1)}")
        team_uri = URIRef(ex+f"/{TEAM[i].replace(' ', '_')}")
        player_uri = URIRef(ex+f"/{PLAYER[i].replace(' ', '_')}")
        time_uri = Literal(TIME_STAMP[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS[i]).strip())
        game = Literal(GAME_LABELS[i])

        g.add((dangerous_play_uri, RDF.type, ex.Dangerous_Play))
        g.add((team_uri, RDF.type, ex.Team))
        g.add((team_uri, RDFS.label, Literal(TEAM[i].replace(' ', '_'))))
        g.add((player_uri, RDF.type, ex.Player))
        g.add((player_uri, RDFS.label, Literal(PLAYER[i].replace(' ', '_'))))
        g.add((dangerous_play_uri, RDFS.comment, labels))
        g.add((dangerous_play_uri, ex.conceded_by, player_uri))
        g.add((dangerous_play_uri, ex.happened_at, time_uri))
        g.add((player_uri, ex.playsFor, team_uri))

 
        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((dangerous_play_uri, ex.at_game, game))

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

    matches_game = []
    # matches_game = re.findall(pattern_match_game, text)

    for sentence in sentences_simple:
        match_player = re.search(pattern_players_simple, sentence)
        match_team = re.search(pattern_teams_simple, sentence)
        match_time = re.search(pattern_time, sentence)
        match_game = re.search(pattern_match_game, sentence)
        if match_team and match_player and match_time:
            matches_teams_simple.append(match_team.group(1))
            matches_players_simple.append(match_player.group(1))    
            matches_time.append(match_time.group(0)) 
            matches_game.append(match_game.group(0))

    for sentence in sentences_conceded:
        match_player = re.search(pattern_players_conceded, sentence)
        match_team = re.search(pattern_teams_conceded, sentence)
        match_time = re.search(pattern_time, sentence)
        match_game = re.search(pattern_match_game, sentence)
        if match_team and match_player and match_time:
            matches_teams_conceded.append(match_team.group(1))
            matches_players_conceded.append(match_player.group(1))      
            matches_time.append(match_time.group(0))  
            matches_game.append(match_game.group(0))
       
           

    patterns = [
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [
        {"label": "TEAM", "pattern": team} for team in matches_teams_conceded + matches_teams_simple
    ] + [
        {"label": "PLAYER", "pattern": player} for player in matches_players_conceded + matches_players_simple
    ] + [
        {"label": "GAME", "pattern": game} for game in matches_game    
    ]

    with open('web_scrap/txt_files/categories/penalty_sentences.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    sentences = text.split('\n') 

    ruler.add_patterns(patterns)
    doc = nlp(text)

    TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    GAME_LABELS = [ent.text for ent in doc.ents if ent.label_ == "GAME"]

    LABELS = []
    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])


    for i in range(len(LABELS)):
        penalty_uri = URIRef(ex+f"/Penalty{str(i+1)}")
        team_uri = URIRef(ex+f"/{TEAM[i].replace(' ', '_')}")
        player_uri = URIRef(ex+f"/{PLAYER[i].replace(' ', '_')}")
        time_uri = Literal(TIME_STAMP[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS[i]).strip())
        game = Literal(GAME_LABELS[i])
        
        g.add((penalty_uri, RDF.type, ex.Penalty))
        g.add((team_uri, RDF.type, ex.Team))
        g.add((team_uri, RDFS.label, Literal(TEAM[i].replace(' ', '_'))))
        g.add((player_uri, RDF.type, ex.Player))
        g.add((player_uri, RDFS.label, Literal(PLAYER[i].replace(' ', '_'))))
        g.add((penalty_uri, RDFS.comment, labels))
        g.add((penalty_uri, ex.penalty_caused_by, player_uri))
        g.add((penalty_uri, ex.happened_at, time_uri))
        g.add((player_uri, ex.playsFor, team_uri))  

        
        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((penalty_uri, ex.at_game, game))


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

    pattern_time = r"\d+\+?\d*'" # for all sentences 
    pattern_team = r"- ([^-]+) -" # for NEW_ATTACKING_ATTEMPT and MISSED_CHANCE 

    pattern_assist = r'\. Assist - (.+?)\.$'

    # -----------------> NEW ATTACKING ATTEMPT <----------------------------

    matches_game_list = []

    for sentence in sentences_new_attacking_attempt:
        matches_team = re.findall(pattern_team, sentence)
        matches_time = re.findall(pattern_time, sentence)
        matches_game = re.search(pattern_match_game, sentence)
        if matches_team and matches_time:
            desired_time = matches_time[0]
            desired_team = matches_team[0]
            desired_game = matches_game[0]
            matches_time_list_new_attacking_attempt.append(desired_time)
            matches_team_list_new_attacking_attempt.append(desired_team)
            matches_game_list.append(desired_game)

    # ----------------> MISSED CHANCE <------------------------------

    for sentence in sentences_missed_chance:
        matches_team = re.findall(pattern_team, sentence)
        matches_time = re.findall(pattern_time, sentence)
        matches_game = re.search(pattern_match_game, sentence)
        if matches_team and matches_time:
            desired_time = matches_time[0]
            desired_team = matches_team[0]
            desired_game = matches_game[0]
            matches_time_list_missed_chance.append(desired_time)
            matches_team_list_missed_chance.append(desired_team)
            matches_game_list.append(desired_game)


    # ---------------> SHOT BLOCKED <----------------------------------

    for sentence in sentences_shot_blocked:
        matches_team = re.findall(pattern_team, sentence)
        matches_time = re.findall(pattern_time, sentence)
        matches_game = re.search(pattern_match_game, sentence)
        if matches_team and matches_time:
            desired_time = matches_time[0]
            desired_team = matches_team[0]
            desired_game = matches_game[0]
            matches_time_list_shot_blocked.append(desired_time)
            matches_team_list_shot_blocked.append(desired_team)
            matches_game_list.append(desired_game)

    # ----------------> HITS BAR <---------------------------------------

    for sentence in sentences_hits_bar:
        matches_team = re.findall(pattern_team, sentence)
        matches_time = re.findall(pattern_time, sentence)
        matches_game = re.search(pattern_match_game, sentence)
        if matches_team and matches_time:
            desired_time = matches_time[0]
            desired_team = matches_team[0]
            desired_game = matches_game[0]
            matches_time_list_hits_bar.append(desired_time)
            matches_team_list_hits_bar.append(desired_team)
            matches_game_list.append(desired_game)

    # --------------> Από εδώ και κάτω γίνεται το NER για τα Attacking Attempts.         
    with open('web_scrap/txt_files/categories/attacking_attempt_sentences.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # remove Assist part from sentences
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
    ] + [
        {"label": "GAME", "pattern": game} for game in matches_game_list
    ]

    ruler.add_patterns(patterns)
    doc = nlp("\n".join(processed_lines))

    TIME = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    WAY_OF_ATTEMPT = [ent.text for ent in doc.ents if ent.label_ == "WAY_OF_ATTEMPT"]
    GAME_LABELS = [ent.text for ent in doc.ents if ent.label_ == "GAME"]
    LABELS = []
    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])

    for i in range(len(LABELS)):
        attacking_attempt_uri = URIRef(ex+f"/Attacking_Attempt{str(i+1)}")
        team_uri = URIRef(ex+f"/{TEAM[i].replace(' ', '_')}")
        player_uri = URIRef(ex+f"/{PLAYER[i].replace(' ', '_')}")
        way_of_attempt = Literal(WAY_OF_ATTEMPT[i].replace(' ', '_'))
        time_uri = Literal(TIME[i].replace(' ', '_'))
        labels = Literal(re.sub(pattern_match_game, "", LABELS[i]).strip())
        game = Literal(GAME_LABELS[i])

        g.add((attacking_attempt_uri, RDF.type, ex.Attacking_Attempt))
        g.add((team_uri, RDF.type, ex.Team))
        g.add((team_uri, RDFS.label, Literal(TEAM[i].replace(' ', '_'))))
        g.add((player_uri, RDF.type, ex.Player))
        g.add((player_uri, RDFS.label, Literal(PLAYER[i].replace(' ', '_'))))
        g.add((attacking_attempt_uri, RDFS.comment, labels))
        g.add((attacking_attempt_uri, ex.counts_for, team_uri))
        g.add((attacking_attempt_uri, ex.way_of_attempt, way_of_attempt))
        g.add((attacking_attempt_uri, ex.noted_by, player_uri))
        g.add((attacking_attempt_uri, ex.happened_at, time_uri))
        g.add((player_uri, ex.playsFor, team_uri))

       
        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((attacking_attempt_uri, ex.at_game, game))


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
    matches_game = re.findall(pattern_match_game, text)
    # Define EntityRuler patterns
    patterns = [
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [
        {"label": "TEAM", "pattern": team} for team in matches_teams
    ] + [
        {"label": "PLAYER", "pattern": player} for player in matches_players
    ] + [
        {"label": "GAME", "pattern": game} for game in matches_game        
    ]

    # Add patterns to the EntityRuler
    ruler.add_patterns(patterns)
    doc = nlp(text)

    TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
    PLAYER = [ent.text.strip() for ent in doc.ents if ent.label_ == "PLAYER"]
    TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    GAME_LABELS = [ent.text for ent in doc.ents if ent.label_ == "GAME"]
    if card_type == "yellow":
        YELLOW_CARD = ["YELLOW_CARD" + str(i+1) for i in range(len(TEAM))] 
    elif card_type == "red":
        RED_CARD = ["RED_CARD" + str(i+1) for i in range(len(TEAM))] 


    if card_type == "yellow":
        LABELS = []
        for i in range(len(sentences)-1):
            LABELS.append(sentences[i])

        for i in range(len(LABELS)):
            yellow_card_uri = URIRef(ex+f"/Yellow_Card{str(i+1)}")
            team_uri = URIRef(ex+f"/{TEAM[i].replace(' ', '_')}")
            player_uri = URIRef(ex+f"/{PLAYER[i].replace(' ', '_')}")
            time_uri = Literal(TIME_STAMP[i])
            labels = Literal(re.sub(pattern_match_game, "", LABELS[i]).strip())
            game = Literal(GAME_LABELS[i])

            g.add((yellow_card_uri, RDF.type, ex.Yellow_Card))
            g.add((team_uri, RDF.type, ex.Team))
            g.add((team_uri, RDFS.label, Literal(TEAM[i].replace(' ', '_'))))
            g.add((player_uri, RDF.type, ex.Player))
            g.add((player_uri, RDFS.label, Literal(PLAYER[i].replace(' ', '_'))))
            g.add((yellow_card_uri, RDFS.comment, labels))
            g.add((yellow_card_uri, ex.card_counts_for, team_uri))
            g.add((yellow_card_uri, ex.recieved_by, player_uri))
            g.add((yellow_card_uri, ex.happened_at, time_uri))
            g.add((player_uri, ex.playsFor, team_uri))

    
            index_games_list = game.replace("MATCH_", "").strip()
            game = URIRef(ex+f"/{game.replace(' ', '_')}")
            g.add((game, RDF.type, ex.Match))
            g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
            g.add((yellow_card_uri, ex.at_game, game))
    elif card_type == "red":
        LABELS = []
        for i in range(len(sentences)-1):
            LABELS.append(sentences[i])
        
        for i in range(len(LABELS)):
            red_card_uri = URIRef(ex+f"/Red_Card{str(i+1)}")
            team_uri = URIRef(ex+f"/{TEAM[i].replace(' ', '_')}")
            player_uri = URIRef(ex+f"/{PLAYER[i].replace(' ', '_')}")
            time_uri = Literal(TIME_STAMP[i])
            labels = Literal(re.sub(pattern_match_game, "", LABELS[i]).strip())
            game = Literal(GAME_LABELS[i])

            g.add((red_card_uri, RDF.type, ex.Red_Card))
            g.add((team_uri, RDF.type, ex.Team))
            g.add((team_uri, RDFS.label, Literal(TEAM[i].replace(' ', '_'))))
            g.add((player_uri, RDF.type, ex.Player))
            g.add((player_uri, RDFS.label, Literal(PLAYER[i].replace(' ', '_'))))
            g.add((red_card_uri, RDFS.comment, labels))
            g.add((red_card_uri, ex.card_counts_for, team_uri))
            g.add((red_card_uri, ex.recieved_by, player_uri))
            g.add((red_card_uri, ex.happened_at, time_uri))
            g.add((player_uri, ex.playsFor, team_uri))

            index_games_list = game.replace("MATCH_", "").strip()
            game = URIRef(ex+f"/{game.replace(' ', '_')}")
            g.add((game, RDF.type, ex.Match))
            g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
            g.add((red_card_uri, ex.at_game, game))

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
    matches_game_list = []
    for sentence in sentences_no_injury:
            match_team = re.search(pattern_team_no_injury, sentence)
            match_time = re.search(pattern_time, sentence)
            match_game = re.search(pattern_match_game, sentence)

            if match_team and match_time:
                match_team_no_injury.append(match_team.group(1))
                match_time_no_injury.append(match_time.group(0))
                matches_game_list.append(match_game.group(0))


    for sentence in sentences_injury:
            match_team = re.search(pattern_team_injury, sentence)
            match_time = re.search(pattern_time, sentence)
            match_player = re.search(pattern_player_injury, sentence)
            match_game = re.search(pattern_match_game, sentence)

            if match_player and match_team and match_time:
                match_player_injury.append(match_player.group(1))
                match_team_injury.append(match_team.group(1))
                match_time_injury.append(match_time.group(0))
                matches_game_list.append(match_game.group(0))

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
    ] + [
        {"label": "GAME", "pattern": game} for game in matches_game_list
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

    GAME_LABELS_1 = [ent.text for ent in doc1.ents if ent.label_ == "GAME"]
    GAME_LABELS_2 = [ent.text for ent in doc2.ents if ent.label_ == "GAME"]
    GAME_LABELS_3 = [ent.text for ent in doc3.ents if ent.label_ == "GAME"]
    LABELS_1 = []
    for i in range(len(sentences_no_injury)):
        LABELS_1.append(sentences_no_injury[i])

    LABELS_2 = []
    for i in range(len(sentences_injury)):
        LABELS_2.append(sentences_injury[i])


    LABELS_3 = []
    for i in range(len(sentences_over)):
        LABELS_3.append(sentences_over[i])        
    
    ind = 0
    for i in range(len(TIME_IN_MATCH)):
        delay_uri = URIRef(ex+f"/Delay{str(ind+1)}")
        team_uri = URIRef(ex+f"/{TEAM_IN_MATCH[i].replace(' ', '_')}")
        time_uri = Literal(TIME_IN_MATCH[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS_1[i]).strip())
        game = Literal(GAME_LABELS_1[i])
            
        g.add((delay_uri, RDF.type, ex.Delay))
        g.add((team_uri, RDF.type, ex.Team))
        g.add((team_uri, RDFS.label, Literal(TEAM_IN_MATCH[i].replace(' ', '_'))))
        g.add((delay_uri, RDFS.comment, labels))
        g.add((delay_uri, ex.happened_at, time_uri))  
        g.add((delay_uri, ex.delay_caused_from, team_uri))   

        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((delay_uri, ex.at_game, game))

        ind += 1
    for i in range(len(TIME_INJURY)):
        delay_uri = URIRef(ex+f"/Delay{str(ind+1)}")
        team_uri = URIRef(ex+f"/{TEAM_INJURY[i].replace(' ', '_')}")
        player_uri = URIRef(ex+f"/{PLAYER_INJURY[i].replace(' ', '_')}")
        time_uri = Literal(TIME_INJURY[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS_2[i]).strip())
        game = Literal(GAME_LABELS_2[i])

        g.add((delay_uri, RDF.type, ex.Delay))
        g.add((team_uri, RDF.type, ex.Team))
        g.add((team_uri, RDFS.label, Literal(TEAM_INJURY[i].replace(' ', '_'))))
        g.add((player_uri, RDF.type, ex.Player))
        g.add((player_uri, RDFS.label, Literal(PLAYER_INJURY[i].replace(' ', '_'))))
        g.add((delay_uri, RDFS.comment, labels))
        g.add((delay_uri, ex.player_injured, player_uri))
        g.add((delay_uri, ex.happened_at, time_uri))
        g.add((delay_uri, ex.delay_caused_from, team_uri)) 
        g.add((player_uri, ex.playsFor, team_uri))

        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((delay_uri, ex.at_game, game))

        ind += 1
    for i in range(len(TIME_OVER)):
        delay_uri = URIRef(ex+f"/Delay{str(ind+1)}")
        time_uri = Literal(TIME_OVER[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS_3[i]).strip())
        game = Literal(GAME_LABELS_3[i])

        
        g.add((delay_uri, RDF.type, ex.Delay))
        g.add((delay_uri, RDFS.comment, labels))
        g.add((delay_uri, ex.happened_at, time_uri))  

        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((delay_uri, ex.at_game, game))

        ind += 1 

def first_half_end_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open("web_scrap/txt_files/categories/first_half_sentences.txt", 'r', encoding='utf-8') as f:
        text = f.read()
    sentences = text.split('\n')

    # Define the regex pattern 
    pattern_score = r"ended\s*-\s*(.+)"
    pattern_time = r"\d+\+?\d*'"

    # Find matches in each sentence based on regexes above.
    matches_score = re.findall(pattern_score, text)
    matches_time = re.findall(pattern_time, text)
    matches_game = re.findall(pattern_match_game, text)
    # Define EntityRuler patterns
    patterns = [
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [
        {"label": "SCORE", "pattern": score} for score in matches_score\
    ] + [
        {"label": "GAME", "pattern": game} for game in matches_game            
    ]

    # Add patterns to the EntityRuler
    ruler.add_patterns(patterns)
    doc = nlp(text)

    SCORE = [ent.text for ent in doc.ents if ent.label_ == "SCORE"]
    TIME_STAMP = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    GAME_LABELS_temp =  [ent.text for ent in doc.ents if ent.label_ == "GAME"]
    LABELS = []
    GAME_LABELS = []
    for i in range(1,len(sentences),2):
        LABELS.append(sentences[i])
        GAME_LABELS.append(GAME_LABELS_temp[i])

    for i in range(len(LABELS)):
        first_half_uri = URIRef(ex+f"/First_Half{str(i+1)}")
        score_uri = Literal(SCORE[i])
        time_uri = Literal(TIME_STAMP[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS[i]).strip())
        game = Literal(GAME_LABELS[i])
            

        g.add((first_half_uri, RDF.type, ex.First_Half))
        g.add((first_half_uri, RDFS.comment, labels))
        g.add((first_half_uri, ex.ended_at, time_uri))
        g.add((first_half_uri, ex.ended_with_score, score_uri))

        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((first_half_uri, ex.at_game, game))
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


    matches_score_begin = []
    matches_time_begin = []
    matches_score_end = []
    matches_time_end = []

    matches_all_games_list_list = []

    for sentence in sentences_begin:
        match_score = re.search(pattern_start_score, sentence)
        match_time = re.search(pattern_time_begin, sentence)
        match_game = re.search(pattern_match_game, sentence)
        if match_score and match_time and match_game:
            matches_score_begin.append(match_score.group(1))
            matches_time_begin.append(match_time.group(0))
            matches_all_games_list_list.append(match_game.group(0))


    for sentence in sentences_end:
        match_score = re.search(pattern_end_score, sentence)
        match_time = re.search(pattern_time_end, sentence)
        match_game = re.search(pattern_match_game, sentence)
        if match_score and match_time and match_game:
            matches_score_end.append(match_score.group(1))
            matches_time_end.append(match_time.group(0))
            matches_all_games_list_list.append(match_game.group(0))

    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")
    # Define EntityRuler patterns
    patterns = [
            {"label": "TIME", "pattern": time} for time in matches_time_end + matches_time_begin
        ] + [
            {"label": "SCORE", "pattern": team} for team in matches_score_begin + matches_score_end
        ] + [
            {"label": "GAME", "pattern": game} for game in matches_all_games_list_list    
    ]

    ruler.add_patterns(patterns)

    text1 = '\n'.join(sentences_begin)
    doc1 = nlp(text1)

    text2 = '\n'.join(sentences_end)
    doc2 = nlp(text2)

    TIME_BEGIN = [ent.text for ent in doc1.ents if ent.label_ == "TIME"]
    TIME_END = [ent.text for ent in doc2.ents if ent.label_ == "TIME"]

    GAME_LABELS_1 = [ent.text for ent in doc1.ents if ent.label_ == "GAME"]
    GAME_LABELS_2 = [ent.text for ent in doc2.ents if ent.label_ == "GAME"]

    LABELS_1 = []
    for i in range(0,len(sentences_begin)):
        LABELS_1.append(sentences_begin[i])

    SCORE_BEGIN = [ent.text for ent in doc1.ents if ent.label_ == "SCORE"]
    SCORE_END = [ent.text for ent in doc2.ents if ent.label_ == "SCORE"]
    LABELS_2 = []
    for i in range(0,len(sentences_end)):
        LABELS_2.append(sentences_end[i])

    for i in range(len(LABELS_1)):
        second_half_uri = URIRef(ex+f"/Second_Half{str(i+1)}")
        score_uri = Literal(SCORE_BEGIN[i])
        time_uri = Literal(TIME_BEGIN[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS_1[i]).strip())
        game = Literal(GAME_LABELS_1[i])

        g.add((second_half_uri, RDF.type, ex.Second_Half))
        g.add((second_half_uri, RDFS.comment, labels))
        g.add((second_half_uri, ex.started_at, time_uri))
        g.add((second_half_uri, ex.started_with_score, score_uri))   
        
        
        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((second_half_uri, ex.at_game, game))

    for i in range(len(LABELS_2)):
        second_half_uri = URIRef(ex+f"/Second_Half{str(i+1)}")
        score_uri = Literal(SCORE_END[i])
        time_uri = Literal(TIME_END[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS_2[i]).strip())
        game = Literal(GAME_LABELS_2[i])

        g.add((second_half_uri, RDF.type, ex.Second_Half))
        g.add((second_half_uri, RDFS.comment, labels))
        g.add((second_half_uri, ex.ended_at, time_uri))
        g.add((second_half_uri, ex.ended_with_score, score_uri))

        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((second_half_uri, ex.at_game, game))
   
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

    matches_score_begin = []
    matches_time_begin = []
    matches_score_end = []
    matches_time_end = []

    matches_all_games_list_list = []

    for sentence in sentences_begin:
        match_score = re.search(pattern_start_score, sentence)
        match_time = re.search(pattern_time_begin, sentence)
        match_game = re.search(pattern_match_game, sentence)
        if match_score:
            matches_score_begin.append(match_score.group(1))
        if match_time:
            matches_time_begin.append(match_time.group(0))
        if match_game:
            matches_all_games_list_list.append(match_game.group(0))
         

    # Extract matches for "ended" sentences
    for sentence in sentences_end:
        match_score = re.search(pattern_end_score, sentence)
        match_time = re.search(pattern_time_end, sentence)
        match_game = re.search(pattern_match_game, sentence)

        if match_score:
            matches_score_end.append(match_score.group(1))
        if match_time:
            matches_time_end.append(match_time.group(0))
        if match_game:
            matches_all_games_list_list.append(match_game.group(0))


    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    # Define EntityRuler patterns
    patterns = [
            {"label": "TIME", "pattern": time} for time in matches_time_end + matches_time_begin
        ] + [
            {"label": "SCORE", "pattern": team} for team in matches_score_begin + matches_score_end
        ] + [
            {"label": "GAME", "pattern": game} for game in matches_all_games_list_list    
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

    GAME_LABELS_1 = [ent.text for ent in doc1.ents if ent.label_ == "GAME"]
    GAME_LABELS_2 = [ent.text for ent in doc2.ents if ent.label_ == "GAME"]

    LABELS_2 = []
    for i in range(0,len(sentences_end)):
        LABELS_2.append(sentences_end[i])


    for i in range(len(LABELS_1)):
        extra_time_first_half_uri = URIRef(ex+f"/First_Half_Extra_Time{str(i+1)}")
        score_uri = Literal(SCORE_BEGIN[i])
        time_uri = Literal(TIME_BEGIN[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS_1[i]).strip())
        game = Literal(GAME_LABELS_1[i])

        g.add((extra_time_first_half_uri, RDF.type, ex.First_Half_Extra_Time))
        g.add((extra_time_first_half_uri, RDFS.comment, labels))
        g.add((extra_time_first_half_uri, ex.started_at, time_uri))
        g.add((extra_time_first_half_uri, ex.started_with_score, score_uri))   

        
        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((extra_time_first_half_uri, ex.at_game, game))

    for i in range(len(LABELS_2)):
        extra_time_first_half_uri = URIRef(ex+f"/First_Half_Extra_Time{str(i+1)}")
        score_uri = Literal(SCORE_END[i])
        time_uri = Literal(TIME_END[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS_2[i]).strip())
        game = Literal(GAME_LABELS_2[i])

        g.add((extra_time_first_half_uri, RDF.type, ex.First_Half_Extra_Time))
        g.add((extra_time_first_half_uri, RDFS.comment, labels))
        g.add((extra_time_first_half_uri, ex.ended_at, time_uri))
        g.add((extra_time_first_half_uri, ex.ended_with_score, score_uri))

        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((extra_time_first_half_uri, ex.at_game, game))


def extra_time_second_half_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

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

    matches_score_begin = []
    matches_time_begin = []
    matches_score_end = []
    matches_time_end = []
    
    matches_all_games_list_list = []

    for sentence in sentences_begin:
        match_score = re.search(pattern_start_score, sentence)
        match_time = re.search(pattern_time_begin, sentence)
        match_game = re.search(pattern_match_game, sentence)
        if match_score:
            matches_score_begin.append(match_score.group(1))
        if match_time:
            matches_time_begin.append(match_time.group(0))
        if match_game:
            matches_all_games_list_list.append(match_game.group(0))


    # Extract matches for "ended" sentences
    for sentence in sentences_end:
        match_score = re.search(pattern_end_score, sentence)
        match_time = re.search(pattern_time_end, sentence)
        match_game = re.search(pattern_match_game, sentence)
        if match_score:
            matches_score_end.append(match_score.group(1))
        if match_time:
            matches_time_end.append(match_time.group(0))
        if match_game:
            matches_all_games_list_list.append(match_game.group(0))


    # Define EntityRuler patterns
    patterns = [
            {"label": "TIME", "pattern": time} for time in matches_time_end + matches_time_begin
        ] + [
            {"label": "SCORE", "pattern": team} for team in matches_score_begin + matches_score_end
        ] + [
            {"label": "GAME", "pattern": game} for game in matches_all_games_list_list
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

    GAME_LABELS_1 = [ent.text for ent in doc1.ents if ent.label_ == "GAME"]
    GAME_LABELS_2 = [ent.text for ent in doc2.ents if ent.label_ == "GAME"]

    for i in range(len(LABELS_1)):
        second_half_extra_time_uri = URIRef(ex+f"/Second_Half_Extra_Time{str(i+1)}")
        score_uri = Literal(SCORE_BEGIN[i])
        time_uri = Literal(TIME_BEGIN[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS_1[i]).strip())
        game = Literal(GAME_LABELS_1[i])

        g.add((second_half_extra_time_uri, RDF.type, ex.Second_Half_Extra_Time))
        g.add((second_half_extra_time_uri, RDFS.comment, labels))
        g.add((second_half_extra_time_uri, ex.started_at, time_uri))
        g.add((second_half_extra_time_uri, ex.started_with_score, score_uri))   


        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((second_half_extra_time_uri, ex.at_game, game))

    for i in range(len(LABELS_2)):
        second_half_extra_time_uri = URIRef(ex+f"/Second_Half_Extra_Time{str(i+1)}")
        score_uri = Literal(SCORE_END[i])
        time_uri = Literal(TIME_END[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS_2[i]).strip())
        game = Literal(GAME_LABELS_1[i])

        g.add((second_half_extra_time_uri, RDF.type, ex.Second_Half_Extra_Time))
        g.add((second_half_extra_time_uri, RDFS.comment, labels))
        g.add((second_half_extra_time_uri, ex.ended_at, time_uri))
        g.add((second_half_extra_time_uri, ex.ended_with_score, score_uri)) 

        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((second_half_extra_time_uri, ex.at_game, game))


def end_game_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open('web_scrap/txt_files/categories/end_game_sentences.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    sentences = text.split('\n')

    pattern_score = r" - \s*(.*)"
    matches_score = re.findall(pattern_score, text)
    matches_game = re.findall(pattern_match_game, text)
    # Define EntityRuler patterns
    patterns = [
        {"label": "SCORE", "pattern": team} for team in matches_score
    ] + [
        {"label": "GAME", "pattern": game} for game in matches_game        
    ]

    ruler.add_patterns(patterns)
    doc = nlp(text)

    SCORE = [ent.text for ent in doc.ents if ent.label_ == "SCORE"]
    GAME_LABELS = [ent.text for ent in doc.ents if ent.label_ == "GAME"]
    LABELS = []
    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])
        
    for i in range(len(LABELS)):
        end_game_uri = URIRef(ex+f"/End_Game{str(i+1)}")
        score_uri = Literal(SCORE[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS[i]).strip())
        game = Literal(GAME_LABELS[i])

        g.add((end_game_uri, RDF.type, ex.End_Game))
        g.add((end_game_uri, RDFS.comment, labels))
        g.add((end_game_uri, ex.ended_with_score, score_uri))

        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((end_game_uri, ex.at_game, game))

def goal_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    goal_sentences = []
    own_goal_sentences = []
    with open('web_scrap/txt_files/categories/goal_sentences.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if "Goal!" in line:
                    goal_sentences.append(line.strip())
                else:
                    own_goal_sentences.append(line.strip())

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
    matches_all_games_list_list = []
    for sentence in goal_sentences:
        matches_team = re.findall(pattern_team, sentence)
        matches_time = re.findall(pattern_time, sentence)
        matches_player = re.findall(pattern_player, sentence)
        matches_score = re.findall(pattern_score, sentence)
        matches_way = re.findall(pattern_way_of_scoring, sentence)
        match_game = re.search(pattern_match_game, sentence)
        if matches_team and matches_time and matches_player and matches_score and matches_way and match_game:
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
            matches_all_games_list_list.append(match_game.group(0))

    matches_player_list_goal = [player + ' -' for player in matches_player_list_goal]
    matches_team_list_goal = [team + ' -' for team in matches_team_list_goal]

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
        match_game = re.search(pattern_match_game, sentence)
        if matches_player and matches_team and matches_score and matches_time and match_game:
            desired_player = matches_player[0]
            desired_team = matches_team[0]
            desired_score = matches_score[0]
            desired_time = matches_time[0]

            matches_player_list_own_goal.append(desired_player.strip())
            matches_team_list_own_goal.append(desired_team.strip())
            matches_score_list_own_goal.append(desired_score.strip())
            matches_time_list_own_goal.append(desired_time.strip())
            matches_all_games_list_list.append(match_game.group(0))

    matches_player_list_own_goal = [player + ',' for player in matches_player_list_own_goal]
    matches_team_list_own_goal = [team + '.' for team in matches_team_list_own_goal]

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
    ] + [    
        {"label": "GAME", "pattern": game} for game in matches_all_games_list_list        
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

    GAME_LABELS_1 = [ent.text for ent in doc1.ents if ent.label_ == "GAME"]
    GAME_LABELS_2 = [ent.text for ent in doc2.ents if ent.label_ == "GAME"]

    LABELS_1 = []
    for i in range(len(goal_sentences)):
        LABELS_1.append(goal_sentences[i])

    LABELS_2 = []
    for i in range(len(own_goal_sentences)):
        LABELS_2.append(own_goal_sentences[i])
    
    for i in range(len(LABELS_1)):
        goal_uri = URIRef(ex+f"/Goal_Scored{str(i+1)}")
        team_uri = URIRef(ex+f"/{TEAM_GOAL[i].replace(' ', '_')}")
        player_uri = URIRef(ex+f"/{PLAYER_GOAL[i].replace(' ', '_')}")
        labels = Literal(re.sub(pattern_match_game, "", LABELS_1[i]).strip())
        game = Literal(GAME_LABELS_1[i])
        score_uri = Literal(SCORE_GOAL[i])
        way_of_scoring_uri = Literal(WAY_OF_SCORING[i])
        time_uri = Literal(TIME_STAMP_GOAL[i])

        g.add((goal_uri, RDF.type, ex.Goal_Scored))
        g.add((team_uri, RDF.type, ex.Team))
        g.add((team_uri, RDFS.label, Literal(TEAM_GOAL[i].replace(' ', '_'))))
        g.add((player_uri, RDF.type, ex.Player))
        g.add((player_uri, RDFS.label, Literal(PLAYER_GOAL[i].replace(' ', '_'))))
        g.add((goal_uri, RDFS.comment, labels))
        g.add((goal_uri, ex.scored_by, player_uri))
        g.add((goal_uri, ex.counts_for, team_uri))
        g.add((goal_uri, ex.scored_with, way_of_scoring_uri)) 
        g.add((goal_uri, ex.makes_score, score_uri))
        g.add((goal_uri, ex.happened_at, time_uri))  

        
        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((goal_uri, ex.at_game, game))


    for j in range(len(LABELS_2)):
        own_goal_uri = URIRef(ex+f"/Own_Goal{str(j+1)}")
        team_uri = URIRef(ex+f"/{TEAM_OWN_GOAL[j].replace(' ', '_')}")
        player_uri = URIRef(ex+f"/{PLAYER_OWN_GOAL[j].replace(' ', '_')}")
        labels = Literal(re.sub(pattern_match_game, "", LABELS_2[j]).strip())
        score_uri = Literal(SCORE_OWN_GOAL[j])
        time_uri = Literal(TIME_STAMP_OWN_GOAL[j])
        game = Literal(GAME_LABELS_2[j])

        g.add((own_goal_uri, RDF.type, ex.Own_Goal))
        g.add((team_uri, RDF.type, ex.Team))
        g.add((team_uri, RDFS.label, Literal(TEAM_OWN_GOAL[j].replace(' ', '_'))))
        g.add((player_uri, RDF.type, ex.Player))
        g.add((player_uri, RDFS.label, Literal(PLAYER_OWN_GOAL[j].replace(' ', '_'))))
        g.add((own_goal_uri, RDFS.comment, labels))
        g.add((own_goal_uri, ex.scored_by, player_uri))
        g.add((own_goal_uri, ex.makes_score, score_uri))
        g.add((player_uri, ex.playsFor, team_uri))
        g.add((own_goal_uri, ex.happened_at, time_uri))

        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((own_goal_uri, ex.at_game, game))
    
def assist_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    with open("web_scrap/txt_files/categories/assist_sentences.txt", 'r', encoding='utf-8') as file:
        text = file.read()
    sentences = text.split('\n')

    pattern_assisted_event = r"(Attacking_Attempt|Goal_Scored)(\d+)"
    pattern_player  = r"-\s(.*?)(?=\swith|\sfollowing|\safter|\.\s)"

    matches_assisted_event = []
    matches_game = re.findall(pattern_match_game, text)
    matches_players = re.findall(pattern_player, text)
    matches_all_games_list_list = re.findall(pattern_match_game, text)

    matches_ = re.findall(pattern_assisted_event, text)

    for match in matches_:
        extracted_match = match[0] + match[1]
        matches_assisted_event.append(extracted_match)

    patterns = [
        {"label": "PLAYER", "pattern": player} for player in matches_players
    ] + [
        {"label": "ASSISTED", "pattern": assisted} for assisted in matches_assisted_event
    ] + [
        {"label": "GAME", "pattern": game} for game in matches_all_games_list_list       
        
    ]

    ruler.add_patterns(patterns)
    doc = nlp(text)

    PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    ASSISTED_EVENT = [ent.text for ent in doc.ents if ent.label_ == "ASSISTED"]
    GAME_LABELS = [ent.text for ent in doc.ents if ent.label_ == "GAME"]


    LABELS = []
    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])


    for i in range(len(LABELS)):
        assist_uri = URIRef(ex+f"/Assist{str(i+1)}")
        player_uri = URIRef(ex+f"/{PLAYER[i].replace(' ', '_')}")
        assisted_event_uri = URIRef(ex +f"/" + ASSISTED_EVENT[i])
        game = Literal(GAME_LABELS[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS[i]).strip())
        
        g.add((assist_uri, RDF.type, ex.Assist))
        g.add((assist_uri, ex.assist_made_by, player_uri))
        g.add((assist_uri, RDFS.comment, labels))  
        g.add((assist_uri, ex.refers_to, assisted_event_uri))

        g.add((player_uri, RDF.type, ex.Player))
        g.add((player_uri, RDFS.label, Literal(PLAYER[i].replace(' ', '_'))))



        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((assist_uri, ex.at_game, game))


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
    matches_game = re.findall(pattern_match_game, text)
    patterns = [
        {"label": "TIME", "pattern": time} for time in matches_time
    ] + [
        {"label": "DECISION", "pattern": dec} for dec in matche_var_decision
    ] + [
        {"label": "GAME", "pattern": game} for game in matches_game        
    ]

    ruler.add_patterns(patterns)
    doc = nlp(text)

    TIME = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
    DECISION = [ent.text for ent in doc.ents if ent.label_ == "DECISION"]
    GAME_LABELS = [ent.text for ent in doc.ents if ent.label_ == "GAME"]
  
    LABELS = []
    for i in range(len(sentences)-1):
        LABELS.append(sentences[i])

    for i in range(len(LABELS)):
        var_uri = URIRef(ex+f"/VAR{str(i+1)}")
        time_uri = Literal(TIME[i])
        decision_uri = Literal(DECISION[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS[i]).strip())
        game = Literal(GAME_LABELS[i])
        g.add((var_uri, RDF.type, ex.VAR))
        g.add((var_uri, RDFS.comment, labels)) 
        g.add((var_uri, ex.happened_at, time_uri))
        g.add((var_uri, ex.decision_made, decision_uri))
        
        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((var_uri, ex.at_game, game))

def penalty_procedure_ner():
    nlp = spacy.load("en_core_web_lg", disable=["ner"])
    ruler = nlp.add_pipe("entity_ruler")

    penalty_goal_sentences = []
    penalty_shootout_begins_sentences = []
    pentalty_shootout_ends_sentences = []
    pentalty_saved_sentences = []
    penalty_missed_sentences = []
    matches_all_games_list_list = []

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
        match_game = re.search(pattern_match_game, sentence)
        if match_score and match_time:
            desired_time = match_time[0]
            desired_score = match_score[0]

            matches_time_begins.append(desired_time)
            matches_score_begins.append(desired_score)
            matches_all_games_list_list.append(match_game.group(0))

    for sentence in pentalty_shootout_ends_sentences:
        match_time = re.findall(pattern_time, sentence)
        match_score = re.findall(pattern_score_ends, sentence)
        match_game = re.findall(pattern_match_game, sentence)
        if match_score and match_time:
            desired_time = match_time[0]
            desired_score = match_score[0]
            desired_game= match_game[0]

            matches_time_ends.append(desired_time)
            matches_score_ends.append(desired_score)
            matches_all_games_list_list.append(desired_game)

    for sentence in pentalty_saved_sentences:
        match_time = re.findall(pattern_time, sentence)
        match_player = re.findall(pattern_player_saved, sentence)
        match_team = re.findall(pattern_team_saved, sentence)
        match_way = re.findall(pattern_way_saved, sentence)
        match_game = re.findall(pattern_match_game, sentence)
        if match_time and match_player and match_team and match_way:
            desired_time = match_time[0]
            desired_player = match_player[0]
            desired_team = match_team[0]
            desired_way = match_way[0]
            desired_game= match_game[0]

            matches_time_saved.append(desired_time)
            matches_player_saved.append(desired_player)
            matches_team_saved.append(desired_team)
            matches_way_saved.append(desired_way)
            matches_all_games_list_list.append(desired_game)

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
        match_game = re.search(pattern_match_game, sentence)

        if match_time and match_player and match_team and match_way:
            desired_time = match_time[0]
            desired_player = match_player[0]
            desired_team = match_team[0]
            desired_way = match_way[0]

            matches_time_missed.append(desired_time)
            matches_player_missed.append(desired_player)
            matches_team_missed.append(desired_team)
            matches_way_missed.append(desired_way)
            matches_all_games_list_list.append(match_game.group(0))

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
        match_game = re.search(pattern_match_game, sentence)
        if match_game:
            matches_all_games_list_list.append(match_game.group(0))
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
            full_match = player_name_match.group(0).strip()
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
    ] + [
        {"label": "GAME", "pattern": game} for game in matches_all_games_list_list
    ]
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

    GAME_LABELS_1 = [ent.text for ent in doc1.ents if ent.label_ == "GAME"]
    GAME_LABELS_2 = [ent.text for ent in doc2.ents if ent.label_ == "GAME"]
    GAME_LABELS_3 = [ent.text for ent in doc3.ents if ent.label_ == "GAME"]
    GAME_LABELS_4 = [ent.text for ent in doc4.ents if ent.label_ == "GAME"]
    GAME_LABELS_5 = [ent.text for ent in doc5.ents if ent.label_ == "GAME"]

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

    for i in range(len(TIME_BEGINS)):
        penalty_procedure_uri = URIRef(ex+f"/Penalty_Procedure{str(i+1)}")
        score_uri = Literal(SCORE_BEGINS[i])
        time_uri = Literal(TIME_BEGINS[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS_1[i]).strip())
        game = Literal(GAME_LABELS_2[i])

        g.add((penalty_procedure_uri, RDF.type, ex.Penalty_Procedure))
        g.add((penalty_procedure_uri, RDFS.comment, labels))   
        g.add((penalty_procedure_uri, ex.happened_at, time_uri))
        g.add((penalty_procedure_uri, ex.started_with_score, score_uri))

        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((penalty_procedure_uri, ex.at_game, game))

    for i in range(len(TIME_ENDS)):
        penalty_procedure_uri = URIRef(ex+f"/Penalty_Procedure{str(i+1)}")
        score_uri = Literal(SCORE_ENDS[i])
        time_uri = Literal(TIME_ENDS[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS_2[i]).strip())
        game = Literal(GAME_LABELS_3[i])

        g.add((penalty_procedure_uri, RDF.type, ex.Penalty_Procedure))
        g.add((penalty_procedure_uri, RDFS.comment, labels))    
        g.add((penalty_procedure_uri, ex.ended_with_score, score_uri))

        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((penalty_procedure_uri, ex.at_game, game))

    ind = 0
    for i in range(len(TIME_SAVED)):
        penalty_no_goal = URIRef(ex+f"/Penalty_No_Goal{str(ind+1)}")
        team_uri = URIRef(ex+f"/{TEAM_SAVED[i].replace(' ', '_')}")
        player_uri = URIRef(ex+f"/{PLAYER_SAVED[i].replace(' ', '_')}")
        way_uri = Literal(WAY_SAVED[i])
        time_uri = Literal(TIME_SAVED[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS_3[i]).strip())
        game = Literal(GAME_LABELS_4[i])
   
       

        g.add((penalty_no_goal, RDF.type, ex.Penalty_No_Goal))
        g.add((penalty_no_goal, RDFS.comment, labels))  
        g.add((penalty_no_goal, ex.happened_at, time_uri))
        g.add((penalty_no_goal, ex.missed_by, player_uri))
        g.add((penalty_no_goal, ex.missed_with, way_uri))
        g.add((penalty_no_goal, ex.missed_for, team_uri))
        g.add((player_uri, ex.playsFor, team_uri))

        g.add((player_uri, RDF.type, ex.Player))
        g.add((player_uri, RDFS.label, Literal(PLAYER_SAVED[i].replace(' ', '_'))))

        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((penalty_no_goal, ex.at_game, game))

        ind += 1

    for i in range(len(TIME_MISSED)):     
        penalty_no_goal = URIRef(ex+f"/Penalty_No_Goal{str(ind+1)}")
        team_uri = URIRef(ex+f"/{TEAM_MISSED[i].replace(' ', '_')}")
        player_uri = URIRef(ex+f"/{PLAYER_MISSED[i].replace(' ', '_')}")
        way_uri = Literal(WAY_MISSED[i])
        time_uri = Literal(TIME_MISSED[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS_4[i]).strip())
        game = Literal(GAME_LABELS_5[i])

        g.add((penalty_no_goal, RDF.type, ex.Penalty_No_Goal))
        g.add((penalty_no_goal, RDFS.comment, labels))  
        g.add((penalty_no_goal, ex.happened_at, time_uri))
        g.add((penalty_no_goal, ex.missed_by, player_uri))
        g.add((penalty_no_goal, ex.missed_with, way_uri))
        g.add((penalty_no_goal, ex.missed_for, team_uri))
        g.add((player_uri, ex.playsFor, team_uri))

    
        g.add((player_uri, RDF.type, ex.Player))
        g.add((player_uri, RDFS.label, Literal(PLAYER_MISSED[i].replace(' ', '_'))))

        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((penalty_no_goal, ex.at_game, game))

        ind += 1

    for i in range(len(TIME_GOAL)):
        penalty_goal = URIRef(ex+f"/Penalty_Scored_Goal{str(i+1)}")
        team_uri = URIRef(ex+f"/{TEAM_GOAL[i].replace(' ', '_')}")
        player_uri = URIRef(ex+f"/{PLAYER_GOAL[i].replace(' ', '_')}")
        score_uri = Literal(SCORE_GOAL[i])
        way_uri = Literal(WAY_GOAL[i])
        time_uri = Literal(TIME_GOAL[i])
        labels = Literal(re.sub(pattern_match_game, "", LABELS_5[i]).strip())
        game = Literal(GAME_LABELS_1[i])
        
        g.add((penalty_goal, RDF.type, ex.Penalty_Scored_Goal))
        g.add((penalty_goal, RDFS.comment, labels))
        g.add((penalty_goal, ex.makes_score, score_uri))
        g.add((penalty_goal, ex.happened_at, time_uri))
        g.add((penalty_goal, ex.scored_by, player_uri))
        g.add((penalty_goal, ex.scored_with, way_uri))
        g.add((penalty_goal, ex.counts_for, team_uri))
        g.add((player_uri, ex.playsFor, team_uri)) 

        
        g.add((player_uri, RDF.type, ex.Player))
        g.add((player_uri, RDFS.label, Literal(PLAYER_GOAL[i].replace(' ', '_'))))

        index_games_list = game.replace("MATCH_", "").strip()
        game = URIRef(ex+f"/{game.replace(' ', '_')}")
        g.add((game, RDF.type, ex.Match))
        g.add((game, RDFS.comment, Literal(all_games_list[int(index_games_list)])))
        g.add((penalty_goal, ex.at_game, game))

ex = Namespace("http://www.semanticweb.org/vogia/ontologies/2024/3/untitled-ontology-53/")
g = Graph() 
g.bind("ex", ex)
g.parse("web_scrap/rdf_files/football.ttl")
pattern_match_game = r"MATCH_+\d+"


all_games_list = []

with open("web_scrap/txt_files/matches.txt", "r", encoding="utf-8") as file:
    text = file.read()
game_sentences = text.split('\n')
for sentence in game_sentences:
    all_games_list.append(sentence.strip())
    
corner_ner()
hand_ball_ner()
offside_ner()
foul_ner()
dangerous_play_ner()
card_ner("yellow")
card_ner("red")
free_kick_ner()
substitution_ner()
penalty_ner()
delay_ner()
first_half_end_ner()
second_half_sentences_ner()   
extra_time_first_half_ner()
extra_time_second_half_ner()
end_game_ner()
var_decision_ner()
penalty_procedure_ner()
goal_ner()
attacking_attempt_ner()
assist_ner()

g.serialize("web_scrap/rdf_files/output_graph.ttl", format="turtle")
