from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import io
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = 'client_secret.json'
TOKEN_FILE = 'token.json'

def authenticate():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds

def download_file_from_drive(file_id, output_name):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(output_name, 'wb')
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Downloading: {int(status.progress() * 100)}%")

    print(f"✅ File restored as {output_name}!")

if __name__ == '__main__':
    # Replace with your uploaded file's actual ID from Google Drive
    file_id = '18zqYAq1U0LOF0dw66PEwiA__S5avv-0I'
    output_file = 'restored_sample.txt'
    download_file_from_drive(file_id, output_file)
