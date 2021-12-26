#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict, List
from PyQt5.QtCore import QMimeData
import pandas as pd
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from openpyxl.styles import Alignment, Border, Side
from pandas import DataFrame
from src.dialog.assesmentGroupDialog import AssesmentGroupDialog

from utils import backend
import random
from utils.pandasModel import PandasModel

ASSES_CELL_COL = "E"
LENGTH_CELL_COL = "F"
ASSES_CELL_WIDTH = 50
LENGTH_CELL_WIDTH = 20
GRADE_COL = 0
CLASS_COL = 1
STDNUM_COL = 2
NAME_COL = 3
ASSES_COL = 4
LENGTH_COL = 5

dataFrameList = []
classTextList = []

alignCenter = Alignment(horizontal='center', vertical='center')
wrapText = Alignment(vertical="center", wrapText=True)
allroundBorder = Border(left=Side(border_style="thin",
                                  color='000000'),
                        right=Side(border_style="thin",
                                   color='000000'),
                        top=Side(border_style="thin",
                                 color='000000'),
                        bottom=Side(border_style="thin",
                                    color='000000'))

def resetAddedSubjectList(self):
    try:
        self.subjectGroups = []
        subjectList: QListWidget = self.exlAddedSubWidget
        widgetItems: List[QListWidgetItem] = self.originalAddedSubjects[:]
        for item, idx in zip(widgetItems, range(len(widgetItems))):
            subjectList.item(idx).setText(item.text())
            subjectList.item(idx).setWhatsThis(item.whatsThis())
    except Exception as e:
        print(e)


def setSelectedSubjectGroup(self):
    """
    평가 항목 그룹 지정 함수
    평가 항목을 선택하고 해당 그룹의 이름을 입력하면 평가 항목 리스트의 
    평가 항목명의 서두에 그룹의 이름이 추가됨
    """
    groupName = ""
    groupIds = []
    subjectListWidget: QListWidget = self.exlAddedSubWidget
    if len(subjectListWidget.selectedItems()) == 0:
        return QMessageBox.about(self, "알림", "평가 항목 그룹을 생성할 평가 항목을 지정해주세요.")

    selectedSubjects: List[QListWidgetItem] = subjectListWidget.selectedItems()
    win = AssesmentGroupDialog()
    r = win.showModal()
    if r:
        groupName: str = win.edit.text()
        randomSelection: str = win.selectionSize.text()
        if not randomSelection.isdigit():
            return QMessageBox.about(self, "알림", "평가그룹 항목 추출 개수는 정수여야 합니다.")
        if len(subjectListWidget.selectedItems()) < int(randomSelection):
            return QMessageBox.about(self, "알림", "평가그룹 항목 추출 개수는 선택된 그룹 개수이하여야 합니다.")

    if groupName == "":
        return QMessageBox.about(self, "알림", "평가 항목 그룹 이름을 입력해주세요.")

    for item in selectedSubjects:
        if ">>" in item.text():
            return QMessageBox.about(self, "알림", "이미 평가 항목 그룹에 속하는 항목이 존재합니다.")
        
    

    for item in selectedSubjects:
        orgName: str = item.text()
        item.setText(f"[{groupName}]>>{orgName}")
        groupIds.append(int(item.whatsThis()))

    self.subjectGroups.append({
        "groupName": groupName,
        "subjectIds":  groupIds,
        "randomSelection": int(randomSelection)
    })

    subjectListWidget.clearSelection()


# 엑셀 테이블 항목 선택 시 내용 표시 함수
def exlActivateEdit(self):
    focusedItem = self.exlClassListWidget.currentItem()
    if focusedItem is None:
        self.exlAseEdit.setPlainText("")
        return
    if focusedItem.column() == ASSES_COL:
        content = self.exlClassListWidget.currentItem().text()
        self.exlAseEdit.setPlainText(content)


def showAssesLengthAndState(self, currentContent, row):
    contentLength = len(currentContent)
    contentLengthByte = len(currentContent.encode("utf-8"))
    lengthItem = QTableWidgetItem(str(contentLength) + "자 (" + str(contentLengthByte)
                                  + "바이트)")
    self.exlClassListWidget.setItem(row, LENGTH_COL, lengthItem)
    if contentLength > 1000 or contentLengthByte > 3000:
        self.exlClassListWidget.item(
            row, LENGTH_COL).setBackground(QtGui.QColor(255, 0, 0))


