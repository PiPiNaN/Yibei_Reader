from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings

class ReaderWidget(QWebEngineView):
    def __init__(self):
        super().__init__()
       
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.ForceDarkMode, False)        
        self.show()

    def load_file(self, filepath):        
        f = str(filepath).replace("\\", "/")
        self.setUrl(QUrl(f"file:///{f}"))
        self.show()