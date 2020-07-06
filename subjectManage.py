#!/usr/bin/env python
# -*- coding: utf-8 -*-
import backend, sqlite3
from PyQt5.QtWidgets import *
from PyQt5.Qt import QApplication, QClipboard
from PyQt5 import QtCore
from operator import itemgetter

deleteAssesId = []

def addNewSubjectItem(self):
    QTreeWidgetItem(self.subTreeWidget, ["새과목"])
    
def addChildSub(self):
    if(self.subTreeWidget.currentItem().parent()):
        return QMessageBox.about(self, "주의", "하위 과목은 한개만 생성 가능합니다.")
    parentItem = self.subTreeWidget.currentItem()
    childItem = QTreeWidgetItem(parentItem)
    childItem.setText(0, "새항목")
    
def copyContent(self, obj):
    tableWidget = obj
    mimeType = 'application/x-qt-windows-mime;value="Csv"'
    clipboard = QApplication.clipboard()
    mimeData = clipboard.mimeData()
    if(mimeType in mimeData.formats()): # 엑셀에서 복사해온 텍스트인지 확인
        text = clipboard.text()
        content = text.split("\n")
        if(obj.rowCount() == 0):
            for i in range(0, len(content)-1):
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
    aseList = self.grdAseList
    stndName = self.grdAseScoreName
    stndGre = self.grdAseScoreGre
    stndLess = self.grdAseScoreLess
    clickedStndItem = List.currentItem()
    if(len(clickedStndItem.whatsThis().split(",")) == 4):
        subId, grade, greater, less = clickedStndItem.whatsThis().split(",")
        count = aseList.rowCount()
        
        stndName.setPlainText(grade)
        stndGre.setPlainText(greater)
        stndLess.setPlainText(less)
        for i in range(0, count):
            aseList.removeRow(0)
        
        assesments = backend.returnAssesmentContentBySubIdAndGrade(int(subId), grade)
        row = 0
        for assesment in assesments:
            col = 0
            content = assesment[1]
            aseList.insertRow(row)
            item = QTableWidgetItem(content)
            aseList.setItem(row, col, item)
            row += 1
            
    elif(len(clickedStndItem.whatsThis().split(",")) == 2):
        greater, less = clickedStndItem.whatsThis().split(",")
        count = aseList.rowCount()
        grade = List.currentItem().text()
        stndName.setPlainText(grade)
        stndGre.setPlainText(greater)
        stndLess.setPlainText(less)
        for i in range(0, count):
            aseList.removeRow(0)
            
#과목 리스트에서 과목 선택 조회 하면 과목 세부 내용 조회 함수
def searchSub(self):
    subTreeWidget = self.subTreeWidget
    if(subTreeWidget.currentItem() is None):
        return 
    clickedSubId = subTreeWidget.currentItem().whatsThis(0)
    if(clickedSubId == ''):
        clickedSubId = -1

    subId = int(clickedSubId)
    grdStndList = []
    
    if(subId):
        #조회된 과목 등급 점수표 조회 및 출력
        List = self.grdStndList
        grdStndList = self.grdStndList
        StndList = backend.returnAssesmentStandardBySubId(subId)
        StndList = sorted(StndList, key=itemgetter(1), reverse=True)
        print(StndList)
        List.clear()
        
        for standard in StndList:
            subId, name, greater, less = standard
            whats = str(subId) + "," + str(name) + "," + str(greater) + "," + str(less)
            item = QListWidgetItem(name)
            item.setWhatsThis(whats)
            List.addItem(item)

def showSub(self, treeWidget):
    subList = backend.returnSubList()
    subTreeWidget = treeWidget
    subTreeWidget.clear()
    subTreeWidget.setColumnCount(1)
    subTreeWidget.setHeaderLabels(["과목"])

    for i in range (0, len(subList)):
        if(subList[i][2] is None):
            subId = subList[i][0]
            subName = subList[i][1]
            parentItem = QTreeWidgetItem(subTreeWidget, [subName])
            parentItem.setWhatsThis(0,str(subId))

    for i in range(0, len(subList)):
        if(subList[i][2] is not None):
            subId = subList[i][0]
            subName = backend.returnSubNameBySubId(subList[i][2])
            childName = subList[i][1]
            parentId = subList[i][2]
            it = QTreeWidgetItemIterator(subTreeWidget)
            while it.value():
                if it.value() is not None and int(it.value().whatsThis(0)) == int(parentId):
                    childItem = QTreeWidgetItem(it.value())
                    childItem.setWhatsThis(0,str(subId))
                    childItem.setText(0,childName)
                it += 1
                
