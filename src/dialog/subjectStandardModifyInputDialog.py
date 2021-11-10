import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *

form_class = uic.loadUiType("layout/subjectStandardModify.ui")[0]

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
        self.btnOK.clicked.connect(self.onOKButtonClicked)
        self.btnCancel.clicked.connect(self.onCancelButtonClicked)
    def onOKButtonClicked(self):
        self.accept()
    def onCancelButtonClicked(self):
        self.reject()
    def showModal(self):
        return super().exec_()