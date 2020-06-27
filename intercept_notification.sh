#if i have to store the summary and data of notification  bubble then add a print() where i've called the timer.
#Output stored in -> AutoReplyToLP/temp.txt
#Directly check and Do shitty things at the time when it capture the notification
dbus-monitor --session "interface='org.freedesktop.Notifications'" | grep --line-buffered "string" | python formatnotification.py
