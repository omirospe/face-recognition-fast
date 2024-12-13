from app.services import ImageProcessor, VectorSearch
from app.models.requests.detection import FaceDetectionRequest
import requests
from app.helpers import save_file_from_url
from app.logger import logging


async def process_face_embeddings(request: FaceDetectionRequest):
    status = None
    error = None
    try:
        temp_file_path = await save_file_from_url(str(request.photo_url), request.id)

        embeddings = ImageProcessor.get_embeddings(
            path=temp_file_path
        )

        embedding_vector = VectorSearch.save_embeddings(
            embeddings=embeddings,
            id=request.id
        )

        status = 200

    except Exception as e:
        logging.error(
            f"Exception occured while processing face embeddings in background task: {e}")
        error = str(e)
        status = 500

    try:
        response_data = {'status': status, "error": error,
                         "metadata": request.metadata, "id": request.id}

        response = requests.post(
            request.callback_url,
            json=response_data
        )
    except Exception as e:
        logging.error("Exception occured in callback: {e}")
