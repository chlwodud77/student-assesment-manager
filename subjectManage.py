#!/usr/bin/env python
# -*- coding: utf-8 -*-
from operator import itemgetter

from PyQt5 import QtCore
from PyQt5.Qt import QApplication
from PyQt5.QtWidgets import *

import backend
from copySubjectManage import CopySubjectManage
from subjectInputDialog import SubjectInput
from subjectModInputDialog import SubjectModInput
from subjectStandardModifyInputDialog import StandardModifyInput


def getTextFromSubjectInput():
    win = SubjectInput()
    r = win.showModal()
    if r:
        text = win.edit.text()
        return text
    else:
        return False


def getTextFromSubjectModInput():
    win = SubjectModInput()
    r = win.showModal()
    if r:
        text = win.edit.text()
        return text
    else:
        return False


def openSubjectManage(self):
    a = CopySubjectManage()
    a.show()
    self.showSub(self.subTreeWidget)


def addNewSubjectItem(self):
    subName = getTextFromSubjectInput()
    if subName:
        subId = backend.createParentSubject(subName)
        item = QTreeWidgetItem(self.subTreeWidget, [subName])
        item.setWhatsThis(0, str(subId))
    else:
        return


def addChildSub(self):
    if self.subTreeWidget.currentItem() is None:
        return QMessageBox.about(self, "주의", "하위 과목을 생성할 상위 과목을 선택해주세요.")
    if self.subTreeWidget.currentItem().parent():
        return QMessageBox.about(self, "주의", "하위 과목은 한개만 생성 가능합니다.")
    subName = getTextFromSubjectInput()
    if subName:
        parentItem = self.subTreeWidget.currentItem()
        parentItemSubId = parentItem.whatsThis(0)
        childSubId = backend.createChildSubject(subName, int(parentItemSubId))
        childItem = QTreeWidgetItem(parentItem)
        childItem.setWhatsThis(0, str(childSubId))
        childItem.setText(0, subName)
    else:
        return


def copyContent(obj):
    mimeType = 'application/x-qt-windows-mime;value="Csv"'
    clipboard = QApplication.clipboard()
    mimeData = clipboard.mimeData()
    if mimeType in mimeData.formats():  # 엑셀에서 복사해온 텍스트인지 확인
        text = clipboard.text()
        content = text.split("\n")
        if obj.rowCount() == 0:
            for i in range(0, len(content) - 1):
                obj.insertRow(obj.rowCount())
                item = QTableWidgetItem(str(content[i]))
                obj.setItem(i, 0, item)


def editItem(self):
    subTreeWidget = self.subTreeWidget
    selectedItem = self.subTreeWidget.currentItem()
    selectedItem.setFlags(selectedItem.flags() | QtCore.Qt.ItemIsEditable)
    subTreeWidget.editItem(selectedItem, 0)


def showAssesment(self):
    List = self.grdStndList
    assesWidget = self.grdAseList
    stndName = self.grdAseScoreName
    stndGre = self.grdAseScoreGre
    stndLess = self.grdAseScoreLess
    clickedStndItem = List.currentItem()
    self.grdAseEdit.clear()
    clearQTableWidget(assesWidget)

    if clickedStndItem.whatsThis() is not None:
        stndId = int(clickedStndItem.whatsThis())
        grade, greater, less = backend.returnStandardById(stndId)
        stndName.setText(grade)
        stndGre.setText(str(greater))
        stndLess.setText(str(less))
        assesments = backend.returnAssesmentsByStandardId(stndId)
        if not assesments:
            return QMessageBox.about(self, "오류", "평가문 불러오기 오류.")
        row = 0
        col = 0
        for asses in assesments:
            assesId, assesContent = asses
            item = QTableWidgetItem(assesContent)
            item.setWhatsThis(str(assesId))
            assesWidget.insertRow(row)
            assesWidget.setItem(row, col, item)
            row += 1
    header = self.grdAseList.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.Stretch)


def resetStndInfoLabel(self):
    self.grdAseScoreName.setText("")
    self.grdAseScoreGre.setText("")
    self.grdAseScoreLess.setText("")


