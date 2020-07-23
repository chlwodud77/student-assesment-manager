#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, backend, sqlite3, random
from PyQt5.QtWidgets import *
from PyQt5.Qt import QApplication, QClipboard
from PyQt5 import QtCore

#점수 입력 테이블 항목 선택 시 내용 표시 함수
def activateScoreEdit(self):
    focusedItem = self.classListWidget.currentItem()
    content = focusedItem.text()
    self.scoreAseEdit.setPlainText(content)
    
def copyContent(self, col):
    mimeType = 'application/x-qt-windows-mime;value="Csv"'
    clipboard = QApplication.clipboard()
    mimeData = clipboard.mimeData()
    if(mimeType in mimeData.formats()): # 엑셀에서 복사해온 텍스트인지 확인
        text = clipboard.text()
        content = text.split("\n")
        #복사해온 텍스트 행이 기존 테이블에 있는 행과 비교시 적거나 같을 때만 붙여넣기
        if(self.classListWidget.currentRow() == 0 and self.classListWidget.rowCount() >= len(content)-1): 
            for i in range(0, len(content)-1):
                item = QTableWidgetItem(str(content[i]))
                self.classListWidget.setItem(i, col, item)
            
#점수 입력 테이블 항목 선택 후 텍스트 편집기에서 편집해주는 함수
def changeScoreAse(self):
    focusedItem = self.classListWidget.currentItem()
    currentContent = self.scoreAseEdit.toPlainText()
    focusedItem.setText(currentContent)

#과목 선택 시 라벨에 선택 과목 표시 함수
def showSubClickedLabel(self):
    self.subClickedLabel.setText(self.scoreSubTreeWidget.currentItem().text(0))
    
