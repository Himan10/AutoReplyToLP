# REPLY TO LINKIN PARK FORUM

## Task List
- [x] Fetch email message (DONE)
- [x] Send email message (DONE)
- [ ] Creating a random text generator.
- [x] Reading the notification pop-up

## Some details :
  1. Fetch email message -> Whenever someone quoted my message or mentioned me in one of their comment then LP forum sends a mail to notify about those messages. So, this step working is very basic like, it only fetches those messages which come from <linkinpark@discoursemail.com and are UNREAD too.
    You can check the fetched message (stored in fetched_message.txt) how the quote tags and mentions are arranged
  
  2. Send email message -> Here i created a MIME message object (from scratch) which includes :
        
       = main/sub_type =
        1. text/plain
        2. text/html
        3. image/jpg
     
     Now, after combining all these MIME classes(MIMEText, MIMEBase) objects with MIMEMultipart('related') i can easily send mails by using smtp.sendmail(fromAddr, toAddr, msg)
