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
from email.mime.base import MIMEBase # Base = application/octet-stream
from email.mime.multipart import MIMEMultipart  # multipart = mixed
from email.mime.text import MIMEText  # multipart = text/plain
from email.policy import default  # Make a use of RFC and \n For line ending
from email import encoders
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
            raise Exception(f'Login Error - {err}')

    def message_body(self, Message: str):
        """ Message body : payload and headers
        Creating a MIME Msg. object from scratch

        Related
         |__Alternative
                |_ plain/text
                |_ plain/html
         |_Image
        """
        # Related - Send images with messages
        msg_root = MIMEMultipart('related')

        # Add mail headers - From, To, Subject
        msg_root["From"] = self.user
        with open("message.txt", "r") as fp:
            data = fp.readlines()

        msg_root["To"] = ToAddr = data[6].split(":")[1].strip()
        msg_root["Subject"] = data[2].split(":")[1].strip()
        msg_root.preamble = 'This is a Multi part message Plain Text/Image'

        # Alternative - diff. type of same content
        # text/plain
        msgAlt = MIMEMultipart('alternative')

        if Message is None:
            raise Exception("Emtpy Message")
        msgAlt.attach(MIMEText(Message, 'plain', 'utf-8'))

        # text/html
        Message = Message.replace('\n', '<br>')
        html = """\
        <html>
        <head></head>
        <body>
        <p>Hi!<br>
        %s
        </p>
        <img src="cid:image1"><br>
        </body>
        </html> """ % Message

        msgAlt.attach(MIMEText(html, 'html'))
        msg_root.attach(msgAlt)

        # MIMEBase = application/octet-stream -> contain documents
        p = MIMEBase('application', 'octet-stream')

        with open('resources/linkinpark.jpg', 'rb') as pic_file:
            p.set_payload(pic_file.read())

        encoders.encode_base64(p)
        p.add_header('Content-Disposition', 'attachment', filename='linkinpark.png')
        p.add_header('Content-ID', '<image1>')
        msg_root.attach(p)

        # Send mail
        # server.sendmail(self.user, ToAddr, msg_root.as_string())
        return ToAddr, msg_root


if __name__ == "__main__":
    """ testing purpose """

    load_dotenv()   # load username/password from environment file
    username = getenv('USERNAME')
    password = getenv('PASSWORD')

    lp = SendToLPForum(username, password)
    smtp_server = lp.login()

    # Read random generated message from file
    lp_message = None
    with open('message2.txt', 'r') as file:
        lp_message = file.read()

    toAddr, email_message = lp.message_body(lp_message)
    smtp_server.sendmail(username, toAddr, email_message.as_string())
