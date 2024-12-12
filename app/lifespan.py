from fastapi import FastAPI
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from app.logger import logging

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Manage the application lifecycle.
    
    Args:
        app: FastAPI application instance
        
    Yields:
        None
    """
    try:
        # Startup
        logging.info("App start")
        
        yield
        
    except Exception as e:
        logging.error(f"Startup error: {str(e)}")
        raise
        
    finally:
        # Shutdown
        logging.info("App shutdown")
