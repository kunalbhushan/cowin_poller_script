# COWIN Poller Script
Python script to poll COWIN and notify in case slots are available based on inputs

Currently only supports MacOS (Darwin) for platform notifications

List of districts with district IDs : https://drive.google.com/file/d/1007DlyZesRhXQY6NEr3wAJEvt0XINdhh/view?usp=sharing

Dependencies:
Python 3

Usage:
~~~
	python3 cowin_poller_script.py
~~~

	OR


~~~
	python3 cowin_poller_script.py "<comma separated List of districts>" <Threshold> <min age> <free/paid> <subsequent weeks to check for> <polling interval>
~~~
