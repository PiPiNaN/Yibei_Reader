from PySide6.QtCore import *

import nltk
from argostranslate import package, translate

class ArgosTranslator(QObject):

    def __init__(self):
        super().__init__()     
        #初始化加载离线模型   
        package.install_from_path("./models/translate-en_zh-1_9.argosmodel")
        installed_lang = translate.get_installed_languages()
        self.translation_en_zh = installed_lang[0].get_translation(installed_lang[1])

    @staticmethod
    def instance():
        if not hasattr(ArgosTranslator, "_instance") or ArgosTranslator._instance is None:
            ArgosTranslator._instance = ArgosTranslator()
        return ArgosTranslator._instance
    
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
                result = self.translation_en_zh.translate(s)
                # print(result[0])
                text_zh += result            
        except:
            text_zh = "翻译出错了"
        return text_zh

