import tempfile
import requests
import os
import mimetypes
from fastapi import UploadFile
import shutil
from app.models.errors import FileHandlingError


async def save_file_from_url(url: str, id: str) -> str:
    """
    Downloads and saves a file while detecting its type.

    Args:
        url (str): The URL to download from
        id (str): Identifier for the saved file

    Returns:
        tuple[str, str]: (file_path, mime_type)
    """
    response = requests.get(url)
    response.raise_for_status()

    temp_dir = tempfile.mkdtemp()

    url_mime_type, _ = mimetypes.guess_type(url)

    final_mime_type = url_mime_type or 'application/octet-stream'

    extension = mimetypes.guess_extension(final_mime_type) or '.webp'

    file_path = os.path.join(temp_dir, f"{id}{extension}")

    with open(file_path, 'wb') as f:
        f.write(response.content)

        return file_path


async def save_file(file: UploadFile):
    """
    Saves file in temp directory

    Args:
        file (UploadFile): The file to save

    Returns:
        file_path (str): Temporary directory

    """
    try:
        name = file.filename
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, name)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file_path

    except Exception as e:
        FileHandlingError(f"Unexpected error occured while saving file {e}")
