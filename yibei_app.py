import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from sympy import im
from worker_thread import *
# from reader_widget import *
from pdfviewer import *
from reader_thread import *
from pathlib import Path
import shutil
import pymupdf

PDF_NAME = "demo.pdf"
BASE_DIR = Path.cwd() / "files"

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Yibei Paper Reader")

        self.current_pdf = BASE_DIR / PDF_NAME

        #初始化工具栏
        self.initToolbar()

        # main area
        layout = QHBoxLayout()  
        
        splitter1 = QSplitter()
        self.pdfviewer1 = PDFViewer()
        splitter1.addWidget(self.pdfviewer1)
        self.pdfviewer2 = PDFViewer()
        splitter1.addWidget(self.pdfviewer2)
        layout.addWidget(splitter1)
        # self.pdfviewer1.load_file(self.current_pdf)
        # self.pdfviewer2.load_file(self.current_pdf)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # init left dockable widget
        self.initLeftWidget()

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        print("MainWindow init finish.")

    def initToolbar(self):
        toolbar = QToolBar("toolbar")
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.import_action = QAction(QIcon("./icons/icons-importpdf-64.png"),"导入PDF文件",self)
        self.import_action.triggered.connect(self.onImportPDF)
        toolbar.addAction(self.import_action)

        toolbar.addSeparator()

        self.read_action = QAction(QIcon("./icons/icons-read.png"), "朗读", self)
        self.read_action.triggered.connect(self.onReadPDF)
        toolbar.addAction(self.read_action)

        toolbar.addSeparator()

        self.combobox = QComboBox()
        self.combobox.addItems(["Argostranslate", "Opus", "Mbart"])
        self.combobox.currentIndexChanged.connect(self.onModelChoose)
        toolbar.addWidget(self.combobox)

        self.translate_action = QAction(QIcon("./icons/icons_en_zh-96.png"),"英译汉", self)
        self.translate_action.triggered.connect(self.onTranslateClick)
        toolbar.addAction(self.translate_action)

        self.addToolBar(toolbar)   

    def onModelChoose(self, index):        
        self.translator_choice = index
        return 

    def onImportPDF(self):
        dialog = QFileDialog(self) 
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("PDFs (*.pdf *PDF)")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            for f in filenames:
                doc = pymupdf.open(f)
                # print(doc.metadata["title"])
                if doc.metadata["title"]:
                    rename = (doc.metadata["title"] +".pdf").replace(':',"")
                    shutil.copy(f, BASE_DIR / rename)
                else:
                    shutil.copy(f, BASE_DIR)
            print(filenames)

    def onReadPDF(self):
        self.reader = ReaderThread(self.current_pdf)
        self.reader.start()
        return

    def onTranslateClick(self):
        self.thread = WorkerThread(self.current_pdf, self.translator_choice)
        self.thread.progress.connect(self.workprogress)
        self.thread.finished.connect(self.workcompleted)
        self.translate_action.setEnabled(False)
        self.thread.start()

    def workprogress(self, str):
        print(str)
        self.statusbar.showMessage(str)

    def workcompleted(self, finished):        
        if finished:
            self.translate_action.setEnabled(True)
        self.statusbar.showMessage("翻译工作已完成。")        
        self.pdfviewer2.load_file(str(self.current_pdf).replace(".pdf", "-zh.pdf"))

    def initLeftWidget(self):        
        left = QDockWidget()

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.West)
        tabs.setMovable(True)
        
        self.file_list = QListView()
        model = QFileSystemModel()
        model.setRootPath(str(BASE_DIR))   
        model.setNameFilterDisables(False)
        model.setNameFilters({"*.pdf", "*.md", "*.txt"}) 
        self.file_list.setModel(model)
        self.file_list.setRootIndex(model.index(str(BASE_DIR)))
        self.file_list.doubleClicked.connect(self.onFileListDoubleClicked)

        tabs.addTab(self.file_list, "Library")
        left.setWidget(tabs)
        left.setFloating(False)

        self.addDockWidget(Qt.LeftDockWidgetArea, left)

    def onFileListDoubleClicked(self, index):
        item = self.file_list.model().itemData(index)          
        self.statusbar.showMessage(f"已选择{item[0]}")   
        self.current_pdf = BASE_DIR / item[0]
        pdf_en = BASE_DIR / item[0]         
        pdf_zh = BASE_DIR / item[0].replace(".pdf", "-zh.pdf")       
        self.pdfviewer1.load_file(pdf_en)
        self.pdfviewer2.load_file(pdf_zh)
        

if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    print("window show")
    sys.exit(app.exec())