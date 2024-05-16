import spacy
from spacy.pipeline import EntityRuler
import re

# # Load Spacy model and disable named entity recognition
# nlp = spacy.load("en_core_web_lg", disable=["ner"])
# ruler = nlp.add_pipe("entity_ruler")

# # Read text from file
# with open('web_scrap/txt_files/categories/substitution_sentences.txt', 'r', encoding='utf-8') as f:
#     text = f.read()

# # Define the regex pattern for player going in and out
# pattern = r"\.\s*([\w\s'-]+)\s+for\s+([\w\s'-]+?)(?=\s*-?\s*(?:injury)?[.\n]|$)"




# # Find all substitutions using regex
# matches = re.findall(pattern, text)

# # Create list of substitutions
# substitutions = [(out.strip(), inn.strip()) for out, inn in matches]

# # Define EntityRuler patterns for substitutions
# patterns = [{"label": "PLAYER_IN", "pattern": player_out} for player_out, _ in substitutions] + \
#            [{"label": "PLAYER_OUT", "pattern": player_in} for _, player_in in substitutions]

# # Add patterns to the EntityRuler
# ruler.add_patterns(patterns)

# # Process text with the EntityRuler
# doc = nlp(text)

# # Extract entities
# PLAYER_IN = [ent.text for ent in doc.ents if ent.label_ == "PLAYER_IN"]
# PLAYER_OUT = [ent.text for ent in doc.ents if ent.label_ == "PLAYER_OUT"]

# with open("test.txt", 'w', encoding='utf-8') as f:
#     for i in range(len(PLAYER_IN)):
#         f.write(PLAYER_IN[i]+"\n")
# # Print results
# print("Number of PLAYER_IN entities:", len(PLAYER_IN))
# print("Number of PLAYER_OUT entities:", len(PLAYER_OUT))
# print("PLAYER_IN entities:", PLAYER_IN)
# print("PLAYER_OUT entities:", PLAYER_OUT)v

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
        #print(desired_time, '  ', desired_team)

# print(len(matches_time_list_new_attacking_attempt))
# print(len(matches_team_list_new_attacking_attempt))


for ind in range(len(sentences_new_attacking_attempt)):
    if "Assist" in sentences_new_attacking_attempt[ind]:
        matches_assist = re.findall(pattern_assist, sentences_new_attacking_attempt[ind])
        if matches_assist:  # Check if matches_assist is not empty
            assist_text = matches_assist[0]  # Access the first element of the list
            string_to_append = matches_time_list_new_attacking_attempt[ind] + " Assist - " + assist_text + ". " +  " - " + matches_team_list_new_attacking_attempt[ind] + ". Attacking Attempt"
            matches_assist_list.append(string_to_append)
        else:
            # If no match found, append an empty string
            matches_assist_list.append("")

# print(matches_assist_list)     

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
        #print(desired_time, '  ', desired_team)

# print(len(matches_time_list_missed_chance))
# print(len(matches_team_list_missed_chance))


for ind in range(len(sentences_missed_chance)):
    if "Assist" in sentences_missed_chance[ind]:
        matches_assist = re.findall(pattern_assist, sentences_missed_chance[ind])
        if matches_assist:  # Check if matches_assist is not empty
            assist_text = matches_assist[0]  # Access the first element of the list
            string_to_append =  matches_time_list_missed_chance[ind] + " Assist - " + assist_text + ". " + " - " + matches_team_list_missed_chance[ind] + ". Attacking Attempt"
            matches_assist_list.append(string_to_append)
        else:
            # If no match found, append an empty string
            matches_assist_list.append("")

# print(matches_assist_list)  

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
        #print(desired_time, '  ', desired_team)

# print(len(matches_time_list_shot_blocked))
# print(len(matches_team_list_shot_blocked))


for ind in range(len(sentences_shot_blocked)):
    if "Assist" in sentences_shot_blocked[ind]:
        matches_assist = re.findall(pattern_assist, sentences_shot_blocked[ind])
        if matches_assist:  # Check if matches_assist is not empty
            assist_text = matches_assist[0]  # Access the first element of the list
            string_to_append = matches_time_list_shot_blocked[ind] + " Assist - " + assist_text + ". " +  " - " + matches_team_list_shot_blocked[ind] + ". Attacking Attempt"
            matches_assist_list.append(string_to_append)
        else:
            # If no match found, append an empty string
            matches_assist_list.append("")

# print(len(matches_assist_list))


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
        #print(desired_time, '  ', desired_team)

# print(len(matches_time_list_hits_bar))
# print(len(matches_team_list_hits_bar))


for ind in range(len(sentences_hits_bar)):
    if "Assist" in sentences_hits_bar[ind]:
        matches_assist = re.findall(pattern_assist, sentences_hits_bar[ind])
        if matches_assist:  # Check if matches_assist is not empty
            assist_text = matches_assist[0]  # Access the first element of the list
            string_to_append = matches_time_list_hits_bar[ind] + " Assist - " + assist_text + ". " + " - " + matches_team_list_hits_bar[ind] + ". Attacking Attempt"
            matches_assist_list.append(string_to_append)
        else:
            # If no match found, append an empty string
            matches_assist_list.append("")

# print(len(matches_assist_list))


# ----------------> HITS BAR <---------------------------------------

# with open("web_scrap/txt_files/categories/assist_sentences.txt", 'a', encoding='utf-8') as file:
#     for ind in range(len(matches_assist_list)):
#         file.write(matches_assist_list[ind] + "\n")



# --------------> Από εδώ και κάτω γίνεται το NER για τα Attacking Attempts.         
with open("web_scrap/txt_files/categories/attacking_attempt_sentences.txt", 'r', encoding='utf-8') as file:
    text = file.read()


pattern_way_of_attempt = r"-\s*([^.]+)\."
pattern_player = r"\.\s*([^-.]+)\s*-(?!\s*Assist)"

matches_player = []

matches_time_list = re.findall(pattern_time, text)

text_without_hits_bar = sentences_missed_chance + sentences_new_attacking_attempt + sentences_shot_blocked


for ind in (text_without_hits_bar):
    matches = re.findall(pattern_player, ind)
    if matches:
        player = matches[0]
        matches_player.append(player)

#print((matches_player))

matches_teams = matches_team_list_new_attacking_attempt + matches_team_list_shot_blocked + matches_team_list_missed_chance + matches_team_list_hits_bar

# matches_team_list = re.findall(pattern_team, text)
matches_way_of_attempt_list = re.findall(pattern_way_of_attempt, text)


print((matches_teams))
# print(len(matches_time_list))
# print((matches_player_list))
# # print(len(matches_team_list))
#print((matches_way_of_attempt_list))


patterns = [
    {"label": "TIME", "pattern": time}for time in matches_time_list
] + [
    {"label": "TEAM", "pattern": team}for team in matches_teams
] + [
    {"label": "PLAYER", "pattern": player}for player in matches_player   
] + [
    {"label": "WAY_OF_ATTEMPT", "pattern": way}for way in matches_way_of_attempt_list        

]

ruler.add_patterns(patterns)
doc = nlp(text)


TIME = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
TEAM = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
# PLAYER = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
# WAY_OF_ATTEMPT = [ent.text for ent in doc.ents if ent.label_ == "WAY_OF_ATTEMPT"]

# print("sssss")
print((TIME))
# print(len(TEAM))
# print(len(PLAYER))
# print(len(WAY_OF_ATTEMPT))
# print("\n\n")