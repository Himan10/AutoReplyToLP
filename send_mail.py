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
import ssl  # for secure connection
import logging
from dotenv import load_dotenv
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart # multipart = mixed
from email.mime.text import MIMEText # multipart = text/plain
from email.policy import default  # Make a use of RFC and \n For line ending
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

    def message_body(self, server, Message=None):
        """ Message body : payload and headers
        Creating a Msg. object from scratch """

        data = []
        msg = MIMEMultipart()

        # Add headers
        msg['From'] = self.user
        with open('message', 'r') as fp:
            data = fp.readlines()

        msg['To'] = To = data[6].split(':')[1].strip()
        msg['Subject'] = data[4].split(':')[1].strip()

        # Attach a payload to the MIME msg object
        if Message is None:
            raise Exception('Emtpy Message')

        msg.attach(MIMEText(Message, 'plain'))
        Message = msg.as_string()
        server.sendmail(self.user, To, Message)


if __name__ == "__main__":
    load_dotenv()  # load user/password to environment variables
    username = getenv("USERNAME")
    password = getenv("PASSWORD")
    lp = SendToLPForum(username, password)
    server = lp.login()

    # Get message content from File
    lp_message = '''
    Hey Man, how are you? Doing good?
    Yeah, TBH i tried to make a hybrid theory soldier once but it's
    too damn hard man.. i mean, whoever did this deserves a huge respect.
    and let's see coz my after doing this Dealpool/Taskmaster pencil drawing,
    i'll try to draw The Hunting Party poster. Cya man.. Take care and
    good wishes to all of the LP family members '''
    msg = lp.message_body(server, lp_message)
