import os
os.environ["PHONEMIZER_ESPEAK_LIBRARY"] = r"C:\Program Files\eSpeak NG\libespeak-ng.dll"
os.environ["PHONEMIZER_ESPEAK_PATH"] = r"C:\Program Files\eSpeak NG\espeak-ng.exe"
print("PHONEMIZER_ESPEAK_LIBRARY:", os.environ.get("PHONEMIZER_ESPEAK_LIBRARY"))
print("PHONEMIZER_ESPEAK_PATH:", os.environ.get("PHONEMIZER_ESPEAK_PATH"))
from Kokoro.kokoro import generate
import torch
from Kokoro.models import build_model
from pathlib import Path
import pymupdf
from PySide6.QtCore import *
import pyaudio

class ReaderThread(QThread):

    def __init__(self, pdfpath: Path):
        super().__init__()
        self.pdfenpath = pdfpath

        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.MODEL = build_model('./Kokoro/kokoro-v0_19.pth', device)
        self.VOICE_NAME = [
            'af',
            'af_bella', 'af_sarah', 'am_adam', 'am_michael',
            'bf_emma', 'bf_isabella', 'bm_george', 'bm_lewis',
            'af_nicole', 'af_sky',
        ][5]
        self.VOICEPACK = torch.load(
            f'./Kokoro/voices/{self.VOICE_NAME}.pt', weights_only=True).to(device)
        print(f'Loaded voice: {self.VOICE_NAME}')

    def run(self):
        doc_en = pymupdf.open(str(self.pdfenpath))
        # 按页进行处理
        for page in doc_en:
            blocks = page.get_text("blocks")
            for block in blocks:
                text_en = block[4].replace(
                    '-\n', '').replace('\2\n', '').replace('\n', ' ')
                print(text_en)
                #朗读
                audio, out_ps = generate(
                    self.MODEL, text_en, self.VOICEPACK, lang=self.VOICE_NAME[0])
                P = pyaudio.PyAudio()
                stream = P.open(rate=24000, format=pyaudio.paFloat32, channels=1, output=True)
                stream.write(audio.tobytes())
                stream.close()
                P.terminate()
