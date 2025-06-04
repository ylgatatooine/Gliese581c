# Import necessary FastAPI and utility modules
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import uuid, os, re
import logging

from youtuber import YouTuber

# Initialize FastAPI app and static/template directories
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Home page route: renders the main HTML page
@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint to fetch YouTube transcript and return as a downloadable file
@app.post("/get-transcript/")
async def get_transcript(request: Request):

    logger.info("/get-transcript/ endpoint called")
    data = await request.json()

    logger.info(f"Request data: {data}")
    url = data.get("url")

    # Validate the YouTube URL
    if not url or "youtube.com" not in url:
        logger.error("Invalid YouTube URL received.")
        raise HTTPException(status_code=400, detail="Invalid YouTube URL.")

    video_id = extract_video_id(url)

    logger.info(f"Extracted video_id: {video_id}")
    try:
        # Fetch transcript using YouTubeTranscriptApi
        youtuber = YouTuber()
        transcript =  youtuber.get_transcript_by_id(video_id)
        logger.info(f"Transcript fetched, length: {len(transcript)} entries")

        # Save transcript to a temporary file
        filename = f"./tmp/{uuid.uuid4()}.txt"
        with open(filename, "w") as f:
            f.write(transcript)
        logger.info(f"Transcript written to file: {filename}")

        # Return the file as a download
        return FileResponse(path=filename, filename="transcript.txt", media_type='text/plain')
        
    except Exception as e:
        logger.error(f"Error fetching transcript: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Helper function to extract the video ID from a YouTube URL
def extract_video_id(url: str) -> str:
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if not match:
        raise ValueError("Invalid YouTube URL format.")
    return match.group(1)