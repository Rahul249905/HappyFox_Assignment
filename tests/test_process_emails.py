import unittest
from unittest.mock import MagicMock, patch
from email_manager.process_emails import EmailProcessor
from email_manager.models import Email
import json

class TestEmailProcessor(unittest.TestCase):
    @patch('email_manager.process_emails.GmailAuthenticator')
    @patch('email_manager.process_emails.get_session')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='[{"predicate": "All", "conditions": [{"field": "from_address", "predicate": "Equals", "value": "test@example.com"}], "actions": ["Mark as read"]}]')
    def test_process_emails_success(self, mock_open, mock_get_session, mock_GmailAuthenticator):
        mock_service = MagicMock()
        mock_GmailAuthenticator().authenticate.return_value = mock_service

        mock_email = MagicMock(spec=Email)
        mock_email.id = '1'
        mock_email.from_address = 'test@example.com'
        mock_email.subject = 'Test Subject'
        mock_email.received_date = '2022-01-01T00:00:00'

        mock_session = MagicMock()
        mock_session.query().all.return_value = [mock_email]
        mock_get_session.return_value = mock_session

        email_processor = EmailProcessor()
        email_processor.process_emails()

        # Validate that the correct actions were taken
        mock_service.users().messages().modify.assert_called_once_with(
            userId='me', id='1', body={'removeLabelIds': ['UNREAD']}
        )

    @patch('email_manager.process_emails.GmailAuthenticator')
    @patch('email_manager.process_emails.get_session')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_process_emails_exception_handling(self, mock_open, mock_get_session, mock_GmailAuthenticator):
        mock_open.side_effect = Exception('Error loading rules')
        email_processor = EmailProcessor()
        with self.assertRaises(Exception):
            email_processor.process_emails()
        # Add assertions here to validate the error handling/logging

if __name__ == '__main__':
    unittest.main()
