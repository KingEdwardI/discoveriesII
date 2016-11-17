#!/local/bin/python
import json
import sys

argIn = sys.argv[1]

def main():
    orderJSON, arabicImageLinks = readJSON(argIn)
    #  sortJSON(orderJSON)
    #  makeOrder(orderJSON)
    #  print getOrderNums(orderJSON)
    #  makeOrderHeader(arabicImageLinks, orderJSON)
    #  makeHTML(orderJSON)
    #  insertArabic(arabicImageLinks, orderJSON)
    #  makeSymbolTableOne(orderJSON)
    #  makeSymbolTableTwo(orderJSON)
    #  makeSize(arabicImageLinks, orderJSON)
    #  makeItemDescription(orderJSON)
    makeOneSided(arabicImageLinks, orderJSON)


def getOrderNums(json):
    #TODO
    itemDescription = []
    arabicDescription = []
    orderNum = []
    batchNum = ''
    for item in json:
        if not any(item['itemSort'] in i for i in itemDescription):
            itemDescription.append(item['itemSort'] + " | " + item['metal'] + " " + item['type'] + " " + item['attr1'] + " " + item['attr2'])
            arabicDescription.append(item['metal'] + " | " + item['type'] + " | " + item['attr1'] + " | " + item['attr2'])
            orderNum.append(item['itemNum'])
            batchNum = (item['batchNum'])
    return map(lambda x: x.encode('ascii'), itemDescription), map(lambda x: x.encode('ascii'), arabicDescription), map(lambda x: x.encode('ascii'), orderNum), batchNum

def insertArabic(arabic, json):
    # TODO
    """ gets the Arabic image links and replaces whatever is provided with the link """
    itemDescription, arabicDescription, orderNum, batchNum = getOrderNums(json)

    englishDescrip = []
    arabicDescrip = []

    for description in arabicDescription:
        englishDescrip.append(description.split('|'))
    
    for description in englishDescrip:
        holdDescrip = []
        for word in description:
            for key in arabic:
                if key in word.lower():
                    holdDescrip.append(arabic[key])
        arabicDescrip.append(holdDescrip)
    
    return arabicDescrip

def makeOrderHeader(arabic, json):
    itemDescription, englishDescription, orderNum, batchNum = getOrderNums(json)
    arabicDescription = insertArabic(arabic, json)

    orderTitle = []
        
    for (detail, arabicDetail) in zip(itemDescription, arabicDescription):
        content = ''
        content += "<div style='height:50px;width:575px;'class='orderDescData'>"
        content += "<span class='orderDescription'>" + detail + "</span>"
        for detail in arabicDetail:
            content += "<span class='arabic'><img src='" + detail + "'> | </span>"
        content += "<span class='batchNumber'>" + batchNum + "</span>"
        content += "</div>"
        orderTitle.append(content)

    return orderTitle

def makeHTML(json):
    """build out the whole html page"""

    order = makeOrder(json)
    boilerplate = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title></title><link rel="stylesheet" type="text/css" href="./test.css"></head><body>'
    endplate = '</body></html>'

    html = ''
    html += boilerplate
    html += order
    html += endplate

    print html

def test():
    html = '<div class="order"><div class="orderdesc">C2SL | blah blah |</div>'
    html += '<div class="orderItem"><table class="item"><tbody><tr><td class="symbol">A</td></tr><tr><td class="symbol">B</td></tr><tr><td class="symbol">C</td></tr><tr><td class="symbol">D</td></tr><tr><td class="symbol">E</td></tr></tbody></table><div class="size">4</div><div class="itemDesc">CSOA<br>sig -EDDIE<br> 8583958390</div></div>'
    print html

def makeSymbolTableOne(json):

    symbolTablesOne = []

    for item in json:
        if item['type'] != 'ring' and item['type'] != 'bracelet' and item['attr1'] != '2sided': 
            symbolTable = ''
            symbolTable += '<table class="itemSymbols"><tbody>'
            for letter in item['side1symb']:
                symbolTable += '<tr><td class="symbol ' + item['side1lang'] + '">' + letter + '</td></tr>'

            symbolTable += '</tbody></table>'
            symbolTablesOne.append(symbolTable)

    return symbolTablesOne

