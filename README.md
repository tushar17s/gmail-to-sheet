 Gmail to Google Sheets Automation (Python)

^ Project Overview :

This project is a Python-based backend automation that securely connects to Gmail using OAuth 2.0, fetches unread emails, extracts important details, and logs them into a Google Sheet. After successfully storing the data, the emails are marked as read to prevent duplicate entries on future runs.

^ Features :

Secure OAuth 2.0 authentication (no password handling)
Fetches unread emails from Gmail Inbox
Extracts sender, subject, date, and message content
Stores structured data in Google Sheets
Prevents duplicate processing by marking emails as read
Modular and clean backend architecture

^ How It Works (Flow) :

Authenticate user using OAuth 2.0
Fetch unread emails from Gmail Inbox
Parse email headers and decode plain text body
Append extracted data as rows in Google Sheets
Mark processed emails as read

^ Project Structure :

gmail_to_sheet/
│
├── src/
│   ├── main.py               # Orchestrates the complete flow
│   ├── gmail_service.py      # Gmail API & OAuth handling
│   ├── email_parser.py       # Parses MIME email content
│   ├── sheets_service.py     # Google Sheets API integration
│
├── credentials/              # OAuth credentials (ignored)
├── config.py                 # Sheet configuration
├── requirements.txt          # Project dependencies
├── .gitignore                # Security exclusions
└── README.md

^ Security Considerations :

OAuth credentials (credentials.json) and tokens (token.json) are not committed to the repository.
The application follows the principle of least privilege using scoped permissions.
Gmail access is granted only with explicit user consent.

^ Technologies Used :

Python 3
Google Gmail API
Google Sheets API
OAuth 2.0

^ Installation & Setup :

pip install -r requirements.txt


Note: Users must create their own Google Cloud project and OAuth credentials to run this application.

^ Output :

Each unread email is logged as a new row in Google Sheets

Columns include:
From
Subject
Date
Content

^ Learning Outcome :

This project demonstrates real-world backend concepts such as OAuth authentication, API integration, data parsing, persistence, and idempotent processing.