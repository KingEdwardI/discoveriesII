#!/usr/bin/python
# version 0.5
"""
Strategy: Build an html page containing orders for Discoveries - Egyptian Imports, from a JSON file.
            take in JSON order form, and create a view-file in html - styled inline.
            there are three main jewelery types plus the order description: one-sided, two-sided, bands.
            each are created individually and joined together to create a full page.
            Future version may take in .csv as well as .json

JSON model:
    {
    "itemSort"  : "string"
    "itemNum": "string",
    "type": "string",
    "metal": "string",
    "style": "string",
    "size": "string",
    "attr1": "string",
    "attr2": "string",
    "side1lang": "string",
    "side1symb": "string",
    "side2lang": "string",
    "side2symb": "string",
    "label": "string",
    "customerNum": "string",
    "batchNum": "string",
    "orderNum": "string"
    }
"""
import json
import sys
from unidecode import unidecode


argIn = sys.argv[1]
argOut = sys.argv[2]

bandTypes = ['ring','bracelet','ring band', 'band']

def main():

    orderJSON = readJSON(argIn)
    writeHTML(orderJSON)
    #  makeHTML(orderJSON)

def getOrderNums(json):
    """
    create the order description for the orders. organize by 'itemSort', from the json

    :returns: dict of lists, containing strings as html
    :rtype: dict
    """

    itemDescDict = {} # {itemSort : itemDesc}

    for item in json:
        # create a unique identifier for each item and append 'z' if it's a band for sorting in the future
        if any(item['type'].lower() in s for s in bandTypes): 
            identifier = "z" + item['itemSort'].lower() + item['type'].lower() + item['attr1'].lower().replace(' ', '')
        else:
            identifier = item['itemSort'].lower() + item['type'].lower() + item['attr1'].lower().replace(' ', '')
            # create a view-model for each item in an order
        if identifier not in itemDescDict:
            itemDescDict[identifier] = "<div class='orderDescData'><span class='orderDescription'>"
            itemDescDict[identifier] += item['itemSort'] + " | " + item['metal'] + " " + item['type'] + " " + item['attr1'] + " " + item['attr2'] + " | </span><span class='arabic'>" 
            if item['metal'] != '':
                itemDescDict[identifier] += "<img src='.img/" + item['metal'].lower().replace(' ', '')+ ".jpg'>" 
            if item['type'] != '':
                itemDescDict[identifier] += "<img src='.img/" + item['type'].lower().replace(' ', '')+ ".jpg'>"
            if item['attr1'] != '':
                itemDescDict[identifier] += "<img src='.img/" + item['attr1'].lower().replace(' ', '')+ ".jpg'>" 
            if item['attr2'] != '':
                itemDescDict[identifier] += "<img src='.img/" + item['attr2'].lower().replace(' ', '')+ ".jpg'>"
            itemDescDict[identifier] += "</span><span class='batchNum'>" + item['batchNum'].lower() + "</span></div>"

    return itemDescDict

def makeOneSided(json):
    """
    create the order form for one sided pieces of jewelery. organize by identifier for distinction later.
    
    :returns: dictionary of lists of html strings. 
    :rtype: dict
    """

    itemOneSided = {}

    # create the keys, from unique identifier.
    for item in json:
        if not any(item['type'].lower() in s for s in bandTypes) and item['attr1'].lower().replace(' ','') != '2sided':
            identifier = item['itemSort']
            itemOneSided[unidecode(identifier)] = []

    for item in json:
        if not any(item['type'].lower() in s for s in bandTypes) and item['attr1'].lower().replace(' ', '') != '2sided':
            buildItem = "<div class='item oneSided'><table class='itemSymbols'><tbody>"
            for letter in item['side1symb']:
                buildItem += "<tr><td class='symbol " + item['side1lang'].lower() + "'>" + letter.upper() + "</td></tr>"
            buildItem += "</tbody></table><div class='itemDescription'>"
            if item['size'] != '':
                buildItem += "<div class='size arabic'><img src='.img/" + str(item['size']) + ".jpg'></div>"
            else: 
                buildItem += "<div class='size arabic'></div>"
            buildItem += "<div class='description'> " + item['itemNum'] + " " + str(item['size']) + "<br>" + item['label'] + "<br>"
            buildItem += str(item['orderNum']) + "<br></div></div></div>"
            identifier = item['itemSort']
            itemOneSided[unidecode(identifier)].append(buildItem)

    return itemOneSided

