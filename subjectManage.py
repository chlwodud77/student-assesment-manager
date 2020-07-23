#!/usr/bin/env python
# -*- coding: utf-8 -*-
import backend, sqlite3
from PyQt5.QtWidgets import *
from PyQt5.Qt import QApplication, QClipboard
from PyQt5 import QtCore
from operator import itemgetter

deleteAssesment = []
previousSubId = -1
previousStndId = -1
currentSubId = -1
currentStndId = -1

class subjectStore:
    def __init__(self):
        self.standard = []
        self.assesment = []

    def getStandard(self):
        return self.standard
    
    def addStandard(self, subId ="", grade="", greater="", less=""):
        # container = [subId, grade, greater, less]
        container = dict(subId=subId, grade=grade, greater=greater, less=less)
        if(container not in self.standard):
            self.standard.append(container)

    def modifyStandard(self, subId, grade, greater, less):
        pass
    
    def findAssesment(self, assesId):
        for asses in self.assesment:
            if(str(asses["assesId"]) == str(assesId)):
                return asses
            
    def findAssesmentBySubIdAndGrade(self, subId, grade):
        for asses in self.assesment:
            if(str(asses["subId"]) == str(subId) and str(asses["grade"]) == str(grade)):
                return asses
    
    def getAssesment(self):
        return self.assesment
    
    def addAssesment(self, assesId="", subId="", grade="", greater="", less="", content=""):
        # container = [assesId, subId, grade, greater, less, content]
        container = dict(assesId=assesId, subId=subId, grade=grade,
                        greater=greater, less=less, content=content)
        if(container not in self.assesment):
            self.assesment.append(container)
    
    def deleteAssesment(self, container):
        if(container in self.assesment):
            self.assesment.remove(container)
            print("assesments : ",self.assesment)
    
    def modifyAssesment(self, assesId, content):
        for asses in self.assesment:
            if(asses["assesId"] == assesId):
                asses["content"] = content
        print("assesments: ",self.assesment)
    
    def reset(self):
        self.standard = []

store = subjectStore()

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

def occurChange(self, row, column):
    pass

def showAssesment(self):
    global previousStndId, currentStndId
    List = self.grdStndList
    aseList = self.grdAseList
    stndName = self.grdAseScoreName
    stndGre = self.grdAseScoreGre
    stndLess = self.grdAseScoreLess
    clickedStndItem = List.currentItem()
    
    if(len(clickedStndItem.whatsThis().split(",")) == 4):
        subId, grade, greater, less = clickedStndItem.whatsThis().split(",")
        print(subId, grade)
        count = aseList.rowCount()
        
        stndName.setPlainText(grade)
        stndGre.setPlainText(greater)
        stndLess.setPlainText(less)
        for i in range(0, count):
            aseList.removeRow(0)
        
        assesments = backend.returnAssesmentContentBySubIdAndGrade(int(subId), grade)
        row = 0
        
        if(assesments is None):
            col = 0
            newAsses = store.findAssesmentBySubIdAndGrade(str(subId), str(grade))
            for asses in newAsses:
                aseList.insertRow(row)
                assesId = asses["assesId"]
                subId   = asses["subId"]
                grade   = asses["grade"]
                greater = asses["greater"]
                less    = asses["less"]
                content = asses["content"]
                # assesId, subId, grade, greater, less, content = asses
                item = QTableWidgetItem(content)
                item.setWhatsThis(str(assesId) + "," + str(subId) + "," + str(grade) 
                        + "," + str(greater) + "," + str(less))
                aseList.setItem(row, col, item)
                row += 1
                
        for assesment in assesments:
            isDeleted = False
            isExist = False
            col = 0
            assesId, content = assesment
            for delete in deleteAssesment:
                if(str(delete["assesId"]) == str(assesId)):
                    isDeleted = True
                    
            for asses in store.assesment:
                if(str(asses["assesId"]) == str(assesId)):
                    isExist = True
                    
            if(not isDeleted):
                if(isExist):
                    aseList.insertRow(row)
                    existAsses = store.findAssesment(str(assesId))
                    assesId = existAsses["assesId"]
                    subId   = existAsses["subId"]
                    grade   = existAsses["grade"]
                    greater = existAsses["greater"]
                    less    = existAsses["less"]
                    content = existAsses["content"]
                    # assesId, subId, grade, greater, less, content = existAsses
                    item = QTableWidgetItem(content)
                    item.setWhatsThis(str(assesId) + "," + str(subId) + "," + str(grade) 
                                    + "," + str(greater) + "," + str(less))
                    aseList.setItem(row, col, item)
                    row += 1
                else:
                    store.addAssesment(str(assesId), str(subId), str(grade), str(greater), str(less), str(content))
                    aseList.insertRow(row)
                    item = QTableWidgetItem(content)
                    item.setWhatsThis(str(assesId) + "," + str(subId) + "," + str(grade) 
                                    + "," + str(greater) + "," + str(less))
                    aseList.setItem(row, col, item)
                    row += 1
            
