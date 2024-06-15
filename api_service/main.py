from fastapi import FastAPI
import uvicorn
from app.config import PORT, INTERNAL_MEDIA_SERVICE

if INTERNAL_MEDIA_SERVICE:
    from app.internal_router import router
else:
    from app.external_router import router

# Initialize the FastAPI app
app = FastAPI()
app.include_router(router)


# Function to run the app
def start():
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)


# Main guard for running the application
if __name__ == "__main__":
    start()
