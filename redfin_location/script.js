function greatSchools() {
  $('.schools-content table .school-name').each(function (index, node) {
    var schoolName = $(node).html();
    var schoolState = $('.region').first().text();
    $.get('//www.greatschools.org/gsr/search/suggest/school?query=' + schoolName, function(data, status) {
      if (status == "success" && data.length > 0) {
        var dataIndex = -1;
        for (var i = 0; i < data.length; i++) {
          if (data[i].state == schoolState) {
            dataIndex = i;
            break;
          }
        }
        if (dataIndex == -1) {
          return;
        }
        $('#gsRating').append('<li id="gsRating' + index + '">Loading ...</li>');
        var gsUrl = "//www.greatschools.org" + data[dataIndex].url;
        $.get(gsUrl, function(schoolData) {
          var schoolDom = $(schoolData);
          // rating
          var ratingElements = schoolDom.find(".school-info .rs-gs-rating").contents().filter(function() { return this.nodeType === 3; });
          var rating = ratingElements[0].textContent.trim();
          // test score (roughly old rating for California) and other ratings
          var ratingTitlesContainer = schoolDom.find("#academics-tour-anchor");
          var ratingTitlesStr = "";
          if (ratingTitlesContainer !== undefined) {
            var ratingTitles = $(ratingTitlesContainer).find('.toc-entry');
            for (var i = 0; i < ratingTitles.length; i++) {
              ratingTitlesStr += $(ratingTitles[i]).find('span')[0].innerText;
              var ratingScoresElements = $(ratingTitles[i]).find(".gs-rating").contents().filter(function() { return this.nodeType === 3; });
              if (ratingScoresElements !== undefined && ratingScoresElements.length > 0) {
                var scoreInt = parseInt(ratingScoresElements[0].textContent.trim());
                ratingTitlesStr += ' <span style="' + getRatingCss(scoreInt) + '">' + scoreInt + '</span> ';
              } else {
                ratingTitlesStr += ' N/A ';
              }
            }
          }
          // ethnicity and lowIncome
          // Super ugly hack because jquery selector doesn't seem to find the script tag
          var element = document.createElement('div');
          element.insertAdjacentHTML('beforeend', schoolData);
          var scripts = element.querySelectorAll('script');
          var script = undefined;
          for (var i = 0; i < scripts.length; i++) {
            if (scripts[i].innerHTML.indexOf('gon.ethnicity') > -1) {
              script = scripts[i];
              break;
            }
          }
          var ethnicity = '';
          var lowIncome = '';
          if (script !== undefined) {
            var scriptText = script.innerHTML;
            // compute ethnicity
            var start = scriptText.indexOf('gon.ethnicity=[') + 'gon.ethnicity='.length;
            var end = scriptText.indexOf(']', start) + 1;
            var ethnicityJson = JSON.parse(scriptText.substring(start, end));
            for (var i = 0; i < ethnicityJson.length; i++) {
              ethnicity += ethnicityJson[i].breakdown + ' ' + Math.round(ethnicityJson[i].school_value) + '%';
              if (i == 3) { // only print top 4
                break;
              }
              if (i != ethnicityJson.length - 1) {
                ethnicity += ' | ';
              }
            }
            // compute low income
            start = scriptText.indexOf('gon.subgroup=') + 'gon.subgroup='.length;
            end = scriptText.indexOf(';', start);
            var lowIncomeJson = JSON.parse(scriptText.substring(start, end));
            lowIncome = lowIncomeJson['Students participating in free or reduced-price lunch program'][0].school_value + '%';
          }
          var ratingInt = parseInt(rating);
          var wstr = '';
          wstr += '<span style="' + getRatingCss(ratingInt) + '">' + rating + '</span> ';
          wstr += '<a href="http://' + gsUrl + '" target="_blank">' + $(node).html() + '</a>';
          wstr += "<ul>";
          if (ratingTitlesStr != '') {
            wstr += '<li>' + ratingTitlesStr + '</li>';
          }
          if (ethnicity != '') {
            wstr += '<li>Ethnicity: ' + ethnicity + '</li>';
          }
          if (lowIncome != '') {
            wstr += '<li>Students from low-income families: ' + lowIncome + '</li>'
          }
          wstr += '</ul>';
          $('#gsRating' + index).html(wstr);
        });
      }
    });
  });
}

function getRatingCss(rating) {
  var ratingCSS = "display: inline-block; height: 25px; width: 25px; line-height: 25px; border-radius: 50%; color: white; text-align: center; background-color: ";
  if (rating <= 3) {
    ratingCSS += "rgb(195, 81, 75);";
  } else if (rating <= 7) {
    ratingCSS += "rgb(236, 132, 62);";
  } else {
    ratingCSS += "rgb(64, 167, 83);";
  }
  return ratingCSS;
}

// Copied from: http://stackoverflow.com/questions/149055/how-can-i-format-numbers-as-money-in-javascript
function formatMoney(n) {
  c = 0;
  d = '.';
  t = ',';
  p = '$';
  c = isNaN(c = Math.abs(c)) ? 2 : c;
  d = d == undefined ? "," : d;
  t = t == undefined ? "." : t;
  s = n < 0 ? "-" : "";
  i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "";
  j = (j = i.length) > 3 ? j % 3 : 0;
  return p + s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
};

