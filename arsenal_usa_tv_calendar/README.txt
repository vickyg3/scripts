Never miss an arsenal game!

This script adds every arsenal game automatically to your Google Calendar
along with the TV channel it is going to be telecasted.

Instructions to use:
  * Go to http://drive.google.com
  * Click on Create -> Script
  * Paste the contents of arsenal_usa_calendar.gs into the editor.
  * Save.
  * Run once to create calendar events for the next 4 matches or so.
  * For future matches, you need to set up a trigger:
      - When in Editor, click on: Resources -> Current project's triggers
      - Click "Add new trigger"
      - In the "Run" dropdown, select "fetchScheduleAndUpdateCalendar".
      - Select the remaining drop-downs as follows:
          -> Time-Driven
          -> Week Timer
          -> Every Monday (this can be any day - does not matter)
          -> Midnight to 1am (this can be any time - does not matter)
      - Doing these will make sure newer matche schedules are added to your
        calendar as and when they are available.

Notes:
  * The python script is the one that fetches the list of upcoming games
    and TV channels telecasting those games. This is for reference only,
    you are free to use a hosted version of this script here: 
    (http://linode.foamsnet.com/arsenal/).
  * This script adds events assuming your time zone is PT. To change that,
    you can change the convertToPST function accordingly.
