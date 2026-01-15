# OAuth Authentication

# Script checks if a valid token already exists

# If yes → reuse it

# If not → user logs in via browser

# Token is saved for future runs

# Fetch Unread Emails

# Gmail API is queried for unread inbox emails

# Only message IDs are fetched (optimized design)

# Parse Email Content

# Full email is fetched using message ID

# Headers (From, Subject, Date) are extracted

# Body is decoded from Base64

# Only text/plain content is used

# Large content is safely truncated

# Persist Data

# Clean email data is appended to Google Sheets

# Each email becomes one row

# Update State

# Email is marked as read

# Prevents duplicate entries on future runs


from src.gmail_service import get_gmail_service, fetch_unread_emails, mark_as_read
from src.email_parser import extract_email_details
from src.sheets_service import get_sheets_service, append_row

gmail_service = get_gmail_service()
sheets_service = get_sheets_service()

messages = fetch_unread_emails(gmail_service)

for msg in messages:
    email = extract_email_details(gmail_service, msg["id"])

    row = [
        email["from"],
        email["subject"],
        email["date"],
        email["body"]
    ]

    append_row(sheets_service, row)

    # Mark email as read AFTER successful append
    mark_as_read(gmail_service, msg["id"])

print("Emails appended and marked as read")
