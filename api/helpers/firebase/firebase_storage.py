from tempfile import SpooledTemporaryFile
from typing import List
from fastapi import UploadFile
from fastapi import status
from fastapi.responses import JSONResponse
import firebase_admin
from firebase_admin import storage, credentials

cred = credentials.Certificate(r"api\helpers\firebase\market-project-key.json")

firebase_admin.initialize_app(cred, {
    "storageBucket": "market-project-1f3f4.appspot.com"
})

bucket = storage.bucket()

async def upload_files_to_firebase(incoming_file: UploadFile, folder: str):
    try:
        if incoming_file is not None:
            file_path = f"{folder}/{incoming_file.filename}"
            
            blob = bucket.blob(file_path)
            incoming_file.file.seek(0)
            blob.upload_from_file(incoming_file.file,
             content_type=incoming_file.content_type,
             predefined_acl="publicRead")

            url = blob.public_url
            return url
        else:
            return None

    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content=str(e))
    

async def upload_lists_to_firebase(incoming_files: List[UploadFile],folder: str):
    try:
        if isinstance(incoming_files,list):
            files_urls = []
            for incoming_file in incoming_files:

                content = await incoming_file.read()
                
                temp_file = SpooledTemporaryFile()
                temp_file.write(content)
                temp_file.seek(0)  
                
                #blob = bucket.blob(incoming_file.filename)
                #blob.upload_from_file(temp_file, content_type=incoming_file.content_type, predefined_acl="publicRead")
                #url = blob.public_url

                incoming_file.file = temp_file

                url = await upload_files_to_firebase(incoming_file,folder)

                files_urls.append(url)
                
                temp_file.close()

            return files_urls
        else:
            return None
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))