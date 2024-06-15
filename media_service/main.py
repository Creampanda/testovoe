from fastapi import FastAPI
import uvicorn
from app.config import PORT
from app.internal import router as internal_router
from api_service.app import external_router as external_router

# Initialize the FastAPI app
app = FastAPI()
app.include_router(external_router, prefix="/external")
app.include_router(internal_router, prefix="/internal")


# Function to run the app
def start():
    uvicorn.run("main:app", host="0.0.0.0", port=PORT)


# Main guard for running the application
if __name__ == "__main__":
    start()
