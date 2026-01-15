# gmail_service.py:

# Handles authentication

# Manages tokens

# Talks to Gmail API

# Manages email state


from googleapiclient.discovery import build
# build() creates a client object for Google APIs , without it You cannot talk to Gmail API at all
from google.oauth2.credentials import Credentials
# To load an existing token.json, To reuse authentication without browser every time , if removed You’ll have to log in every run
from google.auth.transport.requests import Request
# Helps refresh an expired access token , if removed : Script will fail after token expires
from google_auth_oauthlib.flow import InstalledAppFlow
# Starts the OAuth browser flow , Handles “login with Google”
import os
# Lets you check if token.json exists

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/spreadsheets"
] 
# This defines WHAT your app is allowed to do. Token must know all permissions in advance If you change scopes Old token becomes invalid , You must delete token.json
# OAuth tokens are scope-bound and immutable
TOKEN_PATH = "token.json"
CREDS_PATH = "credentials/credentials.json"
# credentials.json → identifies the app ; token.json → identifies YOU (user session)

def get_gmail_service():
    # Start with no credentials, We will try to load or create them
    creds = None
    
    # Load saved token if exists
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        # Load OAuth token from file ; Attach defined scopes

    # If no valid credentials, authenticate again
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request()) # Refreshes expired access token automatically , Uses refresh token silently
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
            # Starts OAuth browser flow, Starts OAuth browser flow, Google returns a new token , browser opens because :Browser is trusted environment
        
        # Save token for reuse
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json()) #Saves token locally

    service = build("gmail", "v1", credentials=creds)
    # Creates Gmail API client, Creates Gmail API client, Fully authenticated
    return service

def fetch_unread_emails(service, max_results=5):
    # Give unread emails from Inbox
    # userId="me" → authenticated user
    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"],
        maxResults=max_results
    ).execute()
#  ID returned : Performance , Lightweight , Industry-standard API design
    messages = results.get("messages", [])
    # here .get() : Avoids crash if no emails
    return messages

def mark_as_read(service, message_id):
    # Prevent duplicate processing
    # Gmail label system = state
    # Removing UNREAD = marking as read
    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={
            "removeLabelIds": ["UNREAD"]
        }
    ).execute()
