# from PyQt5.Qt import QApplication
from PyQt5.QtWidgets import QApplication


def getCopyContent():
    # mimeType = 'application/x-qt-windows-mime;value="Csv"'
    clipboard = QApplication.clipboard()
    # mimeData = clipboard.mimeData()
    # print(mimeData.formats())
    # print(clipboard.text())
    # if mimeType in mimeData.formats():  # 엑셀에서 복사해온 텍스트인지 확인
    #     text = clipboard.text()
    #     content = text.split("\n")
    #     content.remove("")
    #     print(content)
    #     return content
    text = clipboard.text()
    content = text.split("\n")
    content.remove("")
    return content