def exlSaveToFile(self):
    global dataFrameList, classTextList
    dfList = dataFrameList
    clList = classTextList
    if not dfList:
        return QMessageBox.about(self, "주의", "엑셀로 저장할 항목들을 추가해주세요.")
    name, _ = QFileDialog.getSaveFileName(
        self, 'Save File', '', 'Excel files (*.xlsx)')

    if name == "":
        return

    with pd.ExcelWriter(name, engine="openpyxl") as writer:
        for df, cl in zip(dfList, clList):
            df.to_excel(writer, sheet_name=cl, index=False)

        for cl in clList:
            worksheet = writer.sheets[cl]
            worksheet.column_dimensions[ASSES_CELL_COL].width = ASSES_CELL_WIDTH
            worksheet.column_dimensions[LENGTH_CELL_COL].width = LENGTH_CELL_WIDTH
            for col, i in zip(worksheet.columns, range(0, worksheet.max_column)):
                if i != ASSES_COL:
                    for cell in col:
                        cell.alignment = alignCenter
                        cell.border = allroundBorder
                if i == ASSES_COL:
                    for cell in col:
                        if cell.row == 1:
                            cell.alignment = alignCenter
                            cell.border = allroundBorder
                        else:
                            cell.alignment = wrapText
                            cell.border = allroundBorder
    dataFrameList = []


def returnClassInteger(classes):
    classes = classes.replace(" ", "")
    grade, ban = classes.split("학년")
    ban = ban.replace("반", "")
    return int(grade), int(ban)


def exlAllShowClassList(self):
    widget = self.exlClassWidget
    widget.clear()
    classList = backend.returnClassList()

    for grade, classes in classList:
        item = QListWidgetItem(str(grade) + "학년 " + str(classes) + "반")
        widget.addItem(item)


def exlAddClassList(self):
    srcWidget = self.exlClassWidget
    targetWidget = self.exlAddedClassList
    if srcWidget.selectedItems() is not None:
        items = srcWidget.selectedItems()
        for item in items:
            newItem = QListWidgetItem(item.text())
            targetWidget.addItem(newItem)


def exlExtClassList(self):
    widget = self.exlAddedClassList
    if widget.currentItem() is not None:
        row = widget.currentRow()
        widget.takeItem(row)


def exlAllShowSubList(self):
    self.subjectGroups = []
    widget = self.exlSubWidget
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
            childSubjects = backend.returnChildSubjectsFromParentId(
                int(parentId))
            if len(childSubjects) == 0:
                it += 1
            for child in childSubjects:
                childId = int(child[0])
                childName = child[1]
                item = QTreeWidgetItem(it.value())
                item.setWhatsThis(0, str(childId))
                item.setText(0, childName)
        it += 1


def exlAddSubList(self):
    srcWidget = self.exlSubWidget
    targetWidget = self.exlAddedSubWidget
    if srcWidget.selectedItems() is not None:
        items = srcWidget.selectedItems()
        for item in items:
            if item.parent() is not None:  # 자식 노드이면
                parentItem = item.parent()
                parentName = parentItem.text(0)
                childName = item.text(0)
                childId = item.whatsThis(0)
                newItem = QListWidgetItem(
                    str(parentName) + " - " + str(childName))
                newItem.setWhatsThis(str(childId))
                targetWidget.addItem(newItem)
                
    self.originalAddedSubjects = getItemsFromQListWWidget(targetWidget)



def exlExtSubList(self):
    widget = self.exlAddedSubWidget
    if widget.currentItem() is not None:
        row = widget.currentRow()
        widget.takeItem(row)


def getItemsFromQListWWidget(listWidget: QListWidget) -> List[QListWidgetItem]:
    items: List[QListWidgetItem] = []
    for idx in range(listWidget.count()):
        items.append(listWidget.item(idx).clone())
    return items


