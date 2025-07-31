# api/transcribe.py
from http.server import BaseHTTPRequestHandler
import json
import subprocess
import whisper
import yt_dlp
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body)

        url = data.get("url")
        output_file = "audio.mp3"

        # Download audio
        subprocess.run(["yt-dlp", "-x", "--audio-format", "mp3", "-o", output_file, url])

        # Transcribe with Whisper
        model = whisper.load_model("base")
        result = model.transcribe(output_file)

        response = {
            "transcript": result["text"]
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
