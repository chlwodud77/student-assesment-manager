#!/usr/bin/env python
# -*- coding: utf-8 -*-
import backend
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

CELL_WIDTH = 50
GRADE_COL = 0
CLASS_COL = 1
STDNUM_COL = 2
NAME_COL = 3
ASSES_COL = 4
LENGTH_COL = 5


align_center        = Alignment(horizontal='center', vertical='center')
wrap_text           = Alignment(vertical="center", wrapText=True)
allround_border     = Border(left =Side(border_style="thin",
                                        color='000000'),
                            right =Side(border_style="thin",
                                        color='000000'),
                            top   =Side(border_style="thin",
                                        color='000000'),
                            bottom=Side(border_style="thin",
                                        color='000000'))

#엑셀 테이블 항목 선택 시 내용 표시 함수
def exlActivateEdit(self):
    focusedItem = self.exlClassListWidget.currentItem()
    if(focusedItem is None):
        self.exlAseEdit.setPlainText("")
        return 
    if(focusedItem.column() == ASSES_COL):
        content = self.exlClassListWidget.currentItem().text()
        self.exlAseEdit.setPlainText(content)
        
def showAssesLengthAndState(self, currentContent, row):
    contentLength = len(currentContent)
    contentLengthByte = len(currentContent.encode("utf-8"))
    lengthItem = QTableWidgetItem(str(contentLength)+" 자 ("+str(contentLengthByte)
                                    +"바이트)" )
    self.exlClassListWidget.setItem(row, LENGTH_COL, lengthItem)
    if(contentLength > 1000 or contentLengthByte > 3000):
        self.exlClassListWidget.item(row, LENGTH_COL).setBackground(QtGui.QColor(255,0,0))

#엑셀 테이블 항목 선택 후 텍스트 편집기에서 편집해주는 함수
def exlChangeAse(self):
    focusedItem = self.exlClassListWidget.currentItem()
    if(focusedItem is None):
        return
    if(focusedItem.column() == ASSES_COL):
        currentContent = self.exlAseEdit.toPlainText()
        focusedItem.setText(currentContent)
        focusedRow = focusedItem.row()
        showAssesLengthAndState(self, currentContent, focusedRow)

#최종 엑셀 파일로 저장 함수
def exlSaveToFile(self):
    name, _ = QFileDialog.getSaveFileName(self, 'Save File','','Excel files (*.xlsx)')
    headers = ["이름", "학년", "반", "번호", "평가"]
    if(name != ""):
        filename = name
        wb = Workbook()
        ws = wb.active
        ws.column_dimensions["E"].width = CELL_WIDTH
        content = []
        for i in range(0, self.exlClassListWidget.rowCount()):
            p = []
            p.append(self.exlClassListWidget.item(i,NAME_COL).text())
            p.append(int(self.exlClassListWidget.item(i,GRADE_COL).text()))
            p.append(int(self.exlClassListWidget.item(i,CLASS_COL).text()))
            p.append(int(self.exlClassListWidget.item(i,STDNUM_COL).text()))
            if(self.exlClassListWidget.item(i,ASSES_COL) is not None):
                p.append(self.exlClassListWidget.item(i,ASSES_COL).text())
            else:
                p.append("")
            content.append(p)
        for x in range(1, 2):
            for y in range(1,6):
                ws.cell(row = x, column = y).value = headers[y-1]
                ws.cell(row = x, column = y).alignment = align_center
                ws.cell(row = x, column = y).border = allround_border
        for x in range(2,len(content)+2):
            for y in range(1,6):
                ws.cell(row = x, column = y).value = content[x-2][y-1]
                if(y != 5):
                    ws.cell(row = x, column = y).alignment = align_center
                if(y == 5):
                    ws.cell(row = x, column = y).alignment = wrap_text
                ws.cell(row = x, column = y).border = allround_border
        wb.save(filename)
        QMessageBox.about(self, "결과", "저장 성공.")
            