def exlPrintMultiAsses(self):
    tabwidget = self.totalAssesTab
    tabwidget.clear()
    classList = []
    subjectList: List[dict] = []
    global dataFrameList
    global classTextList

    dataFrameList = []
    classTextList = []

    classListWidget: QListWidget = self.exlAddedClassList
    subjectListWidget: QListWidget = self.exlAddedSubWidget
    classListCnt: int = classListWidget.count()
    subjectListCnt: int = subjectListWidget.count()

    if classListCnt == 0 or subjectListCnt == 0:
        return

    classItems: List[QListWidgetItem] = getItemsFromQListWWidget(
        classListWidget)

    subjectItems: List[QListWidgetItem] = getItemsFromQListWWidget(
        subjectListWidget)

    for item in classItems:
        classText = item.text()
        classTextList.append(classText)
        grade, classes = returnClassInteger(classText)
        classList.append([grade, classes])

    # self.subjectGroups 리스트 안에 [{"groupName": "name", "subjectIds": ['12','13','14',...]}, ...]
    # 식으로 존재하니까 해당 자료 참조해서
    # 평가 항목을 먼저 생성하고 랜덤하게 몇개를 추출할지 선택해서 평가문 생성

    for item in subjectItems:
        if ">>" in item.text():
            subjectList.append({
                "isGroupSubject": True,
                "groupName": item.text(),
                "subjectId": int(item.whatsThis())
            })
        else:
            subjectList.append({
                "isGroupSubject": False,
                "subjectId": int(item.whatsThis())
            })

    for item in classList:
        grade, classes = item
        gradeList = []
        classList = []
        assesment = []
        contentLengthList = []
        classMemberList = backend.returnClassMemberName(
            int(grade), int(classes))
        studentNumberList = backend.returnClassMemberNumber(
            int(grade), int(classes))
        studentIdList = backend.returnClassMemberNumber(
            int(grade), int(classes))

        for i in range(0, len(studentNumberList)):
            num = str(studentNumberList[i])
            studentNumberList[i] = num[3:]

        for i in range(0, len(classMemberList)):
            gradeList.append(grade)
            classList.append(classes)
        rawData = {"학년": gradeList, "반": classList,
                   "번호": studentNumberList, "이름": classMemberList}

        for studentId in studentIdList:

            groupSubjectSelectList: List[int] = []

            for group in self.subjectGroups:
                subjectIds: List[int] = group["subjectIds"]
                selectedIds: List[int] = random.sample(
                    subjectIds, k=group["randomSelection"])
                for ids in selectedIds:
                    if ids not in groupSubjectSelectList:
                        groupSubjectSelectList.append(ids)

            assesText = ""
            tmpAsses = ["" for _ in range(self.exlAddedSubWidget.count())]
            i = 0

            for subject in subjectList:
                subjectId: int = subject["subjectId"]
                isGroupSubject: bool = subject["isGroupSubject"]
                if isGroupSubject == True:
                    if subjectId in groupSubjectSelectList:
                        data = backend.returnStudentAssesmentBySubId(
                            subjectId, studentId)
                        if data:
                            tmpAsses[i] = data[0]
                        else:
                            tmpAsses[i] == " "
                    i += 1
                else:
                    data = backend.returnStudentAssesmentBySubId(
                        subjectId, studentId)
                    if data:
                        tmpAsses[i] = data[0]
                    else:
                        tmpAsses[i] == " "
                    i += 1

            printAsses = ["" for _ in range(self.exlAddedSubWidget.count())]
            # 평가위치 셔플
            # 셔플할인덱스와 셔플안할인덱스를 분리하고 셔플 할 인덱스를 랜덤 순서 돌리고 인데스 별로 새로 평가문추가
            if self.assesmentShuffleCheckBox.isChecked():
                noShuffleIndex = []
                shuffleIndex = list(range(self.exlAddedSubWidget.count()))
                if self.exlAddedSubWidget.selectedItems() is not None:
                    items = self.exlAddedSubWidget.selectedItems()
                    for it in items:
                        noShuffleIndex.append(
                            self.exlAddedSubWidget.indexFromItem(it).row())

                    for rmi in noShuffleIndex:
                        shuffleIndex.remove(rmi)

                    tmpIndex = shuffleIndex[:]
                    random.shuffle(tmpIndex)

                    for j in range(len(noShuffleIndex)):
                        printAsses[noShuffleIndex[j]
                                   ] = tmpAsses[noShuffleIndex[j]]

                    for j in range(len(shuffleIndex)):
                        printAsses[tmpIndex[j]] = tmpAsses[shuffleIndex[j]]

            else:
                printAsses = tmpAsses

            for asses in printAsses:
                if asses != "":
                    if asses is None:
                        continue
                    asses = asses.strip()
                    # 줄바꿈모드 확인
                    if self.lineChangeCheckBox.isChecked():
                        assesText = assesText + "\n" + asses
                    else:
                        assesText = assesText + " " + asses

            assesText = assesText.strip()

            contentLength = len(assesText)
            contentLengthByte = len(assesText.encode("utf-8"))

            if self.lineChangeCheckBox.isChecked():
                for asses in assesText:
                    if "\n" in asses:
                        contentLength -= 1

            contentLengthList.append(str(contentLength) + " 자 (" +
                                     str(contentLengthByte) + " 바이트)")
            assesment.append(assesText)

        rawData["평가"] = assesment
        rawData["글자수(바이트)"] = contentLengthList

        df = DataFrame(rawData)
        dataFrameList.append(df)

    for df, classText in zip(dataFrameList, classTextList):
        tab = QWidget()
        model = PandasModel(df)
        view = QTableView(tab)
        view.setModel(model)
        header = view.horizontalHeader()
        header.setSectionResizeMode(GRADE_COL, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(CLASS_COL, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(STDNUM_COL, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(NAME_COL, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(ASSES_COL, QHeaderView.Stretch)
        header.setSectionResizeMode(LENGTH_COL, QHeaderView.ResizeToContents)
        tabwidget.addTab(view, classText)