def makeTwoSided(json):
    """
    create the order form for two sided pieces of jewelery. organize by identifier for distinction later.

    :returns: dictionary of lists of html strings
    :rtype: dict
    """

    itemTwoSided = {}

    # create the key with unique identifier
    for item in json:
        if not any(item['type'].lower() in s for s in bandTypes) and item['attr1'].lower().replace(' ', '') == '2sided':
            itemTwoSided[item['itemSort']] = []

    # create the values for keys
    for item in json:
        if not any(item['type'].lower() in s for s in bandTypes) and item['attr1'].lower().replace(' ', '') == '2sided':
            buildItem = "<div class='item twoSided'><table class='itemSymbols'><tbody>"
            print len(item['side1symb'])
            print len(item['side2symb'])
            if len(item['side1symb']) > len(item['side2symb']):
                length = len(item['side1symb'])
            else:
                length = len(item['side2symb'])
            print length
            for i in range(length):
                print i
                try:
                    buildItem += "<tr><td class='side1 symbol " + item['side1lang'].lower() + "'>" + item['side1symb'][i].upper() + "</td>"
                    buildItem += "<td class='side2 symbol " + item['side2lang'].lower() + "'>" + item['side2symb'][i].upper() + "</td></tr>"
                except IndexError:
                    buildItem += "<tr><td class='blank'> </td></tr>"
            buildItem += "</tbody></table><div class='itemDescription'>"
            buildItem += "<div class='size arabic'><img src='.img/" + str(item['size']) + ".jpg'></div>"
            buildItem += "<div class='description'>" + item['itemNum'] + " " + str(item['size']) + "<br>" + item['label'] + "<br>"
            buildItem += str(item['orderNum']) + "<br></div></div></div>"
            itemTwoSided[item['itemSort']].append(buildItem)

    return itemTwoSided

def makeBand(json):
    """
    create the order form for band jewelery. organize by identifier for distinction later.

    :returns: dictionary of lists of html strings
    :rtype: dict
    """

    itemBand = {}
    
    # create key with unique identifier
    for item in json:
        if any(item['type'].lower() in s for s in bandTypes):
            itemBand[item['itemSort']] = []

    # create values
    for item in json:
        if any(item['type'].lower() in s for s in bandTypes):
            buildItem = "<div class='item band'><div><table class='itemSymbols'><tbody><tr>"
            for letter in item['side1symb']:
                buildItem += "<td class='symbol " + item['side1lang'].lower() + "'>" + letter.upper() + "</td>"
            buildItem += "<td class='blank'></td>"
            buildItem += "<td class='size arabic'><img src='.img/" + str(item['size']).lower() + ".jpg'></td>"
            buildItem += "</tbody></table></div><div class='itemDescription'>"
            buildItem += "<div class='description'>" + item['itemNum'] + str(item['size']) + " " + item['label'] + " "
            buildItem += str(item['orderNum']) + "</div></div></div>"
            itemBand[item['itemSort']].append(buildItem)

    return itemBand

def makeHTML(json):
    """
    build out the whole html page
    loop through all of the previously created html information and create a full html page based on that information

    oneSideds, twoSideds, bands, orders = {
        "identifier" : "html string"
    }
    """

    orders = getOrderNums(json) 
    oneSideds = makeOneSided(json)
    twoSideds = makeTwoSided(json)
    bands = makeBand(json)
    print bands
    sortOrder = sorted(orders.items())

    boilerplate = "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title></title><style> @font-face {  font-family: 'heiro';src: url('.fonts/Hiero.ttf');}@font-face {font-family: 'astro';src: url('.fonts/Astro.ttf');}@font-face {font-family: 'greek';src: url('.fonts/greek.ttf');}.hiero {font-family: 'heiro';font-size: 30px;}.astro {font-family: 'astro';font-size: 30px;}.greek {font-family: 'greek';font-size: 30px;}div.orderDescData {max-height: 50px;margin-bottom: 10px;}span.arabic > img {max-height: 50px;max-width: 150px;}div.item {float: left;display: flex-inline;height: 445px;border-right: 1px solid black;margin-bottom: 20px;}div.item.oneSided {width: 100px;}div.item.twoSided {width: 115px;}div.size > img {display: block;margin: 0 auto;}div.orderDescData:last-child {clear: right;}table.itemSymbols {width: 100%;}td.symbol {width: 30px;height: 30px;text-align: center;}div.item {position: relative;}div.itemDescription {position: absolute;bottom: 0;max-width: 100%;overflow: hidden;white-space: nowrap;}div.band {height: 90px;width: auto;}div.description {margin: 10px; font-size: 12px}div.break {clear: both;}</style></head><body>"
    endplate = "</body></html>"

    html = ""
    html += boilerplate
    x1, x2, x3 = 0, 0, 0 # for counting orders to insert line breaks
    # create OneSided
    for key, order in sortOrder: 
        html += "<div class='break'></div>"
        html += "<div class='order'>"
        o = 0 
        for oneSided in oneSideds:
            o = 0 
            if oneSided.lower() in key.lower():
                html += "<div class='break'></div>"
                html += order
                for item in oneSideds[oneSided]:
                    if o % 6 == 0 and o != 0:
                        html += "<div class='break'></div>" + order
                    html += item 
                    o += 1
        t = 0
        for twoSided in twoSideds:
            t = 0
            if twoSided.lower() in key.lower():
                html += "<div class='break'></div>"
                html += order
                for item in twoSideds[twoSided]:
                    if t % 5 == 0 and t != 0 :
                        html += "<div class='break'></div>" + order
                    html += item 
                    t += 1
        for band in bands:
            if band.lower() in key.lower():
                for item in bands[band]:
                    html += "<div class='break'></div>" + order
                    html += item 

    html += endplate

    #  print html
    return html

def writeHTML(json):
    """write out to a specified file."""

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
    return order

if __name__ == "__main__":
    main()
