#!/usr/bin/python
# version 0.8
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

    # loop through items in json file
    for item in json:
        # create a unique identifier for each item and append 'z' if it's a band for sorting in the future
        if any(item['type'].lower() in s for s in bandTypes): 
            identifier = "z" + item['itemSort'].lower()
        # if the jewelery is not in the bandTypes array, create unique ID for each item
        else:
            identifier = item['itemSort'].lower()
        # create a view-model for each item in an order
        if identifier not in itemDescDict:
            # wrapper for the items div
            itemDescDict[identifier] = "<div class='orderDescData'><span class='orderDescription'>"
            # span for item description
            itemDescDict[identifier] += item['itemSort'] + " | " + item['metal'] + " " + item['type'] + " " + item['style'] + " " + item['attr1'] + " " + item['attr2'] + " | </span><span class='arabic'>" 
            # append Arabic images, in place of words. If the item does not have that attribute, it is not added.
            if item['metal'] != '':
                itemDescDict[identifier] += "<img src='.img/" + item['metal'].lower().replace(' ', '')+ ".jpg'>" 
            if item['type'] != '':
                itemDescDict[identifier] += "<img src='.img/" + item['type'].lower().replace(' ', '')+ ".jpg'>"
            if item['style'] != '':
                itemDescDict[identifier] += "<img src='.img/" + item['style'].lower().replace(' ', '')+ ".jpg'>"
            if item['attr1'] != '':
                itemDescDict[identifier] += "<img src='.img/" + item['attr1'].lower().replace(' ', '')+ ".jpg'>" 
            if item['attr2'] != '':
                itemDescDict[identifier] += "<img src='.img/" + item['attr2'].lower().replace(' ', '')+ ".jpg'>"
            # appending batchNumber, and closing divs
            itemDescDict[identifier] += "</span><span class='batchNum'>" + item['batchNum'].lower() + "</span></div>"

    return itemDescDict

def makeOneSided(json):
    """
    create the order form for one sided pieces of jewelery. organize by identifier for distinction later.
    one sided items are printed vertically
    
    :returns: dictionary of lists of html strings. 
    :rtype: dict
    """

    itemOneSided = {}

    # loop through items in the json file and create unique identifers for each item that is oneSided. (this does not have to be sorted)
    for item in json:
        if not any(item['type'].lower() in s for s in bandTypes) and item['attr1'].lower().replace(' ','') != '2sided':
            itemOneSided[unidecode(item['itemSort'])] = []

    # loop through the items and create an html string of the item
    for item in json:
        # todo: need to use itemOneSided for this
        if not any(item['type'].lower() in s for s in bandTypes) and item['attr1'].lower().replace(' ', '') != '2sided':
            # item opening tags
            buildItem = "<div class='item oneSided'><table class='itemSymbols'><tbody>"
            # loop through the characters in side1symb
            for letter in item['side1symb']:
                # create a table row for that character. creates a class for that based on side1lang
                buildItem += "<tr><td class='symbol " + item['side1lang'].lower() + "'>" + letter.upper() + "</td></tr>"
            # close tags. begin building the description of the item
            buildItem += "</tbody></table><div class='itemDescription'>"
            # check if the item has contents in the size field
            if item['size'] != '':
                # add with size from item from arabic images (which are all lowercase with no spaces)
                buildItem += "<div class='size arabic'><img src='.img/" + str(item['size']).lower().replace(' ', '') + ".jpg'></div>"
            else: 
                # add in a blank div
                buildItem += "<div class='size arabic'></div>"
            # create the english description
            buildItem += "<div class='description'> " + item['itemNum'] + "<br>" + item['customerNum'] + ' ' + item['label'] + "<br>"
            # close tags
            buildItem += str(item['orderNum']) + "<br></div></div></div>"
            identifier = item['itemSort']
            # create a dict-list entry for that identifier
            itemOneSided[unidecode(identifier)].append(buildItem)

    return itemOneSided

def makeTwoSided(json):
    """
    create the order form for two sided pieces of jewelery. organize by identifier for distinction later.
    two sided jewelery is printed vertically

    :returns: dictionary of lists of html strings
    :rtype: dict
    """

    itemTwoSided = {}

    # loop through items in the json file and create unique identifers for each item that is twoSided. (this does not have to be sorted)
    for item in json:
        if not any(item['type'].lower() in s for s in bandTypes) and item['attr1'].lower().replace(' ', '') == '2sided':
            itemTwoSided[item['itemSort']] = []

    # loop through the items and create the html entry for twoSided items
    for item in json:
        # todo: need to use itemTwoSided in this...
        if not any(item['type'].lower() in s for s in bandTypes) and item['attr1'].lower().replace(' ', '') == '2sided':
            # ceate wrapper for these items
            buildItem = "<div class='item twoSided'><table class='itemSymbols'><tbody>"
            # if the first side is longer than the second (or vice versa) need to print all characters of each side
            if len(item['side1symb']) > len(item['side2symb']):
                length = len(item['side1symb'])
                # build the each side
                for i in range(length):
                    buildItem += "<tr><td class='side1 symbol " + item['side1lang'].lower() + "'>" + item['side1symb'][i].upper() + "</td>"
                    # try to build the second side
                    try:
                        buildItem += "<td class='side2 symbol " + item['side2lang'].lower() + "'>" + item['side2symb'][i].upper() + "</td></tr>"
                    # if the second side has less characters add an empty table data
                    except IndexError:
                        buildItem += "<td class='side2 symbol'> </td>"
            else:
                length = len(item['side2symb'])
                # build the each side
                for i in range(length):
                    # try to build the first side
                    try:
                        # add a class for the items first side characters, create the row>data for that character
                        buildItem += "<tr><td class='side1 symbol " + item['side1lang'].lower() + "'>" + item['side1symb'][i].upper() + "</td>"
                    # if the first side does not have a character, add an empty table data
                    except IndexError:
                        buildItem += "<td class='side1 symbol'> </td>"
                    # add a class for the items second side characters, create the row>data for that character and close row
                    buildItem += "<td class='side2 symbol " + item['side2lang'].lower() + "'>" + item['side2symb'][i].upper() + "</td></tr>"
            # close table with characters and start building that items description
            buildItem += "</tbody></table><div class='itemDescription'>"
            # add that items size
            buildItem += "<div class='size arabic'><img src='.img/" + str(item['size']).lower() + ".jpg'></div>"
            # add in that items number
            buildItem += "<div class='description'>" + item['itemNum'] + "<br>" + item['customerNum'] + ' ' + item['label'] + "<br>"
            # add in the orderNum
            buildItem += str(item['orderNum']) + "<br></div></div></div>"
            # add to the dict
            itemTwoSided[item['itemSort']].append(buildItem)

    return itemTwoSided

