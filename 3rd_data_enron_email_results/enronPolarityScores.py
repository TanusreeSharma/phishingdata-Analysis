import sys
import csv
import string
import numpy as np
import matplotlib.pyplot as plt
import nltk.data
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import sentiment
from nltk import word_tokenize
from collections import Counter
from nltk.corpus import stopwords



# Adapted from https://programminghistorian.org/en/lessons/sentiment-analysis

if(len(sys.argv) != 3):
    print("Usage: python3 enronPolarityScores.py <pathtodatafile> <pathtowritefile>")
    sys.exit()

# Open file to read in data
filename = sys.argv[1]
outfile = sys.argv[2]
# Initialize fields and rows arrays
fields = []
rows = []

# Read data in from csv file
csv_file = open(filename, encoding="ISO-8859-1")
csv_reader = csv.reader(csv_file, delimiter=',')
fields = next(csv_reader)

csv.field_size_limit(sys.maxsize)

out_csv_file = open(outfile, mode = 'w')
csv_writer = csv.writer(out_csv_file, delimiter=',')
csv_writer.writerow(['message', 'compound', 'neg', 'neu', 'pos'])


# Analyze sentiment on email contents usign NLTK and tokenizer
sid = SentimentIntensityAnalyzer()
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
# Initalize results dictionary
total = 0
sumVals = [0,0,0,0]
emotion_list = []
# Go through each row in the dataset
# for i in range(10000):
for row in csv_reader:
    # row = next(csv_reader)
    message_text = row[1].split("\n", 15)[15]
    scores = sid.polarity_scores(message_text)
    # Write results to outfile
    csv_writer.writerow([message_text, scores['compound'], scores['neg'], scores['neu'], scores['pos']])
    total+=1
    sumVals[0] += scores['compound']
    sumVals[1] += scores['neg']
    sumVals[2] += scores['neu']
    sumVals[3] += scores['pos']
    # Covert to lowercase
    # lower_case = message_text.lower()
    # # remove punctuation
    # cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
    # # Tokenize words
    # tokenized_words = word_tokenize(cleaned_text, "english")
    # # Remove stop words
    # final_words = []
    # for word in tokenized_words:
    #     if word not in stopwords.words('english'):
    #         final_words.append(word)
    #
    # # Get emotions text
    # with open('../emotions.txt', 'r') as file:
    #     for line in file:
    #         clear_line = line.replace('\n', '').replace(',', '').replace("'", '').strip()
    #         word, emotion = clear_line.split(':')
    #         if word in final_words:
    #             emotion_list.append(emotion)

# emotions = Counter(emotion_list)

# Print out the average polarity score
sigfig = 3
print("total:", total)
with open("enronResults.txt", mode = 'w') as file:
    file.write("Overall Polarity Scores\n")
    file.write(f"compound: {round(sumVals[0]/total, sigfig)}, neg: {round(sumVals[1]/total, sigfig)}, neu: {round(sumVals[2]/total, sigfig)}, pos: {round(sumVals[3]/total, sigfig)}")
    # file.write("\nEmotion Tally\n")
    # file.write(str(emotions))
