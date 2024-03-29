#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import re

from PyQt5.QtWidgets import *

from src.dialog.multiAssesInput import MultiAssesInput
from src.dialog.setScoreFromExcel import SetScoreFromExcel
from utils import backend, copyFromExl

NAME_COL = 0
HAKBUN_COL = 1
SCORE_COL = 2
ASSES_COL = 3

REGEX = re.compile('^[+-]?\d*(\.?\d+)$')


def resizeColumnWidth(self):
    header = self.classListWidget.horizontalHeader()
    header.setSectionResizeMode(ASSES_COL, QHeaderView.Stretch)
    header.setSectionResizeMode(NAME_COL, QHeaderView.ResizeToContents)
    header.setSectionResizeMode(HAKBUN_COL, QHeaderView.ResizeToContents)
    header.setSectionResizeMode(SCORE_COL, QHeaderView.ResizeToContents)


def openMultiAssesInput():
    a = MultiAssesInput()
    a.show()


def openTotalScoreSetInput(self):
    return QMessageBox.about(self, "알림", "현재 기능은 수정중이여서 사용할 수 없습니다.")
    a = SetScoreFromExcel()
    a.show()


def copyContent(self, col):
    widget = self.classListWidget
    content = copyFromExl.getCopyContent()
    if content:
        # 복사해온 텍스트 행이 기존 테이블에 있는 행과 비교시 적거나 같을 때만 붙여넣기
        if widget.currentRow() == 0 and widget.rowCount() >= len(content):
            for i in range(0, len(content)):
                if col == SCORE_COL:
                    if widget.item(i, col).whatsThis():
                        scoreId = widget.item(i, col).whatsThis()
                        print(scoreId)
                        scoreItem = QTableWidgetItem(str(content[i]))
                        scoreItem.setWhatsThis(scoreId)
                        widget.setItem(i, col, scoreItem)
                    else:
                        item = QTableWidgetItem(str(content[i]))
                        widget.setItem(i, col, item)

                if col == ASSES_COL:
                    comboBox = widget.cellWidget(i, col)
                    comboBox.addItem(str(content[i]))
                    comboBox.setCurrentText(str(content[i]))


# 점수 입력 테이블 항목 선택 후 텍스트 편집기에서 편집해주는 함수
def changeScoreAse(self):
    focusedItem = self.classListWidget.currentItem()
    currentContent = self.scoreAseEdit.toPlainText()
    focusedItem.setText(currentContent)


def resetSelectedScore(self):
    widget = self.classListWidget
    items = widget.selectedItems()
    if not items:
        return QMessageBox.about(self, "주의", "초기화 할 점수를 선택해주세요.")
    for item in items:
        col = item.column()
        if col != SCORE_COL:
            return QMessageBox.about(self, "주의", "초기화 할 점수만 선택해주세요.")
        item.setText("")

    return QMessageBox.about(self, "알림", "선택된 점수 초기화 완료. DB 반영하려면 저장 눌러주세요.")


def resetAllScore(self):
    widget = self.classListWidget
    rowCount = widget.rowCount()
    for row in range(0, rowCount):
        widget.item(row, SCORE_COL).setText("")

    return QMessageBox.about(self, "알림", "전체 점수 초기화 완료. DB 반영하려면 저장 눌러주세요.")


# 과목 선택 시 라벨에 선택 과목 표시 함수
def showSubClickedLabel(self):
    self.subClickedLabel.setText(self.scoreSubTreeWidget.currentItem().text(0))


# 점수로 생성된 평가문 저장해주는 함수
def saveAssesment(self):
    buttonReply = QMessageBox.question(self, '알림', "과목 평가를 저장하시겠습니까?", QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.Yes)
    if buttonReply == QMessageBox.Yes:
        if self.scoreSubTreeWidget.currentItem() is None:
            return QMessageBox.about(self, "오류", "과목을 선택해주세요.")
        if self.scoreSubTreeWidget.currentItem() is not None and self.classListWidget.rowCount() == 0:
            return QMessageBox.about(self, "오류", "학급을 불러와주세요.")

        subId = int(self.scoreSubTreeWidget.currentItem().whatsThis(0))
        widget = self.classListWidget

        for row in range(0, widget.rowCount()):
            if widget.item(row, SCORE_COL).whatsThis() != "":  # 기존 스코어 존재
                score = widget.item(row, SCORE_COL).text()
                regTest = REGEX.match(score)
                if regTest:
                    score = float(score)
                elif score.replace(" ", "") == "":
                    score = None
                elif not score.replace(" ", "").isdigit():
                    return QMessageBox.about(self, "주의", "점수는 공백 또는 숫자만 입력하세요.")
                scoreId = int(widget.item(row, SCORE_COL).whatsThis())
                asses = widget.cellWidget(row, ASSES_COL).currentText()
                backend.updateScoreById(scoreId, score, asses)
            else:  # 기존에 스코어 존재 X
                score = widget.item(row, SCORE_COL).text()
                if widget.cellWidget(row, ASSES_COL) is None:
                    asses = widget.item(row, ASSES_COL).text()
                else:
                    asses = widget.cellWidget(row, ASSES_COL).currentText()
                regTest = REGEX.match(score)
                if regTest:
                    score = float(score)
                elif score == "":
                    score = None
                elif not regTest:
                    return QMessageBox.about(self, "주의", "점수는 공백 또는 숫자만 입력하세요.")
                stdId = int(widget.item(row, HAKBUN_COL).text())
                backend.saveScore(subId, stdId, score, asses)  # 새로 저장.
        QMessageBox.about(self, "결과", "점수 저장 성공.")
        showScoreList(self)


