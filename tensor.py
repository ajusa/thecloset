import tensorflow as tf
import numpy as np
import pandas as pd
import json
import csv
import requests
from textblob.classifiers import NaiveBayesClassifier

from flask import Flask
app = Flask(__name__)

tops = []
bottoms = []
outfits = []
topColors = []
bottomColors = []
outfit = []
#awesomeOutfits = []
column = ["topColors", "bottomColors"]
@app.route("/giveGoodOutfit", methods = ['POST'])
def hello():
    if request.method == 'POST': #only take in one
       good_outfit = request.get_json()
       outfit = json.loads(good_outfit)
       #make more outfits
       #return main(outfit) ##TODO an array of jsons, size will be whatever arham wants
       myOutfits = main()

@app.route("/giveBadOutfit", methods = ['POST'])
def hi():
    if request.method == 'POST': #only take in one
       neg_outfit = request.get_json()
       outfit = json.loads(neg_outfit)
       return main(outfit)

@app.route("/getOutfits", methods=['GET'])
def yo():
    if request.method == 'GET':  # only take in one
        return createAllOutfits()

def createAllOutfits():
    articles = requests.get("http://35.3.111.174:3000/getCloset").text
    # parsedArticles = articles.text
    parsedArticles = json.loads(articles)

    for i in range(0, parsedArticles.__len__()):
        pos = parsedArticles[i]['pos']
        print(pos)

        if pos == 'top':
            tops.append(parsedArticles[i])
        elif parsedArticles[i]['pos'] == 'bottom':
            bottoms.append(parsedArticles[i])

    for i in range(0, tops.__len__()):
        for j in range(0, bottoms.__len__()):
            if tops[i]['style'] == bottoms[j]['style']:
                outfits.append([tops[i], bottoms[j]])

    #for i in range(0, outfits.__len__()):
     #   print(outfits[i])

    return outfits

def main():#sjs):
    awesomeOutfits = []
    #for j in range(0, tops.__len__()):
     #   rgb = tuple(int(tops[j]['color'][i:i+2], 16) for i in (0, 2 ,4))
      #  topColors.append(rgb)

    #for j in range(0, bottoms.__len__()):
     #   rgb = tuple(int(bottoms[j]['color'][i:i + 2], 16) for i in (0, 2, 4)) #thx stackoverflow
      #  bottomColors.append(rgb)
    outfit = '[{"type": "shorts", "color": "blue", "style": "fancy"}, {"type": "jacket", "color": "blue", "style": "fancy"}]' #weather, #"outfits.json"
    outfit = json.loads(outfit)
    f = csv.writer(open("colors.csv", "wb+"))
    f.writeRow(["color"])

    #colors = outfit[0]['color'] + " " + outfit[1]['color']
    #train = [
     #   {"text": colors, "label": "pos"}
    #]

    #with open("colors.csv", 'r') as fp:
    cl = NaiveBayesClassifier("colors.csv", format='csv')
    #prob = cl.prob_classify(outfit)

    possible = createAllOutfits()
    for i in range(0, possible.__len__()):
        pcolors = possible[i][0]['color'] + " " + possible[i][1]['color']
        print("HEELLO", pcolors)
        probColor = cl.prob_classify(pcolors)
        if(round(probColor.prob('pos'),2) >= .5):
            awesomeOutfits.append(possible[i])

    return awesomeOutfits

if __name__ == "__main__":
    main()