# Why this file matters:

# Emails are not plain strings

# Gmail stores them in MIME format

# Body is Base64 encoded

# Gmail gives:

# Headers array

# Payload tree

# Base64 encoded content

# So we need a translator.

import base64
# Imports Python’s Base64 decoding module , base64 , why ? : Safe transmission over HTTP
MAX_BODY_LENGTH = 45000
#  gmail stores headers as list of dictionaries
def get_header(headers, name):
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]
    return ""


def extract_email_details(service, message_id):
    message = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    payload = message.get("payload", {}) # payload is The entire email structure containing headers, body
    headers = payload.get("headers", [])

    sender = get_header(headers, "From")
    subject = get_header(headers, "Subject")
    date = get_header(headers, "Date")

    body = ""

    if "parts" in payload: # as email has single or multiple parts
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain":
                data = part["body"].get("data")
                if data:
                    body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                    # Decode it into bytes
                    #  errors="ignore": Some emails contain invalid characters so prevent crash
                    break
    else:
        # Don’t have parts
        # Body is directly in payload
        data = payload.get("body", {}).get("data")
        if data:
            body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
    if len(body) > MAX_BODY_LENGTH:
        body = body[:MAX_BODY_LENGTH] + " ...[TRUNCATED]"
        # Handles large emails safely
    return {
        "from": sender,
        "subject": subject,
        "date": date,
        "body": body.strip()
    }
