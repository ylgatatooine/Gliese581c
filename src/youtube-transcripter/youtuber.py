from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YouTuber:
    """
    Fetch and format YouTube video transcripts.
    """
    def get_transcript_by_url(self, video_url: str) -> str:
        """
        Get transcript from a YouTube URL.
        """
        try:
            video_id = self.extract_video_id(video_url)
            return self.get_transcript_by_id(video_id)
        except Exception as e:
            return f"Error fetching transcript: {e}"

    def get_transcript_by_id(self, video_id: str) -> str:
        """
        Get transcript from a YouTube video ID.
        """
        try:
            logger.info(f"Fetching transcript for video ID: {video_id}")
            transcript = YouTubeTranscriptApi.get_transcript(video_id)

            logger.info("Format the transcript ... ")

            formatter = TextFormatter()
            formatted_transcript = formatter.format_transcript(transcript)

            logger.info("Transcript retrieved successfully!")
            return formatted_transcript
        except Exception as e:
            return f"Error fetching transcript: {e}"

    @staticmethod
    def extract_video_id(video_url: str) -> str:
        """
        Extract video ID from a YouTube URL.
        """
        match = re.search(r"v=([a-zA-Z0-9_-]+)", video_url)
        if not match:
            raise ValueError("Invalid YouTube URL format.")
        return match.group(1)

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    youtuber = YouTuber()
    transcript = youtuber.get_transcript_by_url(video_url)
    print("\nTranscript:\n")
    print(transcript)
