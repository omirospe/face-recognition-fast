from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints.api import face_router, misc_router
from app.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

# origins = [
#     "http://192.168.41.46",
#     "http://localhost",
#     "http://localhost:8080",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(misc_router)
app.include_router(face_router)
