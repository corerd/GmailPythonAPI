Send email via Gmail authenticating with OAuth2
===============================================

Google provides the `oauth2.py` script and library to implement and debug OAuth2.
The script can be used as a standalone utility for generating and authorizing
OAuth tokens, and for generating OAuth2 authentication strings from OAuth tokens.

`oauth2.py` can be downloaded from the Google source [repository](
https://raw.githubusercontent.com/google/gmail-oauth2-tools/master/python/oauth2.py).
At the time of writing, the script works on Python 2.4 or greater,
but is not Python 3 compatible.

Instructions for using `oauth2.py` is available on the Google
[wiki](https://github.com/google/gmail-oauth2-tools/wiki/OAuth2DotPyRunThrough).


Generate OAuth2 Credentials
---------------------------
There are 2 types of Credentials:

- The **Client ID** and **Client secret** obtained registering the application
  on [Google Developers Console](https://console.developers.google.com).

- An authorizing **OAuth tokens** generated from the above Client ID and secret.


### Registering An Application

1. Open the [Google Developers Console](https://console.developers.google.com).

2. From the project drop-down, choose **Create a new project**, enter
   a name for the project, and optionally, edit the provided project ID.
   Click **Create**.

3. On the Credentials page, select **Create credentials**,
   then select **OAuth client ID**.

4. You may be prompted to set a product name on the Consent screen;
   if so, click **Configure consent screen**, supply the requested information,
   and click **Save** to return to the Credentials screen.

5. Select **Other** for the **Application type**, and enter any additional
   information required.

6. Click **Create**.

7. Click **OK** to dismiss the resulting pop-up showing the **client ID**
   and **client secret**.

8. Click the **Download JSON** button to the right of the client ID.

9. Move this file to your working directory and rename it `client_secret.json`.
