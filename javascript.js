// TODO: page numbers
//       arabic text
//       print single-sided 8x
//       print 2-sided 4x
//       re-print order on line-break
//       size
//       formatting


$(function() {
 // sort objects function
  function compare(a,b) {
  if (a.side1symb < b.side1symb)
    return -1;
  if (a.side1symb > b.side1symb)
    return 1;
  return 0;
  }

  // check for undefined values
  function undefchk(obj) {
    $.each(obj, function(index, element) {
      if(typeof element === undefined || !element) {
        obj[index] = '|';
      }
    });
  }

  // get json for arabic images
  var arabic;
  console.log(arabic)

  $.getJSON("http://localhost:8001/json/smalltest.json", function(data) {
    console.log('success');
    var singlesidecount = 0;
    var doublesidecount = 2;
    var singlecount = 9;
    var doublecount = 5;
    var page = 0;

    // sort by itemNum
    data.sort(function(a,b) {return (a.itemNum > b.itemNum) ? 1 : ((b.itemNum > a.itemNum) ? -1 : 0);} ); 

    // loop through each item in the data array
    $.each(data, function(i, item) {

      // count the items in an order
      if(data[i-1] !== undefined && data[i].itemNum == data[i-1].itemNum){
        itemcount += 1;
        if(itemcount % 8 === 0) {
          doublecount += 5;
        }
        if(itemcount % 16 === 0) {
          singlecount += 9;
        }
      }
      else {
        itemcount = 0;
      }

      /*
       * if(page % 2 === 0 && page !== 0) {
       *   $("body").append("<hr>");
       * }
       */

      // if it is the first item we want to print that order
      if(i === 0) {
        var orderdesc = item.metal + " " + item.type  + " " + item.attr1 + " " + item.attr2;
        $("body").append("<table class='order" + item.itemNum + " order'></table>")
        $("table.order" + item.itemNum).append("<tr class='orderdesc" + i + " orderdesc'></tr>");
        $("table.order" + item.itemNum).append("<tr class='itemrow" + item.itemNum + " itemrow'></tr>");
        $("tr.orderdesc" + i).append("<td class='itemdesc" + item.itemNum + "'>" + item.itemNum + " | </td>");
        $("td.itemdesc" + item.itemNum).append("<span class='orderdesc'>" + orderdesc + " | </span>");
        $("td.itemdesc" + item.itemNum).append("<span class='arabic'>" + orderdesc + " | </span>");
        $("td.itemdesc" + item.itemNum).append("<span class='barch'>" + item.barchNum + " | </span>");
      }

      // if the item's order already exists, we only want to print it once
      else if(i > 0 && data[i].itemNum != data[i-1].itemNum) {
        var orderdesc = item.metal + " " + item.type  + " " + item.attr1 + " " + item.attr2;
        $("body").append("<table class='order" + item.itemNum + " order'></table>")
        $("table.order" + item.itemNum).append("<tr class='orderdesc" + i + " orderdesc'></tr>");
        $("table.order" + item.itemNum).append("<tr class='itemrow" + item.itemNum + " itemrow'></tr>");
        $("tr.orderdesc" + i).append("<td class='itemdesc" + item.itemNum +"'>" + item.itemNum + " | </td>");
        $("td.itemdesc" + item.itemNum).append("<span class='orderdesc'>" + orderdesc + " | </span>");
        $("td.itemdesc" + item.itemNum).append("<span class='arabic'>" + orderdesc + " | </span>");
        $("td.itemdesc" + item.itemNum).append("<span class='barch'>" + item.barchNum + " | </span>");
      }

      // if the item is not of type ring, then we want to print the contents vertically
      if(item.type != 'ring') {
        $("tr.itemrow" + item.itemNum).append("<td class='itemorder" + item.itemNum + i +" itemorder'></td>")
        $("td.itemorder" + item.itemNum + i).append("<table class='item" + i + " itemcontent'></table>");

        // if the first side of jewelery is shorter than the second we need to account for that
        var len1 = item.side1symb.length;
        var len2 = item.side2symb.length;

        // if the first side is longer than the second
        if(len1 >= len2) {
          // build the first side of the jewelery
          var label = item.label.replace(/ /g,'');
          for(h in item.side1symb) {
            $("table.item" + i).append("<tr class='" + label + i + "'><td class='" + item.side1lang.toLowerCase() + " lang'>" + item.side1symb[h] + "</td></tr>");
          }

          // build the second side of the jewelery
          var c = 1;
          for(k in item.side2symb) {
            $("tr." + label + i + ":nth-child(" + (c) + ")").append("<td class='" + item.side2lang.toLowerCase() + " lang'>" + item.side2symb[k] + "</td>");
            c += 1;
          }
        }
        
        // if the second side is longer than the first
        else {
          // build the second side of the jewelery
          var label = item.label.replace(/ /g,'');
          for(k in item.side2symb) {
            $("table.item" + i).append("<tr class='" + label + i + "'><td class='" + item.side2lang.toLowerCase() + " lang'>" + item.side2symb[k] + "</td></tr>");
          }

          // then build the first side
          var c = 1;
          for(var h = 0; h < len2; h++) {
            if(item.side1symb[h] !== undefined) {
              $("tr." + label + i + ":nth-child(" + (c) + ")").prepend("<td class='" + item.side1lang.toLowerCase() + " lang'>" + item.side1symb[h] + "</td>");
            }
            else {
              $("tr." + label + i + ":nth-child(" + (c) + ")").prepend("<td class='" + item.side1lang.toLowerCase() + " lang'> </td>");
            }
            c += 1;
          }
        }

        // build the item description
        $("table.item" + i).append("<tr class='itemdesc" + i +" itemdesc'></tr>");
        $("tr.itemdesc" + i).append("<td class='orderinfo' colspan=2>" + item.itemNum + "<br>" + item.customerNum + " -" + item.label + "<br>" + item.orderNum + "</td>");

        if(itemcount % 4 === 0) {
           $("td.itemorder:nth-child(" + doublecount + ")").css('display', 'block')
           $("td.itemorder:nth-child(" + doublecount + ")").css('clear', 'left')
        }
      }

      // if the item is a ring, we want to print it horizontally
      else {
        $("table.order").addClass("ring")
        label = item.label.replace(/ /g,'');
        $("tr.itemrow" + item.itemNum).append("<td class='itemorder" + item.itemNum + i +"'></td>")
        $("td.itemorder" + item.itemNum + i).append("<table class='item" + i + " itemcontent ring'></table>");
        $("table.item" + i).append("<tr class='" + label + i +"'>");

        // build the ring contents
        for(r in item.side1symb) {
          $("tr." + label + i).append("<td class='" + item.side1lang.toLowerCase() +" lang'>" + item.side1symb[r] + "</td>")
        }

        $("tr." + label + i).append("<td class='lang'> </td><td class='arabic'>small</td>");

        
        // build the item description
        var span = item.side1symb.length;
        $("table.item" + i).append("<tr class='itemdesc" + i +" itemdesc'></tr>");
        $("tr.itemdesc" + i).append("<td colspan=" + span + ">" + item.itemNum + " " + item.customerNum + " -" + item.label + " " + item.orderNum + "</td>");
      }

    });


  }).error(function(){
    console.log('ERROR');
  });

  $.getJSON("http://localhost:8001/json/arabic.json", function(data) { 
      if($('span').hasClass("arabic")) {
        stuff = $('span.arabic').text();
        arr = stuff.split(' ');
        imgsrc = '';
        $.each(data, function(i, item) {
          for(attr in arr) {
            if(arr[attr] === i) {
              console.log('hello')
              imgsrc += '<img height="35px" width="35px"src="http://localhost:8001/' + item + '">'
            }
          }
        });
        $('span.arabic').html(imgsrc);
      }
      if($('td').hasClass("arabic")) {
        stuff = $('td.arabic').text();
        arr = stuff.split(' ');
        imgsrc = '';
        $.each(data, function(i, item) {
          for(attr in arr) {
            if(arr[attr] === i) {
              imgsrc += '<img height="35px" width="35px"src="http://localhost:8001/' + item + '">'
            }
          }
        });
        $('td.arabic').html(imgsrc);
      }
    });
  });
