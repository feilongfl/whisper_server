from whisper_server import app
from flask import request
from whisper_server.tts import Speech
from whisper_server.whisper_gpt import WhisperGPT
import tempfile
from whisper_server.lux import Lux

# global models
whisperGPT = WhisperGPT("openai/whisper-large-v3")
speech = Speech("tts_models/multilingual/multi-dataset/xtts_v2")


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
def v1_audio_transcriptions():
    if request.method != "POST":
        return (
            "Example: curl -X POST -F 'model=openai/whisper-large-v3' -F 'file=@data/BV1R64y1E7Zz.mp3' http://xxxxx/v1/audio/transcriptions",
            400,
        )

    print(request.form)
    print(request.files)
    return exec_whisper(
        request.form["model"]
        if "model" in request.form.keys()
        else whisperGPT.model_id,
        request.files["file"],
    )


@app.route("/v1/bilibili/transcriptions", methods=["POST"])
def v1_bilibili_transcriptions():
    if request.method != "POST":
        return (
            "Example: curl -X POST -F 'model=openai/whisper-large-v3' -F 'BV=BV1R64y1E7Zz' http://xxxxx/v1/audio/transcriptions",
            400,
        )
    print(request.form)  # maybe need a log framework, todo: check model

    with Lux(BV=request.form["BV"]) as lux:
        lux.download().convert(to="mp3")
        return whisperGPT.process(lux.file["audio"])


@app.route("/v1/audio/speech", methods=["POST"])
def v1_audio_speech():
    if request.method != "POST":
        return 'Example: curl -X POST -d "test" http://xxxxx', 400

    speech.play(request.form["text"])
    return "done"
