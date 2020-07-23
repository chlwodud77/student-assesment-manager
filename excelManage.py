#!/usr/bin/env python
# -*- coding: utf-8 -*-
import backend
from openpyxl import load_workbook, Workbook
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

#엑셀 테이블 항목 선택 시 내용 표시 함수
def exlActivateEdit(self):
    focusedItem = self.exlClassListWidget.currentItem()
    if(focusedItem is None):
        row = self.exlClassListWidget.currentRow()
        col = self.exlClassListWidget.currentColumn()
        self.exlClassListWidget.setItem(row, col, QTableWidgetItem(""))
    content = self.exlClassListWidget.currentItem().text()
    self.exlAseEdit.setPlainText(content)

#엑셀 테이블 항목 선택 후 텍스트 편집기에서 편집해주는 함수
def exlChangeAse(self):
    focusedItem = self.exlClassListWidget.currentItem()
    currentContent = self.exlAseEdit.toPlainText()
    focusedItem.setText(currentContent)

#최종 엑셀 파일로 저장 함수
def exlSaveToFile(self):
    name, _ = QFileDialog.getSaveFileName(self, 'Save File','','Excel files (*.xlsx)')
    if(name != ""):
        filename = name
        wb = Workbook()
        ws = wb.active
        content = []
        for i in range(0, self.exlClassListWidget.rowCount()):
            p = []
            p.append(self.exlClassListWidget.item(i,0).text())
            if(self.exlClassListWidget.item(i,2) is not None):
                p.append(self.exlClassListWidget.item(i,2).text())
            else:
                p.append("")
            content.append(p)

        for x in range(1,len(content)+1):
            for y in range(1,3):
                ws.cell(row = x, column = y).value = content[x-1][y-1]
        wb.save(filename)
        QMessageBox.about(self, "결과", "저장 성공.")
            
#학급별 종합 평가 출력 함수
def exlShowTotAssesment(self):
    self.exlClassListWidget.clearContents()
    if(self.exlSubAddedWidget.count() == 0):
        return QMessageBox.about(self, "오류", "과목을 추가해주세요.")
        
    grade, classes = returnClassInteger(self.exlClassList.currentText())    
    # grade = int(self.exlClassList.currentText()[0])
    # classes = int(self.exlClassList.currentText()[4])
    subjectsIds = []
    assesments = []
    members = []
    items = []
    for row in range(self.exlSubAddedWidget.count()):
        item = self.exlSubAddedWidget.item(row)
        items.append(item)
    for item in items:
        subjectsIds.append(int(item.whatsThis()))
    
    for id in subjectsIds:
        assesments.append(backend.returnClassAssesmentBySubId(id, grade, classes))

    members = backend.returnClassMemberList(grade, classes)
    self.exlClassListWidget.setRowCount(len(members))
    self.exlClassListWidget.setColumnCount(3)

    for i in range(0,len(members)):
        nameItem = QTableWidgetItem(str(members[i][0]))
        stdIdItem = QTableWidgetItem(str(members[i][1]))
        stdIdItem.setWhatsThis(str(members[i][1]))
        self.exlClassListWidget.setItem(i, 0, nameItem)
        self.exlClassListWidget.setItem(i, 1, stdIdItem)

    for i in range(0,len(members)):
        stdId = self.exlClassListWidget.item(i,1).text()
        for asses in assesments:
            for row in asses:
                if(int(row[1]) == int(stdId)):
                    if(self.exlClassListWidget.item(i,2) is not None): #기존에 내용이 있는 경우 붙여서 추가
                        orgContent = self.exlClassListWidget.item(i,2).text()
                        orgContent = orgContent.strip()
                        newContent = ""
                        if(orgContent == ""): 
                            newContent = str(row[2])
                        else:
                            newContent = orgContent+" "+str(row[2])
                        assesItem = QTableWidgetItem(newContent)
                        self.exlClassListWidget.setItem(i,2, assesItem)
                    else: #기존에 내용이 없는 빈 칸인 경우
                        assesItem = QTableWidgetItem(str(row[2]))
                        self.exlClassListWidget.setItem(i,2, assesItem)

#학급별 평가 과목 선택 추가 함수
def exlSubAddClass(self):
    if(self.exlSubListWidget.currentItem() is not None):
        item = self.exlSubListWidget.currentItem()
        addItem = QListWidgetItem(str(item.text()))
        addItem.setWhatsThis(str(item.whatsThis()))
        self.exlSubAddedWidget.addItem(addItem)
        
#학급별 평가 과목 선택 빼기 함수
def exlSubExtClass(self):
    if(self.exlSubAddedWidget.currentItem() is not None):
        row = self.exlSubAddedWidget.currentRow()
        self.exlSubAddedWidget.takeItem(row)
        
def returnClassInteger(classes):
    classes = classes.replace(" ","")
    grade, ban = classes.split("학년")
    ban = ban.replace("반","")
    return int(grade), int(ban)
        
#학급별 평가 과목 보여주는 함수
def exlShowClassList(self):
    self.exlSubListWidget.clear()
    self.exlSubAddedWidget.clear()
    if(self.exlClassList.currentText() != ""):
        grade, classes = returnClassInteger(self.exlClassList.currentText())
        # grade = int(self.exlClassList.currentText()[0])
        # classes = int(self.exlClassList.currentText()[4])
        subjects = backend.returnClassSubList(grade,classes)
        subjects = sorted(subjects)

        for subject in subjects:
            parentSubName = backend.returnSubNameBySubId(int(subject[2]))
            name = parentSubName+" - "+subject[1]
            item = QListWidgetItem(str(name))
            item.setWhatsThis(str(subject[0]))
            self.exlSubListWidget.addItem(item)