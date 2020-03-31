""" Basic usage of smtplib For
Sending mails to LinkinPark Forum.
Get the receiver's mail from file(message)

Method 1:
---------
    1. smtplib module (smtp or esmtp: Extended smtp)
        -> Establishing connection
        -> Create a MIME text/image obj. from scratch
        -> Send mail()
        -> Quit()

"""

import smtplib
import ssl  # for secure connection
import logging
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart  # multipart = mixed
from email.mime.text import MIMEText  # multipart = text/plain
from email.policy import default  # Make a use of RFC and \n For line ending
import os

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

    def message_body(self, server, Message=None, ToAddr=None):
        """ Message body : payload and headers
        Creating a Msg. object from scratch """

        data = []
        msg = MIMEMultipart()

        # Add headers
        msg["From"] = self.user
        with open("message", "r") as fp:
            data = fp.readlines()

        if ToAddr is None:
            msg["To"] = ToAddr = data[6].split(":")[1].strip()
        else:
            msg["To"] = ToAddr
        msg["Subject"] = data[4].split(":")[1].strip()

        # Attach a payload to the MIMEText object. Type -> text
        if Message is None:
            raise Exception("Emtpy Message")

        msg.attach(MIMEText(Message, "plain"))
        Message = msg.as_string()
        server.sendmail(self.user, ToAddr, Message)


def main():
    load_dotenv()  # load user/password to environment variables
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    lp = SendToLPForum(username, password)
    server = lp.login()

    # Get message content from File
    lp_message = input(' Enter Message(leave blank to read from file): ')
    if len(lp_message) < 1:
        path = str(input(' Path : '))
        if os.path.exists(path):
            with open(path, 'r') as fp:
                lp_message = fp.read()

    msg = lp.message_body(server, lp_message)
