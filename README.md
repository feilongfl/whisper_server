# whisper server

use whisper as a web server api

## usage

``` shell
poetry run poe serve

curl -X POST -F 'file=@./data/BV158411X7BR.mp3' http://127.0.0.1:5000/whisper | jq
```
