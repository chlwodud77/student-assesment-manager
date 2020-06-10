import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from openpyxl import load_workbook
import sqlite3


#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("manager.ui")[0]


#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.fileUpdBtn.clicked.connect(self.uploadFile)
        self.clsSaveBtn.clicked.connect(self.uploadCls)

    #엑셀로 불러온 학급 구성원 db 에 업로드 
    def uploadCls(self):
        conn = sqlite3.connect("studentManager.db")
        sql = "insert into Student(IdCode, name, grade, class) values (?,?,?,?)"

        focGrade = int(self.grdListComboBox.currentText())
        focClass = int(self.clsListComboBox.currentText())

        try:    
            with conn:
                c = conn.cursor()
                for i in range(self.stdListWidget.rowCount()):
                    placeholder = []
                    for j in range(self.stdListWidget.columnCount()):
                        if j == 0:
                            placeholder.append(int(self.stdListWidget.item(i,j).text()))
                        else: 
                            placeholder.append(self.stdListWidget.item(i,j).text())
                    c.execute(sql, (placeholder[0], placeholder[1], focGrade, focClass))
            QMessageBox.about(self, "결과", "성공")   
        except sqlite3.IntegrityError:
            print("문제 발생")
            QMessageBox.about(self, "오류", "실패")


    #학급 구성원 엑셀 파일로 불러와서 리스트로 보여줌
    def uploadFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        if(fname[0]):    
            wb = load_workbook(filename = fname[0]) 
            ws = wb["Sheet1"]
            max_row = ws.max_row
            max_col = ws.max_column

            widget = self.stdListWidget
            widget.setRowCount(max_row-1)
            widget.setColumnCount(max_col)
            headers = []
            for i in range(1, max_col+1):
                headers.append(str(ws.cell(row=1, column= i).value))
            widget.setHorizontalHeaderLabels(headers)

            for i in range(2, max_row+1):
                for j in range(1, max_col+1):
                    cellValue = str(ws.cell(row=i, column= j).value)
                    item = QTableWidgetItem(cellValue)
                    widget.setItem(i-2,j-1,item)

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()