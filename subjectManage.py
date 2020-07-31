#!/usr/bin/env python
# -*- coding: utf-8 -*-
import backend, sqlite3, store
from PyQt5.QtWidgets import *
from PyQt5.Qt import QApplication, QClipboard
from PyQt5 import QtCore
from operator import itemgetter
from subjectInputDialog import SubjectInput
from subjectStandardModifyInputDialog import StandardModifyInput


# deleteAssesment = []


store = store.subjectStore()

def getTextFromSubjectInput():
    win = SubjectInput()
    r = win.showModal()
    if r:
        text = win.edit.text()
        return text

def addNewSubjectItem(self):
    subName = getTextFromSubjectInput()
    subId = backend.createParentSubject(subName)
    item = QTreeWidgetItem(self.subTreeWidget, [subName])
    item.setWhatsThis(0, str(subId))

def addChildSub(self):
    if(self.subTreeWidget.currentItem() is None):
        return QMessageBox.about(self, "주의", "하위 과목을 생성할 상위 과목을 선택해주세요.")
    if(self.subTreeWidget.currentItem().parent()):
        return QMessageBox.about(self, "주의", "하위 과목은 한개만 생성 가능합니다.")
    subName = getTextFromSubjectInput()
    parentItem = self.subTreeWidget.currentItem()
    parentItemSubId = parentItem.whatsThis(0)
    childSubId = backend.createChildSubject(subName, int(parentItemSubId))
    childItem  = QTreeWidgetItem(parentItem)
    childItem.setWhatsThis(0, str(childSubId))
    childItem.setText(0, subName)
    
def copyContent(self, obj):
    tableWidget = obj
    mimeType    = 'application/x-qt-windows-mime;value="Csv"'
    clipboard   = QApplication.clipboard()
    mimeData    = clipboard.mimeData()
    if(mimeType in mimeData.formats()): # 엑셀에서 복사해온 텍스트인지 확인
        text    = clipboard.text()
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
    List            = self.grdStndList
    aseList         = self.grdAseList
    stndName        = self.grdAseScoreName
    stndGre         = self.grdAseScoreGre
    stndLess        = self.grdAseScoreLess
    clickedStndItem = List.currentItem()
    deleteAssesment = store.getDeleteAssesment()
    
    if(clickedStndItem.whatsThis() is not None):
        stndId = int(clickedStndItem.whatsThis())
        grade, greater, less = backend.returnStandardById(stndId)
        count = aseList.rowCount()
        
        
        stndName.setText(grade)
        stndGre.setText(str(greater))
        stndLess.setText(str(less))
        return
        for i in range(0, count):
            aseList.removeRow(0)
        
        
        assesments = backend.returnAssesmentContentBySubIdAndGrade(int(subId), grade)
        row        = 0
        col        = 0
        for assesment in assesments:
            storedAssesment = store.getAssesment()
            isDeleted = False
            isExist   = False
            col       = 0
            assesId, content = assesment
            for delete in deleteAssesment:
                if(str(delete["assesId"]) == str(assesId)):
                    isDeleted = True
                    
            for asses in storedAssesment:
                if(str(asses["assesId"]) == str(assesId)):
                    isExist = True
                    
            if(not isDeleted):
                if(isExist):
                    existAsses = store.findAssesment(str(assesId))
                    assesId    = existAsses["assesId"]
                    subId      = existAsses["subId"]
                    grade      = existAsses["grade"]
                    greater    = existAsses["greater"]
                    less       = existAsses["less"]
                    content    = existAsses["content"]
                    aseList.insertRow(row)
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
                    
        newAssesment = store.getNewAssesment()
        for asses in newAssesment:
            newAssesId = asses["assesId"]
            newAssesSubId = asses["subId"]
            newAssesGrade = asses["grade"]
            newAssesGreater = asses["greater"]
            newAssesLess = asses["less"]
            newAssesContent = asses["content"]
            if(int(newAssesSubId) == int(subId) and newAssesGrade == grade):
                aseList.insertRow(row)
                item = QTableWidgetItem(newAssesContent)
                item.setWhatsThis(str(newAssesId) + "," + str(newAssesSubId) + "," + str(newAssesGrade) 
                                + "," + str(newAssesGreater) + "," + str(newAssesLess))
                aseList.setItem(row, col, item)
                row += 1

