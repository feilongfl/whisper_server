import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import json
import threading

class WhisperGPT():
    def __init__(self) -> None:
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        model_id = "openai/whisper-large-v3"
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        model.to(device)
        processor = AutoProcessor.from_pretrained(model_id)
        
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
        result = self.pipe(audio) # only one pipe
        self.lock.release()
        return json.dumps(result)
        
    def print(self, result):
        print(result["chunks"])
