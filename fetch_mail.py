"""
Read/Extract Mails using python
Requirements :
    1. imaplib, 2. OS, 3. base64, 4. email
    5. emai.parser -> BytesParser (for parsing the data
    stored inside a file or variable).
"""

import imaplib  # For reading messages
import logging  # For catching logs

# import base64
import os
import email
import re
import socket  # Require for imaplib. connection
from dotenv import load_dotenv  # Require for loading env. variables
from getpass import getpass  # For username/password

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

    def get_message_id(self, obj):
        """ Method for Return the number of mails
        specified in the mailbox. """

        obj.select(mailbox="INBOX")  # Select a mailbox first
        typ, msgnums = obj.search(
            "utf-8", "FROM", "linkinpark@discoursemail.com"
        )  # Search message inside mailbox
        if typ == "OK":
            return msgnums
        return 0

    def fetch_raw_message(self, obj, message_id):
        """ Extracting raw message from message id's.
        message_id contains id's of email messages
        by linkinpark@discoursemail """

        id_ = message_id[0].split()
        latest_email = id_[-1]  # Last id is the latest
        typ, data = obj.fetch(latest_email, "(RFC822)")

        # Convert the fetched binary obj. into a string
        raw_str = data[0][1]  # .decode('utf-8')

        if typ == "OK":
            # raw_text contains two part -> id[0][0] and message body[0][1]
            return raw_str
        else:
            return False

    def extract_contents(self, user_tag, raw_string):
        """ Parse the message :
        header  (recipient information)
        payload (content) """

        # Get Headers
        headers = {}
        message = email.message_from_bytes(raw_string)
        print(" Is Multipart : ", message.is_multipart())
        headers["To"] = message["To"]
        headers["From"] = message["From"]
        headers["Subject"] = message["Subject"]
        headers["Reply-To"] = message["Reply-To"]

        # Get Payloads
        payload_body = None
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                payload_body = message.get_payload()[0]

        payload = payload_body.get_payload()

        # Extract Useful message from a payload
        pattern = r"(\[[\W\w]{9}user_tag.+?(?=\]).+?(?=\[\W\w{5}\]))(.*?(?=\[[\w]{5}))"
        pattern = pattern.replace("user_tag", user_tag)
        payload = repr(payload)
        found = re.search(pattern, payload)

        if found.group(1) and found.group(2) is not None:
            # Write message/headers into a file
            with open("message", "w") as f:
                for key, value in headers.items():
                    f.write(f"{key} : {value}\n\n")
                f.write(f" Quote: {found.group(1)} \n \nMessage: {found.group(2)}")
        else:
            print(False)


def main():
    """ Testing LPForum Class """
    # username = input(" Enter Mail(without Domain) : ")
    # password = getpass(" Enter Password : ")
    load_dotenv()
    # Load username/password from environment variables
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    user_tag = str(input(" Enter your user tag : "))

    # Calling LPForum
    lpclient = LPForum(username, password)
    imap_obj = lpclient.login()
    msg_id = lpclient.get_message_id(imap_obj)
    r_msg = lpclient.fetch_raw_message(imap_obj, msg_id)
    lpclient.extract_contents(user_tag, r_msg)
    imap_obj.close()
    imap_obj.logout()
