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

    # ✅ Mark email as read AFTER successful append
    mark_as_read(gmail_service, msg["id"])

print("Emails appended and marked as read")
