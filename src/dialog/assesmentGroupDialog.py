import sys
from PyQt5.QtWidgets import *


class AssesmentGroupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('평가그룹 이름 입력')
        self.setGeometry(100, 100, 200, 100)
        layout = QVBoxLayout()
        layout.addStretch(1)
        edit = QLineEdit()
        edit.setPlaceholderText("평가그룹 이름 입력")
        font = edit.font()
        font.setPointSize(20)
        edit.setFont(font)
        self.edit = edit
        selectionSize = QLineEdit()
        selectionSize.setPlaceholderText("평가그룹 항목 추출 개수 입력")
        self.selectionSize = selectionSize
        subLayout = QHBoxLayout()

        btnOK = QPushButton("확인")
        btnOK.clicked.connect(self.onOKButtonClicked)
        btnCancel = QPushButton("취소")
        btnCancel.clicked.connect(self.onCancelButtonClicked)
        layout.addWidget(edit)
        layout.addWidget(selectionSize)

        subLayout.addWidget(btnOK)
        subLayout.addWidget(btnCancel)
        layout.addLayout(subLayout)
        layout.addStretch(1)
        self.setLayout(layout)

    def onOKButtonClicked(self):
        self.accept()

    def onCancelButtonClicked(self):
        self.reject()

    def showModal(self):
        return super().exec_()
