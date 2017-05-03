// Create container
var container = '';
container += '<div class="remarks">';
container += '<p class=""><span id="enhancementExtension">';
container += '<h3>Additional Information</h3><br/>';
// Google Map link
container += '<b>Google Maps Link: </b>';
container += '<span id="googleMapsLink">Loading ...</span>';
container += '<br/>';
// Distance to places
container += '<b>Distance to places: </b>';
container += '<span id="distanceToPlaces">Loading ...</span>';
container += '<br/>';
// Greatschools rating
container += '<b>Greatschools Ratings: </b>';
container += '<span><ul id="gsRating"></ul></span>';
container += '</span></p></div>';
// insert container into DOM
$(container).insertBefore($("div .remarks"));

// Generate data
var latitudeObj = $("meta[itemprop='latitude']");
var longitudeObj = $("meta[itemprop='longitude']");
if (latitudeObj.length > 0 && longitudeObj.length > 0) {
  var latitude = latitudeObj.attr("content");
  var longitude = longitudeObj.attr("content");
  // Google maps link
  $('#googleMapsLink').html('<a target="_blank" href="http://maps.google.com/?q=' + latitude + ',' + longitude + '">Link</a>');
  // Distance to places
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
} else {
  $('#googleMapsLink').html('Could not find house location.');
  $('#distanceToPlaces').html('Could not find house location.');
}

// Find up-to-date greatschools rating
$('.schools-content table .school-name').each(function (index, node) {
  $('#gsRating').append('<li id="gsRating' + index + '">Loading ...</li>');
  $.get('//www.redfin.com' + $(node).attr('href'), function(data) {
    var gsUrl = $(data).find('a:contains("School Overview")').attr('href');
    gsUrl = gsUrl.replace('https:', '');
    gsUrl = gsUrl.replace('http:', '');
    console.log(gsUrl);
    $.get(gsUrl, function(schoolData) {
      var schoolDom = $(schoolData);
      // rating
      var ratingElements = schoolDom.find(".school-info .rs-gs-rating").contents().filter(function() { return this.nodeType === 3; });
      var rating = ratingElements[0].textContent.trim();
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
      var wstr = '';
      wstr += '<a href="http://' + gsUrl + '" target="_blank">' + $(node).html() + '</a>';
      wstr += "<ul>";
      wstr += '<li>Rating: ' + rating + '</li>';
      if (ethnicity != '') {
        wstr += '<li>Ethnicity: ' + ethnicity + '</li>';
      }
      if (lowIncome != '') {
        wstr += '<li>Students from low-income families: ' + lowIncome + '</li>'
      }
      wstr += '</ul>';
      $('#gsRating' + index).html(wstr);
    });
  });
});
