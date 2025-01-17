from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import os
import uuid
import shutil
import zipfile

from app.services.separation_service import separate_audio

router = APIRouter()

@router.post("/separate")
async def separate_audio_endpoint(file: UploadFile = File(...)):
    if file.content_type not in ["audio/wav"]:
        raise HTTPException(status_code=400, detail="Uploaded file must be a WAV audio file")

    # Create a temporary directory for input & output
    temp_dir = f"temp_{uuid.uuid4()}"
    os.makedirs(temp_dir, exist_ok=True)

    # Save the uploaded file
    input_filepath = os.path.join(temp_dir, file.filename)
    with open(input_filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Call our service layer to do the separation
    stems_paths = separate_audio(input_filepath, temp_dir)

    # Zip the stems before returning
    zip_filename = os.path.join(temp_dir, "separated_stems.zip")
    with zipfile.ZipFile(zip_filename, "w") as zf:
        for stem_name, stem_path in stems_paths.items():
            zf.write(stem_path, arcname=os.path.basename(stem_path))

    return FileResponse(
        zip_filename,
        media_type='application/x-zip-compressed',
        filename="separated_stems.zip"
    )
#