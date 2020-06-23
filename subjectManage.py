#!/usr/bin/env python
# -*- coding: utf-8 -*-
import backend, sqlite3
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

def addNewSubjectItem(self):
    QTreeWidgetItem(self.subTreeWidget, ["새과목"])
    
def addChildSub(self):
    parentItem = self.subTreeWidget.currentItem()
    childItem = QTreeWidgetItem(parentItem)
    childItem.setText(0, "새항목")

#과목 리스트에서 과목 선택 조회 하면 과목 세부 내용 조회 함수
def searchSub(self):
    subTreeWidget = self.subTreeWidget
    if(subTreeWidget.currentItem() is None):
        return 
    clickedSubId = subTreeWidget.currentItem().whatsThis(0)
    if(clickedSubId == ''):
        clickedSubId = -1

    subId = int(clickedSubId)
    grdARng = []
    grdBRng = []
    grdCRng = []
    
    if(subId):
        #조회된 과목 등급 점수표 조회 및 출력
        grdARng = backend.returnAssesmetnStandardBySubIdAndGrade(subId,"A")
        grdBRng = backend.returnAssesmetnStandardBySubIdAndGrade(subId,"B")
        grdCRng = backend.returnAssesmetnStandardBySubIdAndGrade(subId,"C")

        if(len(grdARng) != 0):
            self.grdAEdit1.setText(str(grdARng[0][0]))
            self.grdAEdit2.setText(str(grdARng[0][1]))
        else:
            self.grdAEdit1.setText(str("없음"))
            self.grdAEdit2.setText(str("없음"))
        if(len(grdBRng) != 0):
            self.grdBEdit1.setText(str(grdBRng[0][0]))
            self.grdBEdit2.setText(str(grdBRng[0][1]))
        else:
            self.grdBEdit1.setText(str("없음"))
            self.grdBEdit2.setText(str("없음"))
        if(len(grdCRng) != 0):
            self.grdCEdit1.setText(str(grdCRng[0][0]))
            self.grdCEdit2.setText(str(grdCRng[0][1]))
        else:
            self.grdCEdit1.setText(str("없음"))
            self.grdCEdit2.setText(str("없음"))

        #조회된 과목 이름 및 평가 출력
        self.subTitleEdit.setText(self.subTreeWidget.currentItem().text(0))
        grdAAse = []
        grdBAse = []
        grdCAse = []
        grdAAse = backend.returnAssesmentContentBySubIdAndGrade(subId, "A")
        grdBAse = backend.returnAssesmentContentBySubIdAndGrade(subId, "B")
        grdCAse = backend.returnAssesmentContentBySubIdAndGrade(subId, "C")

        self.grdAAseList.setRowCount(len(grdAAse))
        self.grdAAseList.setColumnCount(1)
        self.grdBAseList.setRowCount(len(grdBAse))
        self.grdBAseList.setColumnCount(1)
        self.grdCAseList.setRowCount(len(grdCAse))
        self.grdCAseList.setColumnCount(1)

        for i in range(0, len(grdAAse)):
            self.grdAAseList.setItem(i, 0, QTableWidgetItem(grdAAse[i]))
        for i in range(0, len(grdBAse)):
            self.grdBAseList.setItem(i, 0, QTableWidgetItem(grdBAse[i]))
        for i in range(0, len(grdCAse)):
            self.grdCAseList.setItem(i, 0, QTableWidgetItem(grdCAse[i]))

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
    subTitleEdit = self.subTreeWidget.currentItem().text(0)
    grdAEdit1 = self.grdAEdit1.text()
    grdAEdit2 = self.grdAEdit2.text()
    grdBEdit1 = self.grdBEdit1.text()
    grdBEdit2 = self.grdBEdit2.text()
    grdCEdit1 = self.grdCEdit1.text()
    grdCEdit2 = self.grdCEdit2.text()

    grdAList = []
    grdBList = []
    grdCList = []

    for i in range (0,self.grdAAseList.rowCount()):
        for j in range (0,self.grdAAseList.columnCount()):
            grdAList.append(self.grdAAseList.item(i,j).text())

    for i in range (0,self.grdBAseList.rowCount()):
        for j in range (0,self.grdBAseList.columnCount()):
            grdBList.append(self.grdBAseList.item(i,j).text())

    for i in range (0,self.grdCAseList.rowCount()):
        for j in range (0,self.grdCAseList.columnCount()):
            grdCList.append(self.grdCAseList.item(i,j).text())

    conn = sqlite3.connect("studentManager.db")

    #기존 과목 없으면 새로 생성
    try:    
        subName = self.subTitleEdit.text()
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
                        backend.createAssesment(int(childSubId), "A", grdAList[i], int(grdAEdit1), int(grdAEdit2))
                    for i in range(0, len(grdBList)):
                        backend.createAssesment(int(childSubId), "B", grdBList[i], int(grdBEdit1), int(grdBEdit2))
                    for i in range(0, len(grdCList)):
                        backend.createAssesment(int(childSubId), "C", grdCList[i], int(grdCEdit1), int(grdCEdit2))

                else: #부모 노드일 경우
                    backend.createParentSubject(subName)
            else: # 기존에 있던 과목인 경우
                #기존 과목을 참조하여 평가지를 새로 생성 및 수정 (먼저 다 삭제했다가 다시 새로 생성)
                backend.deleteAssesmentBySubId(int(subId))
                
                for i in range(0, len(grdAList)):
                    backend.createAssesment(int(subId), "A", grdAList[i], int(grdAEdit1), int(grdAEdit2))
                for i in range(0, len(grdBList)):
                    backend.createAssesment(int(subId), "B", grdBList[i], int(grdBEdit1), int(grdBEdit2))
                for i in range(0, len(grdCList)):
                    backend.createAssesment(int(subId), "C", grdCList[i], int(grdCEdit1), int(grdCEdit2))
                    
            QMessageBox.about(self, "결과", "성공")
            
    except sqlite3.IntegrityError:
        print("문제 발생")
        QMessageBox.about(self, "오류", "실패")
    showSub(self, self.subTreeWidget)
    showSub(self, self.scoreSubTreeWidget)

