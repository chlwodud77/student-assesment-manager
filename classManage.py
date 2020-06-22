#!/usr/bin/env python
# -*- coding: utf-8 -*-
import backend
from openpyxl import load_workbook, Workbook
from PyQt5.QtWidgets import *
from PyQt5 import QtCore



def uploadCls(self):
    rowCnt = self.stdListWidget.rowCount()
    columnCnt = self.stdListWidget.columnCount()

    for col in range(0, columnCnt):
        header = self.stdListWidget.horizontalHeaderItem(col).text()
        grade = header[0]
        classes = header[2]
        for row in range(0, rowCnt):
            name = self.stdListWidget.item(row,col).text()
            if(name != "" or name is not None):
                backend.saveStudent(name, grade, classes)
                
    QMessageBox.about(self, "결과", "학생 저장 완료.")
    
#학급 구성원 엑셀 파일로 불러와서 리스트로 보여줌
def uploadFile(self):
    fname = QFileDialog.getOpenFileName(self, 'Open file', './')
    if(fname[0]):    
        wb = load_workbook(filename = fname[0]) 
        ws = wb["Sheet1"]
        max_row = ws.max_row
        max_col = ws.max_column

        widget = self.stdListWidget
        widget.setRowCount(max_row-1)
        widget.setColumnCount(max_col)
        headers = []
        for i in range(1, max_col+1):
            headers.append(str(ws.cell(row=1, column= i).value))
        widget.setHorizontalHeaderLabels(headers)

        for i in range(2, max_row+1):
            for j in range(1, max_col+1):
                cellValue = str(ws.cell(row=i, column= j).value)
                item = QTableWidgetItem(cellValue)
                widget.setItem(i-2,j-1,item)