def resetGrdStndRow(self):
    widget = self.grdStndAddWidget
    clearQTableWidget(widget)


# 과목 리스트에서 과목 선택 조회 하면 과목 세부 내용 조회 함수
def searchSub(self):
    clearQTableWidget(self.grdAseList)
    resetStndInfoLabel(self)
    self.grdAseEdit.clear()
    subTreeWidget = self.subTreeWidget
    if subTreeWidget.currentItem() is None:
        return
    clickedSubId = subTreeWidget.currentItem().whatsThis(0)
    if clickedSubId == '':
        clickedSubId = -1
    subId = int(clickedSubId)

    if subId:
        # 조회된 과목 등급 점수표 조회 및 출력
        List = self.grdStndList
        StndList = backend.returnStandardBySubId(int(subId))
        StndList = sorted(StndList, key=itemgetter(2))
        List.clear()

        for standard in StndList:
            stndId, subId, grade, greater, less = standard
            whats = str(stndId)
            item = QListWidgetItem(grade)
            item.setWhatsThis(whats)
            List.addItem(item)


def showSub(treeWidget):
    subList = backend.returnSubList()
    subTreeWidget = treeWidget
    subTreeWidget.clear()
    subTreeWidget.setColumnCount(1)
    subTreeWidget.setHeaderLabels(["과목"])

    for i in range(0, len(subList)):
        if subList[i][2] is None:
            subId = subList[i][0]
            subName = subList[i][1]
            parentItem = QTreeWidgetItem(subTreeWidget, [subName])
            parentItem.setWhatsThis(0, str(subId))

    for i in range(0, len(subList)):
        if subList[i][2] is not None:
            subId = subList[i][0]
            childName = subList[i][1]
            parentId = subList[i][2]
            it = QTreeWidgetItemIterator(subTreeWidget)
            while it.value():
                if it.value() is not None and int(it.value().whatsThis(0)) == int(parentId):
                    childItem = QTreeWidgetItem(it.value())
                    childItem.setWhatsThis(0, str(subId))
                    childItem.setText(0, childName)
                it += 1


def modSubName(self):
    widget = self.subTreeWidget
    if widget.currentItem():
        subId = widget.currentItem().whatsThis(0)
        subName = getTextFromSubjectModInput()
        if subName:
            backend.updateSubNameBySubId(int(subId), subName)
            showSub(self.subTreeWidget)
        else:
            return
    else:
        QMessageBox.about(self, "알림", "수정할 항목을 선택해주세요.")