def delSub(self):
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
        
    QMessageBox.about(self, "결과", "수정 완료. db에 반영하려면 저장 버튼 클릭!")

#평가 내용 선택하면 편집기에 해당 내용 보여줌
def activateEdit(self):
    focusedTab = self.grdAseWidget.currentIndex()
    if(focusedTab == 0):
        widget = self.grdAAseList
        self.grdAseEdit.setPlainText(widget.item(widget.currentRow(), widget.currentColumn()).text())

    elif(focusedTab == 1):
        widget = self.grdBAseList
        self.grdAseEdit.setPlainText(widget.item(widget.currentRow(), widget.currentColumn()).text())

    elif(focusedTab == 2):
        widget = self.grdCAseList
        self.grdAseEdit.setPlainText(widget.item(widget.currentRow(), widget.currentColumn()).text())
        
#평가 내용 항목 지우는 함수
def delAse(self):
    focusedTab = self.grdAseWidget.currentIndex()
    if(focusedTab == 0):
        row = self.grdAAseList.currentRow()
        col = self.grdAAseList.currentColumn()
        self.grdAAseList.removeRow(row)
    
    elif(focusedTab == 1):
        row = self.grdBAseList.currentRow()
        col = self.grdBAseList.currentColumn()
        self.grdBAseList.removeRow(row)

    elif(focusedTab == 2):
        row = self.grdCAseList.currentRow()
        col = self.grdCAseList.currentColumn()
        self.grdCAseList.removeRow(row)
        
    self.grdAseEdit.clear()
    QMessageBox.about(self, "결과", "삭제 완료. db에 반영하려면 저장 버튼 클릭!")
    
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
    QMessageBox.about(self, "결과", "추가 완료. db에 반영하려면 저장 버튼 클릭!")
    