#과목 리스트에서 과목 선택 조회 하면 과목 세부 내용 조회 함수
def searchSub(self):
    subTreeWidget = self.subTreeWidget
    if(subTreeWidget.currentItem() is None):
        return 
    clickedSubId = subTreeWidget.currentItem().whatsThis(0)
    if(clickedSubId == ''):
        clickedSubId = -1
    global currentSubId, previousSubId
    previousSubId = currentSubId
    subId = int(clickedSubId)
    currentSubId = subId
    grdStndList = []
    
    if(subId):
        #조회된 과목 등급 점수표 조회 및 출력
        List = self.grdStndList
        grdStndList = self.grdStndList
        StndList = backend.returnAssesmentStandardBySubId(subId)
        StndList = sorted(StndList, key=itemgetter(1), reverse=True)
        # print(StndList)
        List.clear()
        
        for standard in StndList:
            subId, grade, greater, less = standard
            store.addStandard(str(subId), str(grade), str(greater), str(less))
        
        standards = store.getStandard()
        
        for stand in standards:
            if(stand["subId"] == str(subId)):
                subId   = stand["subId"]
                grade   = stand["grade"]
                greater = stand["greater"]
                less    = stand["less"]
                # subId, grade, greater, less = stand
                whats = str(subId) + "," + str(grade) + "," + str(greater) + "," + str(less)
                item = QListWidgetItem(grade)
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

                    for assesId in deleteAssesment:
                        backend.deleteAssesmentById(int(assesId))
                    for i in range(len(deleteAssesment)):
                        del deleteAssesment[0]

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
    assesList = self.grdAseList
    content = self.grdAseEdit.toPlainText()
    item = assesList.currentItem()
    
    if(item is None):
        return
    
    if(item.whatsThis()[0] != ""):
        assesId = item.whatsThis().split(",")[0]
        store.modifyAssesment(str(assesId), content)
        tempAsses = store.findAssesment(str(assesId))
        assesId = tempAsses["assesId"]
        subId   = tempAsses["subId"]
        grade   = tempAsses["grade"]
        greater = tempAsses["greater"]
        less    = tempAsses["less"]
        content = tempAsses["content"]
        # assesId, subId, grade, greater, less, content = store.findAssesment(str(assesId))
        item = QTableWidgetItem(content)
        item.setWhatsThis(str(assesId) + "," + str(subId) + "," + str(grade)
        + "," + str(greater) + "," + str(less) + "," + str(content))
        assesList.setItem(assesList.currentRow(), assesList.currentColumn(), item)
    else:
        assesList.setItem(assesList.currentRow(), assesList.currentColumn(), QTableWidgetItem(content))
        
#평가 내용 선택하면 편집기에 해당 내용 보여줌
def activateEdit(self):
    widget = self.grdAseList
    Editor = self.grdAseEdit
    Editor.setPlainText(widget.item(widget.currentRow(), widget.currentColumn()).text())

def addGrdStnd(self):
    List = self.grdStndList
    subId = self.subTreeWidget.currentItem().whatsThis(0)
    grade = self.grdAseScoreName.toPlainText()
    greater = self.grdAseScoreGre.toPlainText()
    less = self.grdAseScoreLess.toPlainText()
    if(grade != ""):
        whats = ""
        if(greater != "" and less != ""):
            if(int(greater) >= int(less)):
                return QMessageBox.about(self, "주의", "점수 범위 입력 오류.")
        whats = str(subId) + "," + str(grade) + "," + str(greater) + "," + str(less)
        item = QListWidgetItem(grade)
        item.setWhatsThis(whats)
        List.addItem(item)
        store.addStandard(str(subId), str(grade), str(greater), str(less))
    else:  
        return QMessageBox.about(self, "주의", "이름을 입력하세요.")
        
#평가 내용 항목 지우는 함수
def delAse(self):
    assesList = self.grdAseList
    row = assesList.currentRow()
    col = assesList.currentColumn()
    item = assesList.item(row,col)
    if(item is None):
        return
    if(item.whatsThis() not in deleteAssesment):
        assesId, subId, grade, greater, less, content = item.whatsThis().split(",")
        assesId, subId, grade, greater, less = item.whatsThis().split(",")
        if(assesId != ""):
            # container = [assesId, subId, grade, greater, less]
            container = dict(assesId=assesId, subId=subId, grade=grade,
                            greater=greater, less=less)
            if(container not in deleteAssesment):
                deleteAssesment.append(container)
            store.deleteAssesment(container)
        else:
            # container = [assesId, subId, grade, greater, less]
            container = dict(assesId=assesId, subId=subId, grade=grade,
                            greater=greater, less=less)
            store.deleteAssesment(container)
            
    assesList.removeRow(row)
    print("deleteAssesment: ",deleteAssesment)

    self.grdAseEdit.clear()
    
#평가 내용 추가 함수
def addAse(self):
    stndList = self.grdStndList
    assesList = self.grdAseList
    attributes = stndList.currentItem().whatsThis().split(",")
    subId, grade, greater, less = attributes
    assesId = ""
    content = self.grdAseEdit.toPlainText()
    row = assesList.rowCount()
    
    store.addAssesment(assesId, subId, grade, greater, less, content)
    item = QTableWidgetItem(content)
    item.setWhatsThis(str(assesId) + "," + str(subId) + "," + str(grade) 
                    + "," + str(greater) + "," + str(less) + "," + str(content))
    assesList.insertRow(row)
    assesList.setItem(row, 0, item)

    self.grdAseEdit.clear()