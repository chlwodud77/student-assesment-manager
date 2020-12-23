#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import sys

from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtWidgets import *

from src import classManage, scoreManage, subjectManage, scoreChangeManage, excelManage
from utils.adapter import subjectTreeWidgetAdpater as sa, classComboBoxAdapter as ca

form_class = uic.loadUiType("layout/manager.ui")[0]


class WindowClass(QMainWindow, form_class):
    EXIT_CODE_REBOOT = -123

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showClassList()
        self.showSub(self.subTreeWidget)
        self.showSub(self.scoreSubTreeWidget)
        self.insertClassComboBox(self.classList)
        self.clsSetHeaders()
        self.tabWidget.currentChanged.connect(self.checkChangedTab)
        self.exlAllShowClassList()
        self.exlAllShowSubList()
        ca.insertClassComboBox(self.scoreChangeClassList)
        sa.showSub(self.compareSubjectLeft)
        sa.showSub(self.compareSubjectRight)
        sa.showSub(self.scoreChangeSubject)

        # 메뉴
        self.actionImport_DB.triggered.connect(self.importDatabase)
        self.actionBackup_DB.triggered.connect(self.exportDatabase)

        # 학급추가 탭
        self.stdClassDelBtn.clicked.connect(self.deleteStdClass)
        self.stdDelBtn.clicked.connect(self.deleteStd)
        self.fileUpdBtn.clicked.connect(self.uploadFile)
        self.clsRowAddBtn.clicked.connect(self.clsAddRow)
        self.clsRowDelBtn.clicked.connect(self.clsDelRow)
        self.clsSaveBtn.clicked.connect(self.uploadCls)
        self.clsResetBtn.clicked.connect(self.clsContentReset)

        # 과목관리 탭
        self.addChildBtn.clicked.connect(self.addChildSub)
        self.grdAseDelBtn.clicked.connect(self.delAse)
        self.grdAseAddBtn.clicked.connect(self.addAse)
        self.grdAseModBtn.clicked.connect(self.modAse)
        self.grdAseList.clicked.connect(self.activateEdit)
        self.grdStndAddBtn.clicked.connect(self.addGrdStnd)
        self.grdStndDelBtn.clicked.connect(self.delGrdStnd)
        self.grdStndModBtn.clicked.connect(self.modGrdStnd)
        self.subTreeWidget.itemClicked.connect(self.searchSub)
        self.subAddBtn.clicked.connect(self.addNewSubjectItem)
        self.subModBtn.clicked.connect(self.modSubName)
        self.subDelBtn.clicked.connect(self.delSub)
        self.grdStndList.clicked.connect(self.showAssesment)
        self.grdStndRowAddBtn.clicked.connect(self.addGrdStndRow)
        self.grdStndRowResetBtn.clicked.connect(self.resetGrdStndRow)
        self.grdAseList.installEventFilter(self)
        self.subjectCopyBtn.clicked.connect(self.showSubjectCopy)

        # 점수입력 탭
        # self.classListWidget.clicked.connect(self.activateScoreEdit)
        self.callClassMemberBtn.clicked.connect(self.showClassMemberList)
        self.scoreSubTreeWidget.itemDoubleClicked.connect(self.showClassMemberList)
        self.createAssesmentBtn.clicked.connect(self.insertRandomAssesment)
        self.createIndiAssesmentBtn.clicked.connect(self.insertIndiRandomAssesment)
        self.saveAssesmentBtn.clicked.connect(self.saveAssesment)
        self.scoreSubTreeWidget.itemDoubleClicked.connect(self.showSubClickedLabel)
        self.scoreSubTreeWidget.itemClicked.connect(self.showSubClickedLabel)
        self.scoreAseEdit.textChanged.connect(self.changeScoreAse)
        self.classListWidget.installEventFilter(self)
        self.selectedScoreResetBtn.clicked.connect(self.resetSelectedScore)
        self.allScoreResetBtn.clicked.connect(self.resetAllScore)
        self.totalScoreInput.clicked.connect(self.openTotalScoreSetInput)
        self.multiClassAssesBtn.clicked.connect(self.openMultiAssesInput)

        # 점수변동비교탭
        self.compareSubjectLeft.itemDoubleClicked.connect(self.showLeftSelectedSubject)
        self.compareSubjectRight.itemDoubleClicked.connect(self.showRightSelectedSubject)
        self.scoreChangeSubject.itemDoubleClicked.connect(self.showSelectedSubject)
        self.scoreChangeAssesBtn.clicked.connect(self.showScoreChangeAsses)
        self.scoreChangeSaveBtn.clicked.connect(self.saveScoreChange)

        # 엑셀출력 탭
        self.exlFileSaveBtn.clicked.connect(self.exlSaveToFile)
        self.exlClassAddBtn.clicked.connect(self.exlAddClassList)
        self.exlAddedClassList.itemDoubleClicked.connect(self.exlExtClassList)
        self.exlSubjectAddBtn.clicked.connect(self.exlAddSubList)
        self.exlAddedSubWidget.itemDoubleClicked.connect(self.exlExtSubList)
        self.multiAssesPrintBtn.clicked.connect(self.exlPrintMultiAsses)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_R and e.modifiers() == QtCore.Qt.ControlModifier:
            qApp.exit(WindowClass.EXIT_CODE_REBOOT)

    ##############설정메뉴###########################
    def importDatabase(self):
        DB_NAME = "studentManager.db"
        targetPath = "./"
        addFilePath, _ = QFileDialog.getOpenFileName(self, "Open File",
                                                     "./",
                                                     "Data Base File (*.db)")
        if addFilePath != "":
            buttonReply = QMessageBox.question(self,
                                               '알림', "db 파일을 대체하시겠습니까? 기존 db 파일은 삭제됩니다.",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                if os.path.isfile(DB_NAME):
                    # os.rename(targetPath+DB_NAME, targetPath+"old_"+DB_NAME)
                    os.remove(DB_NAME)
                    shutil.copyfile(addFilePath, targetPath + DB_NAME)
                    QMessageBox.about(self, "알림", "프로그램이 재실행됩니다.")
                    qApp.exit(WindowClass.EXIT_CODE_REBOOT)

    def exportDatabase(self):
        DB_NAME = "studentManager.db"
        originPath = "./"
        saveFilePath, _ = QFileDialog.getSaveFileName(self, "Save File",
                                                      "",
                                                      "Data Base File (*.db)")
        if saveFilePath != "":
            buttonReply = QMessageBox.question(self,
                                               '알림', "db 파일 백업하시겠습니까?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                shutil.copyfile(originPath + DB_NAME, saveFilePath)
                QMessageBox.about(self, "알림", "db 파일이 백업되었습니다.")

    ################-끝-############################

    ##############엑셀출력###########################

    def exlAllShowClassList(self):
        excelManage.exlAllShowClassList(self)

    def exlAddClassList(self):
        excelManage.exlAddClassList(self)

    def exlExtClassList(self):
        excelManage.exlExtClassList(self)

    def exlAllShowSubList(self):
        excelManage.exlAllShowSubList(self)

    def exlAddSubList(self):
        excelManage.exlAddSubList(self)

    def exlExtSubList(self):
        excelManage.exlExtSubList(self)

    # 최종 엑셀 파일로 저장 함수
    def exlSaveToFile(self):
        excelManage.exlSaveToFile(self)

    def exlPrintMultiAsses(self):
        excelManage.exlPrintMultiAsses(self)

    ################-끝-############################

    def showLeftSelectedSubject(self):
        sa.showSelectedSubjectByListWidget(
            self.compareSubjectLeft, self.selectedSubjectLeft, False)

    def showRightSelectedSubject(self):
        sa.showSelectedSubjectByListWidget(
            self.compareSubjectRight, self.selectedSubjectRight, False)

    def showSelectedSubject(self):
        sa.showSelectedSubjectByListWidget(
            self.scoreChangeSubject, self.selectedChangeSubject, False)

    def showScoreChangeAsses(self):
        scoreChangeManage.setScoreChangeAssesment(self)

    def saveScoreChange(self):
        scoreChangeManage.saveScoreChangeAssesment(self)

    ##############점수입력###########################

    def eventFilter(self, obj, event):
        if obj == self.grdAseList:
            if event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_V and event.modifiers() == QtCore.Qt.ControlModifier:
                    subjectManage.copyContent(obj)
                    return True
                else:
                    return False
            else:
                return False
        elif obj == self.classListWidget:
            col = self.classListWidget.currentColumn()
            if event.type() == QtCore.QEvent.KeyPress and int(col) == 3:
                if event.key() == QtCore.Qt.Key_V and event.modifiers() == QtCore.Qt.ControlModifier:
                    scoreManage.copyContent(self, col)
                    return True
                else:
                    return False
            elif event.type() == QtCore.QEvent.KeyPress and int(col) == 2:
                if event.key() == QtCore.Qt.Key_V and event.modifiers() == QtCore.Qt.ControlModifier:
                    scoreManage.copyContent(self, col)
                    return True
                else:
                    return False
            else:
                return False
        else:
            return QMainWindow.eventFilter(self, obj, event)

    def changeScoreAse(self):
        scoreManage.changeScoreAse(self)

    def resetSelectedScore(self):
        scoreManage.resetSelectedScore(self)

    def resetAllScore(self):
        scoreManage.resetAllScore(self)

    # 선택 학급 조회 함수
    def showClassMemberList(self):
        scoreManage.showClassMemberList(self)

    # 과목 선택 시 라벨에 선택 과목 표시 함수
    def showSubClickedLabel(self):
        scoreManage.showSubClickedLabel(self)

    # 점수, 평가 리스트 보여주는 함수
    def showScoreList(self):
        scoreManage.showScoreList(self)

    # 점수로 생성된 평가문 저장해주는 함수
    def saveAssesment(self):
        scoreManage.saveAssesment(self)

    # 점수 등급별 랜덤 평가 생성 함수 (선택)
    def insertIndiRandomAssesment(self):
        scoreManage.insertIndiRandomAssesment(self)

    # 점수 등급별 랜덤 평가 생성 함수 (전체)
    def insertRandomAssesment(self):
        scoreManage.insertRandomAssesment(self)

    # 학급 리스트 출력 함수
    def insertClassComboBox(self, combobox):
        scoreManage.insertClassComboBox(combobox)

    def openTotalScoreSetInput(self):
        scoreManage.openTotalScoreSetInput()

    def openMultiAssesInput(self):
        scoreManage.openMultiAssesInput()

    ################-끝-############################

    ##############과목관리###########################

    # 평가 내용 선택하면 편집기에 해당 내용 보여줌
    def activateEdit(self):
        subjectManage.activateEdit(self)

        # 평가 내용 추가 함수

    def addAse(self):
        subjectManage.addAse(self)

    def addGrdStndRow(self):
        subjectManage.addGrdStndRow(self)

    def addNewSubjectItem(self):
        subjectManage.addNewSubjectItem(self)

    def addChildSub(self):
        subjectManage.addChildSub(self)

    def addGrdStnd(self):
        subjectManage.addGrdStnd(self)

    def delGrdStnd(self):
        subjectManage.delGrdStnd(self)

    def modGrdStnd(self):
        subjectManage.modGrdStnd(self)

    def modSubName(self):
        subjectManage.modSubName(self)

    def delSub(self):
        subjectManage.delSub(self)

    def editItem(self):
        subjectManage.editItem(self)

    def resetGrdStndRow(self):
        subjectManage.resetGrdStndRow(self)

    # 과목 리스트에서 과목 선택 조회 하면 과목 세부 내용 조회 함수
    def searchSub(self):
        subjectManage.searchSub(self)

    def showSub(self, treeWidget):
        subjectManage.showSub(treeWidget)

    def showAssesment(self):
        subjectManage.showAssesment(self)

    # 평가 내용 수정 함수
    def modAse(self):
        subjectManage.modAse(self)

    # 평가 내용 항목 지우는 함수
    def delAse(self):
        subjectManage.delAse(self)

    def showSubjectCopy(self):
        subjectManage.openSubjectManage(self)

    ################-끝-############################

    ##############학급추가###########################

    def deleteStdClass(self):
        classManage.deleteStdClass(self)
        self.insertClassComboBox(self.classList)

    def deleteStd(self):
        classManage.deleteStd(self)
        self.insertClassComboBox(self.classList)

    def clsAddRow(self):
        classManage.clsAddRow(self)

    def clsDelRow(self):
        classManage.clsDelRow(self)

    def clsContentReset(self):
        classManage.clsContentReset(self)

    def clsSetHeaders(self):
        classManage.clsSetHeaders(self)

    def showClassList(self):
        classManage.showClassList(self)

    def uploadCls(self):
        classManage.uploadCls(self)
        self.insertClassComboBox(self.classList)

    # 학급 구성원 엑셀 파일로 불러와서 리스트로 보여줌
    def uploadFile(self):
        classManage.uploadFile(self)

    ################-끝-############################

    def checkChangedTab(self):
        STUDENT_MANAGE = 0
        SUBJECT_MANAGE = 1
        SCORE_MANAGE = 2
        SCORE_CHANGE_MANAGE = 3
        EXCEL_MANAGE = 4
        currentIndex = self.tabWidget.currentIndex()
        if currentIndex == SUBJECT_MANAGE: self.showSub(self.subTreeWidget)
        if currentIndex == SCORE_MANAGE: self.showSub(self.scoreSubTreeWidget)
        if currentIndex == SCORE_CHANGE_MANAGE:
            ca.insertClassComboBox(self.scoreChangeClassList)
            sa.showSub(self.compareSubjectLeft)
            sa.showSub(self.compareSubjectRight)
            sa.showSub(self.scoreChangeSubject)
        if currentIndex == EXCEL_MANAGE:
            self.exlAllShowClassList()
            self.exlAllShowSubList()


if __name__ == "__main__":
    currentExitCode = WindowClass.EXIT_CODE_REBOOT
    while currentExitCode == WindowClass.EXIT_CODE_REBOOT:
        # QApplication : 프로그램을 실행시켜주는 클래스
        app = QApplication(sys.argv)

        # WindowClass의 인스턴스 생성
        myWindow = WindowClass()

        # 프로그램 화면을 보여주는 코드
        myWindow.show()

        # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
        currentExitCode = app.exec_()
        app = None
