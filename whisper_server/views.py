from whisper_server import app
from flask import request
from whisper_server.whisper_gpt import WhisperGPT
import tempfile

# global models
whisperGPT = WhisperGPT("openai/whisper-large-v3")


@app.route("/")
def index():
    return "whisper - api"


def exec_whisper(model, audio_stream):
    if model != whisperGPT.model_id:
        return f"unsupport model: {model}", 400

    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpfile = f"{tmpdirname}/{audio_stream.filename}"
        print(f"temp file: {tmpfile}")
        audio_stream.save(tmpfile)
        return whisperGPT.process(tmpfile)


@app.route("/v1/audio/transcriptions", methods=["POST"])
def upload_file():
    if request.method == "POST":
        print(request.form)
        print(request.files)
        return exec_whisper(
            request.form["model"]
            if "model" in request.form.keys()
            else whisperGPT.model_id,
            request.files["file"],
        )
