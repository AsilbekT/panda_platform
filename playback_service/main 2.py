from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


VIDEO_DIR = Path("/Users/asilbekturgunboev/Desktop/video_conversion/converted_videos/861137dd-802c-4c29-a6d0-c4507b6ca951")

@app.get("/videos/{video_path:path}")
def read_video(video_path: str):
    file_location = VIDEO_DIR / video_path
    print(f"Trying to access file at: {file_location}")
    if file_location.exists() and file_location.is_file():
        return FileResponse(file_location)
    else:
        return {"error": "File not found"}
