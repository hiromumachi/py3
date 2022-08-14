import logging
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='./log/log.txt')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


##アップロードメソッド


def uploadFileToGoogleDrive(fileName, local_path, mime_type,credentials):
    
    '''
    filename:   アップロード先でのファイル名
    local_path: アップロードするファイルのローカルのパス
    '''
    service = build("drive", "v3", credentials=credentials, cache_discovery=True)
    # "parents": ["****"]この部分はGoogle Driveに作成したフォルダのURLの後ろ側の文字列に置き換えてください。
    file_metadata = {"name": fileName, "mimeType": mime_type, "parents": ["1ErP8eN1Soc3RZlIpbHOsc-8EWwKbs-NZ"]}
    media = MediaFileUpload(local_path, mimetype=mime_type, chunksize=1024*1024,resumable=True )
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()
