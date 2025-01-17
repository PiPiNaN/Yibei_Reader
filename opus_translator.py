from PySide6.QtCore import *

import nltk
import time
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class OpusTranslator(QObject):

    def __init__(self):
        super().__init__()     
        #初始化加载离线模型   
        t = time.time()
        self.tokenizer = AutoTokenizer.from_pretrained("./models/opus-mt-en-zh")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("./models/opus-mt-en-zh")        
        print(f"opus model loaded, cost {time.time() - t :.4f}s")

    @staticmethod
    def instance():
        if not hasattr(OpusTranslator, "_instance") or OpusTranslator._instance is None:
            OpusTranslator._instance = OpusTranslator()
        return OpusTranslator._instance
    
    def split_sentences(self, text):
        return nltk.sent_tokenize(text)
    
    def translate(self, text_en):
        text_en = text_en.replace("-\n", "").replace("\n", " ")
        sentences = self.split_sentences(text_en)
        text_zh = ""
        #逐句翻译
        try:
            for s in sentences:   
                s = s.strip()
                # print(s)
                encoded = self.tokenizer([s], return_tensors="pt")
                translation = self.model.generate(**encoded)
                result = self.tokenizer.batch_decode(translation,skip_special_tokens=True)[0]
                # print(result)
                text_zh += result
        except:
            text_zh = "翻译出错了"
        return text_zh
