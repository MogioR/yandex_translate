import httplib2
from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload
from oauth2client.service_account import ServiceAccountCredentials


class GoogleDriveApi:
    def __init__(self, token):
        self.auth_service = None
        self.authorization(token)

    # Authorisation in serves google
    # Accept: authorisation token
    def authorization(self, token):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            token,
            ['https://www.googleapis.com/auth/drive.file'])
        http_auth = credentials.authorize(httplib2.Http())
        self.auth_service = discovery.build('drive', 'v3', http=http_auth)

    def upload_file(self, file: str, folder: str, file_out_name: str = None):
        if file_out_name is None:
            file_out_name = file

        file_metadata = {
            'name': file_out_name,
            'parents': [folder],
            'mimeType': 'text/json'
        }

        media = MediaFileUpload(file, mimetype='text/json')
        self.auth_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
