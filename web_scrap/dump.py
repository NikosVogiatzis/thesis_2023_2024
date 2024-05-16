import re

# Input sentences
sentences = [
    "14' New attacking attempt. Olivier Giroud - AC Milan - shot with left foot from the right side of the six yard box is saved in the right corner.",
    "14' Missed chance. Ruben Loftus-Cheek - AC Milan - shot with the head from the centre of the box missed to the left. Assist - Rade Krunic with a cross after corner.",
    "18' New attacking attempt. Rade Krunic - AC Milan - shot with right foot from outside the box is saved in the top centre of the goal.",
    "19' New attacking attempt. Théo Hernández - AC Milan - shot with the head from the centre of the box is saved in the top centre of the goal. Assist - Rade Krunic with a cross.",
    # Add more sentences here...
]

# Regular expression pattern
pattern = r'- ([^-]+) -'

# Iterate over each sentence
for sentence in sentences:
    # Find the match
    match = re.search(pattern, sentence)
    # Check if match is found
    if match:
        # Extract the desired text
        extracted_text = match.group(1)
        # Print the extracted text
        print(extracted_text)
    else:
        print("No match found.")
