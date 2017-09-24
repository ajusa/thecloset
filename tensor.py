import numpy as np
import json
import csv
import requests
from textblob.classifiers import NaiveBayesClassifier

from flask import Flask, jsonify, request

app = Flask(__name__)

tops = []
bottoms = []
outfits = []
topColors = []
bottomColors = []
outfit = []
first = 0

column = ["topColors", "bottomColors"]

def main(good, bad, receivedOutfit):
    awesomeOutfits = []
    #take out for testing with servers!
    #sampleOutfit = '[{"color":"#ff0000","pos":"bottom","style":["fitness"],"type":"shorts","uid":"-KuiQ2tqmywx7iTFQvxK"},{"color":"#808080","pos":"top","style":["fitness","casual"],"type":"jacket","uid":"-KuiQXAdz38Y0VmX69d7"}]' #,{"color":"#000080","pos":"bottom","style":["fitness","casual"],"type":"jeans","uid":"-KuiQYoNJy7M28O7dm3s"},{"color":"#000080","pos":"top","style":["fitness","casual"],"type":"t-shirt","uid":"-KuiQb3w3P6o8IGen1QP"},{"color":"#000080","pos":"bottom","style":["casual","fitness"],"type":"shorts","uid":"-KujQqjUeOafKnEuuGVc"},{"color":"#ff0000","pos":"top","style":["casual","formal"],"type":"jacket","uid":"-KujQwRArGAG1hkC04lF"},{"color":"#ff0000","pos":"top","style":["casual","fitness"],"type":"t-shirt","uid":"-KujXsZahvMm3dYhNl_D"},{"color":"#000000","pos":"top","style":["casual","fitness"],"type":"t-shirt","uid":"-KujYCmwZ9WxYNYVZq4x"},{"color":"#800080","pos":"top","style":["casual","fitness"],"type":"t-shirt","uid":"-KujYKNXTW9uniEmcwX3"}]'
    #parsedOutfits2 = parsedOutfits
    #parsedOutfits = json.loads(outfit)

    f = csv.writer(open("colors.csv", "wb+"))
    f.writerow(receivedOutfit[0]['color'])
    f.writerow(receivedOutfit[1]['color'])
    outColor = receivedOutfit[0]['color'] + " " + receivedOutfit[1]['color'] #must take care of inversion as well

    if(good):
        train = [(receivedOutfit[0]['color'] + " " + receivedOutfit[1]['color'], 'pos')]
    if(bad):
        train = [(receivedOutfit[0]['color'] + " " + receivedOutfit[1]['color'], 'neg')]
    cl = NaiveBayesClassifier(train)
    #with open("colors.csv", 'r') as fp:
     #   cl = NaiveBayesClassifier(fp, format='csv')

    awesomeOutfits.append(receivedOutfit)
    possible = createAllOutfits()
    #TODO may still need to convert to rgb; good checks if user liked it

    for i in range(0, possible.__len__()):
        pcolors = possible[i][0]['color'] + " " + possible[i][1]['color']
        print(pcolors)
        probColor = cl.prob_classify(pcolors)
        print("\n" + str(round(probColor.prob('pos'), 2)))
        if(round(probColor.prob('pos'),2) >= .5):
            print("WE'VE GOT A MATCH")
            awesomeOutfits.append(possible[i])

    if awesomeOutfits.__len__() == 0:
        awesomeOutfits = possible
    return  awesomeOutfits

@app.route("/giveGoodOutfit", methods = ['POST'])
def goodOutfit():
    if request.method == 'POST':
       outfit = request.get_json()
       #outfit = json.loads(good_outfit)

       output_outfits = (main(False, True, outfit))
       print len(output_outfits)
    return jsonify(output_outfits)

@app.route("/giveBadOutfit", methods = ['POST'])
def badOutfit():
    if request.method == 'POST':
       outfit = request.get_json()
       #outfit = json.loads(neg_outfit)
       output_outfits = main(True, False, outfit)
       print len(output_outfits)
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
