from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os

from config import SPREADSHEET_ID, SHEET_NAME

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
TOKEN_PATH = "token.json"
CREDS_PATH = "credentials/credentials.json"


def get_sheets_service():
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    service = build("sheets", "v4", credentials=creds)
    return service


def append_row(service, row_values):
    body = {
        "values": [row_values]
    }

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="A1",   
        valueInputOption="RAW",
        body=body
    ).execute()
