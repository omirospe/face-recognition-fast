
from fastapi import APIRouter, Depends
from app.settings import get_settings

router = APIRouter(
    prefix='/misc',
    tags=['misc']
)


@router.get("/health")
def read_root():
    """
    Endpoint to check if app is live

    Returns:
        dict[str, str]: (key, status)

    """
    return {"status": "live"}


@router.get("/config")
def read_root(settings=Depends(get_settings)):
    """
    Endpoint to get env vars

    Returns:
        dict[str, unkown]

    """
    return settings
