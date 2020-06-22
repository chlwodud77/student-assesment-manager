#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, backend, sqlite3, random
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

#과목 선택 시 라벨에 선택 과목 표시 함수
def showSubClickedLabel(self):
    self.subClickedLabel.setText(self.scoreSubTreeWidget.currentItem().text(0))
    
#점수로 생성된 평가문 저장해주는 함수
def saveAssesment(self):
    if(self.scoreSubTreeWidget.currentItem() is None):
        QMessageBox.about(self, "오류", "과목을 선택해주세요.")
        return
    if(self.scoreSubTreeWidget.currentItem() is not None and self.classListWidget.rowCount() == 0):
        QMessageBox.about(self, "오류", "학급을 불러와주세요.")
        return
    for row in range(0, self.classListWidget.rowCount()):
        if(self.classListWidget.item(row,2).whatsThis() != ""): #기존 스코어 존재
            asses = self.classListWidget.item(row,3).text()
            score = int(self.classListWidget.item(row,2).text())
            scoreId = int(self.classListWidget.item(row,2).whatsThis())
            stdId = int(self.classListWidget.item(row,1).text())
            subId = int(self.scoreSubTreeWidget.currentItem().whatsThis(0))
            backend.deleteScoreById(scoreId) #기존 스코어 삭제 후 
            backend.saveScore(subId, stdId, score, asses) # 다시 재 저장.
        else: #기존에 스코어 존재 X
            if(self.classListWidget.item(row,2).whatsThis() == "" and self.classListWidget.item(row,2).text() != ""):
                asses = self.classListWidget.item(row,3).text()
                score = int(self.classListWidget.item(row,2).text())
                stdId = int(self.classListWidget.item(row,1).text())
                subId = int(self.scoreSubTreeWidget.currentItem().whatsThis(0))
                backend.saveScore(subId, stdId, score, asses) # 새로 저장.
    QMessageBox.about(self, "결과", "점수 저장 성공.")
    
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
    classes = backend.returnClassList()
    for i in range(0, len(classes)):
        combobox.addItem(str(classes[i][0])+"학년 "+str(classes[i][1])+"반")
        
#선택 학급 조회 함수    
def showClassMemberList(self):     
    grade = int(self.classList.currentText()[0])
    classes = int(self.classList.currentText()[4])
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