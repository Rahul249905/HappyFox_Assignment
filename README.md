# Email Fetcher and Processor

This project is designed to fetch emails from a Gmail account and process them based on specific rules. It uses the Gmail API to interact with the email account and SQLAlchemy for database interactions.

## Prerequisites

- Python 3.6 or higher
- Gmail API credentials
- MySQL database

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Rahul249905/HappyFox_Assignment.git
    cd HappyFox_Assignment
    ```

2. **Set up a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

2. **Install `pipenv`**:
    Set up the environment and install dependencies:
    ```bash
    pipenv install
    pipenv shell
    pip install pipenv
    ```

4. **Set up Gmail API credentials**:
    - Go to the [Google Developer Console](https://console.developers.google.com/).
    - Create a new project.
    - Enable the Gmail API for the project.
    - Create OAuth 2.0 credentials and download the `credentials.json` file.
    - Save the `credentials.json` file in the project root directory.

5. **Run MySQL in Local**:
    - Setup MySQL database in local and make sure it is running .
    - Create a database named `emaildb` in MySQL.
    - create a user having full access to this db.

## Running the Project

1. **Fetch emails**:
    ```bash
    python fetch_emails.py
    ```
    This script authenticates with Gmail, fetches emails from the INBOX and SPAM folders, and stores them in the database.

2. **Process emails**:
    ```bash
    python process_emails.py
    ```
    This script processes the fetched emails based on rules defined in `rules.json` and applies specified actions.

## Code Explanation

### fetch_emails.py
- **EmailFetcher class**: Authenticates with Gmail and fetches emails from specified labels (INBOX, SPAM).
- **fetch_emails method**: Retrieves emails and stores them in the database.

### authenticate.py
- **GmailAuthenticator class**: Handles authentication with Gmail API using OAuth 2.0.
- **authenticate method**: Reads or generates OAuth tokens and returns a Gmail service object.

### process_emails.py
- **EmailProcessor class**: Loads rules from `rules.json` and processes emails from the database.
- **condition_matches method**: Checks if an email meets a specific condition.
- **apply_actions method**: Applies actions to emails based on matched rules.
- **mark_as_read, mark_as_unread, move_message methods**: Perform specific actions on emails using Gmail API.

### models.py
- **Email class**: SQLAlchemy model representing an email.
- **get_session function**: Creates and returns a database session.

## Rules Configuration

- The rules for processing emails are defined in `rules.json`.
- Each rule consists of conditions and actions.
- Conditions specify criteria like `from_address`, `subject`, and `received_date`.
- Actions specify what to do with emails that match the conditions, like marking them as read or moving them to a specific label.

## Logging

- Errors and other information are logged using Python's `logging` module.
- Logs can be found in the console output or configured to be written to a file.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License.

