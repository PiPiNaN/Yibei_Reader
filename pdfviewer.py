from PySide6 import QtCore, QtWidgets, QtWebEngineWidgets

PDFJS =  'file:///pdfjs-4.10.38-dist/web/viewer.html'

class PDFViewer(QtWebEngineWidgets.QWebEngineView):
    def __init__(self):
        super().__init__()
    
    def load_file(self, filepath): 
        f = str(filepath).replace("\\", "/")
        # print(f)
        self.load(QtCore.QUrl(f'{PDFJS}?file={f}#zoom=page-width'))