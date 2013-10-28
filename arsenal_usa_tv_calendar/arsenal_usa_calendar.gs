function monthToIndex(month) {
  var months = {
    "january": 0,
    "february": 1,
    "march": 2,
    "april": 3,
    "may": 4,
    "june": 5,
    "july": 6,
    "august": 7,
    "september": 8,
    "october": 9,
    "november": 10,
    "december": 11
  };
  return months[month.toLowerCase()];
}

function convertToPST(timestamp) {
  var hour = parseInt(timestamp.split(":")[0]);
  if (hour < 3) {
    return hour + 9;
  }
  if (hour > 3) {
    return hour - 3;
  }
}

function getCorrectYear(month) {
  var today = new Date();
  if (today.getMonth() <= month) {
    return today.getFullYear();
  }
  return today.getFullYear() + 1;
}

function fetchScheduleAndUpdateCalendar() {
  var data = UrlFetchApp.fetch("http://linode.foamsnet.com/arsenal/");
  var json = JSON.parse(data);
  for(var i = 0; i < json.length; ++i) {
    var game = json[i];
    var game_exists = false;
    // Check if an event exists
    var game_date = new Date();
    var month = monthToIndex(game[0].split(" ")[0]);
    game_date.setMonth(month);
    game_date.setDate(game[0].split(" ")[1]);
    game_date.setFullYear(getCorrectYear(month));
    var events = CalendarApp.getDefaultCalendar().getEventsForDay(game_date);
    for (var j = 0; j < events.length; ++j) {
      if (events[j].getTitle().toLowerCase().indexOf("arsenal") > -1) {
        game_exists = true;
        break;
      }
    }
    Logger.log(game_exists);
    // Create event if it does not exist
    if (!game_exists) {
      game_date.setHours(convertToPST(game[1]));
      game_date.setMinutes(game[1].split(":")[1].substring(0,2));
      var game_end_time = new Date(game_date);
      game_end_time.setHours(convertToPST(game[1]) + 2);
      var home_or_away = (game[2].indexOf("@") > -1) ? "Away" : "Home";
      var title = "Arsenal vs " + game[3] + " (" + home_or_away + " - " + game[4] + ") on " + game[5];
      CalendarApp.getDefaultCalendar().createEvent(title, game_date, game_end_time);
    }
  }
}
