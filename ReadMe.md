# Habit Tracker by s31368

## Description
This is habit tracker allows to use multiple users. User should Register the system (or login after Registration) to track or enter their Habits. Habits are splitted into two groups "Good" and "Bad" habits.
User can choose one of this groups before adding Habit to the system to track their activity, frequency and the date. Application uses GUI build with 'tkinter', to keep data using JSON serialization, and using decorators, generators and exception handling. 

## Project Structure
* main.py - Contains the GUI and application execution logic.
* tracker.py - Contains the core object-oriented data models (Habit, TrackerManager) and file serialization logic.
* utils.py - Contains helper functions, custom exceptions, and regex validation.
* habits.json - Automatically generated database file storing user data.

## Run Instructions
1. Ensure you have installed PyCharm.
2. Only standart libraries used in this project (tkinter, json, re, os)
3. Run the application by executing:
    main.py


