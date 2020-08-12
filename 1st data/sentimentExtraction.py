import sys
import csv
import string
from collections import Counter
import numpy as np
import nltk.data
from nltk import sentiment
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import word_tokenize
from nltk.corpus import stopwords

# Adapted from https://www.youtube.com/watch?v=tQ_nVSxjn_s

if(len(sys.argv) != 3):
    print("Usage: python3 sentimentExtraction.py <pathtodatafile> <pathtowritefile>")
    sys.exit()

# Open file to read in data
filename = sys.argv[1]
outfile = sys.argv[2]
# Initialize fields and rows arrays
fields = []
rows = []

# Read data in from csv file
with open(filename, encoding="ISO-8859-1") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    fields = next(csv_reader)
    for row in csv_reader:
        rows.append(row)

results = []
emotion_list = []

for row in rows:
    message_text = row[1]
    # Covert to lowercase
    lower_case = message_text.lower()
    # remove punctuation
    cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
    # Tokenize words
    tokenized_words = word_tokenize(cleaned_text, "english")
    # Remove stop words
    final_words = []

    for word in tokenized_words:
        if word not in stopwords.words('english'):
            final_words.append(word)

    # Get emotions text
    with open('emotions.txt', 'r') as file:
        for line in file:
            clear_line = line.replace('\n', '').replace(',', '').replace("'", '').strip()
            word, emotion = clear_line.split(':')
            if word in final_words:
                emotion_list.append(emotion)

with open("results.txt", mode = 'w') as file:
    file.write("Emotion Tally\n")
    file.write(str(Counter(emotion_list)))
