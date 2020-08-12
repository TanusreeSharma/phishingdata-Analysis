import sys
import csv
import numpy as np
import nltk.data
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import sentiment
import matplotlib.pyplot as plt

# Function used to delete zeros from arrays, used when plotting the pos.png, neg.png, and comp.png
def del_zeros(x):
    i = 0
    while(x[i] == 0 or x[i] < 0):
        if(x[i] == 0):
            del x[i]
        else:
            i+=1
    return x
# Adapted from https://programminghistorian.org/en/lessons/sentiment-analysis

if(len(sys.argv) != 3):
    print("Usage: python3 polarityScoresAll.py <pathtodatafile> <pathtowritefile>")
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

# Analyze sentiment on email contents usign NLTK and tokenizer
sid = SentimentIntensityAnalyzer()
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# Initalize results dictionary
results = []
tokenized_results = []
# Go through each row in the dataset
for row in rows:
    message_text = row[1]
    scores = sid.polarity_scores(message_text)
    results.append([message_text, scores['compound'], scores['neg'], scores['neu'], scores['pos']])
    sentences = tokenizer.tokenize(message_text)
    for sentence in sentences:
        scores = sid.polarity_scores(sentence)
        tokenized_results.append([message_text, scores['compound'], scores['neg'], scores['neu'], scores['pos']])


sumVals = [0,0,0,0]
tokenized_sumVals = [0,0,0,0]
# Write results to outfile
with open(outfile, mode = 'w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['message', 'compound', 'neg', 'neu', 'pos'])
    for row in results:
        sumVals[0] += row[1]
        sumVals[1] += row[2]
        sumVals[2] += row[3]
        sumVals[3] += row[4]
        csv_writer.writerow(row)
newfile = "tokenized_" + outfile
with open(newfile, mode = 'w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['message', 'compound', 'neg', 'neu', 'pos'])
    for row in tokenized_results:
        tokenized_sumVals[0] += row[1]
        tokenized_sumVals[1] += row[2]
        tokenized_sumVals[2] += row[3]
        tokenized_sumVals[3] += row[4]
        csv_writer.writerow(row)
# Print out the average polarity score
sigfig = 3
total = len(results)
print("Untokenized Overall Polarity Scores")
print(f"compound: {round(sumVals[0]/total, sigfig)}, neg: {round(sumVals[1]/total, sigfig)}, neu: {round(sumVals[2]/total, sigfig)}, pos: {round(sumVals[3]/total, sigfig)}")
print("Tokenized Overall Polarity Scores")
total = len(tokenized_results)
print(f"compound: {round(tokenized_sumVals[0]/total, sigfig)}, neg: {round(tokenized_sumVals[1]/total, sigfig)}, neu: {round(tokenized_sumVals[2]/total, sigfig)}, pos: {round(tokenized_sumVals[3]/total, sigfig)}")
