import torch
from TTS.api import TTS
import subprocess
import tempfile
import threading


class Speech:
    def __init__(self, model="tts_models/multilingual/multi-dataset/xtts_v2") -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)
        self.lock = threading.Lock()
        pass

    def play(self, text: str):
        self.lock.acquire()
        with tempfile.TemporaryDirectory() as tmpdirname:
            # wav = self.tts.tts(text=text, speaker_wav="tts_sample.wav", language="zh")
            tmpfile = f"{tmpdirname}/output.wav"
            self.tts.tts_to_file(
                text=text,
                speaker_wav="tts_sample.wav",
                language="zh",
                file_path=tmpfile,
            )
            self.proc = subprocess.run(["ls", "-la", tmpfile])
            self.proc = subprocess.run(["mplayer", tmpfile])
        self.lock.release()
