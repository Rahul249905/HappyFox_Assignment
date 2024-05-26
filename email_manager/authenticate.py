# authenticate.py
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import logging

SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.labels'
]
EMAIL = "rahul.career24@gmail.com"  # Specify the email address to authenticate

class GmailAuthenticator:
    def __init__(self):
        self.creds = None

    def authenticate(self):
        try:
            if os.path.exists('../token.json'):
                print("Reading token")
                self.creds = Credentials.from_authorized_user_file('../token.json', SCOPES)
            if not self.creds or not self.creds.valid:
                print("Authenticating")
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file('../credentials.json', SCOPES)
                    self.creds = flow.run_local_server(port=0, prompt='consent', login_hint=EMAIL)
                with open('../token.json', 'w') as token:
                    print("Writing token")
                    token.write(self.creds.to_json())
            return build('gmail', 'v1', credentials=self.creds)
        except Exception as e:
            logging.error("Error occurred during authentication: %s", e)
            raise e
