from PyQt5 import QtGui
from PyQt5.QtWidgets import QTreeWidget, QMessageBox


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
                notice = copySrcName+" 을 "+copyTrgName+" 로 복사하시겠습니까?"
            QMessageBox.question(self, "알림", notice, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
