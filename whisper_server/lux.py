import subprocess
import tempfile


class Lux:
    def __init__(self, source="BiliBili", **kwargs) -> None:
        if source != "BiliBili":
            raise NotImplemented

        self.source = source
        self.para = kwargs
        self.work_dir = tempfile.TemporaryDirectory()
        self.file = {}

    def download(self):
        self.file["video"] = f'{self.work_dir.name}/{self.para["BV"]}.mp4'
        # lux -o tmp -O $BV https://www.bilibili.com/video/$BV

        args = [
            "lux",
            "-o",
            self.work_dir.name,
            "-O",
            self.para["BV"],
            f"https://www.bilibili.com/video/{self.para['BV']}",
        ]
        print(f"subprocess: {args}")
        self.proc = subprocess.run(args)
        self.proc = subprocess.run(["ls", self.work_dir.name])
        return self

    def convert(self, to="mp3"):
        self.file["audio"] = f'{self.work_dir.name}/{self.para["BV"]}.{to}'
        # ffmpeg -i tmp/$BV.mp4 tmp/$BV.mp3
        args = [
            "ffmpeg",
            "-i",
            self.file["video"],
            self.file["audio"],
        ]
        print(f"subprocess: {args}")
        self.proc = subprocess.run(args)
        return self

    def close(self):
        self.work_dir.cleanup()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
