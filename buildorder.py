#!/local/bin/python
import json
import sys
from unidecode import unidecode

argIn = sys.argv[1]

bandTypes = ['ring','bracelet','ring band', 'band']

def main():
    orderJSON, arabicImageLinks = readJSON(argIn)
    #  getOrderNums(orderJSON)
    #  print makeOneSided(orderJSON)
    #  print makeTwoSided(orderJSON)
    #  print makeBand(orderJSON)
    makeHTML(orderJSON)


def getOrderNums(json):
    itemDescDict = {} # {itemSort : itemDesc}
    for item in json:
        identifier = item['itemSort'].lower() + item['type'].lower() + item['attr1'].lower().replace(' ', '')
        if identifier not in itemDescDict:
            itemDescDict[identifier] = "<div class='orderDescData'><span class='orderDescription'>"
            itemDescDict[identifier] += item['itemSort'] + " | " + item['metal'] + " " + item['type'] + " " + item['attr1'] + " " + item['attr2'] + " | </span><span class='arabic'>" 
            if item['metal']:
                itemDescDict[identifier] += "<img src='img/" + item['metal'].lower() + ".jpg'>" 
            if item['type']:
                itemDescDict[identifier] += "<img src='img/" + item['type'].lower() + ".jpg'>"
            if item['attr1']:
                itemDescDict[identifier] += "<img src='img/" + item['attr1'].lower() + ".jpg'>" 
            if item['attr2']:
                itemDescDict[identifier] += "<img src='img/" + item['attr2'].lower() + ".jpg'>"
            itemDescDict[identifier] += "</span><span class='batchNum'>" + item['batchNum'].lower() + "</span></div>"

    return itemDescDict

def makeOneSided(json):

    itemOneSided = {}

    for item in json:
        #  if item['type'].lower() != 'ring' and item['type'].lower() != 'bracelet' and item['attr1'] != '2sided':
        if not any(item['type'].lower() in s for s in bandTypes) and item['attr1'].lower().replace(' ','') != '2sided':
            identifier = item['itemSort'] + item['type'].lower()
            itemOneSided[unidecode(identifier)] = []

    for item in json:
        #  if item['type'].lower() != 'ring' and item['type'].lower() != 'bracelet' and item['attr1'] != '2sided':
        if not any(item['type'].lower() in s for s in bandTypes) and item['attr1'].lower().replace(' ', '') != '2sided':
            buildItem = "<div class='item oneSided'><table class='itemSymbols'><tbody>"
            for letter in item['side1symb']:
                buildItem += "<tr><td class='symbol " + item['side1lang'].lower() + "'>" + letter + "</td></tr>"
            buildItem += "</tbody></table><div class='itemDescription'>"
            buildItem += "<div class='size arabic'><img src='img/" + str(item['size']) + ".jpg'></div>"
            buildItem += "<div class='description'> " + item['itemNum'] + "<br>" + "SIG -" + item['label'] + "<br>"
            buildItem += str(item['orderNum']) + "<br></div></div></div>"
            identifier = item['itemSort'] + item['type'].lower()
            itemOneSided[unidecode(identifier)].append(buildItem)

    return itemOneSided

def makeTwoSided(json):

    itemTwoSided = {}

    for item in json:
        #  if item['type'] != 'ring' and item['type'] != 'bracelet' and item['attr1'] == '2sided':
        if not any(item['type'].lower() in s for s in bandTypes) and item['attr1'].lower().replace(' ', '') == '2sided':
            itemTwoSided[item['itemSort']] = []

    for item in json:
        #  if item['type'] != 'ring' and item['type'] != 'bracelet' and item['attr1'] == '2sided':
        if not any(item['type'].lower() in s for s in bandTypes) and item['attr1'].lower().replace(' ', '') == '2sided':
            buildItem = "<div class='item twoSided'><table class='itemSymbols'><tbody>"
            for side1, side2 in zip(item['side1symb'], item['side2symb']):
                buildItem += "<tr><td class='side1 symbol " + item['side1lang'].lower() + "'>" + side1 + "</td>"
                buildItem += "<td class='side2 symbol " + item['side2lang'].lower() + "'>" + side2 + "</td></tr>"
            buildItem += "</tbody></table><div class='itemDescription'>"
            buildItem += "<div class='size arabic'><img src='img/" + str(item['size']) + ".jpg'></div>"
            buildItem += "<div class='description'>" + item['itemNum'] + "<br>" + "SIG -" + item['label'] + "<br>"
            buildItem += str(item['orderNum']) + "<br></div></div></div>"
            itemTwoSided[item['itemSort']].append(buildItem)

    return itemTwoSided

def makeBand(json):

    itemBand = {}
    
    for item in json:
        #  if item['type'] == 'ring' or item['type'] == 'bracelet':
        if any(item['type'].lower() in s for s in bandTypes):
            itemBand[item['itemSort']] = []

    for item in json:
        #  if item['type'] == 'ring' or item['type'] == 'bracelet':
        if any(item['type'].lower() in s for s in bandTypes):
            itemBand[item['itemSort']] = []
            buildItem = "<div class='item band'><div><table class='itemSymbols'><tbody><tr>"
            for letter in item['side1symb']:
                buildItem += "<td class='symbol " + item['side1lang'].lower() + "'>" + letter + "</td>"
            buildItem += "<td class='blank'></td>"
            buildItem += "<td class='size arabic'><img src='img/" + str(item['size']).lower() + ".jpg'></td>"
            buildItem += "</tbody></table></div><div class='itemDescription'>"
            buildItem += "<div class='description'>" + item['itemNum'] + " SIG -" + item['label'] + " "
            buildItem += str(item['orderNum']) + "</div></div></div>"
            itemBand[item['itemSort']].append(buildItem)
    return itemBand

def makeHTML(json):
    """build out the whole html page"""
    # TODO all rings at the bottom

    orders = getOrderNums(json)
    oneSideds = makeOneSided(json)
    twoSideds = makeTwoSided(json)
    bands = makeBand(json)
    sortOrder = sorted(orders.items())

    #  for order in sortOrder:
        #  print sortOrder[order]

    boilerplate = "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title></title><link rel='stylesheet' type='text/css' href='./test.css'></head><body>"
    endplate = "</body></html>"

    html = ""
    html += boilerplate
    for key, order in sortOrder: 
        if 'ring' not in key and 'bracelet' not in key and '2sided' not in key:
            html += "<div class='break'></div>"
            html += "<div class='order'>"
            html += order
            o = 0 # for counting sortOrder
            for oneSided in oneSideds:
                for item in oneSideds[oneSided]:
                    if o % 8 == 0 and o != 0:
                        html += "<div class='break'></div>" + order
                    html += item 
                    o += 1
            html += "</div>"
        if 'ring' not in key and 'bracelet' not in key and '2sided' in key:
            html += "<div class='break'></div>"
            html += "<div class='order'>"
            html += order
            t = 0
            for twoSided in twoSideds:
                for item in twoSideds[twoSided]:
                    if t % 6 == 0 and t != 0:
                        html += "<div class='break'></div>" + order
                    html += item
                    t += 1
            html += "</div>"
        if 'ring' in key or 'bracelet' in key:
            html += "<div class='break'></div>"
            for band in bands:
                for item in bands[band]:
                    html += "<div class='break'<div class='order'>"
                    html += order
                    html += item
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
