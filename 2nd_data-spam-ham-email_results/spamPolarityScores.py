import sys
import csv
import numpy as np
import nltk.data
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import sentiment
from nltk import word_tokenize

# Adapted from https://programminghistorian.org/en/lessons/sentiment-analysis

if(len(sys.argv) != 3):
    print("Usage: python3 spamPolarityScores.py <pathtodatafile> <pathtowritefile>")
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


email_type = ["spam", "ham"]
# Analyze sentiment on email contents usign NLTK and tokenizer
sid = SentimentIntensityAnalyzer()
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# Initalize results dictionary
results = {}
for type in email_type:
    results[type] = []
# Go through each row in the dataset
for row in rows:
    if(row[0] == "spam" ):
        message_text = row[1]
        scores = sid.polarity_scores(message_text)
        results["spam"].append([message_text, scores['compound'], scores['neg'], scores['neu'], scores['pos']])
        # Uncomment this section to tokenize message contents into phrases, make sure to comment out the two lines above this comment
        # sentences = tokenizer.tokenize(message_text)
        # for sentence in sentences:
        #     scores = sid.polarity_scores(sentence)
        #     results["spam"].append([sentence, scores['compound'], scores['neg'], scores['neu'], scores['pos']])
    else:
        message_text = row[1]
        scores = sid.polarity_scores(message_text)
        results["ham"].append([message_text, scores['compound'], scores['neg'], scores['neu'], scores['pos']])
        # Uncomment this section to tokenize message contents into phrases, make sure to comment out the two lines above this comment
        # sentences = tokenizer.tokenize(message_text)
        # for sentence in sentences:
        #     scores = sid.polarity_scores(sentence)
        #     results["ham"].append([sentence, scores['compound'], scores['neg'], scores['neu'], scores['pos']])

# Write results to outfile
with open("spamResults.csv", mode = 'w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['message', 'compound', 'neg', 'neu', 'pos'])
    for row in results["spam"]:
        csv_writer.writerow(row)
with open("hamResults.csv", mode = 'w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['message', 'compound', 'neg', 'neu', 'pos'])
    for row in results["ham"]:
        csv_writer.writerow(row)

# sumVals["total"] = [0,0,0,0]
# countVals["total"] = 0
# sigfig = 3
# with open("results.txt", mode = 'w') as file:
#     for type in email_type:
#         sumVals["total"] = np.add(sumVals["total"], sumVals[type])
#         countVals["total"] += countVals[type]
#         file.write(f"{type}: compound: {round(sumVals[type][0]/countVals[type], sigfig)}, neg: {round(sumVals[type][1]/countVals[type], sigfig)}, neu: {round(sumVals[type][2]/countVals[type], sigfig)}, pos: {round(sumVals[type][3]/countVals[type], sigfig)}\n")
#     file.write("Overall Polarity Scores\n")
#     file.write(f"compound: {round(sumVals['total'][0]/countVals['total'], sigfig)}, neg: {round(sumVals['total'][1]/countVals['total'], sigfig)}, neu: {round(sumVals['total'][2]/countVals['total'], sigfig)}, pos: {round(sumVals['total'][3]/countVals['total'], sigfig)}")
