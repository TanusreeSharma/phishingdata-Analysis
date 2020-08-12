import sys
import csv
import string
import numpy as np

if(len(sys.argv) != 3):
    print("Usage: python3 tallies.py <pathtodatafile> <pathtowritefile>")
    sys.exit()

# Open file to read in data
filename = sys.argv[1]
outfile = sys.argv[2]
# Initialize fields and rows arrays
fields = []
# Read data in from csv file
csv_file = open(filename, encoding="ISO-8859-1")
csv_reader = csv.reader(csv_file, delimiter=',')
fields = next(csv_reader)

csv.field_size_limit(sys.maxsize)

fields = ["compound", "neg", "neu", "pos"]
counts = {}
counts["compound"] = [0,0,0,0,0,0,0,0,0,0] # -1.0--0.8, -0.8--0.6, -0.6--0.4, -0.4--0.2, -0.2-0.0, 0.0-0.2, 0.2-0.4, 0.4-0.6, 0.6-0.8, 0.8-1.0
counts["neg"] = [0,0,0,0,0,0,0,0,0,0] # -1.0--0.8, -0.8--0.6, -0.6--0.4, -0.4--0.2, -0.2-0.0, 0.0-0.2, 0.2-0.4, 0.4-0.6, 0.6-0.8, 0.8-1.0
counts["neu"] = [0,0,0,0,0,0,0,0,0,0] # -1.0--0.8, -0.8--0.6, -0.6--0.4, -0.4--0.2, -0.2-0.0, 0.0-0.2, 0.2-0.4, 0.4-0.6, 0.6-0.8, 0.8-1.0
counts["pos"] = [0,0,0,0,0,0,0,0,0,0] # -1.0--0.8, -0.8--0.6, -0.6--0.4, -0.4--0.2, -0.2-0.0, 0.0-0.2, 0.2-0.4, 0.4-0.6, 0.6-0.8, 0.8-1.0
# [message_text, scores['compound'], scores['neg'], scores['neu'], scores['pos']]

for row in csv_reader:
    index = 1
    for field in fields:
        if(-1.0 <= float(row[index]) <= -0.8):
            counts[field][0] += 1
        elif(-0.8 < float(row[index]) <= -0.6):
            counts[field][1] += 1
        elif(-0.6 < float(row[index]) <= -0.4):
            counts[field][2] += 1
        elif(-0.4 < float(row[index]) <= -0.2):
            counts[field][3] += 1
        elif(-0.2 < float(row[index]) < 0.0):
            counts[field][4] += 1
        elif(0.0 <= float(row[index]) <= 0.2):
            if(field == "compound" and float(row[index]) == 0.0):
                counts[field][4] += 1
            else:
                counts[field][5] += 1
        elif(0.2 < float(row[index]) <= 0.4):
            counts[field][6] += 1
        elif(0.4 < float(row[index]) <= 0.6):
            counts[field][7] += 1
        elif(0.6 < float(row[index]) <= 0.8):
            counts[field][8] += 1
        elif(0.8 < float(row[index]) <= 1.0):
            counts[field][9] += 1
        index += 1

with open(outfile, mode = 'w') as file:
    file.write("Compound Tallies\n")
    file.write(str(counts["compound"]))
    file.write("\nNegative Tallies\n")
    file.write(str(counts["neg"]))
    file.write("\nNeutral Tallies\n")
    file.write(str(counts["neu"]))
    file.write("\nPositive Tallies\n")
    file.write(str(counts["pos"]))
