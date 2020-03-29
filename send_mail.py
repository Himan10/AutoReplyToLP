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
import logging
from dotenv import load_dotenv
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

    def test(self):
        """ test the connection, if possible or not """
        return smtplib.helo("hello smtp server")

    def login(self):
        """ Login to the smtp server """

        obj = smtplib.SMTP_SSL(self.host, self.port)
        try:
            result = obj.login(self.user, self.passwd)
            return result
        except Exception as err:
            logging.debug(err)
            return False

    def message_body(self, To=None, Message=None):
        """ Message body : payload and headers """

        From = self.user
        if To is None:
            To = "linkinpark@disclosuremail"
        Message = None


if __name__ == "__main__":
    load_dotenv()  # load user/password to environment variables
    username = getenv("USERNAME")
    password = getenv("PASSWORD")
    lp = SendToLPForum(username, password)
    print(lp.login())
