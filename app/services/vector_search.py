from app.managed_services import get_chroma_collection
from typing import Optional
import time
from app.logger import logging


class VectorSearch:
    match_threshold = 0.6

    @staticmethod
    def save_embeddings(embeddings, id: str) -> bool:
        """
            Stores embedings with id 
        """
        chroma_collection = get_chroma_collection()

        chroma_collection.add(
            embeddings=embeddings,
            ids=[id]
        )

        return True
    

    @staticmethod
    def search_embeddings(embeddings) -> Optional[str]:
        try:
            start_timer = time.perf_counter()

            chroma_collection = get_chroma_collection()

            similar_faces = chroma_collection.query(
                query_embeddings=[embeddings],
                n_results=1,
            )

            results_length = len(similar_faces['ids'][0])

            if results_length == 0:
                return None

            distance = similar_faces['distances'][0][0]

            if distance > VectorSearch.match_threshold:
                return None

            id = similar_faces['ids'][0][0]

            end_timer = time.perf_counter()-start_timer
            
            logging.info(
                f"Search embeddings for id {id}: {end_timer}")
            return id

        except Exception as e:
            raise Exception(f"Failed to search with embeddings: {str(e)}")
