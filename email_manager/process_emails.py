# process_emails.py
import json
from email_manager.authenticate import GmailAuthenticator
from email_manager.models import Email, get_session
import datetime
import logging


class EmailProcessor:
    def __init__(self):
        self.session = get_session()
        self.service = GmailAuthenticator().authenticate()

    @staticmethod
    def condition_matches(email, condition):
        try:
            field_name = condition['field']
            predicate = condition['predicate']
            value = condition['value']
            email_field_value = getattr(email, field_name.lower())
            # Handle the 'received_date' field separately
            if field_name == 'received_date':
                days_threshold = int(value)

                # Get the date part of the email's received date
                email_date = email_field_value.date()

                # Calculate the date threshold (current date - days_threshold)
                email_threshold = (datetime.datetime.now().date() - email_date).days

                # Check the predicate
                if predicate == 'Greater than':
                    return email_threshold > days_threshold
                elif predicate == 'Less than':
                    return email_threshold < days_threshold
                else:
                    return False
            else:
                # Handle other fields as before
                if predicate == 'Contains':
                    return value in email_field_value
                elif predicate == 'Does not Contain':
                    return value not in email_field_value
                elif predicate == 'Equals':
                    return email_field_value == value
                elif predicate == 'Does not equal':
                    return email_field_value != value
                else:
                    return False
        except Exception as e:
            logging.error("Error occurred during condition matching: %s", e)
            raise e

    def apply_actions(self, email, actions):
        try:
            for action in actions:
                if action == 'Mark as read':
                    self.mark_as_read(email.id)
                elif action == 'Mark as unread':
                    self.mark_as_unread(email.id)
                elif action.startswith('Move Message'):
                    self.move_message(email.id, action.split(':')[1])
        except Exception as e:
            logging.error("Error occurred during applying actions: %s", e)
            raise e

    def mark_as_read(self, msg_id):
        try:
            self.service.users().messages().modify(userId='me', id=msg_id,
                                                   body={'removeLabelIds': ['UNREAD']}).execute()
        except Exception as e:
            logging.error("Error occurred during marking as read: %s", e)
            raise e

    def mark_as_unread(self, msg_id):
        print(f"Marking as unread: {msg_id}")
        try:
            self.service.users().messages().modify(userId='me', id=msg_id, body={'addLabelIds': ['UNREAD']}).execute()
        except Exception as e:
            logging.error("Error occurred during marking as unread: %s", e)
            raise e

    def move_message(self, msg_id, label):
        try:
            label_id = self.get_label_id(label)
            if label_id:
                self.service.users().messages().modify(userId='me', id=msg_id,
                                                       body={'addLabelIds': [label_id]}).execute()
        except Exception as e:
            logging.error("Error occurred during moving message: %s", e)
            raise e

    def get_label_id(self, label_name):
        try:
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])
            for label in labels:
                if label['name'] == label_name:
                    return label['id']
            return None
        except Exception as e:
            logging.error("Error occurred during getting label ID: %s", e)
            raise e

    def process_emails(self):
        print("Processing emails")
        try:
            with open('../rules.json') as f:
                rules = json.load(f)
                print(f"rules: {rules}")
            emails = self.session.query(Email).all()
            for email in emails:
                for rule in rules:
                    if rule['predicate'] == 'All' and all(
                            self.condition_matches(email, condition) for condition in rule['conditions']):
                        print(f"Applying actions {rule['actions']} for email: {email.id}")
                        self.apply_actions(email, rule['actions'])
                    elif rule['predicate'] == 'Any' and any(
                            self.condition_matches(email, condition) for condition in rule['conditions']):
                        self.apply_actions(email, rule['actions'])
                        print(f"Applied actions {rule['actions']} for email: {email.id}")
        except Exception as e:
            logging.error("Error occurred during processing emails: %s", e)
            raise e


if __name__ == '__main__':
    EmailProcessor().process_emails()
