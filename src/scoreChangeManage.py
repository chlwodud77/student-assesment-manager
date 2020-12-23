#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

from PyQt5.QtWidgets import *

from model import Student, Score, Subject, Standard, Assesment

NAME_COL = 0
HAKBUN_COL = 1
SUBJECTA_COL = 2
SUBJECTB_COL = 3
SCORE_CHANGE_COL = 4
ASSES_COL = 5

global scoreChangeAssesments
scoreChangeAssesments = []


def resizeColumnWidth(header):
    header.setSectionResizeMode(ASSES_COL, QHeaderView.Stretch)
    header.setSectionResizeMode(NAME_COL, QHeaderView.ResizeToContents)
    header.setSectionResizeMode(HAKBUN_COL, QHeaderView.ResizeToContents)
    header.setSectionResizeMode(SUBJECTA_COL, QHeaderView.ResizeToContents)
    header.setSectionResizeMode(SUBJECTB_COL, QHeaderView.ResizeToContents)
    header.setSectionResizeMode(SCORE_CHANGE_COL, QHeaderView.ResizeToContents)
    header.setSectionResizeMode(ASSES_COL, QHeaderView.ResizeToContents)


def setScoreChangeAssesment(self):
    global subjectCId
    subjectAWidget = self.selectedSubjectLeft
    subjectBWidget = self.selectedSubjectRight
    subjectCWidget = self.selectedChangeSubject

    grade, classes = returnClassInteger(self.scoreChangeClassList.currentText())
    studentObjectArray = Student.getStudentsByGradeAndClass(grade, classes)

    if (subjectAWidget.count() == 1 and
            subjectBWidget.count() == 1 and
            subjectCWidget.count() == 1):

        subjectAId = subjectAWidget.item(0).whatsThis()
        subjectBId = subjectBWidget.item(0).whatsThis()
        subjectCId = subjectCWidget.item(0).whatsThis()
        subjectAScoreArray = Score.getScoreBySubIdAndClass(subjectAId, grade, classes)
        subjectBScoreArray = Score.getScoreBySubIdAndClass(subjectBId, grade, classes)
        compareSubject = Subject.getSubjectBySubId(subjectCId)
        compareStandardArray = Standard.getStandardBySubId(subjectCId)
        compareAssesmentArray = Assesment.getAssesmentBySubId(subjectCId)

        if (subjectAScoreArray == [] or subjectBScoreArray == [] or compareSubject == []
                or compareStandardArray == [] or compareAssesmentArray == []):
            return QMessageBox.about(self, "알림", "점수를 비교할 과목들의 점수 존재 여부와 비교 과목 상태를 확인해주세요.")

        showScoreList(self, studentObjectArray, subjectAScoreArray,
                      subjectBScoreArray, compareStandardArray, compareAssesmentArray)
        resizeColumnWidth(self.scoreChangeWidget.horizontalHeader())

    else:
        QMessageBox.about(self, "알림", "비교할 과목들을 모두 선택해주세요!")


