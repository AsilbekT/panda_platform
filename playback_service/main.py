from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


VIDEO_DIR = Path(
    "/Users/asilbekturgunboev/Desktop/video_conversion/converted_videos/")


@app.get("/videos/{video_id:uuid}/{video_path:path}")
def read_video(video_id: UUID, video_path: str):
    file_location = VIDEO_DIR / str(video_id) / video_path
    print(f"Trying to access file at: {file_location}")
    if file_location.exists() and file_location.is_file():
        return FileResponse(file_location)
    else:
        return {"error": "File not found"}
