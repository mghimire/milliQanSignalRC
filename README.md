milliQan Signal Reconstruction
==============================

This collection of programs collects the original as well as the stretched and amplified data from a detector module. The goal is to find a way to reconstruct the original data from the stretched and amplified data. Thus far there is a program to record data into .csv files and save their .pdf plots.

System Requirements
-------------------

Python 2.7.15+ and above

Configuration and Running
-------------------------

[readwvfrm.py](../master/readwvfrm.py) is the program that collects data and saves it. It has the setup
parameter runtime, which determines the amount of time in hours that the program will run and collect data. It also has the parameter timeres, which determines the time intervals in which the program will read data.
For instance, if we set runtime at 0.5 (a half hour) and timeres at 2, then we will collect 0.5x60x60/2 = 900 events.

[correlator.py](../master/correlator.py) is the program that analyzes the data and makes plots of it. It currently analyzes the data to isolate single signal events, calculates the area underneath the original and stretched/amplified signals and correlates them. It also analyzes the timing of the original and stretched/amplified signals and correlates them. Currently the program does all of it for you by just running it. I will update it with modes to do specific actions soon.

The next step is to create a master program that combines both [readwvfrm.py](../master/readwvfrm.py) and [correlator.py](../master/correlator.py) to read out and analyze data from scratch.
