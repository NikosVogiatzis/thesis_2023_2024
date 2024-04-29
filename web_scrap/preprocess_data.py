import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def remove_stopwords(text):
    stop_words = set(stopwords.words('english')) - {'+'}
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word.lower() not in stop_words]
    return ' '.join(filtered_text)

def preprocess_text(text):
    # Remove punctuations
    text = re.sub(r'[^\w\s+]', '', text)
    
    # Remove stop words
    text = remove_stopwords(text)
    
    return text

# Read data from file
with open('web_scrap/commentary.txt', 'r', encoding='utf-8') as file:
    data = file.readlines()

# Preprocess each line of data and write it to the output file
with open('updated_data.txt', 'w', encoding='utf-8') as file:
    for line in data:
        preprocessed_line = preprocess_text(line)
        file.write(preprocessed_line.strip() + '\n')
