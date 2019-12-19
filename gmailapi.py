"""Gmail API requests in Python

PREREQUISITES
Gmail API use the OAuth 2.0 protocol for authentication and authorization.

To make requests to the Gmail API, you'll need to have registered with Google
as an OAuth application and obtained an OAuth client ID and client secret.

You can manage your project in Google Cloud Console:
https://console.cloud.google.com/iam-admin/iam

You can manage Gmail API OAuth credentials in Google APIs & Services Dashboard:
https://console.cloud.google.com/apis/dashboard


CREDITS
How to send email with gmail API and python
https://stackoverflow.com/a/37267330


REFERENCES
Gmail Python API Quickstart to enable the Gmail API 
https://developers.google.com/gmail/api/quickstart/python

Send an email message from the user's account
https://developers.google.com/gmail/api/v1/reference/users/messages/send
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

# If modifying these scopes, delete the TOKEN_FILE.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def GetCredentials(modeIsInteractive=False):
    """Get the OAuth credentials

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
    """Send an email message from the user's account

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
    service = build('gmail', 'v1', credentials=GetCredentials(modeIsInteractive))
    return SendMessage(service, 'me', mail_message)


if __name__ == '__main__':
    print('Get the OAuth credentials for GMAIL API...')
    credentials = GetCredentials(modeIsInteractive=True)
    if credentials:
        print('Done')
    else:
        print('Some error occurred')