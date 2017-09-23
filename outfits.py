import numpy as np
import json
import requests

articles = requests.get("http://35.3.111.174:3000/getCloset").text
#parsedArticles = articles.text
parsedArticles = json.loads(articles)
#print(parsedArticles)

def main():
    #get all possible outfits from the clothing articles
    #send them over
    #receive the liked outfits
    #analyze these using ai and patterns to return better outfits

    #ai should handle colors, some style matching

    #color, pos, style
    tops = []
    bottoms = []
    outfits = []

    for i in range(0, parsedArticles.__len__()):
        pos = parsedArticles[i]['pos']
        print(pos)

        if pos == 'top':
            tops.append(parsedArticles[i])
        elif parsedArticles[i]['pos'] == 'bottom':
            bottoms.append(parsedArticles[i])

    for i in range(0, tops.__len__()):
        for j  in range(0, bottoms.__len__()):
            if tops[i]['style'] == bottoms[j]['style']:
                outfits.append([tops[i], bottoms[j]])

    for i in range(0, outfits.__len__()):
        print(outfits[i])

    return outfits


if __name__ == '__main__':
    main()

