from fastapi import FastAPI
from app.routers import audio_separation

app = FastAPI(
    title="My Audio Separation Service",
    description="FastAPI service that separates audio into stems.",
    version="1.0.0"
)

# Include the audio separation router
app.include_router(audio_separation.router, prefix="/audio", tags=["Audio Separation"])

# Optionally, you can have a simple health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}
