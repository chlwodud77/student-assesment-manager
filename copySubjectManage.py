import sys, random
import backend, excelManage, scoreManage
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from adapter import subjectTreeWidgetAdpater as sa
from model.Subject import Subject
from model.Standard import Standard
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
        buttonReply = QMessageBox.question(self, '알림', "과목 복사를 저장하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        selectedSubjects = []
        selectedParentSubject = Subject()

        if(buttonReply == QMessageBox.Yes):
            try:
                if(self.copiedTreeWidget.currentItem() is not None):
                    item = self.copiedTreeWidget.currentItem()
                    if(item.parent() is None):
                        selectedParentSubject.setId(item.whatsThis(0))
                    else:
                        return QMessageBox.about(self, "알림", "하위항목이 복사될 상위항목을 선택해주세요.")

                else:
                    return QMessageBox.about(self, "알림", "하위항목이 복사될 상위항목을 선택해주세요.")
                
                if(self.copyingTreeWidget.selectedItems() != []):
                    items = self.copyingTreeWidget.selectedItems()
                    for item in items:
                        copiedStandards = []
                        if(item.parent() is not None):
                            name = item.text(0)
                            parentId = selectedParentSubject.getId()
                            originalSubId = item.whatsThis(0)
                            subjectId = backend.createChildSubject(name, parentId)

                            originalStandards = backend.returnStandardBySubId(originalSubId)
                            for stnd in originalStandards:
                                subId = subjectId
                                grade = stnd[2]
                                greater = stnd[3]
                                less = stnd[4]
                                standardId = backend.createStandard(subId, grade, greater, less)
                                standardObj = Standard()
                                standardObj.setId(standardId)
                                standardObj.setSubId(subId)
                                standardObj.setGrade(grade)
                                standardObj.setGreater(greater)
                                standardObj.setLess(less)
                                copiedStandards.append(standardObj)  

                            originalAssesments = backend.returnAssesmentBySubId(originalSubId)

                            for originalStands, copiedStands in zip(originalStandards, copiedStandards):
                                subId = int(subjectId)
                                stndId = copiedStands.getId()
                                originStndId = originalStands[0]

                                for asses in originalAssesments:
                                    if(originStndId == asses[2]):
                                        content = asses[3]
                                        assesId = backend.createAssesment(subId, stndId, content)

                            subjectObj = Subject()
                            subjectObj.setId(subjectId)
                            subjectObj.setName(name)
                            subjectObj.setParentId(parentId)
                            selectedSubjects.append(subjectObj)
                else: 
                    return QMessageBox.about(self,"알림", "복사할 하위항목을 선택해주세요.")
            except:
                return QMessageBox.about(self,"알림", "과목 복사 오류!")

            QMessageBox.about(self, "알림", "과목 복사가 완료되었습니다.")
            self.showSubList()

            
    def show(self):
        dialog = CopySubjectManage()
        dialog.exec_()
