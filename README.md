# whisper server

use whisper as a web server api

## usage

``` shell
poetry env use python
poetry install
poetry run poe serve

curl -X POST -F 'model=openai/whisper-large-v3' -F 'fi
le=@data/BV1n64y1J7Ah.mp3' http://127.0.0.1:5000/v1/au
dio/transcriptions | jq
```
