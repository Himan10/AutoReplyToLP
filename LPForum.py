"""
Read/Extract Mails using python
Requirements :
    1. imaplib, 2. OS, 3. base64, 4. email
"""

import imaplib
import logging
#import base64
#import email
import socket
from getpass import getpass

logging.basicConfig(
    filename="logs",
    filemode="a",
    format=" %(asctime)s -> %(messsage)s ",
    level=logging.DEBUG,
)


class LPForum:
    def __init__(self, email, password):
        """ Constructor """
        self.email_user = email
        self.email_pass = password

    def __str__(self):
        return str(self.email_user)

    def login(self):
        """ Creating a secure connection over SSL socket
        Return an imap4 object to "mail" variable """

        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)

        # login to user account
        try:
            mail.login(self.email_user, self.email_pass)
            return mail
        except imaplib.IMAP4.error as err:
            logging.debug(err)
            return False

    def get_message_body(self, obj):
        """ Method for Return the number of mails
        specified in the mailbox """

        obj.select(mailbox="INBOX")  # Select a mailbox first
        typ, msgnums = obj.search(
            "utf-8", "FROM", "linkinpark@discoursemail.com"
        )  # Search message from mailbox
        if typ == 'OK':
            return msgnums
        return 0

    def fetch_message(self, obj, message_id):
        """ Extracting message from Raw messages.
        message_num contains id of email messages
        by linkinpark@discoursemail """

        id_ = message_id[0].split()
        latest_email = id_[-1]  # Last id is the latest
        typ, data = obj.fetch(latest_email, '(RFC822)')

        # Convert the fetched binary obj. into a string
        raw_text = data[0][1].decode('utf-8')

        if typ == 'OK':
            # Write the raw text into a file
            # data contains two part -> id[0][0] and message body[0][1]
            with open('message', 'w') as f:
                f.write(raw_text)
        else:
            return False

def main():
    """ Testing LPForum Class """
    username = input(" Enter Mail(without Domain) : ")
    password = getpass(" Enter Password : ")
    org = "@gmail.com"
    username = username + org

    # Calling LPForum
    lpclient = LPForum(username, password)
    imap_obj = lpclient.login()
    msg_id = lpclient.get_message_body(imap_obj)
    lpclient.fetch_message(imap_obj, msg_id)
    imap_obj.close()
    imap_obj.logout()
