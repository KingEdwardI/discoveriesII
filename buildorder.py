#!/local/bin/python
import json
import sys
from unidecode import unidecode

argIn = sys.argv[1]

def main():
    orderJSON, arabicImageLinks = readJSON(argIn)
    #  getOrderNums(orderJSON)
    #  print makeOneSided(orderJSON)
    #  print makeTwoSided(orderJSON)
    #  print makeBand(orderJSON)
    makeHTML(orderJSON)


def getOrderNums(json):
    #TODO
    # need to convert this to dictionaries, and anything following it, but need design beforehand
    itemDescDict = {} # {itemSort : itemDesc}
    for item in json:
        identifier = item['itemSort'] + item['type'] + item['attr1']
        if identifier not in itemDescDict:
            itemDescDict[identifier] = "<div class='orderDescData'><span class='orderDescription'>"
            itemDescDict[identifier] += item['itemSort'] + " | " + item['metal'] + " " + item['type'] + " " + item['attr1'] + " " + item['attr2'] + " | </span><span class='arabic'>" 
            if item['metal']:
                itemDescDict[identifier] += "<img src='img/" + item['metal'].lower() + ".jpg'> | " 
            if item['type']:
                itemDescDict[identifier] += "<img src='img/" + item['type'].lower() + ".jpg'> | "
            if item['attr1']:
                itemDescDict[identifier] += "<img src='img/" + item['attr1'].lower() + ".jpg'> | " 
            if item['attr2']:
                itemDescDict[identifier] += "<img src='img/" + item['attr2'].lower() + ".jpg'> | "
            itemDescDict[identifier] += "</span><span class='batchNum'>" + item['batchNum'] + "</span></div>"
    return itemDescDict

def makeOneSided(json):

    itemOneSided = {}

    for item in json:
        if item['type'] != 'ring' and item['type'] != 'bracelet' and item['attr1'] != '2sided':
            identifier = item['itemSort'] + item['type']
            itemOneSided[unidecode(identifier)] = []

    for item in json:
        if item['type'] != 'ring' and item['type'] != 'bracelet' and item['attr1'] != '2sided':
            buildItem = "<div class='item'><table class='itemSymbols'><tbody>"
            for letter in item['side1symb']:
                buildItem += "<tr><td class='symbol " + item['side1lang'].lower() + "'>" + letter + "</td></tr>"
            buildItem += "</tbody></table><div class='itemDescription'>"
            buildItem += "<div class='size arabic'><img src='img/" + item['size'] + ".jpg'></div>"
            buildItem += item['itemNum'] + "<br>" + "SIG -" + item['label'] + "<br>"
            buildItem += str(item['orderNum']) + "<br></div></div>"
            identifier = item['itemSort'] + item['type']
            itemOneSided[unidecode(identifier)].append(buildItem)

    return itemOneSided

def makeTwoSided(json):

    itemTwoSided = {}

    for item in json:
        if item['type'] != 'ring' and item['type'] != 'bracelet' and item['attr1'] == '2sided':
            itemTwoSided[item['itemSort']] = []

    for item in json:
        if item['type'] != 'ring' and item['type'] != 'bracelet' and item['attr1'] == '2sided':
            buildItem = "<div class='item'><table class='itemSymbols'><tbody>"
            for side1, side2 in zip(item['side1symb'], item['side2symb']):
                buildItem += "<tr><td class='side1 symbol " + item['side1lang'] + "'>" + side1 + "</td>"
                buildItem += "<td class='side2 symbol " + item['side2lang'] + "'>" + side2 + "</td></tr>"
            buildItem += "</tbody></table><div class='itemDescription'>"
            buildItem += "<div class='size arabic'><img src='img/" + item['size'] + ".jpg'></div>"
            buildItem += item['itemNum'] + "<br>" + "SIG -" + item['label'] + "<br>"
            buildItem += str(item['orderNum']) + "<br></div></div>"
            itemTwoSided[item['itemSort']].append(buildItem)

    return itemTwoSided

def makeBand(json):

    itemBand = {}
    
    for item in json:
        if item['type'] == 'ring' or item['type'] == 'bracelet':
            itemBand[item['itemSort']] = []

    for item in json:
        if item['type'] == 'ring' or item['type'] == 'bracelet':
            buildItem = "<div class='item'><table class='itemSymbols'><tbody><tr>"
            for letter in item['side1symb']:
                buildItem += "<td class='symbol " + item['side1lang'] + "'>" + letter + "</td>"
            buildItem += "</tbody></table><div class='itemDescription'>"
            buildItem += "<div class='size arabic'><img src='img/" + item['size'] + ".jpg'></div>"
            buildItem += item['itemNum'] + " SIG -" + item['label'] + " "
            buildItem += str(item['orderNum']) + "</div></div>"
            itemBand[item['itemSort']].append(buildItem)
    return itemBand

def makeHTML(json):
    """build out the whole html page"""
    # TODO: reorder the organization of 'orders'

    orders = getOrderNums(json)
    oneSideds = makeOneSided(json)
    twoSideds = makeTwoSided(json)
    bands = makeBand(json)

    #  for order in orders:
        #  print orders[order]

    boilerplate = "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title></title><link rel='stylesheet' type='text/css' href='./test.css'></head><body>"
    endplate = "</body></html>"

    html = ""
    html += boilerplate
    for order in orders: 
        if 'ring' not in order and 'bracelet' not in order and '2sided' not in order:
            html += "<div class='order'>"
            html += orders[order]
            o = 0 # for counting orders
            for oneSided in oneSideds:
                for item in oneSideds[oneSided]:
                    html += item 
            html += "</div>"
        if 'ring' not in order and 'bracelet' not in order and '2sided' in order:
            html += "<div class='order'>"
            html += orders[order]
            for twoSided in twoSideds:
                for item in twoSideds[twoSided]:
                    html += item
            html += "</div>"
        if 'ring' in order or 'bracelet' in order:
            html += "<div class='order'>"
            for band in bands:
                if band == order:
                    for item in bands[band]:
                        html += item
            html += "</div>"
    html += endplate

    print html

def readJSON(filename):
    """
    read in a json file and store its value

    :returns: json file
    :rtype: string
    """
    f = open(filename, "r")
    orderFileJSON = f.read()
    order = json.loads(orderFileJSON)
    f.close()
    k = open('json/arabic.json', 'r')
    arabicFileJSON = k.read()
    arabic = json.loads(arabicFileJSON)
    k.close()
    return order, arabic

if __name__ == "__main__":
    main()
