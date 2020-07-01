"""
Method1
-------
    1. imaplib module
        -> Establish a connection
        -> Select the mailbox
        -> Search for unseen mails
        -> fetch their id
        -> get raw data of each id
        -> perform regex to find msg. patterns
        -> save into a file
        -> quit()
"""

import imaplib  # For reading messages
import logging  # For catching logs
import email
import re
import email.policy
import socket  # Require for imaplib. connection


class LPForum:
    def __init__(self, email, password):
        self.email_user = email
        self.email_pass = password
        self.subscribed_email = "linkinpark@discoursemail.com"

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
            logging.error(err)
            return False

    def get_message_id(self, obj):
        """ Method for Return the number of mails
        specified in the mailbox. """

        obj.select(mailbox="INBOX")  # Select a mailbox first
        _, msgnums = obj.search(
            "utf-8", "(Unseen)", "FROM", self.subscribed_email
        )  # Search message inside mailbox
        logging.info(f"Found unseen mail list : {msgnums}")
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
        for objI in messages_obj:
            payload_body.append(objI.get_payload()[0].get_content())


        user_tag = "Himan10"
        # extract [quote=...] or [/quote]
        regex_pattern = r"(\[/?quote(?:=[^]]*)?\])"
        quote_level = 0
        last_quote_tag = last_quote_message = ""
        found = []

        for payload in payload_body:
            pieces = re.split(regex_pattern, payload)  # [0].split('\n')

            if len(pieces) > 1:
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
                                # print(last_quote_message)
                                found.append(last_quote_message + piece)
                                last_quote_tag = last_quote_message = ""
            else:
                # reply without quoting any message
                # checkout which message to save and which not
                found_mentioned_message = list(
                    filter(lambda x: user_tag in x, pieces[0].split("\n"))
                )  # check for Himan10
                if len(found_mentioned_message) == 0:  # if user_tag doesn't found
                    found.extend(pieces)
                else:
                    found.extend(found_mentioned_message)  # if user_tag found

        # Write the message inside message.txt
        if found is not None:
            with open("txtFiles/message.txt", "w") as file:
                file.write(
                    f' To: {Headers["To"]}\n\n \
Subject: {Headers["Subject"]}\n\n \
From: {Headers["From"][0]}\n\n \
Reply-To: {Headers["Reply-To"][0]}\n\n'
                )

                for message in found:
                    file.write(message)

        # Write the headers inside message2.txt
        i = 0
        with open("txtFiles/message2.txt", "w") as file:
            while i < len(Headers["From"]):
                sender_name = Headers["From"][i].split("via")[0]
                sender_address = Headers["Reply-To"][i]
                file.write(f"{sender_name} - {sender_address}\n")
                i += 1
