import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *

form_class = uic.loadUiType("subjectStandardModify.ui")[0]

class StandardModifyInput(QDialog, form_class):
    def __init__(self, name, greater, less):
        self.name = name
        self.greater = greater
        self.less = less
        super().__init__()
        self.setupUi(self)
        self.initUI()
    def initUI(self):
        self.stndName.setPlainText(self.name)
        self.stndGre.setPlainText(self.greater)
        self.stndLess.setPlainText(self.less)
        
    #     self.setWindowTitle('Sub Window')
    #     self.setGeometry(100, 100, 200, 100)
    #     layout = QVBoxLayout()
    #     layout.addStretch(1)
    #     edit = QLineEdit()
    #     font = edit.font()
    #     font.setPointSize(20)
    #     edit.setFont(font)
    #     self.edit = edit
    #     subLayout = QHBoxLayout()
        
    #     btnOK = QPushButton("확인")
    #     btnOK.clicked.connect(self.onOKButtonClicked)
    #     btnCancel = QPushButton("취소")
    #     btnCancel.clicked.connect(self.onCancelButtonClicked)
    #     layout.addWidget(edit)
        
    #     subLayout.addWidget(btnOK)
    #     subLayout.addWidget(btnCancel)
    #     layout.addLayout(subLayout)
    #     layout.addStretch(1)
    #     self.setLayout(layout)
        self.btnOK.clicked.connect(self.onOKButtonClicked)
        self.btnCancel.clicked.connect(self.onCancelButtonClicked)
    def onOKButtonClicked(self):
        self.accept()
    def onCancelButtonClicked(self):
        self.reject()
    def showModal(self):
        return super().exec_()