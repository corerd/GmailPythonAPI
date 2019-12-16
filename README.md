# Gmail API requests in Python

Gmail API use the [OAuth 2.0 protocol](http://tools.ietf.org/html/rfc6749)
for authentication and authorization.

The description of the OAuth 2.0 authorization scenarios that Google supports
can be found in [Using OAuth 2.0 to Access Google APIs](
https://developers.google.com/identity/protocols/OAuth2).


## Making requests to the Gmail API

First, you'll need to have registered your application with
[Google Cloud Console](https://console.cloud.google.com/iam-admin/iam)
as an OAuth project and obtained Gmail API credentials from the
[Google API Console](https://console.cloud.google.com/apis/dashboard).

Then your client application requests an **access token** from the
Google Authorization Server, extracts a token from the response,
and sends the token to the Gmail API that you want to access.


### Registering An Application

This step is required only once to obtain OAuth 2.0 credentials such as
a **client ID** and **client secret** that are known to both Google
and your application.

Google has speeded up the process to **enable the Gmail API** providing a wizard
that can be found in the [Gmail Python Quickstart](
https://developers.google.com/gmail/api/quickstart/python) tutorial.

The wizard registers for you an OAuth project named **Quickstart** with
**quickstart-random-number** as ID.

The project name can be later changed in your
[Google Cloud Console](https://console.cloud.google.com/iam-admin/iam),
the project ID not.

After the wizard has finished, you'll find the **credentials.json** file
storing your application **client ID** and **client secret**.

Then these Gmail API credentials can be also downloaded any time from your
[Google API Console](https://console.cloud.google.com/apis/dashboard).


### Obtain an access token from the Google Authorization Server

Open a command-line window and enter:
```
python gmail.py
```
to obtain and store in the **token.pickle** file the access token
that grants access to the Gmail API.


## Install the Google Client Library

```
pip install -r requirements.txt
```
