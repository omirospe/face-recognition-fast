from deepface import DeepFace
import time
from app.logger import logging


class ImageProcessor:
    @staticmethod
    def get_embeddings(path: str = None):
        try:
            detection_time_start = time.perf_counter()

            faces = DeepFace.extract_faces(
                img_path=path,
                detector_backend='retinaface'
            )

            total_detection_time = time.perf_counter() - detection_time_start

            logging.info(
                f"Face extraction proccessed in {total_detection_time}s")

            if len(faces) == 0:
                raise Exception("No face detected")
            elif len(faces) > 1:
                raise Exception("Only one face can be added at a time")

            embeddings_time_start = time.perf_counter()

            embeddings = DeepFace.represent(
                img_path=path,
                detector_backend='retinaface'
            )

            embeddings_time_end = time.perf_counter() - embeddings_time_start

            logging.info(f"Embeddings extracted in {embeddings_time_end}s")

            embedding_vector = embeddings[0]['embedding']

            return embedding_vector
        except Exception as e:
            raise Exception(f"Failed to get embeddings: {str(e)}")
