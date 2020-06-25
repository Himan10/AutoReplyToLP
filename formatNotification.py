#!/bin/env python

# this while loop is for not considering two string fields which you get right after starting a process
# Test string ->['string "ShanonPark posted in "HEY! YOU! What are you up to right now! (Part 3)" - Linkin Park / LPU Forums"'] 2 

import sys
import time
import notify2
from fetch_mail import main

def Notify():
    notify2.init('LPforum')
    pop_up = notify2.Notification('Python Script initialized', 'Starts under 11 minutes')    
    pop_up.set_timeout(12000)
    pop_up.set_urgency(0)
    pop_up.show()


def fuckString(data: str) -> str:
    return data[0].split('"', 1)[1].replace('"', '')

wasteLines = 0
while wasteLines <= 1:
    tempInput = sys.stdin.readline()
    wasteLines += 1

del tempInput, wasteLines

# string fields after above two non-considering fields
DataNumber = 0
FromLP = False
matchedApp = None
applications = ['notify-send', "Brave", "Firefox",  "firefox"]
constructData = []

while True:
    try:
        NotifyData = sys.stdin.readline().strip().split('\n')
        if len(NotifyData[0]) <= 1:
            pass
        else:
            if fuckString(NotifyData) in applications:
                matchedApp = fuckString(NotifyData)
                DataNumber = 0
            
            #print(NotifyData, DataNumber)
            if matchedApp in applications:
                if DataNumber == 2:
                    constructData = [fuckString(NotifyData)]
                if DataNumber == 3 and 'linkin park' in constructData[0].lower():
                    Notify() # notify the user about upcoming task
                    time.sleep(10)
                    main() # Run the script fetch_mail 

                DataNumber += 1
    except KeyboardInterrupt as e:
        break
        #print(e)
