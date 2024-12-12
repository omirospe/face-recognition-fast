from fastapi import BackgroundTasks, APIRouter, File, UploadFile, HTTPException, status, Depends
from typing import Annotated
from app.models.requests.detection import FaceDetectionRequest, AddFaceToCollection
from app.background_tasks import process_face_embeddings
from app.helpers import save_file
from app.services import ImageProcessor, VectorSearch
from app.models.responses import FaceSearchResponse, FaceDetectResponse
from app.logger import logging

router = APIRouter(
    prefix='/api/face',
    tags=['face']
)


@router.post("/add", status_code=status.HTTP_200_OK)
async def create_person(request: AddFaceToCollection = Depends()):
    """
    Endpoint to add a face

    Args:
        Photo (UploadFile): Photo of the person

    Returns:
        Success (bool): True or False
    """
    try:

        temp_path = await save_file(file=request.file)

        embeddings = ImageProcessor.get_embeddings(
            path=temp_path
        )

        embedding_vector = VectorSearch.save_embeddings(
            embeddings=embeddings,
            id=request.id
        )
    
    except HTTPException as e:
        raise e

    except Exception as e:
        logging.error(f"Exception occured while adding face in collection: {e}")
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


    return True


@router.post("/detect", response_model=FaceDetectResponse, status_code=status.HTTP_202_ACCEPTED)
async def face_detection(
    request: FaceDetectionRequest,
    backround_tasks: BackgroundTasks = None,
):
    """
        Endpoint for face detection requests

        Args:
            request: The face detection request containing necessary data
            background_tasks: FastAPI background tasks handler

        Returns:
            FaceDetectResponse: Response containing the request id and metadata
        """

    backround_tasks.add_task(process_face_embeddings, request)

    return {
        "id": request.id,
        "metadata": request.metadata,
        "status": status.HTTP_202_ACCEPTED,
        "details": "Job added to queue"
    }


@router.post("/search", response_model=FaceSearchResponse, status_code=status.HTTP_200_OK)
async def face_search(photo: Annotated[UploadFile, File()]):
    """
    Perform face detection and vector search

    Args:
        Photo (UploadFile): Photo of the person

    Returns:
        Id (str): The id associated with that photo
    """
    try:

        temp_path = await save_file(file=photo)

        embeddings = ImageProcessor.get_embeddings(
            path=temp_path
        )

        id = VectorSearch.search_embeddings(
            embeddings=embeddings
        )

        if not id:
            raise HTTPException(
                detail="No result found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        return {"id": id}

    except HTTPException as e:
        raise e

    except Exception as e:
        logging.error(f"Exception occured in face search: {e}")
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
