from wisper_server import app
from flask import request
from wisper_server.whisper_gpt import WhisperGPT
import tempfile

# global models
whisperGPT = WhisperGPT()

@app.route('/')
def index():
    return 'whisper - api'

def exec_whisper(audio_stream):
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpfile = f"{tmpdirname}/{audio_stream.filename}"
        print(f"temp file: {tmpfile}")
        audio_stream.save(tmpfile)
        return whisperGPT.process(tmpfile)

@app.route('/whisper', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        print(request.files)
        return exec_whisper(request.files['file'])
