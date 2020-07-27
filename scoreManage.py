#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, backend, sqlite3, random
from PyQt5.QtWidgets import *
from PyQt5.Qt import QApplication, QClipboard
from PyQt5 import QtCore

#점수 입력 테이블 항목 선택 시 내용 표시 함수
def activateScoreEdit(self):
    focusedItem = self.classListWidget.currentItem()
    content     = focusedItem.text()
    self.scoreAseEdit.setPlainText(content)
    
def copyContent(self, col):
    mimeType  = 'application/x-qt-windows-mime;value="Csv"'
    clipboard = QApplication.clipboard()
    mimeData  = clipboard.mimeData()
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
    focusedItem    = self.classListWidget.currentItem()
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
                asses   = self.classListWidget.item(row,3).text()
                score   = int(self.classListWidget.item(row,2).text())
                scoreId = int(self.classListWidget.item(row,2).whatsThis())
                stdId   = int(self.classListWidget.item(row,1).text())
                subId   = int(self.scoreSubTreeWidget.currentItem().whatsThis(0))
                
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
    
def returnGradeAssesments(assesments, grade):
    parsedAssesments = []
    for asses in assesments:
        assesGrade   = asses[1]
        assesContent = asses[2]
        if(assesGrade == grade):
            parsedAssesments.append(assesContent)
    return parsedAssesments
    
#점수, 평가 리스트 보여주는 함수
def showScoreList(self):
    scoreInfo  = []
    subId      = int(self.scoreSubTreeWidget.currentItem().whatsThis(0))
    stdId      = []
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

    subId         = int(self.scoreSubTreeWidget.currentItem().whatsThis(0))
    grdStandard   = backend.returnAssesmentStandardBySubId(subId)
    assesmentList = backend.returnAssesmentBySubId(subId)
    
    items = []
    items = self.classListWidget.selectedItems()

    for i in range(0, len(items)):
        if(self.classListWidget.selectedItems()[i].column() is 2):
            row   = self.classListWidget.selectedItems()[i].row()
            score = self.classListWidget.item(row,2).text()
            if(score == ""):
                self.classListWidget.setItem(row,3,QTableWidgetItem(""))
            else:
                for stnd in grdStandard:
                    grade   = stnd[1]
                    greater = int(stnd[2])
                    less    = int(stnd[3])
                    if(greater <= int(score) and int(score) <= less):
                        assesments = returnGradeAssesments(assesmentList, grade)
                        randomIndex = random.randint(0, len(assesments)-1)
                        self.classListWidget.setItem(row,3,QTableWidgetItem(assesments[randomIndex]))

#점수 등급별 랜덤 평가 생성 함수 (전체)
def insertRandomAssesment(self):
    if(self.scoreSubTreeWidget.currentItem() is None):
        return QMessageBox.about(self, "오류", "과목을 선택해주세요.")

    subId         = int(self.scoreSubTreeWidget.currentItem().whatsThis(0))
    grdStandard   = backend.returnAssesmentStandardBySubId(subId)
    assesmentList = backend.returnAssesmentBySubId(subId)

    for row in range(0, self.classListWidget.rowCount()):
        score = self.classListWidget.item(row,2).text()
        if(score == ""):
            self.classListWidget.setItem(row,3,QTableWidgetItem(""))
        else:
            for stnd in grdStandard:
                grade   = stnd[1]
                greater = int(stnd[2])
                less    = int(stnd[3])
                if(greater <= int(score) and int(score) <= less):
                    assesments  = returnGradeAssesments(assesmentList, grade)
                    randomIndex = random.randint(0, len(assesments)-1)
                    print(assesments)
                    self.classListWidget.setItem(row, 3, QTableWidgetItem(assesments[randomIndex]))

#학급 리스트 출력 함수
def insertClassComboBox(self, combobox):
    combobox.clear()
    classes = backend.returnClassList()
    for i in range(0, len(classes)):
        combobox.addItem(str(classes[i][0])+"학년 "+str(classes[i][1])+"반")
        
def returnClassInteger(classes):
    classes    = classes.replace(" ","")
    grade, ban = classes.split("학년")
    ban        = ban.replace("반","")
    return int(grade), int(ban)
    
#선택 학급 조회 함수    
def showClassMemberList(self):
    grade, classes = returnClassInteger(self.classList.currentText())     
    members        = backend.returnClassMemberList(grade, classes) 
    headers        = ["이름", "학번", "점수", "평가"]

    self.classListWidget.setRowCount(len(members))
    self.classListWidget.setColumnCount(4)
    self.classListWidget.setHorizontalHeaderLabels(headers)

    for i in range(0, len(members)):
        name  = QTableWidgetItem(str(members[i][0]))
        stdId = QTableWidgetItem(str(members[i][1]))
        self.classListWidget.setItem(i, 0, name)
        self.classListWidget.setItem(i, 1, stdId)
    
    self.showScoreList()