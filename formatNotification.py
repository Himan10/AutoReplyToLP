#!/bin/env python

# this while loop is for not considering two string fields which you get right after starting a process
# ['string "ShanonPark posted in "HEY! YOU! What are you up to right now! (Part 3)" - Linkin Park / LPU Forums"'] 2 
import sys

def fuckString(data: str) -> str:
    return data[0].split('"', 1)[1].replace('"', '')

wasteLines = 0
while wasteLines <= 1:
    tempInput = sys.stdin.readline()
    wasteLines += 1

del tempInput, wasteLines

# string fields after above two non-considering fields
DataNumber = 0
matchedApp = None
applications = ['notify-send', 'discord', "KDE Connect", "Brave", "Firefox",  "firefox"]
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
                    with open('temp.txt', 'a') as file:
                        file.write(f'{constructData[0]} : {NotifyData[0].split("string")[1]}\n')

                DataNumber += 1
    except KeyboardInterrupt as e:
        break
        #print(e)
