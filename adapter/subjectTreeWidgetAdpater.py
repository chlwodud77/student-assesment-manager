import backend
from PyQt5.QtWidgets import *


def showSub(self, treeWidget):
    subList       = backend.returnSubList()
    subTreeWidget = treeWidget
    subTreeWidget.clear()
    subTreeWidget.setColumnCount(1)
    # subTreeWidget.setHeaderLabels(["과목"])

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

def showSelectedSubjectByListWidget(self, srcWidget, listWidget, isMultiple):
    srcWidget = srcWidget
    targetWidget = listWidget

    if(isMultiple == False):
        listWidget.takeItem(0)

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
                targetWidget.addItem(newItem)
