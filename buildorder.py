#!/usr/bin/python
import json
import sys
from unidecode import unidecode

argIn = sys.argv[1]
argOut = sys.argv[2]

bandTypes = ['ring','bracelet','ring band', 'band']

def main():
    orderJSON, arabicImageLinks = readJSON(argIn)
    #  getOrderNums(orderJSON)
    #  print makeOneSided(orderJSON)
    #  print makeTwoSided(orderJSON)
    #  print makeBand(orderJSON)
    #  makeHTML(orderJSON)
    writeHTML(orderJSON)


def getOrderNums(json):
    itemDescDict = {} # {itemSort : itemDesc}
    for item in json:
        if any(item['type'].lower() in s for s in bandTypes):
            identifier = "z" + item['itemSort'].lower() + item['type'].lower() + item['attr1'].lower().replace(' ', '')
        else:
            identifier = item['itemSort'].lower() + item['type'].lower() + item['attr1'].lower().replace(' ', '')
        if identifier not in itemDescDict:
            itemDescDict[identifier] = "<div class='orderDescData'><span class='orderDescription'>"
            itemDescDict[identifier] += item['itemSort'] + " | " + item['metal'] + " " + item['type'] + " " + item['attr1'] + " " + item['attr2'] + " | </span><span class='arabic'>" 
            if item['metal']:
                itemDescDict[identifier] += "<img src='.img/" + item['metal'].lower() + ".jpg'>" 
            if item['type']:
                itemDescDict[identifier] += "<img src='.img/" + item['type'].lower() + ".jpg'>"
            if item['attr1']:
                itemDescDict[identifier] += "<img src='.img/" + item['attr1'].lower() + ".jpg'>" 
            if item['attr2']:
                itemDescDict[identifier] += "<img src='.img/" + item['attr2'].lower() + ".jpg'>"
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
            buildItem += "<div class='size arabic'><img src='.img/" + str(item['size']) + ".jpg'></div>"
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
            buildItem += "<div class='size arabic'><img src='.img/" + str(item['size']) + ".jpg'></div>"
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
            buildItem += "<td class='size arabic'><img src='.img/" + str(item['size']).lower() + ".jpg'></td>"
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

    boilerplate = "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title></title><style> @font-face {  font-family: 'heiro';src: url('.fonts/Hiero.ttf');}@font-face {font-family: 'astro';src: url('.fonts/Astro.ttf');}@font-face {font-family: 'greek';src: url('.fonts/greek.ttf');}.hiero {font-family: 'heiro';font-size: 30px;}.astro {font-family: 'astro';font-size: 30px;}.greek {font-family: 'greek';font-size: 30px;}div.orderDescData {max-height: 50px;margin-bottom: 10px;}span.arabic > img {max-height: 50px;max-width: 150px;}div.item {float: left;display: flex-inline;height: 445px;border-right: 1px solid black;margin-bottom: 20px;}div.item.oneSided {width: 85px;}div.item.twoSided {width: 115px;}div.size > img {display: block;margin: 0 auto;}div.orderDescData:last-child {clear: right;}table.itemSymbols {width: 100%;}td.symbol {width: 30px;height: 30px;text-align: center;}div.item {position: relative;}div.itemDescription {position: absolute;bottom: 0;max-width: 100%;overflow: hidden;white-space: nowrap;}div.band {height: 90px;width: auto;}div.description {margin: 10px;}div.break {clear: both;}</style></head><body>"
    endplate = "</body></html>"

    html = ""
    html += boilerplate
    x1, x2, x3 = 0, 0, 0
    for key, order in sortOrder: 
        if 'ring' not in key and 'bracelet' not in key and '2sided' not in key and x1 == 0:
            html += "<div class='break'></div>"
            html += "<div class='order'>"
            html += order
            o = 0 # counting for line breaks
            for oneSided in oneSideds:
                for item in oneSideds[oneSided]:
                    if o % 8 == 0 and o != 0:
                        html += "<div class='break'></div>" + order
                    html += item 
                    o += 1
            html += "</div>"
            x1 += 1
        if 'ring' not in key and 'bracelet' not in key and '2sided' in key and x2 == 0:
            html += "<div class='break'></div>"
            html += "<div class='order'>"
            html += order
            t = 0
            #  print twoSideds
            for twoSided in twoSideds:
                for item in twoSideds[twoSided]:
                    if t % 6 == 0 and t != 0:
                        html += "<div class='break'></div>" + order
                    html += item
                    t += 1
            html += "</div>"
            x2 += 1
        if 'ring' in key or 'bracelet' in key and x3 == 0:
            html += "<div class='break'></div>"
            for band in bands:
                for item in bands[band]:
                    html += "<div class='break'<div class='order'>"
                    html += order
                    html += item
            x3 += 1
    html += endplate

    return html

def writeHTML(json):

    html = makeHTML(json)
    f = open(argOut, "w")
    f.write(html)
    f.close()

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