def returnGradeAssesments(assesments, grade):
    parsedAssesments = []
    for asses in assesments:
        assesGrade = asses[1]
        assesContent = asses[2]
        if assesGrade == grade:
            parsedAssesments.append(assesContent)
    return parsedAssesments


# 점수, 평가 리스트 보여주는 함수
def showScoreList(self):
    subId = int(self.scoreSubTreeWidget.currentItem().whatsThis(0))
    rowCount = self.classListWidget.rowCount()
    widget = self.classListWidget

    for row in range(0, rowCount):
        stdId = int(widget.item(row, HAKBUN_COL).text())
        scoreId = None
        score = None
        asses = None
        if backend.returnScore(subId, stdId) is not None:
            scoreId, score, asses = backend.returnScore(subId, stdId)
        # print(scoreId, score, asses)
        if scoreId is not None:  # 점수표 존재
            if score is None and asses is not None:  # 점수 미존재, 평가문 존재
                score = ""
                scoreItem = QTableWidgetItem(str(score))
                scoreItem.setWhatsThis(str(scoreId))
                comboItem = QComboBox()
                comboItem.addItem(asses)
                comboItem.setEditable(True)
                widget.setItem(row, SCORE_COL, scoreItem)
                widget.setCellWidget(row, ASSES_COL, comboItem)
            elif score is not None and asses is None:  # 점수 존재, 평가문 미존재
                asses = ""
                scoreItem = QTableWidgetItem(str(score))
                scoreItem.setWhatsThis(str(scoreId))
                comboItem = QComboBox()
                comboItem.addItem(asses)
                comboItem.setEditable(True)
                widget.setItem(row, SCORE_COL, scoreItem)
                widget.setCellWidget(row, ASSES_COL, comboItem)
            elif score is None and asses is None:  # 점수 미존재, 평가문 미존재
                score = ""
                asses = ""
                scoreItem = QTableWidgetItem(str(score))
                scoreItem.setWhatsThis(str(scoreId))
                comboItem = QComboBox()
                comboItem.addItem(asses)
                comboItem.setEditable(True)
                widget.setItem(row, SCORE_COL, scoreItem)
                widget.setCellWidget(row, ASSES_COL, comboItem)
            elif score is not None and asses is not None:  # 점수 존재, 평가문 존재
                possibleAssesments = getPossibleAssesmentByScore(subId, int(score))
                if asses not in possibleAssesments:
                    possibleAssesments.append(asses)
                scoreItem = QTableWidgetItem(str(score))
                scoreItem.setWhatsThis(str(scoreId))
                comboItem = QComboBox()
                comboItem.addItems(possibleAssesments)
                comboItem.setCurrentText(asses)
                comboItem.setEditable(True)
                widget.setItem(row, SCORE_COL, scoreItem)
                widget.setCellWidget(row, ASSES_COL, comboItem)
        else:  # 점수표 미존재
            scoreItem = QTableWidgetItem("")
            scoreItem.setWhatsThis("")
            comboItem = QComboBox()
            comboItem.addItem("")
            comboItem.setEditable(True)
            widget.setItem(row, SCORE_COL, scoreItem)
            widget.setCellWidget(row, ASSES_COL, comboItem)

    return


def getPossibleAssesmentByScore(subId, score):
    items = backend.returnScoreRangeAndContentBySubId(int(subId))
    possibleAssesments = []
    for item in items:
        content = item[3]
        greater = float(item[1])
        less = float(item[2])
        if greater < score <= less:
            possibleAssesments.append(content)
    return possibleAssesments


