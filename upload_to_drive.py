import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 1. Tells Google what kind of access we want
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate():
    creds = None

    # Checks if user has already logged in before
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If not, ask them to log in with Google
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # This will open a browser to log in with your Google account
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)  # Make sure this file is in the same folder
            creds = flow.run_local_server(port=0)

        # Save login for future runs
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def upload_file_to_drive(file_path):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_name = os.path.basename(file_path)

    # Create file metadata and media content
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, resumable=True)

    # Upload the file
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print(f"✅ File uploaded successfully! File ID: {file.get('id')}")

# 🔥 TEST: Upload this file (change the path to your file)
upload_file_to_drive('sample.txt')
