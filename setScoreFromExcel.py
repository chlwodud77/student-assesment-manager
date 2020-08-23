import sys, random
import backend, scoreManage
import pandas as pd
import numpy as np
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QAbstractTableModel, Qt
from pandasModel import PandasModel

form_class = uic.loadUiType("setScoreFromExcel.ui")[0]

class SetScoreFromExcel(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showSubs()
        self.getExlBtn.clicked.connect(self.getExlFile)
        self.tabWidget.tabCloseRequested.connect(self.removeTab)
        self.addSubBtn.clicked.connect(self.addSub)
        self.listWidget.itemDoubleClicked.connect(self.extSub)
        self.currentTabSaveBtn.clicked.connect(self.saveCurrentTabScore)
        self.allTabSaveBtn.clicked.connect(self.saveAllTabScore)
        self.sheet_to_df_map = []

    def getExlFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './', 'Excel files (*.xlsx *.xls)')
        if(fname[0]):
            self.sheet_to_df_map = []
            tabWidget = self.tabWidget
            while(tabWidget.count() != 0):
                tabWidget.removeTab(tabWidget.currentIndex())
            xls = pd.ExcelFile(fname[0])
            for sheet_name in xls.sheet_names:
                self.sheet_to_df_map.append(xls.parse(sheet_name))

            for df, name in zip(self.sheet_to_df_map, xls.sheet_names):
                tab = QWidget()
                model = PandasModel(df)
                view = QTableView(tab)
                view.setModel(model)
                tabWidget.addTab(view, name)
    
    def removeTab(self, index):
        self.tabWidget.removeTab(index)
        self.sheet_to_df_map.pop(index)

    def saveAllTabScore(self):
        tabWidget = self.tabWidget
        tabCount = tabWidget.count()
        for i in range(0, tabCount):
            tabWidget.setCurrentIndex(i)
            self.saveCurrentTabScore()


    def saveCurrentTabScore(self):
        subjectIdList = []
        tabWidget = self.tabWidget
        subWidget = self.listWidget
        subTabCol = self.lineEdit.text()
        currentTabIndex = tabWidget.currentIndex()
        subjectListCnt = subWidget.count()

        for i in range(0, subjectListCnt):
            subjectId = subWidget.item(i).whatsThis()
            subjectIdList.append(int(subjectId))

        if(subWidget.count() != 0 and subTabCol.isdigit()):
            stdIdList = []
            scoreList = []
            df = self.sheet_to_df_map[currentTabIndex]
            columns = list(df)

            for i in range(0, len(columns)):
                if(i == 0):
                    stdIdList.append(df[columns[i]].values.tolist())
                    for stdId in stdIdList[0]:
                        if(len(str(stdId)) != 5):
                            return QMessageBox.about(self, "주의", tabWidget.tabText(tabWidget.currentIndex())+ " 탭에서 불러온 파일에서 학번 정보를 찾을 수 없습니다.")
                if(i >= int(subTabCol)-1):
                    scoreList.append(df[columns[i]].values.tolist())

            if(subjectListCnt != len(scoreList)):
                return QMessageBox.about(self, "주의", tabWidget.tabText(tabWidget.currentIndex())+ " 탭에서 추가할 점수의 과목과 불러온 파일의 점수 열의 개수를 확인해주세요.")
            
            for subId, scores in zip(subjectIdList, scoreList):
                for stdId, i  in zip(stdIdList[0], range(0,len(stdIdList[0]))):
                    isScoreExists = backend.returnIfStudentSubjectScoreExist(subId, stdId)
                    score = scores[i]
                    assesments = scoreManage.getPossibleAssesmentByScore(subId, score)
                    if(len(assesments) == 0):
                        content = ""
                        if(isScoreExists is not None):
                            backend.updateScoreAndAssesBySubIdAndStdId(subId, stdId, score, content)
                        else:
                            backend.saveScore(subId, stdId, score, content)
                    else:
                        randomIndex = random.randint(0, len(assesments)-1)
                        content = assesments[randomIndex]
                        if(isScoreExists is not None):
                            backend.updateScoreAndAssesBySubIdAndStdId(subId, stdId, score, content)
                        else:
                            backend.saveScore(subId, stdId, score, content)
            return QMessageBox.about(self, "결과", tabWidget.tabText(tabWidget.currentIndex())+" 탭 점수 입력 완료.")

    def showSubs(self):
        widget = self.treeWidget
        subList       = backend.returnSubList()
        subTreeWidget = widget
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

    def addSub(self):
        srcWidget = self.treeWidget
        trgWidget = self.listWidget
        if(srcWidget.selectedItems() is not None):
            items = srcWidget.selectedItems()
            for item in items:
                if(item.parent() is not None): #자식 노드이면
                    parentItem = item.parent()
                    parentName = parentItem.text(0)
                    childName = item.text(0)
                    childId = item.whatsThis(0)
                    newItem = QListWidgetItem(str(parentName) + " - " + str(childName))
                    newItem.setWhatsThis(str(childId))
                    trgWidget.addItem(newItem)
    
    def extSub(self):
        widget = self.listWidget
        if(widget.currentItem() is not None):
            row = widget.currentRow()
            widget.takeItem(row)


    def show(self):
        dialog = SetScoreFromExcel()
        dialog.exec_()
        
