#dbus-monitor --session "interface=org.freedesktop.Notifications" | grep --line-buffered "string" > ~/python/pyproject/LPforum/Dbus/temp.txt
# Directly check and Do shitty things at the time when it capture the notification
dbus-monitor --session "interface='org.freedesktop.Notifications'" | grep --line-buffered "string" | python /home/hi-man/python/pyproject/LPforum/Dbus/formatNotification.py
