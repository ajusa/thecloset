import numpy as np
import json
import csv
import requests
from textblob.classifiers import NaiveBayesClassifier
import collections

from flask import Flask, jsonify, request

app = Flask(__name__)

tops = []
bottoms = []
outfits = []
topColors = []
bottomColors = []
outfit = []
first = 0
output_outfits = []
awesomeOutfits = []
clothesMatchesOptions = []

column = ["topColors", "bottomColors"]

def main(bad, good, receivedOutfit):
    global awesomeOutfits

    #potential = createAllOutfits();

    #   receivedColorSet = outfitColors(receivedOutfit)

    # if(good):
    #     train = [(receivedColorSet, 'pos')]
    # if(bad):
    #     train = [(receivedColorSet, 'neg')]
    # cl = NaiveBayesClassifier(train)
    #
    # affinityMap = {}
    # print "Done with training AI"
    # if (good):
    #     for i in range(0, len(potential)):
    #         potentialColorSet = outfitColors(potential[i])
    #         colorSetProbablities = cl.prob_classify(potentialColorSet)
    #         colorSetAffinity = colorSetProbablities.prob('pos')
    #         affinityMap.update({str(i):str(colorSetAffinity)})
    #         print "index:affinity - " + str(i) + ":" + str(colorSetAffinity)
    #     outfitOrder = sorted(affinityMap, key=affinityMap.__getitem__)
    #     for i in range(0, len(outfitOrder)):
    #         awesomeOutfits.append(potential[int(outfitOrder[i])])
    #
    # return awesomeOutfits
    awesomeOutfits = algorithm(bad, good, receivedOutfit)
    return awesomeOutfits

def outfitColors(outfit):
    first_color = hex_to_rgb(str(outfit[0]["color"]))
    second_color = hex_to_rgb(str(outfit[1]["color"]))
    return str(first_color) + " " + str(second_color)

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_dif(rgb_anchor, rgb_test):
    return [abs(rgb_anchor[0]-rgb_test[0]), abs(rgb_anchor[1]-rgb_test[1]), abs(rgb_anchor[2]-rgb_test[2])]

@app.route("/giveGoodOutfit", methods = ['POST'])
def goodOutfit():
    if request.method == 'POST':
       outfit = request.get_json()
       #outfit = json.loads(good_outfit
       output_outfits = (main(False, True, outfit))
    return jsonify(output_outfits)

@app.route("/giveBadOutfit", methods = ['POST'])
def badOutfit():
    if request.method == 'POST':
       outfit = request.get_json()
       #outfit = json.loads(neg_outfit)
       output_outfits = main(True, False, outfit)
    return jsonify(output_outfits)

@app.route("/getOutfits", methods=['GET'])
def sendAllOutfits():
    return jsonify(createAllOutfits())

def algorithm(bad, good, liked):
    clothing_matches = []
    testTops = []
    testBottoms = []
    outfits = createAllOutfits()
    global clothesMatchesOutfits

    #liked = '[{"type": "shorts", "color": "black", "style": "fancy"}, {"type": "shirt", "color": "blue", "style": "fancy"}]'
    top_rgb = hex_to_rgb(liked[0]["color"])
    lwr_rgb = hex_to_rgb(liked[1]["color"])

    for i in range(0,outfits.__len__()-1):
        testTop_rgb = hex_to_rgb(outfits[i]["color"])
        print(testTop_rgb)
        testLwr_rgb = hex_to_rgb(outfits[i+1]["color"])
        print(testLwr_rgb)

        difTop = rgb_dif(top_rgb, testTop_rgb)
        difLwr = rgb_dif(lwr_rgb, testLwr_rgb)
        print(difTop)
        print(difLwr)

        if difTop[0] <= 51 and difTop[1] <= 51 and difTop[2] <= 51: #in a good range
            if(good):
                clothing_matches.append(outfits[i][0]) #type is top
            if(bad):
                clothing_matches.insert(0, outfits[i][0]) #type is top

        if difLwr[0] <= 51 and difLwr[1] <= 51 and difLwr[2] <= 51:
            if (good):
                clothing_matches.append(outfits[i][1])  # type is top
            if (bad):
                clothing_matches.insert(0, outfits[i][1])  # type is top

    #now that we have some similar things in clothing_matches...
    for i in range(0, clothing_matches.__len__()):
        pos = clothing_matches[i]['pos']

        if pos == 'top':
            testTops.append(clothing_matches[i])

        elif outfit[i]['pos'] == 'bottom':
            testBottoms.append(clothing_matches[i])

    for i in range(0, testTops.__len__()):
        for j in range(0, testBottoms.__len__()):
            if any(k in testTops[i]['style'] for k in testBottoms[j]['style']):
                clothesMatchesOutfits.append([testTops[i], testBottoms[j]])  # combine tops and bottoms to form all possible outputs

    return clothesMatchesOutfits


def createAllOutfits():
    outfits = []
    tops = []
    bottoms = []
    articles = requests.get("http://35.3.111.174:3000/getCloset").text

    #articles = '[{"color":"#ff0000","pos":"bottom","style":["fitness"],"type":"shorts","uid":"-KuiQ2tqmywx7iTFQvxK"},{"color":"#808080","pos":"top","style":["fitness","casual"],"type":"jacket","uid":"-KuiQXAdz38Y0VmX69d7"}, {"color":"#000080","pos":"bottom","style":["fitness","casual"],"type":"jeans","uid":"-KuiQYoNJy7M28O7dm3s"},{"color":"#000080","pos":"top","style":["fitness","casual"],"type":"t-shirt","uid":"-KuiQb3w3P6o8IGen1QP"},{"color":"#000080","pos":"bottom","style":["casual","fitness"],"type":"shorts","uid":"-KujQqjUeOafKnEuuGVc"},{"color":"#ff0000","pos":"top","style":["casual","formal"],"type":"jacket","uid":"-KujQwRArGAG1hkC04lF"},{"color":"#ff0000","pos":"top","style":["casual","fitness"],"type":"t-shirt","uid":"-KujXsZahvMm3dYhNl_D"},{"color":"#ff0000","pos":"bottom","style":["casual","fitness"],"type":"jeans","uid":"-KujYCmwZ9WxYNYVZq4x"},{"color":"#808080","pos":"top","style":["casual","fitness"],"type":"t-shirt","uid":"-KujYKNXTW9uniEmcwX3"}]'

    outfit = json.loads(articles) #parsedArticles
    #print(articles)

    for i in range(0, outfit.__len__()):
        pos = outfit[i]['pos']

        if pos == 'top':
            tops.append(outfit[i])

        elif outfit[i]['pos'] == 'bottom':
            bottoms.append(outfit[i])

    for i in range(0, tops.__len__()):
        for j in range(0, bottoms.__len__()):
            if any(k in tops[i]['style'] for k in bottoms[j]['style']):
                outfits.append([tops[i], bottoms[j]]) #combine tops and bottoms to form all possible outputs
    return outfits