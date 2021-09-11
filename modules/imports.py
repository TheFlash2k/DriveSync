from webbrowser import get
from google.oauth2.utils import handle_error_response
import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from .mime_types import mime_types

### -> From : https://learndataanalysis.org/google-drive-api-in-python-getting-started-lesson-1/
def Create_Service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    cred = None
    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)
    
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        return service
    except Exception as e:
        print(f"[-] Unable to initialize the Google Drive API. Error Occurred! Details: {e}")
        return None


def get_mime_type(file_name):
    # # To get the file type, we firstly reverse the file and then get the position of the first . and read the data till that and reverse the read data:
    # # I Tried using magic but it didn't work:
    # return magic.from_file(file_name, mime=True)
    file_type = file_name[::-1]
    file_type = file_type[:file_type.find('.') + 1][::-1].lower()
    try:
        return mime_types[file_type]
    except KeyError:
        print(f"[-] Type {file_type} doesn't exist in our known mime_types database. Kindly add to the database...")
        return None