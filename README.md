# REPLY TO LINKIN PARK FORUM

## Task List
- [x] Fetch email message (DONE)
- [x] Send email message (DONE)
- [ ] Creating a random text generator.
- [x] Reading the notification pop-up

## Some details :
  1. **Fetch email message** : Whenever someone quoted my message or mentioned me in one of their comment then LP forum sends a mail to notify about those messages. So, this step working is very basic like, it only fetches those messages which come from <linkinpark@discoursemail.com and are UNREAD too.
    You can check the fetched message (stored in fetched_message.txt) how the quote tags and mentions are arranged
  
  2. **Send email message** : Here i created a MIME message object (from scratch) which includes :
        
       = main/sub_type =
        1. text/plain
        2. text/html
        3. image/jpg
     
     Now, after combining all these MIME classes(MIMEText, MIMEBase) objects with MIMEMultipart('related') i can easily send mails by using smtp.sendmail(fromAddr, toAddr, msg)

  3. **Capture incoming Notifications** : Here, i used a tool called "dbus-monitor" which helps us to monitor the messages going   through Dbus message bus. This Dbus message bus mentioned here refers to the Session bus which is mainly used for communication   between two applications. 

        In easiest way, think of a Dbus-daemon as a PIPE connected with two or more services or programs (using dbus-library). Now, this tool monitors the message going through this PIPE and print the raw data to stdout. 

     ```
     DISCORD -> send notification
                |
                |
                | -> dbus-monitor
                |
                | 
     DUNST -> Receive notification && Print
     ```

        Once i received the raw data which contains some arrays, strings, signals, methods, sender and destination service. It is     kinda hard to parse this raw data but we can perform regex search here to extract the contents having char "string", because  mostly the   summary, data and application are of type string. Then my next task is to format it. So, we can only get the   required data like   -> header : payload.

        I wrote a python script to do this and save the formatted data into a file or i have done one more thing i.e., Check if the notification came from LPForum then run other py script (fetchmail.py and sendmail.py) otherwise keep scanning the summary of   incoming notifications.  