function zillow(address, cityStateZip) {
  var apiKey = 'X1-ZWz196sfugrtaj_6a5jo';
  var searchUrl = '//www.zillow.com/webservice/GetSearchResults.htm?';
  var urlParams = {
    'zws-id': apiKey,
    'address': address,
    'citystatezip': cityStateZip,
    'rentzestimate': 'true'
  };
  searchUrl += $.param(urlParams);
  $.get(searchUrl, function(xmlData) {
    var data = $(xmlData);
    var wstr = '';
    if (data.has('homedetails')) {
      wstr += '<ul>';
      var link = $(data.find('homedetails')[0]).text();
      wstr += '<li><a href="' + link + '" target="_blank">Link: ' + link + '</a></li>';
      if (data.has('zestimate')) {
        var zestimateNode = $(data.find('zestimate')[0]);
        var zestimate = formatMoney($(zestimateNode.find('amount')).text());
        if ($("span[data-rf-test-id='avmLdpPrice']").length > 0) {
          zestimate += ' | <i>Redfin Estimate:</i> ' +  $($("span[data-rf-test-id='avmLdpPrice']")[0]).find('.value').text();
        }
        var zestimateLow = formatMoney($(zestimateNode.find('low')).text());
        var zestimateHigh = formatMoney($(zestimateNode.find('high')).text());
        var zestimateRange = zestimateLow + ' - ' + zestimateHigh;
        var rentZestimateNode = $(data.find('rentzestimate')[0]);
        var rentZestimate = formatMoney($(rentZestimateNode.find('amount')).text());
        var rentZestimateLow = formatMoney($(rentZestimateNode.find('low')).text());
        var rentZestimateHigh = formatMoney($(rentZestimateNode.find('high')).text());
        var rentZestimateRange = rentZestimateLow + ' - ' + rentZestimateHigh;
        wstr += '<li><i>Zestimate:</i> ' + zestimate + '</li>';
        wstr += '<li><i>Zestimate Range:</i> ' + zestimateRange + '</li>';
        wstr += '<li><i>Rent Zestimate:</i> ' + rentZestimate + '</li>';
        wstr += '<li><i>Rent Zestimate Range:</i> ' + rentZestimateRange + '</li>';
      }
      wstr += '</ul>';
    } else {
      wstr = 'Unable to load Zillow Data';
    }
    $('#zillowInfo').html(wstr);
  });
};

function distanceToPlaces(latitude, longitude) {
  $.getJSON("//maps.googleapis.com/maps/api/directions/json?origin=" + latitude + "," + longitude + "&destination=3003+Bunker+Hill+Lane+Santa+Clara+CA", function(data1) {
    $.getJSON("//maps.googleapis.com/maps/api/directions/json?origin=" + latitude + "," + longitude + "&destination=1600+Amphitheatre+Parkway+Mountain+View+CA", function(data2) {
      var cisco = data1.routes[0].legs[0].distance.text;
      var google = data2.routes[0].legs[0].distance.text;
      var wstr = "";
      wstr += "<a href=\"https://maps.google.com?saddr=" + latitude + "," + longitude + "&daddr=3003+Bunker+Hill+Lane+Santa+Clara+CA\" target=\"_blank\">";
      wstr += "Cisco: " + cisco;
      wstr += "</a>";
      wstr += " | ";
      wstr += "<a href=\"https://maps.google.com?saddr=" + latitude + "," + longitude + "&daddr=1600+Amphitheatre+Parkway+Mountain+View+CA\" target=\"_blank\">";
      wstr += "Google: " + google;
      wstr += "</a>";
      // insert into DOM
      $('#distanceToPlaces').html(wstr);
    });
  });
};

function googleMaps(latitude, longitude) {
  $('#googleMapsLink').html('<a target="_blank" href="http://maps.google.com/?q=' + latitude + ',' + longitude + '">Link</a>');
};

// Create container
var container = '';
container += '<div class="remarks">';
container += '<p class=""><span id="enhancementExtension">';
container += '<h3>Enhanced Redfin Data</h3><br/>';
// Google Map link
container += '<b>Google Maps Link: </b>';
container += '<span id="googleMapsLink">Loading ...</span>';
container += '<br/>';
// Distance to places
container += '<b>Distance to places: </b>';
container += '<span id="distanceToPlaces">Loading ...</span>';
container += '<br/>';
// Zillow
container += '<b>Zillow: </b>';
container += '<span id="zillowInfo">Loading ...</span>';
container += '<br/>';
// Greatschools rating
container += '<b>Greatschools Ratings: </b>';
container += '<span><ul id="gsRating"></ul></span>';
container += '</span></p></div>';
// insert container into DOM
$(container).insertBefore($("div .remarks"));

var addressObj = $("span[itemprop='streetAddress']");
var cityStateZipObj = $('span .citystatezip');
if (addressObj.length > 0 && cityStateZipObj.length > 0) {
  var address = $(addressObj[0]).text().trim();
  var cityStateZip = $(cityStateZipObj[0]).text().trim();
  zillow(address, cityStateZip);
}
var latitudeObj = $("meta[itemprop='latitude']");
var longitudeObj = $("meta[itemprop='longitude']");
if (latitudeObj.length > 0 && longitudeObj.length > 0) {
  var latitude = latitudeObj.attr("content");
  var longitude = longitudeObj.attr("content");
  googleMaps(latitude, longitude);
  distanceToPlaces(latitude, longitude);
} else {
  $('#googleMapsLink').html('Could not find house location.');
  $('#distanceToPlaces').html('Could not find house location.');
}
greatSchools();
