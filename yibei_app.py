import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from worker_thread import *
from reader_widget import *
from pathlib import Path

PDF_NAME = "demo.pdf"
BASE_DIR = Path("files")

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
        self.reader1 = ReaderWidget()
        splitter1.addWidget(self.reader1)
        self.reader2 = ReaderWidget()
        splitter1.addWidget(self.reader2)
        layout.addWidget(splitter1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # init left dockable widget
        self.initLeftWidget()

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

    def initToolbar(self):
        toolbar = QToolBar("toolbar")

        self.import_action = QAction(QIcon("./icons/icons_import-100.png"),"导入PDF文件",self)
        toolbar.addAction(self.import_action)

        self.translate_action = QAction(QIcon("./icons/icons_en_zh-96.png"),"英译汉", self)
        self.translate_action.triggered.connect(self.onTranslateClick)
        toolbar.addAction(self.translate_action)

        self.addToolBar(toolbar)       
    
    def onTranslateClick(self):
        self.thread = WorkerThread(self.current_pdf)
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
        self.reader2.load_file(str(self.current_pdf).replace(".pdf", "-zh.pdf"))

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
        self.reader1.load_file(pdf_en)
        self.reader2.load_file(pdf_zh)
        

if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()

    sys.exit(app.exec())