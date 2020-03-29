""" Basic usage of smtplib For
Sending mails to LinkinPark Forum (linkinpark@disclosuremail.com)

Method 1:
---------
    1. smtplib modul (smtp or esmtp: Extended smtp)
        -> Establishing connection
        -> Send mail()
        -> Quit()
"""

import smtplib
import ssl # for secure connection
import logging
from dotenv import load_dotenv
import re
from os import getenv

logging.basicConfig(
    filename="logs",
    filemode="a",
    format=" SMTP: %(asctime)s - %(message)s",
    level=logging.DEBUG,
)


class SendToLPForum:
    """ Send mails to LinkinPark Forum """

    def __init__(self, username, password):
        self.user = username
        self.passwd = password
        self.host = "smtp.gmail.com"
        self.port = 465  # Port (ssl=465, tls=587)

    def login(self):
        """ Login to the smtp server """

        # load the system trusted CA certificates
        # enable host checking and certificates validation
        context = ssl.create_default_context()

        server = smtplib.SMTP_SSL(self.host, self.port, context=context)
        try:
            server.login(self.user, self.passwd)
            return server
        except Exception as err:
            logging.debug(err)

    def message_body(self, server, To=None, Message=None):
        """ Message body : payload and headers """

        From = self.user
        if To is None:
            with open('message', 'r') as file:
                To = file.readlines()[6]

            pattern = r'\<(.+)\>'
            To = re.split(pattern, To)[-2]
            To = To.replace('<', '')
        print(To)
        Message = """\
        Subject: Hi Linkin Park
        
        I swear for the last time
        I won't trust myself with you """
        #server.connect(self.host, self.port)
        server.sendmail(From, To, Message)


if __name__ == "__main__":
    load_dotenv()  # load user/password to environment variables
    username = getenv("USERNAME")
    password = getenv("PASSWORD")
    lp = SendToLPForum(username, password)
    server = lp.login()
    lp.message_body(server)
