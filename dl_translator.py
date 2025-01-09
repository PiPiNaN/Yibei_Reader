import dl_translate as dlt
import time
import nltk
from PySide6.QtCore import *

class DlTranslator(QObject):

    def __init__(self):
        super().__init__()     
        #初始化加载离线模型
        t = time.time()
        self.mt = dlt.TranslationModel("./models/m2m100_418M", model_family="m2m100")  # Slow when you load it for the first time
        print(f"model loaded, cost {time.time() - t :.4f}s")

    @staticmethod
    def instance():
        if not hasattr(DlTranslator, "_instance") or DlTranslator._instance is None:
            DlTranslator._instance = DlTranslator()
        return DlTranslator._instance

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
                result = self.mt.translate(s, source=dlt.lang.ENGLISH, target=dlt.lang.CHINESE)
                # print(result[0])
                text_zh += result
        except:
            text_zh = "翻译出错了"
        return text_zh