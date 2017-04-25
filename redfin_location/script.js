var latitudeObj = $("meta[itemprop='latitude']");
var longitudeObj = $("meta[itemprop='longitude']");
if (latitudeObj.length > 0 && longitudeObj.length > 0) {
  var latitude = latitudeObj.attr("content");
  var longitude = longitudeObj.attr("content");
  $.getJSON("//maps.googleapis.com/maps/api/directions/json?origin=" + latitude + "," + longitude + "&destination=3003+Bunker+Hill+Lane+Santa+Clara+CA", function(data1) {
    $.getJSON("//maps.googleapis.com/maps/api/directions/json?origin=" + latitude + "," + longitude + "&destination=1600+Amphitheatre+Parkway+Mountain+View+CA", function(data2) {
      var cisco = data1.routes[0].legs[0].distance.text;
      var google = data2.routes[0].legs[0].distance.text;
      var wstr = "";
      wstr += "<div class=\"info-block left-divider\">";
      wstr += "<div class=\"statsLabel\">";
      wstr += "<a href=\"https://maps.google.com?saddr=" + latitude + "," + longitude + "&daddr=3003+Bunker+Hill+Lane+Santa+Clara+CA\" target=\"_blank\">";
      wstr += "Cisco: " + cisco;
      wstr += "</a>";
      wstr += "<br/><br/>";
      wstr += "<a href=\"https://maps.google.com?saddr=" + latitude + "," + longitude + "&daddr=1600+Amphitheatre+Parkway+Mountain+View+CA\" target=\"_blank\">";
      wstr += "Google: " + google;
      wstr += "</a>";
      wstr += "</div>";
      wstr += "</div>";
      //$("div[data-rf-test-id='abp-homeinfo-homemainstats']").append(wstr);
      $(wstr).insertAfter($("div .shareButtonWrapper"));
    });
  });
}