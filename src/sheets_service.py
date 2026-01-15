# sheets_service.py is responsible for authenticating with Google Sheets and persisting structured data into a spreadsheet.
# Google Sheets is NOT a database
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os

from config import SPREADSHEET_ID, SHEET_NAME

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
# This token is allowed to:

# Read

# Write

# Append
# to Google Sheets

TOKEN_PATH = "token.json" # token.json → user session
CREDS_PATH = "credentials/credentials.json" #credentials.json → app identity


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

    service = build("sheets", "v4", credentials=creds) # Create Sheets API client
    # service = “A logged-in Google Sheets session”
    return service


def append_row(service, row_values):
    body = {
        "values": [row_values]
    }
# "values": [
#     ["from", "subject", "date", "body"]
# ] if not nested list then spreadsheet takes each character as a separate row , as api always expected 2D data
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="A1",   
        valueInputOption="RAW",
        body=body
    ).execute()
# SPREADSHEET_ID : Identifies the Google Sheet, range="A1" :  “Use this sheet and append to the next empty row”
# valueInputOption="RAW" : Store data exactly as given