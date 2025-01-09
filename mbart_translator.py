from PySide6.QtCore import *

import nltk
import time
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

class MBartTranslator(QObject):

    def __init__(self):
        super().__init__()     
        #初始化加载离线模型   
        t = time.time()
        self.model = MBartForConditionalGeneration.from_pretrained("./models/mbart-large-50-many-to-many-mmt")
        self.tokenizer = MBart50TokenizerFast.from_pretrained("./models/mbart-large-50-many-to-many-mmt")
        print(f"model loaded, cost {time.time() - t :.4f}s")

    @staticmethod
    def instance():
        if not hasattr(MBartTranslator, "_instance") or MBartTranslator._instance is None:
            MBartTranslator._instance = MBartTranslator()
        return MBartTranslator._instance
    
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
                encoded_input = self.tokenizer(s, return_tensors="pt")

                translation_result = self.model.generate(
                    **encoded_input,
                    forced_bos_token_id = self.tokenizer.lang_code_to_id["zh_CN"]
                )

                result = self.tokenizer.batch_decode(translation_result, skip_special_tokens=True)
                # print(result[0])
                text_zh += result[0]
        except:
            text_zh = "翻译出错了"
        return text_zh