def showScoreList(self, studentArray, scoreAArray, scoreBArray, standardArray, assesmentArray):
    widget = self.scoreChangeWidget
    widget.clear()
    headers = ["이름", "학번", "과목1점수", "과목2점수", "점수변동", "평가"]

    widget.setRowCount(len(studentArray))
    widget.setColumnCount(len(headers))
    widget.setHorizontalHeaderLabels(headers)

    commonAssesment1 = self.commonTextA.toPlainText()
    commonAssesment2 = self.commonTextB.toPlainText()

    commonAssesments = [commonAssesment1, commonAssesment2]

    for student, i in zip(studentArray, range(len(studentArray))):
        stdId = student.getId()
        name = student.getName()
        scoreAObj = getScoreByStdId(scoreAArray, stdId)
        scoreBObj = getScoreByStdId(scoreBArray, stdId)
        scoreChange = getScoreChange(scoreAObj, scoreBObj)
        assesment = getAssesmentFromScoreChange(scoreChange, standardArray, assesmentArray)
        assesment = addDescriptionToAsses(scoreChange, assesment, commonAssesments)

        nameItem = QTableWidgetItem(str(name))
        stdIdItem = QTableWidgetItem(str(stdId))
        scoreAItem = QTableWidgetItem(
            str(scoreAObj.getScore())) if scoreAObj.getScore() is not None else QTableWidgetItem("")
        scoreBItem = QTableWidgetItem(
            str(scoreBObj.getScore())) if scoreBObj.getScore() is not None else QTableWidgetItem("")
        scoreChangeItem = QTableWidgetItem(str(scoreChange)) if scoreChange is not None else QTableWidgetItem("")
        scoreAssesItem = QTableWidgetItem(str(assesment)) if assesment is not None else QTableWidgetItem("")

        widget.setItem(i, NAME_COL, nameItem)
        widget.setItem(i, HAKBUN_COL, stdIdItem)
        widget.setItem(i, SUBJECTA_COL, scoreAItem)
        widget.setItem(i, SUBJECTB_COL, scoreBItem)
        widget.setItem(i, SCORE_CHANGE_COL, scoreChangeItem)
        widget.setItem(i, ASSES_COL, scoreAssesItem)

        scoreObject = Score.Score()
        scoreObject.setSubId(subjectCId)
        scoreObject.setStdId(stdId)
        scoreObject.setScore(scoreChange)
        scoreObject.setAsses(assesment)
        scoreChangeAssesments.append(scoreObject)


def saveScoreChangeAssesment(self):
    if not scoreChangeAssesments: return QMessageBox.about(self, "알림", "점수변동평가를 먼저 생성해주세요.")
    for score in scoreChangeAssesments:
        subId = score.getSubId()
        stdId = score.getStdId()
        scoreNum = score.getScore()
        asses = score.getAsses()

        if Score.isScoreExist(subId, stdId):
            result = Score.saveScore(subId, stdId, scoreNum, asses)
            if result:
                QMessageBox.about(self, "알림", "점수변동평가 저장 완료.")
            else:
                return QMessageBox.about(self, "알림", "점수변동평가 저장 실패.")
        else:
            result = Score.updateScore(subId, stdId, scoreNum, asses)
            if result:
                QMessageBox.about(self, "알림", "점수변동평가 업데이트 완료.")
            else:
                return QMessageBox.about(self, "알림", "점수변동평가 저장 실패.")

    del scoreChangeAssesments[:]


def addDescriptionToAsses(scoreChange, assesment, commonAssesments):
    if scoreChange is None or assesment is None: return None
    # if scoreChange > 0:
    #     return "점수가 " + str(scoreChange) + "점 향상되어 " + assesment
    # elif scoreChange < 0:
    #     return "점수가 " + str(scoreChange) + "점 하락하여 " + assesment
    return commonAssesments[0] + " " + str(scoreChange) + " " + commonAssesments[1] + " " + assesment


def getScoreByStdId(scoreArray, stdId):
    try:
        for score in scoreArray:
            if score.getStdId() == stdId:
                return score
    except Exception as e:
        print(e)
        return []


def getScoreChange(scoreA, scoreB):
    try:
        if scoreA.getScore() is None or scoreB.getScore() is None: return
        return scoreB.getScore() - scoreA.getScore()
    except Exception as e:
        print(e)


def getAssesmentFromScoreChange(changeScore, standardArray, assesmentArray):
    try:
        if changeScore is None: return

        changeScore = float(changeScore)
        for standard in standardArray:
            greater = standard.getGreater()
            less = standard.getLess()
            if greater < changeScore <= less:
                assesment = getRandomAssesmentByStndId(assesmentArray, standard.getId())
                return assesment

    except Exception as e:
        print(e)


def getRandomAssesmentByStndId(assesmentArray, stndId):
    try:
        assesments = []
        for assesment in assesmentArray:
            assesStndId = assesment.getStandardId()
            if assesStndId == stndId: assesments.append(assesment.getContent())

        random.shuffle(assesments)
        return assesments[0]
    except Exception as e:
        print(e)


def returnClassInteger(classes):
    classes = classes.replace(" ", "")
    grade, ban = classes.split("학년")
    ban = ban.replace("반", "")
    return int(grade), int(ban)
