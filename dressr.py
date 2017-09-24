import numpy as np
import json
import csv
import requests

from flask import Flask, jsonify, request

app = Flask(__name__)

tops = []
bottoms = []
outfits = []
topColors = []
bottomColors = []
outfit = []
first = 1
output_outfits = []
awesomeOutfits = []
clothesMatchesOutfits = []
badMatches = []
liked = []
#badColors = []
clothing_matches = []

badOutfits = []

articles = []

column = ["topColors", "bottomColors"]

def main(bad, good, receivedOutfit):
    global awesomeOutfits
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

@app.route("/giveCloset", methods=['PUT'])
def receiveCloset():
    global articles
    articles = request.get_json()
    print len(articles)
    return "success"

@app.route("/getOutfits", methods=['GET'])
def sendAllOutfits():
    return jsonify(createAllOutfits())

def algorithm(bad, good, liked):
    global clothing_matches
    testTops = []
    testBottoms = []

    badTops = []
    badBottoms = []
    outfits = createAllOutfits()

    global badMatches
    global badOutfits
    global clothesMatchesOutfits
    clothesMatchesOutfits = []

    #liked = '[{"type": "shorts", "color": "black", "style": "fancy"}, {"type": "shirt", "color": "blue", "style": "fancy"}]'
    top_rgb = hex_to_rgb(liked[0]["color"])
    lwr_rgb = hex_to_rgb(liked[1]["color"])

    for i in range(0, outfits.__len__()):
        testTop_rgb = hex_to_rgb(outfits[i][0]["color"])
        # print(testTop_rgb)
        testLwr_rgb = hex_to_rgb(outfits[i][1]["color"])
        # print(testLwr_rgb)

        difTop = rgb_dif(top_rgb, testTop_rgb)
        difLwr = rgb_dif(lwr_rgb, testLwr_rgb)
        # print(difTop)
        # print(difLwr)

        if difTop[0] <= 51 and difTop[1] <= 51 and difTop[2] <= 51:  # in a good range
            if (good):
                clothing_matches.append(outfits[i][0])  # type is top
            if (bad): #we disliked it
                # clothing_matches.insert(0, outfits[i][0]) #type is top
                badMatches.append(outfits[i][0])

        if difLwr[0] <= 51 and difLwr[1] <= 51 and difLwr[2] <= 51:
            if (good):
                clothing_matches.append(outfits[i][1])  # type is lwr
            if (bad):
                # clothing_matches.insert(0, outfits[i][1])  # type is lwr
                badMatches.append(outfits[i][1]) #was bad colors

        # style checker
        if outfits[i][0]["style"] == liked[0]["style"] or outfits[i][0]["style"] == liked[1]["style"]:
            if (not clothing_matches.__contains__(outfits[i][0])):
                if (good):
                    clothing_matches.append(outfits[i][0])
                    if (bad):
                        badMatches.append(outfits[i][0])

        if outfits[i][1]["style"] == liked[0]["style"] or outfits[i][1]["style"] == liked[1]["style"]:
            if (not clothing_matches.__contains__(outfits[i][1])):
                if (good):
                    clothing_matches.append(outfits[i][1])
                if(bad):
                    badMatches.append(outfits[i][1])

    #now that we have some similar things in clothing_matches...START MAKING THE OUTFITS
    #make bad outfits!!!!!!!!!!!!!!!
    for i in range(0, badMatches.__len__()):
        pos = badMatches[i]['pos']

        if pos == 'top':
            badTops.append(badMatches[i])

        elif badMatches[i]['pos'] == 'bottom':
            badBottoms.append(badMatches[i])

    #calculate the bad outfits and exclude them from the thing
    for i in range(0, badTops.__len__()):
        for j in range(0, badBottoms.__len__()):
            if any(k in badTops[i]['style'] for k in badBottoms[j]['style']):
                badOutfits.append([badTops[i], badBottoms[j]])

    #calculate good outfit - tops and bottoms
    for i in range(0, clothing_matches.__len__()):
        pos = clothing_matches[i]['pos']

        if pos == 'top':
            testTops.append(clothing_matches[i])

        elif clothing_matches[i]['pos'] == 'bottom':
            testBottoms.append(clothing_matches[i])

    for i in range(0, testTops.__len__()):
        for j in range(0, testBottoms.__len__()):
            if any(k in testTops[i]['style'] for k in testBottoms[j]['style']):
                currentOutfit = [testTops[i], testBottoms[j]]

                if(not currentOutfit in clothesMatchesOutfits and not currentOutfit in badOutfits): #Matches):
                    clothesMatchesOutfits.append([testTops[i], testBottoms[j]])  # combine tops and bottoms to form all possible outputs

    if(len(clothesMatchesOutfits) == 0 and badOutfits.__len__()): #Matches.__len__() > 0):
        print("doesnt like anything, only dislikes :(")
        for i in range(0, badOutfits.__len__()): #was matches
            theseOutfits = [x for x in outfits if x not in badOutfits]
        return theseOutfits
    else:
        return clothesMatchesOutfits


def createAllOutfits():
    outfits = []
    tops = []
    bottoms = []
    global articles

    print str(len(articles))
    #articles = '[{"color":"#ff0000","pos":"bottom","style":["fitness"],"type":"shorts","uid":"-KuiQ2tqmywx7iTFQvxK"},{"color":"#808080","pos":"top","style":["fitness","casual"],"type":"jacket","uid":"-KuiQXAdz38Y0VmX69d7"}, {"color":"#000080","pos":"bottom","style":["fitness","casual"],"type":"jeans","uid":"-KuiQYoNJy7M28O7dm3s"},{"color":"#000080","pos":"top","style":["fitness","casual"],"type":"t-shirt","uid":"-KuiQb3w3P6o8IGen1QP"},{"color":"#000080","pos":"bottom","style":["casual","fitness"],"type":"shorts","uid":"-KujQqjUeOafKnEuuGVc"},{"color":"#ff0000","pos":"top","style":["casual","formal"],"type":"jacket","uid":"-KujQwRArGAG1hkC04lF"},{"color":"#ff0000","pos":"top","style":["casual","fitness"],"type":"t-shirt","uid":"-KujXsZahvMm3dYhNl_D"},{"color":"#ff0000","pos":"bottom","style":["casual","fitness"],"type":"jeans","uid":"-KujYCmwZ9WxYNYVZq4x"},{"color":"#808080","pos":"top","style":["casual","fitness"],"type":"t-shirt","uid":"-KujYKNXTW9uniEmcwX3"}]'
    if articles.__len__() > 0: #to make sure request successful
        #outfit = json.loads(articles) #parsedArticles
        #print(articles)
        outfit = articles
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