def delSub(self):
    buttonReply = QMessageBox.question(self, '알림', "선택 과목을 삭제하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if buttonReply == QMessageBox.Yes:
        clickedItem = self.subTreeWidget.currentItem()
        if clickedItem is None:
            QMessageBox.about(self, "결과", "삭제할 과목을 선택해주세요.")
            return
        if clickedItem.whatsThis(0) == '':
            self.subTreeWidget.removeItemWidget(clickedItem, 0)
            showSub(self.subTreeWidget)
        else:
            clickedSubId = int(clickedItem.whatsThis(0))
            if backend.deleteSubById(clickedSubId):
                QMessageBox.about(self, "결과", "삭제 성공")
            else:
                QMessageBox.about(self, "결과", "삭제 실패")
        showSub(self.subTreeWidget)
        showSub(self.scoreSubTreeWidget)


# 평가 내용 선택하면 편집기에 해당 내용 보여줌
def activateEdit(self):
    widget = self.grdAseList
    Editor = self.grdAseEdit
    Editor.setPlainText(widget.item(widget.currentRow(), widget.currentColumn()).text())


def addGrdStndRow(self):
    widget = self.grdStndAddWidget
    widget.insertRow(widget.rowCount())


def getListFromQTableWidget(widget):
    tableList = []
    totalRows = widget.rowCount()
    totalCols = widget.columnCount()

    for row in range(0, totalRows):
        content = []
        for col in range(0, totalCols):
            if widget.item(row, col) is None:
                return False
            colItem = widget.item(row, col).text()
            content.append(colItem)
        tableList.append(content)

    return tableList


def clearQTableWidget(widget):
    while widget.rowCount() != 0:
        widget.removeRow(0)


def addGrdStnd(self):
    List = self.grdStndList
    if self.subTreeWidget.currentItem() is None:
        return QMessageBox.about(self, "주의", "등급을 추가할 과목을 선택하세요.")
    tableList = getListFromQTableWidget(self.grdStndAddWidget)
    if not tableList:
        return QMessageBox.about(self, "주의", "등급 내용을 모두 채워주세요.")

    subId = self.subTreeWidget.currentItem().whatsThis(0)
    for content in tableList:
        grade, greater, less = content
        if grade != "":
            if greater != "" and less != "":
                if float(greater) >= float(less):
                    return QMessageBox.about(self, "주의", "점수 범위 입력 오류.")
            item = QListWidgetItem(grade)
            List.addItem(item)
            backend.createStandard(int(subId), grade, float(greater), float(less))
        else:
            return QMessageBox.about(self, "주의", "이름을 입력하세요.")

    searchSub(self)
    clearQTableWidget(self.grdStndAddWidget)


def modGrdStnd(self):
    if self.grdStndList.currentItem() is None:
        return QMessageBox.about(self, "주의", "등급 기준을 선택해주세요.")
    stndId = self.grdStndList.currentItem().whatsThis()
    name = self.grdAseScoreName.text()
    greater = self.grdAseScoreGre.text()
    less = self.grdAseScoreLess.text()
    win = StandardModifyInput(name, greater, less)
    r = win.showModal()
    if r:
        name = win.stndName.toPlainText()
        greater = win.stndGre.toPlainText()
        less = win.stndLess.toPlainText()
        backend.updateStandard(int(stndId), name, float(greater), float(less))
        searchSub(self)
        return QMessageBox.about(self, "알림", "등급 기준 수정완료.")


def delGrdStnd(self):
    if self.grdStndList.currentItem() is None:
        return QMessageBox.about(self, "주의", "등급 기준을 선택해주세요.")
    buttonReply = QMessageBox.question(self, '알림', "등급 기준을 삭제하시겠습니까? 등급 기준 안에 있던 평가문도 같이 삭제됩니다.",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if buttonReply == QMessageBox.Yes:
        widget = self.grdStndList
        clickedItem = widget.currentItem()
        stndId = int(clickedItem.whatsThis())
        backend.deleteStandradById(stndId)
        backend.deleteAssesmentByStndId(stndId)
        searchSub(self)
        return QMessageBox.about(self, "알림", "등급 기준 삭제완료.")


# 평가 내용 추가 함수
def addAse(self):
    stndList = self.grdStndList
    subjectList = self.subTreeWidget
    if stndList.currentItem() is None or subjectList.currentItem() is None:
        return QMessageBox.about(self, "주의", "평가를 추가할 과목 또는 등급을 선택해주세요.")
    subId = subjectList.currentItem().whatsThis(0)
    stndId = stndList.currentItem().whatsThis()
    content = self.grdAseEdit.toPlainText()
    backend.createAssesment(int(subId), int(stndId), content)
    showAssesment(self)
    self.grdAseEdit.clear()


# 평가 내용 수정 함수
def modAse(self):
    assesList = self.grdAseList
    content = self.grdAseEdit.toPlainText()
    item = assesList.currentItem()
    if item is None:
        return QMessageBox.about(self, "주의", "수정할 평가문을 선택해주세요.")
    assesId = item.whatsThis()
    backend.updateAssesment(int(assesId), content)
    showAssesment(self)
    self.grdAseEdit.clear()
    return QMessageBox.about(self, "알림", "수정완료.")


# 평가 내용 항목 지우는 함수
def delAse(self):
    if self.grdAseList.currentItem() is None:
        return QMessageBox.about(self, "주의", "삭제할 평가문을 선택하세요.")
    assesList = self.grdAseList
    assesItems = assesList.selectedItems()
    for item in assesItems:
        assesId = item.whatsThis()
        backend.deleteAssesmentById(int(assesId))
    showAssesment(self)
    self.grdAseEdit.clear()
    return QMessageBox.about(self, "알림", "선택하신 평가문(들)이 삭제되었습니다.")
