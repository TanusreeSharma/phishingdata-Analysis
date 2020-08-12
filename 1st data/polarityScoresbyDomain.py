import sys
import csv
import numpy as np
import nltk.data
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import sentiment
from nltk import word_tokenize

# Adapted from https://programminghistorian.org/en/lessons/sentiment-analysis

if(len(sys.argv) != 3):
    print("Usage: python3 polarityScoresbyDomain.py <pathtodatafile> <pathtowritefile>")
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


email_domains = [".com", ".gov", ".net", ".edu", ".org", "none"]
# Analyze sentiment on email contents usign NLTK and tokenizer
sid = SentimentIntensityAnalyzer()
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# Initalize results dictionary
results = {}
for domain in email_domains:
    results[domain] = []
# Go through each row in the dataset
for row in rows:
    # If there is no sender email, append results to "none" domain
    if( (row[10] == "Y") or (row[10] == "na") ):
        message_text = row[1]
        scores = sid.polarity_scores(message_text)
        results["none"].append([message_text, scores['compound'], scores['neg'], scores['neu'], scores['pos']])
    else:
        # If there is a sender email, append results to appropriate domain
        for domain in email_domains:
            if(row[10].find(domain) != -1):
                message_text = row[1]
                scores = sid.polarity_scores(message_text)
                results[domain].append([message_text, scores['compound'], scores['neg'], scores['neu'], scores['pos']])
                break;

sumVals = {}
countVals = {}
# Write results to outfile
with open(outfile, mode = 'w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['message', 'compound', 'neg', 'neu', 'pos'])
    for domain in email_domains:
        sum = [0,0,0,0]
        count = 0
        for row in results[domain]:
            sum[0] += row[1]
            sum[1] += row[2]
            sum[2] += row[3]
            sum[3] += row[4]
            count += 1
            csv_writer.writerow(row)
        # Print out the average compound value for each token
        sumVals[domain] = sum
        countVals[domain] = count
sumVals["total"] = [0,0,0,0]
countVals["total"] = 0
sigfig = 3
for domain in email_domains:
    sumVals["total"] = np.add(sumVals["total"], sumVals[domain])
    countVals["total"] += countVals[domain]
    print(f"{domain}: compound: {round(sumVals[domain][0]/countVals[domain], sigfig)}, neg: {round(sumVals[domain][1]/countVals[domain], sigfig)}, neu: {round(sumVals[domain][2]/countVals[domain], sigfig)}, pos: {round(sumVals[domain][3]/countVals[domain], sigfig)}")
print("Overall Polarity Scores")
print(f"compound: {round(sumVals['total'][0]/countVals['total'], sigfig)}, neg: {round(sumVals['total'][1]/countVals['total'], sigfig)}, neu: {round(sumVals['total'][2]/countVals['total'], sigfig)}, pos: {round(sumVals['total'][3]/countVals['total'], sigfig)}")
