import os
import io
import time
import wave
import numpy as np
from faster_whisper import WhisperModel
from modules import language

class LocalSTT:
    def __init__(self, model_size=None, compute_type="int8"):
        """
        Initializes the local faster-whisper model.
        English uses the tiny.en model; Portuguese uses the multilingual tiny model.
        """
        self.model_size = model_size or ("tiny" if language.is_portuguese() else "tiny.en")
        self.language = "pt" if language.is_portuguese() else "en"
        print(f"[LOCAL STT] Loading Whisper model ({self.model_size}) into memory...")
        start = time.time()
        # cpu device is forced to avoid needing CUDA setup, int8 keeps RAM usage low
        self.model = WhisperModel(self.model_size, device="cpu", compute_type=compute_type)
        print(f"[LOCAL STT] Model loaded in {time.time() - start:.2f} seconds.")

    def transcribe_audio_file(self, file_path: str) -> str:
        """Transcribes an audio file on disk."""
        segments, info = self.model.transcribe(file_path, beam_size=1, language=self.language)
        text = "".join([segment.text for segment in segments])
        return text.strip()

    def transcribe_audio_data(self, audio_data: bytes, sample_rate: int = 16000) -> str:
        """Transcribes raw PCM audio bytes in memory."""
        # Convert bytes to numpy array (faster-whisper expects a float32 array [-1.0, 1.0])
        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
        
        if sample_rate != 16000:
            import torch
            import torchaudio.transforms as T
            resampler = T.Resample(sample_rate, 16000)
            audio_tensor = torch.from_numpy(audio_np)
            audio_np = resampler(audio_tensor).numpy()
        
        segments, info = self.model.transcribe(audio_np, beam_size=1, language=self.language)
        text = "".join([segment.text for segment in segments])
        return text.strip()

# Singleton instance to avoid reloading the model
_instance = None

def get_stt() -> LocalSTT:
    global _instance
    desired = "tiny" if language.is_portuguese() else "tiny.en"
    if _instance is None or _instance.model_size != desired:
        _instance = LocalSTT(model_size=desired)
    return _instance

if __name__ == "__main__":
    # Test script
    stt = get_stt()
    print("STT Ready. (Pass audio data to transcribe)")
