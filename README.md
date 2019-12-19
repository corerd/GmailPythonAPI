# Gmail API requests in Python

`gmailapi.py` is a client front-end library to make requests
to the Gmail Google API.

Using this script as a standalone application, you can generate and authorize
**OAuth 2.0 tokens** from Google Authorization Server.

Gmail API relies upon [OAuth 2.0 protocol](http://tools.ietf.org/html/rfc6749)
for authentication and authorization.

The description of the OAuth 2.0 authorization scenarios that Google supports
can be found in [Using OAuth 2.0 to Access Google APIs](
https://developers.google.com/identity/protocols/OAuth2).


## Making requests to the Gmail API

First, you'll need a Google account with Gmail enabled.

To enable Gmail API you have to create a new **Cloud Platform project** in
[Google Cloud Console](https://console.cloud.google.com/iam-admin/iam)
and enable the Gmail API in
[Google API Console](https://console.cloud.google.com/apis/dashboard).

Then `gmailapi.py` script requests an OAuth 2.0 **access token** from the
Google Authorization Server, extracts a token from the response,
and sends the token to the Gmail API that you want to access.

Here are the steps required to allow the script to send Gmail API requests.


### 1. Obtain OAuth 2.0 credentials from the Google Cloud Console

This step is required only once to turn on the Gmail API obtaining
the OAuth 2.0 credentials (that is **client ID** and **client secret**)
that are known to both Google and you.

Google has speeded up this process providing the **Enable the Gmail API** wizard
that you can find in the [Gmail Python Quickstart](
https://developers.google.com/gmail/api/quickstart/python) tutorial.

The wizard creates a new Cloud Platform project named **Quickstart** with
**quickstart-random-number** as ID, and automatically enables the Gmail API.

The project can be later renamed in your
[Google Cloud Console](https://console.cloud.google.com/iam-admin/iam),
while the project ID can no more be changed.

After the wizard has finished, you'll find the `credentials.json` file
saving your client configuration including **client ID** and **client secret**.

The client configuration of your project can be also downloaded any time from
the [Google API Console](https://console.cloud.google.com/apis/dashboard).


### 2. Install the Google Client Library

```
pip install -r requirements.txt
```


### 3. Obtain OAuth tokens from the Google Authorization Server

Before the `gmailapi.py` script performs its first Gmail API request,
it must obtain a set of **OAuth 2.0 tokens**, that is:
- an **access token** that grants limited lifetime access to the API;
- a **refresh token** allowing the script to obtain new access tokens.

The script opens your default browser and connects Google Authorization Server
to authenticate itself by means of the **OAuth 2.0 credentials** previously
saved in the `credentials.json` file.

After logging in with your Google account, you are asked to grant the requesting
permissions. If you'll accept, the script will store the received
**OAuth 2.0 tokens** (not username and password) in the `token.pickle` file.

Subsequent runs of the `gmailapi.py` script won't need the browser and can send
API request straight by means the **access token** that has limited lifetime.
If the script needs access to a Gmail API beyond the lifetime of its access token,
it will proceed automatically requesting a new one from the Google Authorization
Server by means of the **refresh token**.


# Security advice

The `gmailapi.py` script doesn't save any username and password,
but it reads and writes the `credentials.json` and `token.pickle`files
that contain your personal Google account data.

Please, keep these files in a secure private location and
don't put their content in any public sharing service such as GitHub.


# Credits

[How to send email with gmail API and python](
https://stackoverflow.com/a/37267330) at Stack Overflow


# References

[Using OAuth 2.0 to Access Google APIs](
https://developers.google.com/identity/protocols/OAuth2)

[Gmail Python API Quickstart to enable the Gmail API](
https://developers.google.com/gmail/api/quickstart/python)

[Send an email message from the user's Gmail account](
https://developers.google.com/gmail/api/v1/reference/users/messages/send)


# Apache License, Version 2.0

Copyright (c) 2019 Corrado Ubezio

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at [Apache Software Foundation](
http://www.apache.org/licenses/LICENSE-2.0).

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
