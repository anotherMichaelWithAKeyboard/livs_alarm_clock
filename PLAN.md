# Custom Alarm Clock

This project is a Custom Alarm clock with these base line features.
I have a raspberripi 5, I want to install nixOS onto it and then set it up as this custom alarm clock. I would like to define all the baseline dependencies, and then simulate the environment So i can test it on my current laptop. I would like the layout to be simple and intuitive and I want to be able to ssh into the pi incase I need to update anything.

## Baseline Features:
Display Time:
    - Digital Clock, Maybe even like a flip animation as if its paper.
    - HH:MM (am/pm) 12 hour clock. sync with Melbourne time.
Set an alarm:
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
