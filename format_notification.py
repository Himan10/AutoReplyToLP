#!/bin/env python

import sys
import notify2
import logging
import time
from setup import main

logging.basicConfig(
    filename="logs.txt",
    filemode="w",
    format="%(asctime)s - %(message)s",
    level=logging.INFO,
)


def EditString(data: str) -> str:
    return data[0].split('"', 1)[1].replace('"', "")


def Notify(summary, data, urgency, timeout=800000):
    pop_up = notify2.Notification(summary, data)
    pop_up.set_urgency(urgency)
    pop_up.set_timeout(timeout)
    return pop_up


def countdownTimer(timeMS):
    minute = timeMS // 60000
    second = 59
    pop_up = Notify(f"{minute:02d} : {second:02d}", "Time Left", 1)

    while minute > -1:
        pop_up.update(f"Time Left -> {minute:02d} : {second:02d}")
        time.sleep(1)
        pop_up.show()
        if second == 0:
            minute -= 1
            second = 60
        second -= 1
    pop_up.update("Countdown Completed")
    pop_up.show()

# Ignore the first two string fields
wasteLines = 0
while wasteLines <= 1:
    tempInput = sys.stdin.readline()
    wasteLines += 1

del tempInput, wasteLines


# string fields after above two non-considering fields
DataNumber = 0
matchedApp = None
applications = ["notify-send", "Brave", "Firefox", "firefox"]
constructData = []
notify2.init("AutoReplyToLP")

while True:
    try:
        NotifyData = sys.stdin.readline().strip().split("\n")
        if len(NotifyData[0]) <= 1:
            pass
        else:
            if EditString(NotifyData) in applications:
                matchedApp = EditString(NotifyData)
                DataNumber = 0

            # print(NotifyData, DataNumber)
            if matchedApp in applications:
                if DataNumber == 2:
                    constructData = [EditString(NotifyData)]
                if DataNumber == 3 and "linkin park" in constructData[0].lower():
                    countdownTimer(800000)  # timer
                    main()  # launching main program

                DataNumber += 1
    except KeyboardInterrupt as e:
        break
        logging.error("shutting down coz of interrupt")
