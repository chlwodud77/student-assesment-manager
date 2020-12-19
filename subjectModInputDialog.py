import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *

form_class = uic.loadUiType("subjectModInputDialog.ui")[0]

class SubjectModInput(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
    def initUI(self):
        self.btnOk.clicked.connect(self.onOKButtonClicked)
        self.btnCancel.clicked.connect(self.onCancelButtonClicked)
    def onOKButtonClicked(self):
        self.accept()
    def onCancelButtonClicked(self):
        self.reject()
    def showModal(self):
        return super().exec_()