# 점수 등급별 랜덤 평가 생성 함수 (선택)
def insertIndiRandomAssesment(self):
    widget = self.classListWidget
    if self.scoreSubTreeWidget.currentItem() is None:
        return QMessageBox.about(self, "오류", "과목을 선택해주세요.")

    subId = int(self.scoreSubTreeWidget.currentItem().whatsThis(0))
    items = widget.selectedItems()
    if not items:
        return QMessageBox.about(self, "주의", "평가를 생성할 점수를 선택해주세요. (중복선택가능)")

    for i in range(0, len(items)):
        if widget.selectedItems()[i].column() is SCORE_COL:
            row = widget.selectedItems()[i].row()
            score = widget.item(row, SCORE_COL).text()
            asses = ""
            if widget.item(row, ASSES_COL):
                asses = widget.item(row, ASSES_COL).text()
            if score == "" and asses != "":
                comboItem = QComboBox()
                comboItem.addItems([""])
                comboItem.setEditable(True)
                widget.setCellWidget(row, ASSES_COL, comboItem)
            elif score != "" and asses == "":
                assesments = getPossibleAssesmentByScore(subId, float(score))
                if len(assesments) == 0:
                    comboItem = QComboBox()
                    comboItem.addItems([""])
                    comboItem.setEditable(True)
                    widget.setCellWidget(row, ASSES_COL, comboItem)
                else:
                    randomIndex = random.randint(0, len(assesments) - 1)
                    comboItem = QComboBox()
                    comboItem.addItems(assesments)
                    comboItem.setCurrentIndex(randomIndex)
                    comboItem.setEditable(True)
                    widget.setCellWidget(row, ASSES_COL, comboItem)
        else:
            return QMessageBox.about(self, "주의", "평가를 생성할 점수를 선택해주세요. (중복선택가능)")
    return QMessageBox.about(self, "알림", "선택 평가 생성 완료. DB에 반영하려면 저장 눌러주세요.")


# 점수 등급별 랜덤 평가 생성 함수 (전체)
def insertRandomAssesment(self):
    widget = self.classListWidget
    rowCount = widget.rowCount()
    if self.scoreSubTreeWidget.currentItem() is None:
        return QMessageBox.about(self, "오류", "과목을 선택해주세요.")

    subId = int(self.scoreSubTreeWidget.currentItem().whatsThis(0))

    for row in range(0, rowCount):
        score = widget.item(row, SCORE_COL).text()
        asses = ""
        if widget.item(row, ASSES_COL):
            asses = widget.item(row, ASSES_COL).text()
        if score == "" and asses != "":
            comboItem = QComboBox()
            comboItem.addItems([""])
            comboItem.setEditable(True)
            widget.setCellWidget(row, ASSES_COL, comboItem)

        elif score != "" and asses == "":
            assesments = getPossibleAssesmentByScore(subId, float(score))
            if len(assesments) == 0:
                comboItem = QComboBox()
                comboItem.addItems([""])
                comboItem.setEditable(True)
                widget.setCellWidget(row, ASSES_COL, comboItem)
            else:
                randomIndex = random.randint(0, len(assesments) - 1)
                comboItem = QComboBox()
                comboItem.addItems(assesments)
                comboItem.setCurrentIndex(randomIndex)
                comboItem.setEditable(True)
                widget.setCellWidget(row, ASSES_COL, comboItem)
    return QMessageBox.about(self, "알림", "전체 평가 생성 완료. DB에 반영하려면 저장 눌러주세요.")


# 학급 리스트 출력 함수
def insertClassComboBox(combobox):
    combobox.clear()
    classes = backend.returnClassList()
    for i in range(0, len(classes)):
        combobox.addItem(str(classes[i][0]) + "학년 " + str(classes[i][1]) + "반")


def returnClassInteger(classes):
    classes = classes.replace(" ", "")
    grade, ban = classes.split("학년")
    ban = ban.replace("반", "")
    return int(grade), int(ban)


# 선택 학급 조회 함수
def showClassMemberList(self):
    self.standardListWidget.clear()
    if self.scoreSubTreeWidget.currentItem() is None:
        return QMessageBox.about(self, "주의", "학급 리스트를 불러올 과목을 선택해주세요.")
    subId = int(self.scoreSubTreeWidget.currentItem().whatsThis(0))
    grade, classes = returnClassInteger(self.classList.currentText())
    members = backend.returnClassMemberList(grade, classes)
    standards = backend.returnStandardBySubId(subId)
    headers = ["이름", "학번", "점수", "평가"]
    self.selectedSubjectLabel.setText(self.scoreSubTreeWidget.currentItem().text(0))
    for stnd in standards:
        content = "기준: " + stnd[2] + "  " + str(stnd[3]) + " 초과  " + str(stnd[4]) + " 이하"
        self.standardListWidget.addItem(content)

    self.classListWidget.setRowCount(len(members))
    self.classListWidget.setColumnCount(4)
    self.classListWidget.setHorizontalHeaderLabels(headers)

    for i in range(0, len(members)):
        name = QTableWidgetItem(str(members[i][0]))
        stdId = QTableWidgetItem(str(members[i][1]))
        self.classListWidget.setItem(i, NAME_COL, name)
        self.classListWidget.setItem(i, HAKBUN_COL, stdId)

    self.showScoreList()
    resizeColumnWidth(self)
