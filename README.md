# COWIN Poller Script
Python script to poll COWIN and notify in case slots are available based on inputs

Currently only supports MacOS (Darwin) for platform notifications

List of districts with district IDs : https://drive.google.com/file/d/1007DlyZesRhXQY6NEr3wAJEvt0XINdhh/view?usp=sharing

Dependencies:
Python 3

Usage:
~~~
python3 cowin_poller_script.py

Example : 
python3 cowin_poller_script.py
Enter list of districts ids (comma separated) : 651, 650, 141, 145, 140, 146, 147, 143, 148, 149, 144, 150, 142
Enter minimum number of slots (per centre in district) available to notify : 3
Enter minimum age (18/45) : 18
Enter Fee Type (Free/Paid) : Paid
Enter number of weeks to check after the current one : 1
Enter Polling interval in seconds : 100

~~~

	OR

~~~
python3 cowin_poller_script.py "<comma separated List of districts>" <Threshold> <min age> <free/paid> <subsequent weeks to check for> <polling interval>

Example:
python3 cowin_poller_script.py "651, 650, 141, 145, 140, 146, 147, 143, 148, 149, 144, 150, 142" 3 18 Paid 1 100

~~~
