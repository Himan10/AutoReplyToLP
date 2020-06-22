"""
Read/Extract Unseen Mails using python
Requirements :
    1. imaplib, 2. OS, 3. base64, 4. email
    5. emai.parser -> BytesParser (for parsing the data
    stored inside a file or variable).
"""

import imaplib  # For reading messages
import logging  # For catching logs
from time import perf_counter
import sys
import os
import email
import re
import email.policy
import socket  # Require for imaplib. connection
from dotenv import load_dotenv  # Require for loading env. variables

logging.basicConfig(
    filename="logs.txt",
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
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)

            # login to user account
            mail.login(self.email_user, self.email_pass)
            return mail
        except imaplib.IMAP4.error as err:
            logging.debug(err)
            return False

    def get_message_id(self, obj):
        """ Method for Return the number of mails
        specified in the mailbox. """

        obj.select(mailbox="INBOX")  # Select a mailbox first
        _, msgnums = obj.search(
            "utf-8", "(Unseen)", "FROM", "linkinpark@discoursemail.com"
        )  # Search message inside mailbox
        print(msgnums)
        if len(msgnums[0]) > 0:
            return msgnums
        return False

    def fetch_raw_message(self, obj, message_id):
        """ Extracting raw message from message id's.
        message_id contains id's of email messages
        by linkinpark@discoursemail. 
        (RFC822) is a msg. format, defines => header, payload
        """

        ids = message_id[0].split()
        data = []
        for id_ in ids:
            typ, response = obj.fetch(id_, "(RFC822)")
            data.append(response[0][1])

        if typ == "OK":
            # raw_text contains two part -> id[0][0] and message body[0][1]
            return data
        else:
            return False

    def extract_contents(self, raw_data: list):
        """ Parse the message :
        header  (recipient information)
        payload (content) """

        # Get Headers
        Headers = {}
        messages_obj = [
            email.message_from_bytes(raw_, policy=email.policy.default)
            for raw_ in raw_data
        ]

        Headers["To"] = messages_obj[0]["To"]
        Headers["Subject"] = messages_obj[0]["Subject"]

        # Get different headers
        Headers["From"] = []
        Headers["Reply-To"] = []
        for msg in messages_obj:
            Headers["From"].append(msg["From"])
            Headers["Reply-To"].append(msg["Reply-To"])

        # Get Payloads
        payload_body = []
        for message in messages_obj:
            payload_body.append(message.get_payload()[0].get_content())

        user_tag = "Himan10"
        regex_pattern = r"(\[/?quote(?:=[^]]*)?\])"
        quote_level = 0
        last_quote_tag = last_quote_message = ""
        found = []

        for payload in payload_body:
            pieces = re.split(regex_pattern, payload)

            for piece in pieces:
                if piece.startswith("[quote") and user_tag in piece:
                    if quote_level == 0:
                        last_quote_tag = last_quote_message = piece
                    quote_level += 1
                else:
                    if quote_level:
                        last_quote_message += piece
                        if piece.startswith("[/quote"):
                            quote_level -= 1
                    else:
                        if user_tag in last_quote_tag or user_tag in piece:
                            print(last_quote_message)
                            found.append(last_quote_message + piece)
                            last_quote_tag = last_quote_message = ""

        # Write the message inside message.txt
        if found is not None:
            with open("/home/hi-man/python/pyproject/LPforum/txtFiles/message.txt", "w") as file:
                file.write(
                    f' To: {Headers["To"]}\n\n \
Subject: {Headers["Subject"]}\n\n \
From: {Headers["From"][0]}\n\n \
Reply-To: {Headers["Reply-To"][0]}\n\n'
                )

                for message in found:
                    file.write(message)

        # Write the senders name inside message2.txt
        with open("/home/hi-man/python/pyproject/LPforum/txtFiles/message2.txt", "w") as file:
            for eachHeader in Headers['From']:
                sender_name = eachHeader.split('via')[0]
                file.write(f'{sender_name}\n')

        return Headers


def main():
    """ Testing LPForum Class """

    start_time = perf_counter()
    # username = input(" Enter Mail(without Domain) : ")
    # password = getpass(" Enter Password : ")
    load_dotenv()
    # Load username/password from environment variables
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    # Calling LPForum
    lpclient = LPForum(username, password)
    imap_obj = lpclient.login()
    msg_id = lpclient.get_message_id(imap_obj)
    if msg_id is False:
         return False
    r_msg = lpclient.fetch_raw_message(imap_obj, msg_id)
    header = lpclient.extract_contents(r_msg)
    imap_obj.close()
    imap_obj.logout()
    print(perf_counter() - start_time)
    return True

main()
