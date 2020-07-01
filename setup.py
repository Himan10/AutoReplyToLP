#!/bin/env python

import os
import logging
import notify2
from time import perf_counter
from dotenv import load_dotenv
from fetch_mail import LPForum
from send_mail import SendToLPForum
from random_message import GenerateMessage


def Notify(summary, data, urgency, timeout=12000):
    """ Create a notification pop-up
    to aware the user about task status
    """
    pop_up = notify2.Notification(summary, data)
    pop_up.set_urgency(urgency)
    pop_up.set_timeout(timeout)
    pop_up.show()


def main():

    notify2.init("AutoReplyToLP")  # initialize the Dbus connection
    start_time = perf_counter()  # Calculate time for fetch_mail
    
    load_dotenv()
    try:
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
    except:
        logging.error('.env file not loaded')

    # Calling -> fetch_mail.LPForum
    LPclient = LPForum(username, password)
    imap_obj = LPclient.login()
    msg_id = LPclient.get_message_id(imap_obj)
    if msg_id is False:
        Notify("python fetch_mail.py", "Nothing Found", 2)
        quit()
    r_msg = LPclient.fetch_raw_message(imap_obj, msg_id)
    LPclient.extract_contents(r_msg)

    imap_obj.close()
    imap_obj.logout()
    Notify("python fetch_mail.py", "DONE", 0)

    # Create a Random Message
    lp_message = GenerateMessage()

    # Calling -> send_mail.SendToLPForum
    lp = SendToLPForum(username, password)
    smtp_server = lp.login()
    if smtp_server is False:
        Notify("python send_mail.py", "Login Error", 2)
        quit()

    toAddr, email_message = lp.message_body(lp_message)
    smtp_server.sendmail(username, toAddr, email_message.as_string())
    Notify("python send_mail.py", "DONE", 0)

    logging.info(f"Time Taken -> {perf_counter() - start_time}")
