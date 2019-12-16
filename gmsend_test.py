# -*- coding: utf-8 -*-
"""CLI script to send an email message from the user's GMAIL account
"""

from __future__ import print_function

import traceback
import logging

from sys import argv
from random import randint
from datetime import datetime

from apiclient import errors
from gmail import gmSend

TEST_MESSAGE = """Send an email using GMAIL API from Python
with some unicode charaters in the subject
and in the text body à è é ì ò ù
adding random content {}
"""


def gmsend_test(to, attachment=None):
    """Send the email TEST_MESSAGE from the user's account

    Args:
        to: Email address of the receiver.
        attachment: The path to the file to be attached.
    """
    subject = 'gmsend !?test¿¡ at {}.'.format(datetime.now())
    text = TEST_MESSAGE.format(randint(100, 999))
    if attachment:
        text = text + 'with attachment'
    try:
        message = gmSend(to, subject, text, attachment, modeIsInteractive=True)
    except errors.HttpError as e:
        logging.error('HttpError occurred: %s' % e)
    except Exception:
        logging.error(traceback.format_exc())
    else:
        print('SUCCEEDED: Message Sent Id: %s' % message['id'])


def main():
    print('Send a test email message from the user GMAIL account')
    if len(argv) < 2 or len(argv) > 3:
        print('USAGE; gmsend_test <dest-address> [attachment]')
        return
    dest_address = argv[1]
    if len(argv) == 3:
        attached = argv[2]
    else:
        attached = None
    gmsend_test(dest_address, attached)


if __name__ == '__main__':
    main()