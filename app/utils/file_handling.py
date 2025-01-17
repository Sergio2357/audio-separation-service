import os
import shutil
from fastapi import UploadFile

def save_upload_file(upload_file: UploadFile, destination: str) -> None:
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