def resetStndInfoLabel(self):
    self.grdAseScoreName.setText("")
    self.grdAseScoreGre.setText("")
    self.grdAseScoreLess.setText("")

#과목 리스트에서 과목 선택 조회 하면 과목 세부 내용 조회 함수
def searchSub(self):
    # store.reset()
    resetStndInfoLabel(self)
    subTreeWidget = self.subTreeWidget
    if(subTreeWidget.currentItem() is None):
        return 
    clickedSubId = subTreeWidget.currentItem().whatsThis(0)
    if(clickedSubId == ''):
        clickedSubId = -1
    subId         = int(clickedSubId)
    grdStndList   = []
    
    if(subId):
        #조회된 과목 등급 점수표 조회 및 출력
        List        = self.grdStndList
        StndList    = backend.returnStandardBySubId(int(subId))
        StndList    = sorted(StndList, key=itemgetter(2))
        # print(StndList)
        List.clear()
        
        for standard in StndList:
            # store.addStandard(str(subId), str(grade), str(greater), str(less))
            stndId, subId, grade, greater, less = standard
            # whats = str(stndId) + "," + str(subId) + "," + str(grade) + "," + str(greater) + "," + str(less)
            whats = str(stndId)
            item  = QListWidgetItem(grade)
            item.setWhatsThis(whats)
            List.addItem(item)
        # standards = store.getStandard()
        
        # for stand in standards:
        #     if(stand["subId"] == str(subId)):
        #         subId   = stand["subId"]
        #         grade   = stand["grade"]
        #         greater = stand["greater"]
        #         less    = stand["less"]
        #         whats = str(subId) + "," + str(grade) + "," + str(greater) + "," + str(less)
        #         item  = QListWidgetItem(grade)
        #         item.setWhatsThis(whats)
        #         List.addItem(item)

def showSub(self, treeWidget):
    subList       = backend.returnSubList()
    subTreeWidget = treeWidget
    subTreeWidget.clear()
    subTreeWidget.setColumnCount(1)
    subTreeWidget.setHeaderLabels(["과목"])

    for i in range (0, len(subList)):
        if(subList[i][2] is None):
            subId      = subList[i][0]
            subName    = subList[i][1]
            parentItem = QTreeWidgetItem(subTreeWidget, [subName])
            parentItem.setWhatsThis(0,str(subId))

    for i in range(0, len(subList)):
        if(subList[i][2] is not None):
            subId     = subList[i][0]
            subName   = backend.returnSubNameBySubId(subList[i][2])
            childName = subList[i][1]
            parentId  = subList[i][2]
            it = QTreeWidgetItemIterator(subTreeWidget)
            while it.value():
                if it.value() is not None and int(it.value().whatsThis(0)) == int(parentId):
                    childItem = QTreeWidgetItem(it.value())
                    childItem.setWhatsThis(0,str(subId))
                    childItem.setText(0,childName)
                it += 1
                
