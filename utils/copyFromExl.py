from PyQt5.Qt import QApplication

def getCopyContent():
    mimeType = 'application/x-qt-windows-mime;value="Csv"'
    clipboard = QApplication.clipboard()
    mimeData = clipboard.mimeData()
    if mimeType in mimeData.formats():  # 엑셀에서 복사해온 텍스트인지 확인
        text = clipboard.text()
        content = text.split("\n")
        content.remove("")
        return content
