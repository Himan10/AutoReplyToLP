#!/bin/env python

# this while loop is for not considering two string fields which you get right after starting a process
import sys

def fuckString(data: str) -> str:
    return data[0].split(' ')[1].strip('"') 

wasteLines = 0
while wasteLines <= 1:
    tempInput = sys.stdin.readline()
    wasteLines += 1

del tempInput, wasteLines

# string fields after above two non-considering fields
DataNumber = 0
matchedApp = None
applications = ['notify-send', 'discord']
constructData = []
try:
    while True:
        NotifyData = sys.stdin.readline().strip().split('\n')
        if fuckString(NotifyData) in applications:
            matchedApp = fuckString(NotifyData)
            DataNumber = 0
        
        print(NotifyData, DataNumber)
        if matchedApp in applications:
            if DataNumber == 2:
                constructData = [fuckString(NotifyData)]
            if DataNumber == 3:
                with open('temp.txt', 'w') as file:
                    file.write(f'{constructData[0]} : {NotifyData[0].split("string")[1]}\n')

            DataNumber += 1
except KeyboardInterrupt as e:
    print(e)