#과목, 평가 등급 점수, 평가 내용 db 저장 함수
def saveSub(self):
    deleteAssesment = store.getDeleteAssesment()
    assesments      = store.getAssesment()
    newAssesments   = store.getNewAssesment()
    standards       = store.getStandard()
    
    buttonReply = QMessageBox.question(self, '알림', "과목 상세 정보를 저장하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if buttonReply == QMessageBox.Yes:
        if(self.subTreeWidget.currentItem() is None):
            return QMessageBox.about(self, "주의", "정보를 저장할 과목을 선택하세요.")

        #기존 과목 없으면 새로 생성
        try:    
            subName = self.subTreeWidget.currentItem().text(0)
            subId = self.subTreeWidget.currentItem().whatsThis(0)

            if(not subName):
                QMessageBox.about(self, "오류", "과목을 입력하세요")
            else:
                # if(subId == ''): # 기존에 없던 과목인 경우
                #     if(self.subTreeWidget.currentItem().parent()): #하위 노드일 경우
                #         parentItemSubId = self.subTreeWidget.currentItem().parent().whatsThis(0)
                #         if(parentItemSubId == "" ):
                #             return QMessageBox.about(self, "주의", "상위과목을 먼저 저장해주세요.")

                #         parent = self.subTreeWidget.currentItem().parent()
                #         parentName = parent.text(0)
                #         parentId = parent.whatsThis(0)
                #         backend.createChildSubject(subName, int(parentId))
                #         childSubId = backend.returnChildSubjectId(subName, int(parentId))
                #         backend.deleteAssesmentBySubId(int(childSubId))
                #         for asses in newAssesments:
                #             assesSubId   = asses["subId"]
                #             grade   = asses["grade"]
                #             content = asses["content"]
                #             greater = asses["greater"]
                #             less    = asses["less"]
                #             backend.createAssesment(int(assesSubId), grade, content, int(greater), int(less))
                        
                #     else: #부모 노드일 경우
                #         backend.createParentSubject(subName)
                # else: # 기존에 있던 과목인 경우
                if(subId != ""):
                    backend.updateSubNameBySubId(int(subId), subName)
                    
                    for asses in deleteAssesment: # 삭제할 평가 수행
                        assesId = int(asses["assesId"])
                        backend.deleteAssesmentById(assesId)
                            
                    for asses in newAssesments: # 추가된 새로운 평가 생성
                        assesSubId   = asses["subId"]
                        grade   = asses["grade"]
                        content = asses["content"]
                        greater = asses["greater"]
                        less    = asses["less"]
                        backend.createAssesment(int(assesSubId), grade, content, int(greater), int(less))
                        
                    for asses in store.findAssesmentsBySubId(subId): #기존 평가 업데이트
                        assesId = asses["assesId"]
                        grade   = asses["grade"]
                        greater = asses["greater"]
                        less    = asses["less"]
                        content = asses["content"]
                        backend.updateAssesment(int(assesId), content, int(greater), int(less))
                    
                        
                QMessageBox.about(self, "결과", "성공")
                self.grdAseEdit.clear()
                store.reset()
                
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
    
    if(item.whatsThis() is not None):
        assesId = item.whatsThis().split(",")[0]
        if(assesId == ""):
            originAssesContent = item.text()
            newContent = content
            originAssesId, originAssesSubId, originAssesGrade, originAssesGreater, originAssesLess = item.whatsThis().split(",")
            store.modifyNewAssesment(originAssesSubId, originAssesGrade, originAssesContent, newContent)
            showAssesment(self)
        else:
            store.modifyAssesment(str(assesId), content)
            tempAsses = store.findAssesment(str(assesId))
            assesId = tempAsses["assesId"]
            subId   = tempAsses["subId"]
            grade   = tempAsses["grade"]
            greater = tempAsses["greater"]
            less    = tempAsses["less"]
            content = tempAsses["content"]
            item = QTableWidgetItem(content)
            item.setWhatsThis(str(assesId) + "," + str(subId) + "," + str(grade)
                                + "," + str(greater) + "," + str(less))
            assesList.setItem(assesList.currentRow(), assesList.currentColumn(), item)
    else:
        assesList.setItem(assesList.currentRow(), assesList.currentColumn(), QTableWidgetItem(content))
        
#평가 내용 선택하면 편집기에 해당 내용 보여줌
def activateEdit(self):
    widget = self.grdAseList
    Editor = self.grdAseEdit
    Editor.setPlainText(widget.item(widget.currentRow(), widget.currentColumn()).text())

def addGrdStndRow(self):
    widget = self.grdStndAddWidget
    widget.insertRow(widget.rowCount())

def getListFromQTableWidget(self, widget):
    tableList = []
    totalRows = widget.rowCount()
    totalCols = widget.columnCount()
    
    for row in range(0, totalRows):
        content = []
        for col in range(0, totalCols):
            if(widget.item(row, col) is None):
                return False
            colItem = widget.item(row, col).text()
            content.append(colItem)
        tableList.append(content)
    
    return tableList

def clearGrdStndAddWidget(self):
    while(self.grdStndAddWidget.rowCount() != 0):
        self.grdStndAddWidget.removeRow(0)
    
def addGrdStnd(self):
    List = self.grdStndList
    if(self.subTreeWidget.currentItem() is None):
        return QMessageBox.about(self, "주의", "등급을 추가할 과목을 선택하세요.")
    tableList = getListFromQTableWidget(self, self.grdStndAddWidget)
    if(not tableList):
        return QMessageBox.about(self, "주의", "등급 내용을 모두 채워주세요.")
    
    subId     = self.subTreeWidget.currentItem().whatsThis(0)
    for content in tableList:
        grade, greater, less = content
        if(grade != ""):
            whats = ""
            if(greater != "" and less != ""):
                if(int(greater) >= int(less)):
                    return QMessageBox.about(self, "주의", "점수 범위 입력 오류.")
            # whats = str(subId) + "," + str(grade) + "," + str(greater) + "," + str(less)
            item = QListWidgetItem(grade)
            # item.setWhatsThis(whats)
            List.addItem(item)
            # store.addStandard(str(subId), str(grade), str(greater), str(less))
            backend.createStandard(int(subId), grade, int(greater), int(less))
        else:
            return QMessageBox.about(self, "주의", "이름을 입력하세요.")
        
    searchSub(self)
    clearGrdStndAddWidget(self)
        
def delGrdStnd(self):
    buttonReply = QMessageBox.question(self, '알림', "등급 기준을 삭제하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if buttonReply == QMessageBox.Yes:
        widget = self.grdStndList
        clickedItem = widget.currentItem()
        stndId = int(clickedItem.whatsThis())
        backend.deleteStandradById(stndId)
        searchSub(self)
        return QMessageBox.about(self, "알림", "등급 기준 삭제완료.")
    
def modGrdStnd(self):
    if(self.grdStndList.currentItem() is None):
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
        backend.updateStandard(int(stndId), name, int(greater), int(less))
        searchSub(self)
        return QMessageBox.about(self, "알림", "등급 기준 수정완료.")

# def addGrdStnd(self):
    # List = self.grdStndList
    # if(self.subTreeWidget.currentItem() is None):
    #     return QMessageBox.about(self, "주의", "등급을 추가할 과목을 선택하세요.")
    # tableList = getListFromQTableWidget(self.grdStndAddWidget)
    # return print(tableList)
    # subId = self.subTreeWidget.currentItem().whatsThis(0)
    # grade = self.grdAseScoreName.toPlainText()
    # greater = self.grdAseScoreGre.toPlainText()
    # less = self.grdAseScoreLess.toPlainText()
    # if(grade != ""):
    #     whats = ""
    #     if(greater != "" and less != ""):
    #         if(int(greater) >= int(less)):
    #             return QMessageBox.about(self, "주의", "점수 범위 입력 오류.")
    #     whats = str(subId) + "," + str(grade) + "," + str(greater) + "," + str(less)
    #     item = QListWidgetItem(grade)
    #     item.setWhatsThis(whats)
    #     List.addItem(item)
    #     store.addStandard(str(subId), str(grade), str(greater), str(less))
    # else:  
    #     return QMessageBox.about(self, "주의", "이름을 입력하세요.")
        
#평가 내용 항목 지우는 함수
def delAse(self):
    assesList = self.grdAseList
    row = assesList.currentRow()
    col = assesList.currentColumn()
    item = assesList.item(row,col)
    if(item is None):
        return
    
    assesId = item.whatsThis().split(",")[0]
    
    assesId, subId, grade, greater, less = item.whatsThis().split(",")
    content = item.text()
    
    if(assesId == ""):
        store.delNewAsssesment(assesId, subId, grade, greater, less, content)
    else:
        container = dict(assesId=assesId, subId=subId, grade=grade,
                            greater=greater, less=less)
        store.delAssesment(container)
        store.addDeleteAssesment(container)
                
    assesList.removeRow(row)
    showAssesment(self)
    self.grdAseEdit.clear()
    
#평가 내용 추가 함수
def addAse(self):
    stndList = self.grdStndList
    assesList = self.grdAseList
    if(stndList.currentItem() is None):
        return QMessageBox.about(self, "주의", "평가를 추가할 과목 또는 등급을 선택해주세요.")
    attributes = stndList.currentItem().whatsThis().split(",")
    subId, grade, greater, less = attributes
    assesId = ""
    content = self.grdAseEdit.toPlainText()
    row = assesList.rowCount()
    container = dict(assesId="", subId=subId, grade=grade,
                    greater=greater, less=less, content=content)
    store.addnewAssesment(container)
    showAssesment(self)
    self.grdAseEdit.clear()