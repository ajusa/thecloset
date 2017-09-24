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

column = ["topColors", "bottomColors"]

def main(bad, good, receivedOutfit):
    global awesomeOutfits

    potential = createAllOutfits();

    receivedColorSet = outfitColors(receivedOutfit)

    if(good):
        train = [(receivedColorSet, 'pos')]
    if(bad):
        train = [(receivedColorSet, 'neg')]
    cl = NaiveBayesClassifier(train)

    affinityMap = {}
    print "Done with training AI"
    if (good):
        for i in range(0, len(potential)):
            potentialColorSet = outfitColors(potential[i])
            colorSetProbablities = cl.prob_classify(potentialColorSet)
            colorSetAffinity = colorSetProbablities.prob('pos')
            affinityMap.update({str(i):str(colorSetAffinity)})
            print "index:affinity - " + str(i) + ":" + str(colorSetAffinity)
        outfitOrder = sorted(affinityMap, key=affinityMap.__getitem__)
        for i in range(0, len(outfitOrder)):
            awesomeOutfits.append(potential[int(outfitOrder[i])])

    return awesomeOutfits

# def main(good, bad, receivedOutfit):
#     global awesomeOutfits
#
#     #likedOutfits = []
#     #take out for testing with servers!
#     #sampleOutfit = '[{"color":"#ff0000","pos":"bottom","style":["fitness"],"type":"shorts","uid":"-KuiQ2tqmywx7iTFQvxK"},{"color":"#808080","pos":"top","style":["fitness","casual"],"type":"jacket","uid":"-KuiQXAdz38Y0VmX69d7"}]' #,{"color":"#000080","pos":"bottom","style":["fitness","casual"],"type":"jeans","uid":"-KuiQYoNJy7M28O7dm3s"},{"color":"#000080","pos":"top","style":["fitness","casual"],"type":"t-shirt","uid":"-KuiQb3w3P6o8IGen1QP"},{"color":"#000080","pos":"bottom","style":["casual","fitness"],"type":"shorts","uid":"-KujQqjUeOafKnEuuGVc"},{"color":"#ff0000","pos":"top","style":["casual","formal"],"type":"jacket","uid":"-KujQwRArGAG1hkC04lF"},{"color":"#ff0000","pos":"top","style":["casual","fitness"],"type":"t-shirt","uid":"-KujXsZahvMm3dYhNl_D"},{"color":"#000000","pos":"top","style":["casual","fitness"],"type":"t-shirt","uid":"-KujYCmwZ9WxYNYVZq4x"},{"color":"#800080","pos":"top","style":["casual","fitness"],"type":"t-shirt","uid":"-KujYKNXTW9uniEmcwX3"}]'
#     #parsedOutfits2 = parsedOutfits
#     #parsedOutfits = json.loads(outfit)
#
#     f = csv.writer(open("colors.csv", "wb+"))
#     f.writerow(receivedOutfit[0]['color'])
#     f.writerow(receivedOutfit[1]['color'])
#     outColor = receivedOutfit[0]['color'] + " " + receivedOutfit[1]['color'] #must take care of inversion as well
#
#     if(good):
#         train = [(receivedOutfit[0]['color'] + " " + receivedOutfit[1]['color'], 'pos')]
#     if(bad):
#         train = [(receivedOutfit[0]['color'] + " " + receivedOutfit[1]['color'], 'neg')]
#     cl = NaiveBayesClassifier(train)
#     #with open("colors.csv", 'r') as fp:
#      #   cl = NaiveBayesClassifier(fp, format='csv')
#
#     awesomeOutfits.append(receivedOutfit)
#     #likedOutfits.append(receivedOutfit)
#     possible = createAllOutfits()
#     probColor = []
#     probRatings = []
#     probDict = {}
#     #TODO may still need to convert to rgb; good checks if user liked it
#     if(awesomeOutfits.__len__() >= 2):
#         for i in range(0, possible.__len__()):
#             pcolors = possible[i][0]['color'] + " " + possible[i][1]['color']
#             #print(pcolors)
#             probColor = cl.prob_classify(pcolors)
#             #print("\n" + str(round(probColor.prob('pos'), 2)))
#             #probDict.append(probColor.prob('pos'))
#             outfitAffinity = probColor.prob('pos')
#             if(outfitAffinity > 0.5):
#                 print "WE HAVE A MATCH"
#             # awesomeOutfits.append(possible[i])
#             # probRatings.append(probColor.prob('pos'))
#             probDict.update({str(possible[i]): str(outfitAffinity)})
#         awesomeOutfits = sorted(probDict, key=probDict.__getitem__)
#         print sorted(probDict.values())
#
#     #for i in range(0, awesomeOutfits):
#         #awesomeOutfits
#     #for key in sorted(probDict.keys()):
#     #    newDict.update({str(key)}: str(probDict.get()))
#     #awesomeOutfits = collections.OrderedDict(probDict).keys()
#     #sortDict = sorted(probDict.values())
#     ##print(sorted(probDict, key=probDict.get))
#     ##awesomeOutfits = sortDict #orted_probDict.key()
#     if awesomeOutfits.__len__() <= 1:
#         awesomeOutfits = possible
#
#     return awesomeOutfits

def outfitColors(outfit):
    first_color = hex_to_rgb(str(outfit[0]["color"]))
    second_color = hex_to_rgb(str(outfit[1]["color"]))
    return str(first_color) + " " + str(second_color)

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

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