def makeSymbolTableTwo(json):

    symbolTablesTwo = []
    for item in json:
        if item['type'] != 'ring' and item['type'] != 'bracelet' and item['attr1'] == '2sided': 
            symbolTable = ''
            symbolTable += '<table class="itemSymbols"><tbody>'
            for side1, side2 in zip(item['side1symb'], item['side2symb']):
                symbolTable += '<tr><td class="side1 symbol ' + item['side1lang'] + '">' + side1 + '</td>'
                symbolTable += '<td class="side2 symbol ' + item['side2lang'] + '">' + side2 + '</td></tr>'
            symbolTable += '</tbody></table>'
        symbolTablesTwo.append(symbolTable)
    return symbolTablesTwo
        
def makeSize(arabic, json):

    sizesOneSided = []
    sizesTwoSided = []
    sizesBand = []
    for item in json:
        if item['attr1'] != '2sided' and item['type'] != 'ring' and item['type'] != 'bracelet':
            sizeDiv = ''
            for size in arabic:
                if size == item['size'] :
                    sizeDiv += '<div class="size arabic"><img src="' + arabic[size] + '"></div>'
                    sizesOneSided.append(sizeDiv)
        elif item['attr1'] == '2sided' and item['type'] != 'ring' and item['type'] != 'bracelet':
            sizeDiv = ''
            for size in arabic:
                if size == item['size'] :
                    sizeDiv += '<div class="size arabic"><img src="' + arabic[size] + '"></div>'
                    sizesTwoSided.append(sizeDiv)
        elif item['type'] == 'ring' or item['type'] == 'bracelet':
            sizeDiv = ''
            for size in arabic:
                if size == item['size'] :
                    sizeDiv += '<div class="size arabic"><img src="' + arabic[size] + '"></div>'
                    sizesBand.append(sizeDiv)
                    
    return sizesOneSided, sizesTwoSided, sizesBand

def makeItemDescription(json):

    oneSidedDescription = []
    twoSidedDescription = []
    bandDescription = []

    for item in json:
        if item['attr1'] != '2sided' and item['type'] != 'ring' and item['type'] != 'bracelet':
            itemDiv = ''
            itemDiv += '<div class="itemDescription">'
            itemDiv += item['itemNum'] + '<br>'
            itemDiv += 'SIG -' + item['label'] + '<br>'
            itemDiv += str(item['orderNum']) + '<br>'
            itemDiv += '</div>'
            oneSidedDescription.append(itemDiv)
        elif item['attr1'] == '2sided' and item['type'] != 'ring' and item['type'] != 'bracelet':
            itemDiv = ''
            itemDiv += '<div class="itemDescription">'
            itemDiv += item['itemNum'] + '<br>'
            itemDiv += 'SIG -' + item['label'] + '<br>'
            itemDiv += str(item['orderNum']) + '<br>'
            itemDiv += '</div>'
            twoSidedDescription.append(itemDiv)
        elif item['type'] == 'ring' or item['type'] == 'bracelet':
            itemDiv = ''
            itemDiv += '<div class="itemDescription">'
            itemDiv += item['itemNum'] + '<br>'
            itemDiv += 'SIG -' + item['label'] + '<br>'
            itemDiv += str(item['orderNum']) + '<br>'
            itemDiv += '</div>'
            bandDescription.append(itemDiv)
    
    return oneSidedDescription, twoSidedDescription, bandDescription
    

def makeOneSided(arabic, json):
    #TODO
    orderHead = makeOrderHeader(arabic, json)
    symbols = makeSymbolTableOne(json)
    oneSidedSizes, twoSidedSizes, bandSizes = makeSize(arabic, json)
    oneSidedDescription, twoSidedDescription, bandDescription = makeItemDescription(json)

    print len(symbols), len(oneSidedSizes), len(oneSidedDescription), len(orderHead)

    for order in orderHead:
        oneSidedOrder = ''
        oneSidedOrder += '<div class="fullOrder">' + order

def makeTwoSided(json):
    #TODO
    pass

def makeBand(json):
    #TODO
    pass

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
