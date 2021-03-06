""" Basic usage of smtplib For
Sending mails to LinkinPark Forum.
Get the receiver's mail from file(message)

Method 1:
---------
    1. smtplib module (smtp or esmtp: Extended smtp)
        -> Establish a connection
        -> Create a MIME text/image obj. from scratch
        -> Send mail()
        -> Quit()

"""

import ssl  # for creating context - CA certificates
import smtplib
import logging
from email import encoders  # for encoding the data into base64
from email.mime.base import MIMEBase  # Base = application/octet-stream
from email.mime.multipart import MIMEMultipart  # multipart = mixed
from email.mime.text import MIMEText  # multipart = text/plain
from email.policy import default  # Make a use of RFC and \n For line ending


class SendToLPForum:
    """ Send mails to LinkinPark Forum """

    def __init__(self, username, password):
        self.user = username
        self.passwd = password
        self.host = "smtp.gmail.com"
        self.port = 587  # Port (ssl=465, tls=587)

    def login(self):
        """ Login to the smtp server """

        # load the system trusted CA certificates
        # enable host checking and certificates validation
        try:
            context = ssl.create_default_context()

            server = smtplib.SMTP(self.host, self.port)
            server.starttls(context=context)  # secured by tls connection

            server.login(self.user, self.passwd)
            return server
        except Exception as err:
            logging.error(f"SendToLPForum.login : {err}")
            return False

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
        msg_root = MIMEMultipart("related")

        # Add mail headers - From, To, Subject
        msg_root["From"] = self.user
        with open("txtFiles/message.txt", "r") as fp:
            data = fp.readlines()

        msg_root["To"] = ToAddr = data[6].split(":")[1].strip()
        msg_root["Subject"] = data[2].split(":")[1].strip()
        msg_root.preamble = "This is a Multi part message Plain Text/Image"

        # Alternative - diff. type of same content
        # text/plain
        msgAlt = MIMEMultipart("alternative")

        if Message is None:
            raise Exception("Empty Message")
        msgAlt.attach(MIMEText(Message, "plain", "utf-8"))

        # text/html
        Message = Message.replace("\n", "<br>")
        html = (
            """\
        <html>
        <head></head>
        <body>
        <p>Hi!<br>
        %s
        </p>
        <img src="cid:image1"><br>
        </body>
        </html> """
            % Message
        )

        msgAlt.attach(MIMEText(html, "html"))
        msg_root.attach(msgAlt)

        # MIMEBase = application/octet-stream -> contain documents
        p = MIMEBase("application", "octet-stream")

        with open("resources/APlaceForMyHead.jpg", "rb") as pic_file:
            p.set_payload(pic_file.read())

        encoders.encode_base64(p)
        p.add_header(
            "Content-Disposition", "attachment", filename="APlaceForMyHead.png"
        )
        p.add_header("Content-ID", "<image1>")
        msg_root.attach(p)

        # Send mail
        # server.sendmail(self.user, ToAddr, msg_root.as_string())
        return ToAddr, msg_root