#학급별 종합 평가 출력 함수
def exlShowTotAssesment(self):
    self.exlClassListWidget.clearContents()
    if(self.exlSubAddedWidget.count() == 0):
        return QMessageBox.about(self, "오류", "과목을 추가해주세요.")
        
    grade, classes = returnClassInteger(self.exlClassList.currentText())    
    subjectsIds = []
    assesments  = []
    members     = []
    items       = []
    for row in range(self.exlSubAddedWidget.count()):
        item = self.exlSubAddedWidget.item(row)
        items.append(item)
    for item in items:
        subjectsIds.append(int(item.whatsThis()))
    
    for id in subjectsIds:
        assesments.append(backend.returnClassAssesmentBySubId(id, grade, classes))

    members = backend.returnClassMemberList(grade, classes)
    self.exlClassListWidget.setRowCount(len(members))
    self.exlClassListWidget.setColumnCount(6)
    header = self.exlClassListWidget.horizontalHeader() 
    header.setSectionResizeMode(NAME_COL, QHeaderView.ResizeToContents)
    header.setSectionResizeMode(GRADE_COL, QHeaderView.ResizeToContents)
    header.setSectionResizeMode(CLASS_COL, QHeaderView.ResizeToContents)
    header.setSectionResizeMode(STDNUM_COL, QHeaderView.ResizeToContents)
    header.setSectionResizeMode(ASSES_COL, QHeaderView.Stretch)
    header.setSectionResizeMode(LENGTH_COL, QHeaderView.ResizeToContents)

    for i in range(0,len(members)):
        stdName = str(members[i][0])
        stdId = str(members[i][1])
        stdNum = stdId[3:]
        nameItem = QTableWidgetItem(stdName)
        nameItem.setWhatsThis(stdId)
        gradeItem = QTableWidgetItem(str(grade))
        classItem = QTableWidgetItem(str(classes))
        stdNumItem = QTableWidgetItem(stdNum)
        self.exlClassListWidget.setItem(i, NAME_COL, nameItem)
        self.exlClassListWidget.setItem(i, GRADE_COL, gradeItem)
        self.exlClassListWidget.setItem(i, CLASS_COL, classItem)
        self.exlClassListWidget.setItem(i, STDNUM_COL, stdNumItem)
        
    for i in range(0,len(members)):
        stdId = self.exlClassListWidget.item(i,NAME_COL).whatsThis()
        for asses in assesments:
            for row in asses:
                if(row[2] is None):
                    continue
                if(int(row[1]) == int(stdId)):
                    if(self.exlClassListWidget.item(i,ASSES_COL) is not None): #기존에 내용이 있는 경우 붙여서 추가
                        orgContent = self.exlClassListWidget.item(i,ASSES_COL).text()
                        orgContent = orgContent.strip()
                        newContent = ""
                        contentLength = 0
                        contentLengthByte = 0
                        if(orgContent == ""): 
                            newContent = str(row[2])
                        else:
                            newContent = orgContent+" "+str(row[2])
                        assesItem = QTableWidgetItem(newContent)
                        showAssesLengthAndState(self, newContent, i)
                        self.exlClassListWidget.setItem(i,ASSES_COL, assesItem)
                        
                    else: #기존에 내용이 없는 빈 칸인 경우
                        content = str(row[2])
                        assesItem = QTableWidgetItem(content)
                        showAssesLengthAndState(self, content, i)
                        self.exlClassListWidget.setItem(i,ASSES_COL, assesItem)
        if(self.exlClassListWidget.item(i,ASSES_COL) is None):
            assesItem = QTableWidgetItem("")
            showAssesLengthAndState(self, "", i)
            self.exlClassListWidget.setItem(i,ASSES_COL, assesItem)

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
        subjects = backend.returnClassSubList(grade,classes)
        subjects = sorted(subjects)
        for subject in subjects:
            if(subject[2] is None):
                continue
            parentSubName = backend.returnSubNameBySubId(int(subject[2]))
            name = parentSubName+" - "+subject[1]
            item = QListWidgetItem(str(name))
            item.setWhatsThis(str(subject[0]))
            self.exlSubListWidget.addItem(item)