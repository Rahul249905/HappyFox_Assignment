# fetch_emails.py
from email_manager.authenticate import GmailAuthenticator, EMAIL
from email_manager.models import Email, get_session
import datetime
import logging


class EmailFetcher:
    def __init__(self):
        self.service = GmailAuthenticator().authenticate()
        self.session = get_session()

    def fetch_emails(self):
        try:
            print(f"Fetching emails for user: {EMAIL}")
            for label in ['INBOX', 'SPAM']:
                results = self.service.users().messages().list(userId=EMAIL, labelIds=[label]).execute()
                messages = results.get('messages', [])

                for msg in messages:
                    msg_id = msg['id']
                    msg_data = self.service.users().messages().get(userId=EMAIL, id=msg_id).execute()

                    email = Email(
                        id=msg_id,
                        from_address=next(header['value'] for header in msg_data['payload']['headers'] if header['name'] == 'From'),
                        subject=next(header['value'] for header in msg_data['payload']['headers'] if header['name'] == 'Subject'),
                        received_date=datetime.datetime.fromtimestamp(int(msg_data['internalDate']) / 1000)
                    )
                    self.session.merge(email)
                self.session.commit()
        except Exception as e:
            logging.error("Error occurred during fetching emails: %s", e)
            raise e

if __name__ == '__main__':
    EmailFetcher().fetch_emails()