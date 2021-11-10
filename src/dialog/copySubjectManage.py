from PyQt5 import uic
from PyQt5.QtWidgets import *

from model.Subject import Subject
from utils import copyManager
from utils.adapter import subjectTreeWidgetAdapter as sa

form_class = uic.loadUiType("layout/subjectCopyDialog.ui")[0]


class CopySubjectManage(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showSubList()
        self.copySubjectBtn.clicked.connect(self.saveCopySubject)

    def showSubList(self):
        sa.showSub(self.copyingTreeWidget)
        sa.showSub(self.copiedTreeWidget)

    def saveCopySubject(self):
        buttonReply = QMessageBox.question(self, '알림', "과목 복사를 저장하시겠습니까?", QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.Yes)
        selectedParentSubject = Subject()

        if buttonReply == QMessageBox.Yes:
            try:
                if self.copiedTreeWidget.currentItem() is not None:
                    item = self.copiedTreeWidget.currentItem()
                    if item.parent() is None:
                        selectedParentSubject.setId(item.whatsThis(0))
                    else:
                        return QMessageBox.about(self, "알림", "하위항목이 복사될 상위항목을 선택해주세요.")

                else:
                    return QMessageBox.about(self, "알림", "하위항목이 복사될 상위항목을 선택해주세요.")

                if self.copyingTreeWidget.selectedItems():
                    items = self.copyingTreeWidget.selectedItems()
                    for item in items:
                        if item.parent() is not None:
                            name = item.text(0)
                            trgSubParentId = selectedParentSubject.getId()
                            originalSubId = item.whatsThis(0)
                            copyManager.copyChildSubject(name, originalSubId, trgSubParentId)
                else:
                    return QMessageBox.about(self, "알림", "복사할 하위항목을 선택해주세요.")
            except Exception as e:
                print(e)
                return QMessageBox.about(self, "알림", "과목 복사 오류!")

            QMessageBox.about(self, "알림", "과목 복사가 완료되었습니다.")
            self.showSubList()

    def show(self):
        dialog = CopySubjectManage()
        dialog.exec_()
