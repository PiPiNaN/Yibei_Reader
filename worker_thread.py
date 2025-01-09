from PySide6.QtCore import *
import time
import pymupdf
from pathlib import Path
from mbart_translator import MBartTranslator
from argos_translator import ArgosTranslator

class WorkerThread(QThread):
    progress = Signal(str)
    finished = Signal(bool)

    def __init__(self, pdfpath:Path):
        super().__init__()
        self.translator = None
        self.pdfenpath = pdfpath
    
    def run(self):
        print(f"thread run, translating {self.pdfenpath}")

        doc_en = pymupdf.open(str(self.pdfenpath))
        doc_zh = pymupdf.open()
        
        #按页进行处理          
        for page in doc_en:
            #处理进度            
            self.progress.emit(f'Processing page {page.number} of {doc_en.page_count}')
                        
            page2 = doc_zh.new_page()    

            # copy the images
            image_list = page.get_images()    
            if image_list:                
                for index, item in enumerate(image_list):                
                    rects = page.get_image_rects(item)
                    xref = item[0]
                    base_image = doc_en.extract_image(xref)
                    image_bytes = base_image["image"]
                    page2.insert_image(rects[0], stream=image_bytes)

            # translate the text
            blocks = page.get_text("blocks")
            for block in blocks:                
                rect = pymupdf.Rect(x0=block[0], y0=block[1], x1=block[2], y1=block[3])                
                text_en = block[4].replace('-\n', '').replace('\2\n','').replace('\n', ' ')                
                                
                if self.translator is None:
                    self.translator = ArgosTranslator.instance()     
                text_zh = self.translator.translate(text_en)
                
                page2.insert_htmlbox(rect, text_zh)
                page2.add_rect_annot(rect)
        
        doc_zh.save(str(self.pdfenpath).replace(".pdf", "-zh.pdf"))
        doc_en.close()
        self.progress.emit('complete')        
        self.finished.emit(True)
