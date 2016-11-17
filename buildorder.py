import json
import sys

argIn = sys.argv[1]

def main():
    orderJSON, arabicImageLinks = readJSON(argIn)
    #  sortJSON(orderJSON)
    #  makeOrder(orderJSON)
    #  print getOrderNums(orderJSON)
    makeOrderHeader(arabicImageLinks, orderJSON)
    #  makeHTML(orderJSON)
    #  insertArabic(arabicImageLinks, orderJSON)


def getOrderNums(json):
    #TODO
    itemDescription = []
    arabicDescription = []
    orderNum = []
    for item in json:
        if not any(item['itemNum'] in i for i in itemDescription):
            itemDescription.append(item['itemNum'] + " | " + item['metal'] + " " + item['type'] + " " + item['attr1'] + " " + item['attr2'])
            arabicDescription.append(item['metal'] + " | " + item['type'] + " | " + item['attr1'] + " | " + item['attr2'])
            orderNum.append(item['itemNum'])
    return map(lambda x: x.encode('ascii'), itemDescription), map(lambda x: x.encode('ascii'), arabicDescription), map(lambda x: x.encode('ascii'), orderNum)

def insertArabic(arabic, json):
    # TODO
    """ gets the Arabic image links and replaces whatever is provided with the link """
    itemDescription, arabicDescription, orderNum = getOrderNums(json)

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
    itemDescription, englishDescription, orderNum = getOrderNums(json)
    arabicDescription = insertArabic(arabic, json)

    orderTitle = []
        
    for (detail, arabicDetail) in zip(itemDescription, arabicDescription):
        content = ''
        content += "<div style='height:50px;width:575px;'class='orderDescData'>"
        content += "<span class='orderDescription'>" + detail + "</span>"
        for detail in arabicDetail:
            content += "<span class='arabic'><img src='" + detail + "'> | </span>"
        content += "</div>"
        orderTitle.append(content)
    for i in orderTitle:
        print i, '\n'

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

def makeOneSided(json):
    #TODO
    pass

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
