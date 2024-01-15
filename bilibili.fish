#!/usr/bin/env fish

if test (count $argv) -eq 0
    echo "No arguments provided. Exiting..."
    exit 1
end

set BV $argv

mkdir -p tmp
lux -o tmp -O $BV https://www.bilibili.com/video/$BV

ffmpeg -i tmp/$BV.mp4 tmp/$BV.mp3
curl -X POST -F 'model=openai/whisper-large-v3' -F 'file=@tmp/'$BV'.mp3' http://127.0.0.1:5000/v1/audio/transcriptions | jq >tmp/$BV.json

