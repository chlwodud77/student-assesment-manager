from PyQt5 import QtGui
from PyQt5.QtWidgets import QTreeWidget, QMessageBox, QProgressBar
from tqdm import tqdm

from model import Score as Sc
from utils import copyManager
from utils.adapter import subjectTreeWidgetAdapter


class ScoreSubTreeWidget(QTreeWidget):

    def __init__(self):
        QTreeWidget.__init__(self)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(0, 300, 300, 50)
        self.pbar.setHidden(True)

    def dragEnterEvent(self, e: QtGui.QDragEnterEvent):
        if e.source() == self:
            if e.source().currentItem().parent():
                e.accept()

    def dropEvent(self, e: QtGui.QDropEvent):
        if e.source().itemAt(e.pos()) is not None:
            if not e.source().itemAt(e.pos()).parent():
                copySrcName = e.source().currentItem().text(0)
                copyTrgName = e.source().itemAt(e.pos()).text(0)
                notice = copySrcName + " 을 " + copyTrgName + " 로 복사하시겠습니까?"
                buttonReply = QMessageBox.question(self, "알림", notice, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if buttonReply == QMessageBox.Yes:
                    copySrcSubId = e.source().currentItem().whatsThis(0)
                    copyTrgParentSubId = e.source().itemAt(e.pos()).whatsThis(0)
                    copyTrgSubId = copyManager.copyChildSubject(copySrcName, copySrcSubId, copyTrgParentSubId)
                    orgScores = Sc.getScoreBySubId(copySrcSubId)
                    self.pbar.setHidden(False)
                    for scores, irange in zip(orgScores, tqdm(range(len(orgScores)))):
                        status = float(irange / len(orgScores) * 100)
                        self.pbar.setValue(status)
                        copyManager.copyScore(scores, copyTrgSubId)
                    self.pbar.setHidden(True)
                    QMessageBox.about(self, "알림", "과목 및 평가문 복사 완료.")
                    subjectTreeWidgetAdapter.showSub(self)
