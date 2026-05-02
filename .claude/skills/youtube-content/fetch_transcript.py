#!/usr/bin/env python3
"""
Fetch a YouTube video transcript and print it as plain text.
Usage: python3 fetch_transcript.py <youtube_url>
No API key required.
"""
import re
import sys
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url}")


def fetch_transcript(url: str) -> str:
    video_id = extract_video_id(url)
    ytt = YouTubeTranscriptApi()
    transcript = ytt.fetch(video_id)
    return " ".join(segment.text for segment in transcript)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_transcript.py <youtube_url>", file=sys.stderr)
        sys.exit(1)
    print(fetch_transcript(sys.argv[1]))
