import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import json
import threading

# def text_encoder(obj):
#     if 'text' in obj:
#         obj['text'] = obj['text'].encode('utf-8').decode('unicode_escape')
#     return obj

class WhisperGPT:
    def __init__(self, model_id) -> None:
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        self.model_id = model_id
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            self.model_id,
            torch_dtype=torch_dtype,
            low_cpu_mem_usage=True,
            use_safetensors=True,
        )
        model.to(device)
        processor = AutoProcessor.from_pretrained(self.model_id)

        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            max_new_tokens=128,
            chunk_length_s=30,
            batch_size=16,
            return_timestamps=True,
            torch_dtype=torch_dtype,
            device=device,
        )

        self.lock = threading.Lock()

    def process(self, audio: str):
        self.lock.acquire()
        result = self.pipe(audio)  # only one pipe
        self.lock.release()
        return json.dumps(result, ensure_ascii=False)

    def print(self, result):
        print(result["chunks"])
