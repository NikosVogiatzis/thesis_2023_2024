import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word.lower() not in stop_words]
    return ' '.join(filtered_text)

def preprocess_text(text):
    # Remove digits and punctuation
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    
    # Remove stop words
    text = remove_stopwords(text)
    
    return text

# Read data from file
with open('commentary.txt', 'r') as file:
    data = file.read()

# Preprocess data
preprocessed_data = preprocess_text(data)

# Write preprocessed data to file
with open('updated_data.txt', 'w') as file:
    file.write(preprocessed_data)
