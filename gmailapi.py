"""Gmail API requests in Python

This script is both a client front-end library and a command-line application
to make requests to Gmail Google API.

Python 2,7 and 3.6 are fully supported and tested.
The script may work on other versions of 3 though not tested.


PREREQUISITES

Gmail API use the OAuth 2.0 protocol for authentication and authorization.

To enable Gmail API, follow the **Enable the Gmail API** wizard that you can
find in Gmail Python Quickstart tutorial
(https://developers.google.com/gmail/api/quickstart/python).

The wizard creates a new Cloud Platform project named **Quickstart**,
enables the Gmail API and returns the `credentials.json` file containing
the OAuth 2.0 credentials (that is **client ID** and **client secret**)
that are known to both Google and you.

Your client configuration can be later managed in
Google Cloud Console (https://console.cloud.google.com/iam-admin/iam)
and Google API Console (https://console.cloud.google.com/apis/dashboard).


OAUTH 2.0 AUTHORIZATION FLOW 

Before this script can access a Gmail API, it must obtain from the Google
Authorization Server an **access token** that grants access to that API.

Such request requires an authentication step where the user logs in with his
Google account and submits his **client ID** and **client secret** credentials.
Then the user is asked whether he is willing to grant the permissions that
this script is requesting.

Since the **access token** has limited lifetime, it always comes together
a **refresh token**; they are stored in the `token.pickle` file for later use.

The **access token** is sent to the Gmail API in an HTTP authorization header.

If this script needs access to a Gmail API beyond the lifetime of its access
token, it will proceed automatically requesting a new one from the Google
Authorization Server by means of the **refresh token** without any further
user interaction.


EXPORTED FUNCTIONS

GetAccessToken
    obtains an access token from Google Authorization Server.

gmSend
    sends an unicode email message (more an optional attachment)
    from the user's account.

This script can also be run as a standalone command-line application to checkout
**OAuth 2.0 tokens** from Google Authorization Server.


CREDITS

How to send email with gmail API and python
https://stackoverflow.com/a/37267330


REFERENCES

Using OAuth 2.0 to Access Google APIs
https://developers.google.com/identity/protocols/OAuth2

Gmail Python API Quickstart to enable the Gmail API
https://developers.google.com/gmail/api/quickstart/python

Send an email message from the user's Gmail account
https://developers.google.com/gmail/api/v1/reference/users/messages/send


LICENSE

Copyright (c) 2019 Corrado Ubezio

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import print_function

import os
import os.path
import pickle
import base64
from sys import version_info

import mimetypes
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


OAUTH_CLIENT_SECRET_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'

# The variable SCOPES controls the set of resources and operations
# that an access token permits.
# If modifying these scopes, delete the TOKEN_FILE.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def GetAccessToken(modeIsInteractive=False):
    """Obtain an access token from the Google Authorization Server

    Returns:
        credentials or None
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            # TOKEN_FILE has been saved as pickled data
            # using protocol number 2 to comply with python 2.
            # Fix loading issue in python 3 with iso-8859-1 encoding (lattin1).
            # See: https://stackoverflow.com/a/41366785
            if version_info.major > 2:
                creds = pickle.load(token, encoding='iso-8859-1')
            else:
                creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if os.path.exists(OAUTH_CLIENT_SECRET_FILE) and modeIsInteractive:
                flow = InstalledAppFlow.from_client_secrets_file(
                                            OAUTH_CLIENT_SECRET_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
        # Save the credentials (if any) for the next run
        if creds:
            with open(TOKEN_FILE, 'wb') as token:
                # write TOKEN_FILE as pickled data
                # use protocol number 2 to comply with python 2.
                # See: https://stackoverflow.com/a/25843743
                #
                # In python 3 load with with iso-8859-1 encoding
                # to fix loading issue.
                # See: https://stackoverflow.com/a/41366785
                pickle.dump(creds, token, protocol=2)
    return creds


def SendMessage(service, user_id, message):
    """Send an email message.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

    Returns:
        Sent Message.

    Raise:
        errors.HttpError
    """
    message = (service.users().messages().send(userId=user_id, body=message)
            .execute())
    return message


def CreateMessage(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text, 'plain', _charset='utf-8')
    message['to'] = to
    message['from'] = sender
    message['subject'] = Header(subject, 'utf-8')
    return {'raw': base64.urlsafe_b64encode(
                    message.as_string().encode('utf-8')).decode("utf-8")}


def CreateMessageWithAttachment(sender, to, subject, message_text, file_path):
    """Create a message for an email with attachment.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.
        file_path: The path to the file to be attached.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = Header(subject, 'utf-8')

    msg = MIMEText(message_text, 'plain', _charset='utf-8')
    message.attach(msg)

    _, filename = os.path.split(file_path)
    content_type, encoding = mimetypes.guess_type(file_path)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(file_path, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(file_path, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(file_path, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(file_path, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()

    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    return {'raw': base64.urlsafe_b64encode(
                    message.as_string().encode('utf-8')).decode("utf-8")}


def gmSend(to, subject, message_text, attachedFilePath=None,
            modeIsInteractive=False):
    """Send an unicode email message from the user's account

    Args:
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.
        attachedFilePath: The path to the file to be attached.
        modeIsInteractive: attended.

    Returns:
        Sent Message.
    """
    if attachedFilePath:
        mail_message = CreateMessageWithAttachment('me', to, subject,
                                            message_text, attachedFilePath)
    else:
        mail_message = CreateMessage('me', to, subject, message_text)
    service = build('gmail', 'v1', credentials=GetAccessToken(modeIsInteractive))
    return SendMessage(service, 'me', mail_message)


if __name__ == '__main__':
    print('Get the OAuth credentials for GMAIL API...')
    credentials = GetAccessToken(modeIsInteractive=True)
    if credentials:
        print('Done')
    else:
        print('Some error occurred')