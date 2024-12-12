import chromadb
from functools import lru_cache
from app.settings import get_settings

settings = get_settings()


@lru_cache
def get_chroma_collection():
    chroma_client = None
    collection = None

    if settings.APP_ENVIRONMENT == 'LOCAL':
        chroma_client = chromadb.PersistentClient(path="./chroma_db")

        collection = chroma_client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION
        )

    return collection
