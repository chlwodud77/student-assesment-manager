import sys, random
import backend, excelManage, scoreManage
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

form_class = uic.loadUiType("layout/multiAssesInput.ui")[0]


class MultiAssesInput(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showSubList()
        self.showClassList()
        self.addedSubListWidget.itemDoubleClicked.connect(self.extSubFromWidget)
        self.addedClassWidget.itemDoubleClicked.connect(self.extClassFromWidget)
        self.assesBtn.clicked.connect(self.setAsses)
        self.addSubBtn.clicked.connect(self.addSubToWidget)
        self.addClassBtn.clicked.connect(self.addClassToWidget)

    def setAsses(self):
        subjectListWidget = self.addedSubListWidget
        classListWidget = self.addedClassWidget
        subjectIdList = []
        classList = []

        subjectListCnt = subjectListWidget.count()
        classListCnt = classListWidget.count()

        if subjectListCnt == 0 or classListCnt == 0: return QMessageBox.about(self, "주의", "평가를 생성할 과목 또는 학급을 추가해주세요.")

        for i in range(0, subjectListCnt):
            subjectId = subjectListWidget.item(i).whatsThis()
            subjectIdList.append(int(subjectId))

        for i in range(0, classListCnt):
            classText = classListWidget.item(i).text()
            grade, classes = excelManage.returnClassInteger(classText)
            classList.append([grade, classes])

        for subId in subjectIdList:
            for classes in classList:
                grade, cl = classes
                scoreList = backend.returnScoreBySubIdAndClass(subId, int(grade), int(cl))
                for stdId, score in scoreList:
                    content = ""
                    if (score is not None):
                        assesments = scoreManage.getPossibleAssesmentByScore(subId, int(score))
                        if len(assesments) == 0:
                            content = ""
                            backend.updateScoreAssesBySubIdAndStdId(subId, stdId, content)
                        else:
                            randomIndex = random.randint(0, len(assesments) - 1)
                            content = assesments[randomIndex]
                            backend.updateScoreAssesBySubIdAndStdId(subId, stdId, content)
        return QMessageBox.about(self, "알림", "평가 생성 완료.")

    def showSubList(self):
        widget = self.subTreeWidget
        widget.clear()
        widget.setColumnCount(1)
        widget.setHeaderLabels(["과목"])
        parentSubjects = backend.returnParentSubject()
        for parent in parentSubjects:
            parentId = int(parent[0])
            parentName = parent[1]
            item = QTreeWidgetItem(widget, [parentName])
            item.setWhatsThis(0, str(parentId) + "-")

        it = QTreeWidgetItemIterator(widget)
        while it.value():
            if "-" in it.value().whatsThis(0):
                parentId, trash = it.value().whatsThis(0).split("-")
                childSubjects = backend.returnChildSubjectsFromParentId(int(parentId))
                if len(childSubjects) == 0:
                    it += 1
                for child in childSubjects:
                    childId = int(child[0])
                    childName = child[1]
                    item = QTreeWidgetItem(it.value())
                    item.setWhatsThis(0, str(childId))
                    item.setText(0, childName)
            it += 1

    def showClassList(self):
        widget = self.classWidget
        widget.clear()
        classList = backend.returnClassList()

        for grade, classes in classList:
            item = QListWidgetItem(str(grade) + "학년 " + str(classes) + "반")
            widget.addItem(item)

    def addSubToWidget(self):
        srcWidget = self.subTreeWidget
        trgWidget = self.addedSubListWidget
        if srcWidget.selectedItems() is not None:
            items = srcWidget.selectedItems()
            for item in items:
                if item.parent() is not None:  # 자식 노드이면
                    parentItem = item.parent()
                    parentName = parentItem.text(0)
                    childName = item.text(0)
                    childId = item.whatsThis(0)
                    newItem = QListWidgetItem(str(parentName) + " - " + str(childName))
                    newItem.setWhatsThis(str(childId))
                    trgWidget.addItem(newItem)

    def extSubFromWidget(self):
        widget = self.addedSubListWidget
        if widget.currentItem() is not None:
            row = widget.currentRow()
            widget.takeItem(row)

    def addClassToWidget(self):
        srcWidget = self.classWidget
        trgWidget = self.addedClassWidget
        if srcWidget.selectedItems() is not None:
            items = srcWidget.selectedItems()
            for item in items:
                newItem = QListWidgetItem(item.text())
                trgWidget.addItem(newItem)

    def extClassFromWidget(self):
        widget = self.addedClassWidget
        if widget.currentItem() is not None:
            row = widget.currentRow()
            widget.takeItem(row)

    def show(self):
        dialog = MultiAssesInput()
        dialog.exec_()
