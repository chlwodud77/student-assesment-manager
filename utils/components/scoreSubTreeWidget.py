from PyQt5 import QtGui
from PyQt5.QtWidgets import QTreeWidget, QMessageBox
from utils import copyManager
from model import Score as Sc

from utils.adapter import subjectTreeWidgetAdapter


class ScoreSubTreeWidget(QTreeWidget):
    def __init__(self):
        QTreeWidget.__init__(self)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)

    def dragEnterEvent(self, e: QtGui.QDragEnterEvent):
        if e.source() == self:
            if e.source().currentItem().parent():
                e.accept()
                name = e.source().currentItem().text(0)
                print("drag from child self")

    def dropEvent(self, e: QtGui.QDropEvent):
        if e.source().itemAt(e.pos()) is not None:
            if not e.source().itemAt(e.pos()).parent():
                print("drop!")
                copySrcName = e.source().currentItem().text(0)
                copyTrgName = e.source().itemAt(e.pos()).text(0)
                notice = copySrcName + " 을 " + copyTrgName + " 로 복사하시겠습니까?"
                buttonReply = QMessageBox.question(self, "알림", notice, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if buttonReply == QMessageBox.Yes:
                    copySrcSubId = e.source().currentItem().whatsThis(0)
                    copyTrgParentSubId = e.source().itemAt(e.pos()).whatsThis(0)
                    copyTrgSubId = copyManager.copyChildSubject(copySrcName, copySrcSubId, copyTrgParentSubId)
                    orgScores = Sc.getScoreBySubId(copySrcSubId)
                    for scores in orgScores:
                        print(scores.getStdId(), scores.getAsses())
                        copyManager.copyScore(scores, copyTrgSubId)

                    QMessageBox.about(self,"알림", "과목 및 평가문 복사 완료.")
                    subjectTreeWidgetAdapter.showSub(self)



