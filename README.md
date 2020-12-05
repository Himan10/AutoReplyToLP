# REPLY TO LINKIN PARK FORUM

## Work Flow
![Work Flow](/resources/LPworkflow.png)

## Task List
- [x] Fetch email message (DONE)
- [x] Send email message (DONE)
- [x] Creating a random text message (10%)
- [x] Reading the notification pop-up (DONE)

## Some details :
  1. **Fetch email message** : This task is basically related to "fetch incoming emails of LPForum" which are left unseen by the user.
  
      So, whenever someone replies on LPForum and if he/she mentioned me or quoted my message or just re-reply on my message (without mentioned or quoting) then LPForum will notify me by sending me an email. Now once i receive it, the python script will fetch the raw contents of an email and extract those messages which match the following pattern : 

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
      
  2. **Random Text message** : In this task, I've some read file operations which is used to randomly select the sentences from a file and then combine them into one. Also, The structure of a text message would look like :  
  
       = text message =
        * Starting Greets
        * Someone's Quote
        * Tags/Mention
        * Image
     
     There's no particular order for a message to only get construct in one way. I mean, messages from 1st to 3rd will get shuffled every time you call the function inside the file (random_message.py) but an image will always be inserted at the end. Also, i want this task to generate a sensible and accurate message based on  second user reply but for now I'll keep it as a basic prototype and will make changes in future.
  
  3. **Send email message** : Here i created a MIME message object (from scratch) which includes :
        
       = main/sub_type =
        * text/plain - contains random text message.
        * text/html - html version of above message.
        * image/jpg
     
     Now, after combining all these MIME classes(MIMEText, MIMEBase) objects with MIMEMultipart('related') i can easily send mails by using smtp.sendmail(fromAddr, toAddr, msg)

  4. **Capture incoming Notifications** : Here, i used a tool called "dbus-monitor" which helps us to monitor the messages going   through Dbus message bus. This Dbus message bus mentioned here refers to the Session bus which is mainly used for communication   between two applications. 

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

        I've written a python script to do this heck if the notification came from LPForum then run other py script (fetchmail.py and sendmail.py) otherwise keep scanning the summary of   incoming notifications. Also, you can save the summary and data of a notification in a file just to keep track of them.  

## DEMO
 ### Video - [watch the video](https://drive.google.com/file/d/110RPnh1a7zCIK9Ur0WPLrHpaYUhMjOY_/view?usp=sharing)

## Further readings 
1. [Regex](https://www.regular-expressions.info/quickstart.html)
2. [Email Working](https://www.namecheap.com/hosting/how-does-email-work/)
2. [python3 imaplib module](https://docs.python.org/3/library/imaplib.html)
3. [python3 smtplib module](https://docs.python.org/3/library/smtplib.html)
4. [Linux Desktop with Dbus](https://www.linuxjournal.com/article/10455)
5. [python3 email.mime module](https://docs.python.org/3/library/email.mime.html)

#### I'm still working on this project and will continue to work in the future too. Any type of feedback is welcomed and appreciated. 

**[UPDATE]** The forum on which this project is based was closed by Linkin Park. Later they came up with a new forum because of their Hybrid Theory 20th Anniversary. So, I'll do some changes according to the new forum structure.
 
Thankyou. 
