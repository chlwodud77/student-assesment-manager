#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore
import sys, sqlite3, random
import classManage, subjectManage, scoreManage, excelManage

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("manager.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.showSub(self.subTreeWidget)
        self.showSub(self.scoreSubTreeWidget)
        self.insertClassComboBox(self.classList)
        self.insertClassComboBox(self.exlClassList)
        self.exlShowClassList()

        #학급추가 탭
        self.fileUpdBtn.clicked.connect(self.uploadFile)
        self.clsSaveBtn.clicked.connect(self.uploadCls)

        #과목관리 탭
        self.addChildBtn.clicked.connect(self.addChildSub)
        self.grdAseDelBtn.clicked.connect(self.delAse)
        self.grdAseAddBtn.clicked.connect(self.addAse)
        self.grdAseModBtn.clicked.connect(self.modAse)
        self.grdAAseList.clicked.connect(self.activateEdit)
        self.grdBAseList.clicked.connect(self.activateEdit)
        self.grdCAseList.clicked.connect(self.activateEdit)
        self.subSaveBtn.clicked.connect(self.saveSub)
        self.subSrhBtn.clicked.connect(self.searchSub)
        self.subTreeWidget.itemClicked.connect(self.searchSub)
        self.subAddBtn.clicked.connect(self.addNewSubjectItem)
        self.subDelBtn.clicked.connect(self.delSub)

        #점수입력 탭
        self.callClassMemberBtn.clicked.connect(self.showClassMemberList)
        self.createAssesmentBtn.clicked.connect(self.insertRandomAssesment)
        self.createIndiAssesmentBtn.clicked.connect(self.insertIndiRandomAssesment)
        self.saveAssesmentBtn.clicked.connect(self.saveAssesment)
        self.scoreSubTreeWidget.itemDoubleClicked.connect(self.showSubClickedLabel)
        self.scoreSubTreeWidget.itemClicked.connect(self.showSubClickedLabel)

        #엑셀출력 탭
        self.exlClassList.activated.connect(self.exlShowClassList)
        self.exlSubAddBtn.clicked.connect(self.exlSubAddClass)
        self.exlSubExtBtn.clicked.connect(self.exlSubExtClass)
        self.exlFileSaveBtn.clicked.connect(self.exlSaveToFile)
        self.printTotAssesBtn.clicked.connect(self.exlShowTotAssesment)
    
    ##############엑셀출력###########################

    #최종 엑셀 파일로 저장 함수
    def exlSaveToFile(self):
        excelManage.exlSaveToFile(self)

    #학급별 종합 평가 출력 함수
    def exlShowTotAssesment(self):
        excelManage.exlShowTotAssesment(self)

    #학급별 평가 과목 선택 추가 함수
    def exlSubAddClass(self):
        excelManage.exlSubAddClass(self)

    #학급별 평가 과목 선택 빼기 함수
    def exlSubExtClass(self):
        excelManage.exlSubExtClass(self)

    #학급별 평가 과목 보여주는 함수
    def exlShowClassList(self):
        excelManage.exlShowClassList(self)
        
    ################-끝-############################
    
    

    ##############점수입력###########################

    #선택 학급 조회 함수    
    def showClassMemberList(self):     
        scoreManage.showClassMemberList(self)
        
    #과목 선택 시 라벨에 선택 과목 표시 함수
    def showSubClickedLabel(self):
        scoreManage.showSubClickedLabel(self)

    #점수, 평가 리스트 보여주는 함수
    def showScoreList(self):
        scoreManage.showScoreList(self)
            
    #점수로 생성된 평가문 저장해주는 함수
    def saveAssesment(self):
        scoreManage.saveAssesment(self)

    #점수 등급별 랜덤 평가 생성 함수 (선택)
    def insertIndiRandomAssesment(self):
        scoreManage.insertIndiRandomAssesment(self)
        
    #점수 등급별 랜덤 평가 생성 함수 (전체)
    def insertRandomAssesment(self):
        scoreManage.insertRandomAssesment(self)
        
    #학급 리스트 출력 함수
    def insertClassComboBox(self, combobox):
        scoreManage.insertClassComboBox(self, combobox)
    
    ################-끝-############################
    
    

    ##############과목관리###########################
    
    #평가 내용 선택하면 편집기에 해당 내용 보여줌
    def activateEdit(self):
        subjectManage.activateEdit(self)    
    
    #평가 내용 추가 함수
    def addAse(self):
        subjectManage.addAse(self)

    def addNewSubjectItem(self):
        subjectManage.addNewSubjectItem(self)

    def addChildSub(self):
        subjectManage.addChildSub(self)
    
    def delSub(self):
        subjectManage.delSub(self)

    #과목 리스트에서 과목 선택 조회 하면 과목 세부 내용 조회 함수
    def searchSub(self):
        subjectManage.searchSub(self)

    def showSub(self, treeWidget):
        subjectManage.showSub(self, treeWidget)

    #과목, 평가 등급 점수, 평가 내용 db 저장 함수
    def saveSub(self):
        subjectManage.saveSub(self)
        
    # 평가 내용 수정 함수
    def modAse(self):
        subjectManage.modAse(self)

    #평가 내용 항목 지우는 함수
    def delAse(self):
        subjectManage.delAse(self)
        
    ################-끝-############################
    
    

    ##############학급추가###########################
    def uploadCls(self):
        classManage.uploadCls(self)
        
    #학급 구성원 엑셀 파일로 불러와서 리스트로 보여줌
    def uploadFile(self):
        classManage.uploadFile(self)
        
    ################-끝-############################

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()