#점수로 생성된 평가문 저장해주는 함수
def saveAssesment(self):
    buttonReply = QMessageBox.question(self, '알림', "생성된 과목 평가를 저장하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if buttonReply == QMessageBox.Yes:
        if(self.scoreSubTreeWidget.currentItem() is None):
            return QMessageBox.about(self, "오류", "과목을 선택해주세요.")
        if(self.scoreSubTreeWidget.currentItem() is not None and self.classListWidget.rowCount() == 0):
            return QMessageBox.about(self, "오류", "학급을 불러와주세요.")
        
        for row in range(0, self.classListWidget.rowCount()):
            if(self.classListWidget.item(row,2).whatsThis() != ""): #기존 스코어 존재
                asses = self.classListWidget.item(row,3).text()
                score = int(self.classListWidget.item(row,2).text())
                scoreId = int(self.classListWidget.item(row,2).whatsThis())
                stdId = int(self.classListWidget.item(row,1).text())
                subId = int(self.scoreSubTreeWidget.currentItem().whatsThis(0))
                
                if(backend.deleteScoreById(scoreId)): #기존 스코어 삭제 후
                    backend.saveScore(subId, stdId, score, asses) # 다시 재 저장.
            else: #기존에 스코어 존재 X
                if(self.classListWidget.item(row,2).whatsThis() == "" and self.classListWidget.item(row,2).text() != ""):
                    asses = self.classListWidget.item(row,3).text()
                    score = int(self.classListWidget.item(row,2).text())
                    stdId = int(self.classListWidget.item(row,1).text())
                    subId = int(self.scoreSubTreeWidget.currentItem().whatsThis(0))
                    backend.saveScore(subId, stdId, score, asses) # 새로 저장.
        QMessageBox.about(self, "결과", "점수 저장 성공.")
        showScoreList(self)
    
#점수, 평가 리스트 보여주는 함수
def showScoreList(self):
    scoreInfo = []
    subId = int(self.scoreSubTreeWidget.currentItem().whatsThis(0))
    stdId = []
    assesments = []
    for row in range(0, self.classListWidget.rowCount()):
        stdId.append(int(self.classListWidget.item(row,1).text()))
    
    for row in range(0, self.classListWidget.rowCount()):
        if(backend.returnScore(int(subId), int(stdId[row])) is not None):
            scoreInfo.append(backend.returnScore(int(subId), int(stdId[row])))
        else:
            scoreInfo.append(["","",""])
    
    for row in range(0, self.classListWidget.rowCount()):
        asses = []
        if(scoreInfo[row][2] is not ""):
            asses.append(scoreInfo[row][2])
        else:
            asses.append("")
        assesments.append(asses)

    for row in range(0, self.classListWidget.rowCount()):
        if(scoreInfo[row][1] != ""):
            self.classListWidget.setItem(row, 2, QTableWidgetItem(str(scoreInfo[row][1]))) #점수입력
            self.classListWidget.item(row,2).setWhatsThis(str(scoreInfo[row][0])) #점수 id 속성
        else:
            self.classListWidget.setItem(row, 2, QTableWidgetItem(""))

        if(assesments[row][0] != ""):
            self.classListWidget.setItem(row, 3, QTableWidgetItem(str(assesments[row][0]))) #평가입력
        else:
            self.classListWidget.setItem(row, 3, QTableWidgetItem(""))
            
#점수 등급별 랜덤 평가 생성 함수 (선택)
def insertIndiRandomAssesment(self):
    if(self.scoreSubTreeWidget.currentItem() is None):
        QMessageBox.about(self, "오류", "과목을 선택해주세요.")
        return
    grdAList = []
    grdBList = []
    grdCList = []
    subId = int(self.scoreSubTreeWidget.currentItem().whatsThis(0))
    grdStandard = backend.returnAssementStandardBySubId(subId)
    assementList = backend.returnAssesmentBySubId(subId)
    for i in range(0, len(assementList)):
        if(assementList[i][1] == "A"):
            p = []
            p.append(assementList[i][0])
            p.append(assementList[i][2])
            grdAList.append(p)
        elif(assementList[i][1] == "B"):
            p = []
            p.append(assementList[i][0])
            p.append(assementList[i][2])
            grdBList.append(p)
        elif(assementList[i][1] == "C"):
            p = []
            p.append(assementList[i][0])
            p.append(assementList[i][2])
            grdCList.append(p)
    
    items = []
    items = self.classListWidget.selectedItems()

    for i in range(0, len(items)):
        if(self.classListWidget.selectedItems()[i].column() is 2):
            row = self.classListWidget.selectedItems()[i].row()
            score = self.classListWidget.item(row,2).text()
            if(score == ""):
                self.classListWidget.setItem(row,3,QTableWidgetItem(""))
            else:
                for j in range(0, len(grdStandard)):
                    score = int(score)
                    if(grdStandard[j][1] < score and score <= grdStandard[j][2]):
                        if(grdStandard[j][0] == "A"):
                            randomIndex = random.randint(0, len(grdAList)-1)
                            self.classListWidget.setItem(row,3,QTableWidgetItem(grdAList[randomIndex][1]))
                        elif(grdStandard[j][0] == "B"):
                            randomIndex = random.randint(0, len(grdBList)-1)
                            self.classListWidget.setItem(row,3,QTableWidgetItem(grdBList[randomIndex][1]))
                        elif(grdStandard[j][0] == "C"):
                            randomIndex = random.randint(0, len(grdCList)-1)
                            self.classListWidget.setItem(row,3,QTableWidgetItem(grdCList[randomIndex][1]))

#점수 등급별 랜덤 평가 생성 함수 (전체)
def insertRandomAssesment(self):
    if(self.scoreSubTreeWidget.currentItem() is None):
        return QMessageBox.about(self, "오류", "과목을 선택해주세요.")
        
    grdAList = []
    grdBList = []
    grdCList = []
    subId = int(self.scoreSubTreeWidget.currentItem().whatsThis(0))
    grdStandard = backend.returnAssesmentStandardBySubId(subId)
    assementList = backend.returnAssesmentBySubId(subId)
    for i in range(0, len(assementList)):
        if(assementList[i][1] == "A"):
            p = []
            p.append(assementList[i][0])
            p.append(assementList[i][2])
            grdAList.append(p)
        elif(assementList[i][1] == "B"):
            p = []
            p.append(assementList[i][0])
            p.append(assementList[i][2])
            grdBList.append(p)
        elif(assementList[i][1] == "C"):
            p = []
            p.append(assementList[i][0])
            p.append(assementList[i][2])
            grdCList.append(p)

    for row in range(0, self.classListWidget.rowCount()):
        score = self.classListWidget.item(row,2).text()
        if(score == ""):
            self.classListWidget.setItem(row,3,QTableWidgetItem(""))
        else:
            for j in range(0, len(grdStandard)):
                score = int(score)
                if(grdStandard[j][1] < score and score <= grdStandard[j][2]):
                    if(grdStandard[j][0] == "A"):
                        randomIndex = random.randint(0, len(grdAList)-1)
                        self.classListWidget.setItem(row,3,QTableWidgetItem(grdAList[randomIndex][1]))
                    elif(grdStandard[j][0] == "B"):
                        randomIndex = random.randint(0, len(grdBList)-1)
                        self.classListWidget.setItem(row,3,QTableWidgetItem(grdBList[randomIndex][1]))
                    elif(grdStandard[j][0] == "C"):
                        randomIndex = random.randint(0, len(grdCList)-1)
                        self.classListWidget.setItem(row,3,QTableWidgetItem(grdCList[randomIndex][1]))

#학급 리스트 출력 함수
def insertClassComboBox(self, combobox):
    combobox.clear()
    classes = backend.returnClassList()
    for i in range(0, len(classes)):
        combobox.addItem(str(classes[i][0])+"학년 "+str(classes[i][1])+"반")
        
        
def returnClassInteger(classes):
    classes = classes.replace(" ","")
    grade, ban = classes.split("학년")
    ban = ban.replace("반","")
    return int(grade), int(ban)
    
        
#선택 학급 조회 함수    
def showClassMemberList(self):
    grade, classes = returnClassInteger(self.classList.currentText())     
    # grade = int(self.classList.currentText()[0])
    # classes = int(self.classList.currentText()[4])
    print(grade, classes)
    members = backend.returnClassMemberList(grade, classes) 
    headers = ["이름", "학번", "점수", "평가"]

    self.classListWidget.setRowCount(len(members))
    self.classListWidget.setColumnCount(4)
    self.classListWidget.setHorizontalHeaderLabels(headers)

    for i in range(0, len(members)):
        name = QTableWidgetItem(str(members[i][0]))
        stdId = QTableWidgetItem(str(members[i][1]))
        self.classListWidget.setItem(i, 0, name)
        self.classListWidget.setItem(i, 1, stdId)
    
    self.showScoreList()