def makeBand(json):
    """
    create the order form for band jewelery. organize by identifier for distinction later.
    bands are printed horizontally

    :returns: dictionary of lists of html strings
    :rtype: dict
    """

    itemBand = {}
    
    # loop through items in the json file and create unique identifers for each item that is in bandTypes. (this does not have to be sorted)
    for item in json:
        if any(item['type'].lower() in s for s in bandTypes):
            itemBand[item['itemSort']] = []

    # create values
    for item in json:
        # todo: should use itemBand here
        if any(item['type'].lower() in s for s in bandTypes):
            # create a wrapper for these items
            buildItem = "<div class='item band'><div><table class='itemSymbols'><tbody><tr>"
            # loop through the items characters
            for letter in item['side1symb']:
                # create a data column for that character
                buildItem += "<td class='symbol " + item['side1lang'].lower() + "'>" + letter.upper() + "</td>"
            # close the data
            buildItem += "<td class='blank'></td>"

           # create the size column for each item if it exists (this should be printed next to the characters)
            if item['size'] != '':
                buildItem += "<td class='size arabic'><img src='.img/" + str(item['size']).lower() + ".jpg'></td>"
            # if it does not exist, append an empty data column
            else:
                buildItem += "<td class='size arabic'></td>"
            # close item characters, and begin item description
            buildItem += "</tbody></table></div><div class='itemDescription'>"
            # create the itemDescription, to be printed horizontally along the bottom
            buildItem += "<div class='description'>" + item['itemNum'] + item['customerNum'] + ' ' + item['label'] + " "
            # add the order number and close all divs
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
    sortOrder = sorted(orders.items())

    # can be found formatted in tests/boilerplate.html
    boilerplate = "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title></title><style> @font-face {  font-family: 'heiro';src: url('.fonts/Hiero.ttf');}@font-face {font-family: 'astro';src: url('.fonts/Astro.ttf');}@font-face {font-family: 'greek';src: url('.fonts/greek.ttf');}.hiero {font-family: 'heiro';font-size: 30px;}.astro {font-family: 'astro';font-size: 30px;}.greek {font-family: 'greek';font-size: 30px;}div.orderDescData {max-height: 50px;margin-bottom: 10px;}span.arabic > img {max-height: 50px; max-width: 250px;}div.item {border-right: 1px solid black;float: left;display: flex-inline;height: 400px;margin-bottom: 20px;}div.item.oneSided {width: 100px;}div.item.twoSided {width: 115px;}div.size > img {display: block;margin: 0 auto; max-height: 40px; max-width:40px;}div.orderDescData:last-child {clear: right;}table.itemSymbols {width: 100%;}td.symbol {width: 30px;height: 30px;text-align: center;}div.item {position: relative;}div.itemDescription {position: absolute;bottom: 0;max-width: 100%;overflow: hidden;white-space: nowrap;}div.band {height: 90px;width: auto;}div.description {margin: 10px; font-size: 12px}div.break {clear: both;}</style></head><body>"
    endplate = "</body></html>"

    html = ""
    #  append boilerplate
    html += boilerplate
    x1, x2, x3 = 0, 0, 0 # for counting orders to insert line breaks
    # create OneSided
    for key, order in sortOrder: 
        # insert a line break div for each separate order
        html += "<div class='break'></div>"
        # begin an order
        html += "<div class='order'>"
        o = 0 # for counting orders
        # loop through oneSided orders
        for oneSided in oneSideds:
            # for counting items
            o = 0 
            # check if the item matches the order
            if oneSided.lower() == key.lower():
                # add a line break for the first item
                html += "<div class='break'></div>"
                #  add the first order 
                html += order
                #  loop through the items 
                for item in oneSideds[oneSided]:
                    # if 6 items have been printed, add in a line break and add the order again
                    if o % 6 == 0 and o != 0:
                        html += "<div class='break'></div>" + order
                    # add the order
                    html += item 
                    o += 1

        t = 0 # for counting orders
        # loop through twoSided orders
        for twoSided in twoSideds:
            t = 0
            # check if the item matches the order
            if twoSided.lower() in key.lower():
                # add a line break for the first item
                html += "<div class='break'></div>"
                #  add the first order 
                html += order
                #  loop through the items 
                for item in twoSideds[twoSided]:
                    # if 5 items have been printed, add in a line break and add the order again
                    if t % 5 == 0 and t != 0 :
                        html += "<div class='break'></div>" + order
                    # add the order
                    html += item 
                    t += 1

        # loop through band items
        for band in bands:
            # if the item matches the order
            if band.lower() in key.lower():
                # loop through the items
                for item in bands[band]:
                    # add that order and the item for that order
                    html += "<div class='break'></div>" + order
                    html += item 

    # close the body and html tags.
    html += endplate

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
