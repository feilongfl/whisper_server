__version__ = "0.1.0"

from flask import Flask

app = Flask(__name__)

import whisper_server.views
