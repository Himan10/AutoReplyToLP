# REPLY TO LINKIN PARK FORUM

## Task List
- [x] Fetch email message (DONE)
- [x] Send email message (DONE)
- [ ] Creating a random text generator.
- [x] Reading the notification pop-up (DONE)

## Some details :
  1. **Fetch email message** : This task is basically related to fetch incoming emails which are not yet seen, by LPForum. 
  
      So, whenever someone replies on LPForum and if he/she mentioned me or quoted my message or just re-reply on my message (without mentioned or quoting) then LPForum will notify me by sending me an email. Now, once i receive the email, the python script will fetch the raw contents of an email and extract the messages which match the following pattern : 

     ```
     1. Quoted Message + Second person reply
     [quote=Himan10...]
     Second Person reply
     
     2 IF no quoted Message of Himan10 but there are other quoted message, 
     -> Search for the particular reply in which @Himan10 is mentioned
     
     2.1 No quoted Message in the entire message,
     -> Split the lines, Check in which line @Himan10 is mentioned
     
     2.2 No quoted Message and no one mentioned @Himan10 (This is the case of direct reply)
     -> Save the entire message
     ```

      Now this process of fetching the emails from a specific sender is done by using the library -> imaplib (in python). What it does is, it connects you(the    client) to the IMAP server and allows you to perform several functions like selecting the mailbox, search for a particular message from a specific sender and many more. You can read more about imaplib from the given link provided below. 
 
  
  2. **Send email message** : Here i created a MIME message object (from scratch) which includes :
        
       = main/sub_type =
        1. text/plain
        2. text/html
        3. image/jpg
     
     Now, after combining all these MIME classes(MIMEText, MIMEBase) objects with MIMEMultipart('related') i can easily send mails by using smtp.sendmail(fromAddr, toAddr, msg)

  3. **Capture incoming Notifications** : Here, i used a tool called "dbus-monitor" which helps us to monitor the messages going   through Dbus message bus. This Dbus message bus mentioned here refers to the Session bus which is mainly used for communication   between two applications. 

        In easiest way, think of a Dbus-daemon as a PIPE connected with two or more services or programs (using dbus-library). Now, this tool monitors the message going through this PIPE and print the raw data to stdout. 

     ```
     LPforum -> send notification
                |
                |
                | -> dbus-monitor
                |
                | 
     DUNST -> Receive notification && Print
     ```

        Once i received the raw data which contains some arrays, strings, signals, methods, sender and destination service. It is     kinda hard to parse this raw data but we can perform regex search here to extract the contents having char "string", because  mostly the   summary, data and application are of type string. Then my next task is to format it. So, we can only get the   required data like   -> header : payload.

        I wrote a python script to do this and save the formatted data into a file or i have done one more thing i.e., Check if the notification came from LPForum then run other py script (fetchmail.py and sendmail.py) otherwise keep scanning the summary of   incoming notifications.  
