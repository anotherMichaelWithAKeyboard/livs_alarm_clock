# Custom Alarm Clock

This project is a Custom Alarm clock with these base line features.
I have a raspberripi 5, I want to install nixOS onto it and then set it up as this custom alarm clock. I would like to define all the baseline dependencies, and then simulate the environment So i can test it on my current laptop. I would like the layout to be simple and intuitive and I want to be able to ssh into the pi incase I need to update anything.

## Baseline Features:
Display Time:
    - Digital Clock, Maybe even like a flip animation as if its paper.
    - HH:MM (am/pm) 12 hour clock. sync with Melbourne time.
Set an alarm:
LOGIC:
1. Select Destination (save all previous destinations an order them in most often selected)
    1.1 Select Arrival time
2. Select Starting Point (Home, Mika's, ect)
3. according to google maps, show how long it would take to travel if they chose to
    3.1 Drive
    3.2 Public Transport
    3.3 Cycle
4. Depending on which mode of transport they picked:
    4.1 IF Public Transport show the closest: 
        4.1.2 Show three trams According to the PTV api that will get you to your destination before *arrival time*
        4.1.3 Show three trains according to the PTV api that will get you to your destination before *arrival time*
        4.1.4 Show five routes (combination of any public transport. i.e train, tram, train + tram, bus ect.
5. After selecting route you now have a *Departure from Home* time.
6. The User will then select Fluffer time frame
    6.1 List of activities to do before leaving for work. The user can add new activities which has a Name and a length (time, mins)
        6.1.1 Wash hair in full (40mins)
        6.1.2 Have breakfast (10mins) ect
7. The user will have the Alarm time that has subtracted the total fluffer time from the Departure from Home time.
8. Display the difference in time between the current time and the alarm time set.
9. The user can then add estimated snoozes n of length (y in mins), which will push the alarm back the total length of all snoozes. And update the estimated sleep time (length of time between the first alarm and current time)

    - This feature will allow the user to scroll through a menu to set a time. 
    - Displays "Hours of Sleep"- length in time HH:MM from current time to set alarm.
    - OPTION: What Alarm sound, from a list.
        - Custom alarm sounds: Dir with custome mp3 or other audio formats.

Forecast: (Interactive menu that allows the user to check the forecast for the week)
    - Ideally connected to BOM and or willyWeather API
    - Allows the user to check the forecast for the week
    - Easy to see the majority of the weather notes for the coming day
    - Has "can ride" to and from work
        - to work: 6am-8am, from work: 4pm-6pm
        - "can ride" = true if no rain, not too cold, good cycling conditions.

Seasonal Themes:
Photo frame mode:
Weekend/holiday detection:
    - no accidental 6am wakeups on saturday
Commute Planner:
   - Train Schedule
        - Next train time for your commute
        - Next tram time for your commute

Settings:
    - Dim Mode Scheduler
        - Schedule time to Dim the screen
        - Schedule Sleep Duration (how long can it be idle before Dim Mode)
        - Auto Dim after set-alarm: True or False



## TODO
Purchase remaining components
Design a 3D model Case for the monitor and raspberry pi.



### Remaining Components to purchase
Touch Screen
Print the 3D model case