#과목, 평가 등급 점수, 평가 내용 db 저장 함수
def saveSub(self):
    buttonReply = QMessageBox.question(self, '알림', "과목 상세 정보를 저장하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if buttonReply == QMessageBox.Yes:
        if(self.subTreeWidget.currentItem() is None):
            return QMessageBox.about(self, "주의", "정보를 저장할 과목을 선택하세요.")

        subTitleEdit = self.subTreeWidget.currentItem().text(0)
        grdAEdit1 = self.grdAEdit1.text()
        grdAEdit2 = self.grdAEdit2.text()
        grdBEdit1 = self.grdBEdit1.text()
        grdBEdit2 = self.grdBEdit2.text()
        grdCEdit1 = self.grdCEdit1.text()
        grdCEdit2 = self.grdCEdit2.text()

        if(self.subTreeWidget.currentItem().parent()):
            if("" in [grdAEdit1, grdAEdit2, grdBEdit1, grdBEdit2, grdCEdit1, grdCEdit2]):
                return QMessageBox.about(self, "주의", "과목의 평가 기준 점수를 입력하세요.")

        grdAList = []
        grdBList = []
        grdCList = []

        for i in range (0,self.grdAAseList.rowCount()):
            for j in range (0,self.grdAAseList.columnCount()):
                grdAList.append(self.grdAAseList.item(i,j))

        for i in range (0,self.grdBAseList.rowCount()):
            for j in range (0,self.grdBAseList.columnCount()):
                grdBList.append(self.grdBAseList.item(i,j))

        for i in range (0,self.grdCAseList.rowCount()):
            for j in range (0,self.grdCAseList.columnCount()):
                grdCList.append(self.grdCAseList.item(i,j))

        #기존 과목 없으면 새로 생성
        try:    
            subName = self.subTreeWidget.currentItem().text(0)
            subId = self.subTreeWidget.currentItem().whatsThis(0)

            if(not subName):
                QMessageBox.about(self, "오류", "과목을 입력하세요")
            else:
                if(subId == ''): # 기존에 없던 과목인 경우
                    if(self.subTreeWidget.currentItem().parent()): #하위 노드일 경우
                        parent = self.subTreeWidget.currentItem().parent()
                        parentName = parent.text(0)
                        parentId = parent.whatsThis(0)
                        backend.createChildSubject(subName, int(parentId))
                        childSubId = backend.returnChildSubjectId(subName, int(parentId))
                        backend.deleteAssesmentBySubId(int(childSubId))
                        
                        for i in range(0, len(grdAList)):
                            backend.createAssesment(int(childSubId), "A", grdAList[i].text(), int(grdAEdit1), int(grdAEdit2))
                        for i in range(0, len(grdBList)):
                            backend.createAssesment(int(childSubId), "B", grdBList[i].text(), int(grdBEdit1), int(grdBEdit2))
                        for i in range(0, len(grdCList)):
                            backend.createAssesment(int(childSubId), "C", grdCList[i].text(), int(grdCEdit1), int(grdCEdit2))

                    else: #부모 노드일 경우
                        backend.createParentSubject(subName)
                else: # 기존에 있던 과목인 경우
                    backend.updateSubNameBySubId(int(subId), subName)

                    for assesId in deleteAssesId:
                        backend.deleteAssesmentById(int(assesId))
                    for i in range(len(deleteAssesId)):
                        del deleteAssesId[0]

                    for i in range(0, len(grdAList)):
                        if(grdAList[i].whatsThis() != ""):
                            assesId = grdAList[i].whatsThis()
                            backend.updateAssesment(int(assesId), grdAList[i].text(), int(grdAEdit1), int(grdAEdit2))
                        else:
                            backend.createAssesment(int(subId), "A", grdAList[i].text(), int(grdAEdit1), int(grdAEdit2))
                    for i in range(0, len(grdBList)):
                        if(grdBList[i].whatsThis() != ""):
                            assesId = grdBList[i].whatsThis()
                            backend.updateAssesment(int(assesId), grdBList[i].text(), int(grdBEdit1), int(grdBEdit2))
                        else:
                            backend.createAssesment(int(subId), "B", grdBList[i].text(), int(grdBEdit1), int(grdBEdit2))
                    for i in range(0, len(grdCList)):
                        if(grdCList[i].whatsThis() != ""):
                            assesId = grdCList[i].whatsThis()
                            backend.updateAssesment(int(assesId), grdCList[i].text(), int(grdCEdit1), int(grdCEdit2))
                        else:
                            backend.createAssesment(int(subId), "C", grdCList[i].text(), int(grdCEdit1), int(grdCEdit2))
                        
                QMessageBox.about(self, "결과", "성공")
                
        except sqlite3.IntegrityError:
            print("문제 발생")
            QMessageBox.about(self, "오류", "실패")
        showSub(self, self.subTreeWidget)
        showSub(self, self.scoreSubTreeWidget)

def delSub(self):
    buttonReply = QMessageBox.question(self, '알림', "선택 과목을 삭제하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if buttonReply == QMessageBox.Yes:
        clickedItem = self.subTreeWidget.currentItem()
        if(clickedItem is None):
            QMessageBox.about(self, "결과", "삭제할 과목을 선택해주세요.")
            return
        if(clickedItem.whatsThis(0) == ''):
            self.subTreeWidget.removeItemWidget(clickedItem,0)
            showSub(self, self.subTreeWidget)
        else:
            clickedSubId = int(clickedItem.whatsThis(0))
            if(backend.deleteSubById(clickedSubId)):
                QMessageBox.about(self, "결과", "삭제 성공")   
            else:
                QMessageBox.about(self, "결과", "삭제 실패")
        showSub(self, self.subTreeWidget)
        showSub(self, self.scoreSubTreeWidget)

# 평가 내용 수정 함수
def modAse(self):
    focusedTab = self.grdAseWidget.currentIndex()
    if(focusedTab == 0):
        widget = self.grdAAseList
        content = self.grdAseEdit.toPlainText()
        widget.setItem(widget.currentRow(), widget.currentColumn(), QTableWidgetItem(content))

    elif(focusedTab == 1):
        widget = self.grdBAseList
        content = self.grdAseEdit.toPlainText()
        widget.setItem(widget.currentRow(), widget.currentColumn(), QTableWidgetItem(content))

    elif(focusedTab == 2):
        widget = self.grdCAseList
        content = self.grdAseEdit.toPlainText()
        widget.setItem(widget.currentRow(), widget.currentColumn(), QTableWidgetItem(content))
        
#평가 내용 선택하면 편집기에 해당 내용 보여줌
def activateEdit(self):
    widget = self.grdAseList
    Editor = self.grdAseEdit
    Editor.setPlainText(widget.item(widget.currentRow(), widget.currentColumn()).text())

def addGrdStnd(self):
    List = self.grdStndList
    customName = self.grdAseScoreName.toPlainText()
    greater = self.grdAseScoreGre.toPlainText()
    less = self.grdAseScoreLess.toPlainText()
    if(customName != ""):
        whats = ""
        if(greater != "" and less != ""):
            if(int(greater) >= int(less)):
                return QMessageBox.about(self, "주의", "점수 범위 입력 오류.")
        whats = greater + "," + less
        item = QListWidgetItem(customName)
        item.setWhatsThis(whats)
        List.addItem(item)
    else:  
        return QMessageBox.about(self, "주의", "이름을 입력하세요.")
        
#평가 내용 항목 지우는 함수
def delAse(self):
    focusedTab = self.grdAseWidget.currentIndex()
    if(focusedTab == 0):
        row = self.grdAAseList.currentRow()
        col = self.grdAAseList.currentColumn()
        selectedItem = self.grdAAseList.item(row,col)
        if(selectedItem is None):
            return
        if(selectedItem.whatsThis() != ""):
            if(selectedItem.whatsThis() not in deleteAssesId):
                deleteAssesId.append(selectedItem.whatsThis())
        self.grdAAseList.removeRow(row)
    
    elif(focusedTab == 1):
        row = self.grdBAseList.currentRow()
        col = self.grdBAseList.currentColumn()
        selectedItem = self.grdBAseList.item(row,col)
        if(selectedItem is None):
            return
        if(selectedItem.whatsThis() != ""):
            if(selectedItem.whatsThis() not in deleteAssesId):
                deleteAssesId.append(selectedItem.whatsThis())
        self.grdBAseList.removeRow(row)

    elif(focusedTab == 2):
        row = self.grdCAseList.currentRow()
        col = self.grdCAseList.currentColumn()
        selectedItem = self.grdCAseList.item(row,col)
        if(selectedItem is None):
            return
        if(selectedItem.whatsThis() != ""):
            if(selectedItem.whatsThis() not in deleteAssesId):
                deleteAssesId.append(selectedItem.whatsThis())
        self.grdCAseList.removeRow(row)
        
    self.grdAseEdit.clear()
    
#평가 내용 추가 함수
def addAse(self):
    focusedTab = self.grdAseWidget.currentIndex()
    content = self.grdAseEdit.toPlainText()
    item = QTableWidgetItem(content)
            
    if(focusedTab == 0):
        currentRowCnt = self.grdAAseList.rowCount()
        if(currentRowCnt == 0):
            self.grdAAseList.insertRow(currentRowCnt)
            self.grdAAseList.setItem(currentRowCnt, 0, item)
        else:
            self.grdAAseList.insertRow(currentRowCnt)
            self.grdAAseList.setItem(currentRowCnt, 0, item)
    elif(focusedTab == 1):
        currentRowCnt = self.grdBAseList.rowCount()
        if(currentRowCnt == 0):
            self.grdBAseList.insertRow(currentRowCnt)
            self.grdBAseList.setItem(currentRowCnt, 0, item)
        else:
            self.grdBAseList.insertRow(currentRowCnt)
            self.grdBAseList.setItem(currentRowCnt, 0, item)
    elif(focusedTab == 2):
        currentRowCnt = self.grdCAseList.rowCount()
        if(currentRowCnt == 0):
            self.grdCAseList.insertRow(currentRowCnt)
            self.grdCAseList.setItem(currentRowCnt, 0, item)
        else:
            self.grdCAseList.insertRow(currentRowCnt)
            self.grdCAseList.setItem(currentRowCnt, 0, item)
    
    self.grdAseEdit.clear()
    