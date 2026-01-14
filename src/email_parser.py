import base64
MAX_BODY_LENGTH = 45000

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

    payload = message.get("payload", {})
    headers = payload.get("headers", [])

    sender = get_header(headers, "From")
    subject = get_header(headers, "Subject")
    date = get_header(headers, "Date")

    body = ""

    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain":
                data = part["body"].get("data")
                if data:
                    body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                    break
    else:
        data = payload.get("body", {}).get("data")
        if data:
            body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
    if len(body) > MAX_BODY_LENGTH:
        body = body[:MAX_BODY_LENGTH] + " ...[TRUNCATED]"
    return {
        "from": sender,
        "subject": subject,
        "date": date,
        "body": body.strip()
    }
