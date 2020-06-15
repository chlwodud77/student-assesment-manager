import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from openpyxl import load_workbook
import sqlite3, random



#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("manager.ui")[0]


#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.showSub()
        self.insertSubComboBox()
        self.insertClassComboBox()


        self.fileUpdBtn.clicked.connect(self.uploadFile)
        self.clsSaveBtn.clicked.connect(self.uploadCls)
        self.subSaveBtn.clicked.connect(self.saveSub)
        self.subSrhBtn.clicked.connect(self.searchSub)
        self.subDelBtn.clicked.connect(self.delSub)
        
        self.grdAseDelBtn.clicked.connect(self.delAse)
        self.grdAseAddBtn.clicked.connect(self.addAse)
        self.grdAseModBtn.clicked.connect(self.modAse)
        self.grdAAseList.clicked.connect(self.activateEdit)
        self.grdBAseList.clicked.connect(self.activateEdit)
        self.grdCAseList.clicked.connect(self.activateEdit)

        self.callClassMemberBtn.clicked.connect(self.showClassMemberList)
        self.createAssesmentBtn.clicked.connect(self.insertRandomAssesment)

    ##############점수입력###########################

    def returnAssementStandard(self, subId):
        conn = sqlite3.connect("studentManager.db")
        try:
            with conn:
                sql = "SELECT DISTINCT grade, greater, less FROM Assesment WHERE subId = ?"
                return conn.cursor().execute(sql, (subId,)).fetchall()
        except sqlite3.IntegrityError:
            print("과목 조회 오류")


    def returnSubId(self, subName):
        conn = sqlite3.connect("studentManager.db")
        try:
            with conn:
                sql = "SELECT id FROM Subject WHERE subName = ?"
                return conn.cursor().execute(sql, (subName,)).fetchone()[0]
        except sqlite3.IntegrityError:
            print("과목 조회 오류")

    def returnRandomAssesment(self, subId):
        conn = sqlite3.connect("studentManager.db")
        try:
            with conn:
                sql = "SELECT grade, content FROM Assesment WHERE subId = ?"
                return conn.cursor().execute(sql, (subId,)).fetchall()
        except sqlite3.IntegrityError:
            print("과목 평가문 조회 오류")


    def returnClassMemberList(self, grade, classes):
        conn = sqlite3.connect("studentManager.db")
        try:
            with conn:
                sql = "SELECT name, id FROM Student WHERE grade = ? and class = ?"
                return conn.cursor().execute(sql, (grade, classes)).fetchall()
        except sqlite3.IntegrityError:
            print("학급 구성원 조회 오류")

    def returnClassList(self):
        conn = sqlite3.connect("studentManager.db")
        try:
            with conn:
                sql = "SELECT DISTINCT grade, class from Student"
                return conn.cursor().execute(sql).fetchall()
        except sqlite3.IntegrityError:
            print("학급 조회 오류")

    def returnSubList(self):
        conn = sqlite3.connect("studentManager.db")
        conn.row_factory = lambda cursor, row: row[0]
        try:
            with conn:
                sql = "select subName from Subject"
                return conn.cursor().execute(sql).fetchall()

        except sqlite3.IntegrityError:
            print("과목 조회 오류")

    #점수 등급별 랜덤 평가 생성 함수
    def insertRandomAssesment(self):
        grdAList = []
        grdBList = []
        grdCList = []
        subId = self.returnSubId(self.subList.currentText())
        grdStandard = self.returnAssementStandard(subId)
        assementList = self.returnRandomAssesment(subId)
        for i in range(0, len(assementList)):
            if(assementList[i][0] == "A"):
                grdAList.append(assementList[i][1])
            elif(assementList[i][0] == "B"):
                grdBList.append(assementList[i][1])
            elif(assementList[i][0] == "C"):
                grdCList.append(assementList[i][1])

        
        for i in range(0, self.classListWidget.rowCount()):
            for j in range(0, len(grdStandard)):
                if(self.classListWidget.item(i,2)):
                    score = int(self.classListWidget.item(i,2).text())
                    if(grdStandard[j][1] < score and score <= grdStandard[j][2]):
                        if(grdStandard[j][0] == "A"):
                            randomIndex = random.randint(0, len(grdAList)-1)
                            self.classListWidget.setItem(i,3,QTableWidgetItem(grdAList[randomIndex]))
                        elif(grdStandard[j][0] == "B"):
                            randomIndex = random.randint(0, len(grdBList)-1)
                            self.classListWidget.setItem(i,3,QTableWidgetItem(grdBList[randomIndex]))
                        elif(grdStandard[j][0] == "C"):
                            randomIndex = random.randint(0, len(grdCList)-1)
                            self.classListWidget.setItem(i,3,QTableWidgetItem(grdCList[randomIndex]))
    
    #과목 리스트 출력 함수
    def insertSubComboBox(self):
        subjects = self.returnSubList()
        for i in range(0, len(subjects)):
            self.subList.addItem(str(subjects[i]))

    #학급 리스트 출력 함수
    def insertClassComboBox(self):
        classes = self.returnClassList()
        for i in range(0, len(classes)):
            self.classList.addItem(str(classes[i][0])+"학년 "+str(classes[i][1])+"반")

    #선택 학급 조회 함수
    def showClassMemberList(self):     
        grade = int(self.classList.currentText()[0])
        classes = int(self.classList.currentText()[4])
        members = self.returnClassMemberList(grade, classes)
        headers = ["이름", "학번", "점수", "평가"]

        self.classListWidget.setRowCount(len(members))
        self.classListWidget.setColumnCount(4)
        self.classListWidget.setHorizontalHeaderLabels(headers)

        for i in range(0, len(members)):
            name = QTableWidgetItem(str(members[i][0]))
            stdId = QTableWidgetItem(str(members[i][1]))
            self.classListWidget.setItem(i, 0, name)
            self.classListWidget.setItem(i, 1, stdId)
            
        

    ##############과목관리###########################
    
    #선택 과목 삭제 함수
    def delSub(self):
        conn = sqlite3.connect("studentManager.db")
        clickedSub = self.subListWidget.currentItem().text()
        sql1 = "select id from Subject where subName = ?"
        sql2 = "delete from Subject where subName = ?"
        sql3 = "delete from Assesment where subId = ?"
        try:
            with conn:
                c = conn.cursor()
                subId = c.execute(sql1, (clickedSub,)).fetchone()[0]
                if(subId):
                    c.execute(sql2, (clickedSub,))
                    c.execute(sql3, (subId,))
                    QMessageBox.about(self, "결과", "삭제 성공")   

        except sqlite3.IntegrityError:
            print("과목 삭제 문제 발생")
            QMessageBox.about(self, "결과", "삭제 실패")

        self.showSub()


    #과목 리스트에서 과목 선택 조회 하면 과목 세부 내용 조회 함수
    def searchSub(self):
        conn = sqlite3.connect("studentManager.db")
        subListWidget = self.subListWidget
        clickedSub = subListWidget.currentItem().text()
        print(clickedSub)
        sql1 = "select id from Subject where subName = ?"
        sql2 = "select greater, less from Assesment where subId = ? and grade = ?"
        sql3 = "select content from Assesment where subId = ? and grade = ?"
        try:
            with conn:
                c = conn.cursor()
                subId = c.execute(sql1, (clickedSub,)).fetchone()[0]
                grdARng = []
                grdBRng = []
                grdCRng = []
                if(subId):

                    #조회된 과목 등급 점수표 조회 및 출력
                    grdARng = c.execute(sql2, (subId, "A")).fetchall()
                    grdBRng = c.execute(sql2, (subId, "B")).fetchall()
                    grdCRng = c.execute(sql2, (subId, "C")).fetchall()

                    if(len(grdARng) != 0):
                        self.grdAEdit1.setText(str(grdARng[0][0]))
                        self.grdAEdit2.setText(str(grdARng[0][1]))
                    else:
                        self.grdAEdit1.setText(str("없음"))
                        self.grdAEdit2.setText(str("없음"))
                    if(len(grdBRng) != 0):
                        self.grdBEdit1.setText(str(grdBRng[0][0]))
                        self.grdBEdit2.setText(str(grdBRng[0][1]))
                    else:
                        self.grdBEdit1.setText(str("없음"))
                        self.grdBEdit2.setText(str("없음"))
                    if(len(grdCRng) != 0):
                        self.grdCEdit1.setText(str(grdCRng[0][0]))
                        self.grdCEdit2.setText(str(grdCRng[0][1]))
                    else:
                        self.grdCEdit1.setText(str("없음"))
                        self.grdCEdit2.setText(str("없음"))

                    #조회된 과목 이름 및 평가 출력
                    conn.row_factory = lambda cursor, row: row[0]
                    c = conn.cursor()
                    self.subTitleEdit.setText(str(clickedSub))
                    
                    grdAAse = []
                    grdBAse = []
                    grdCAse = []

                    grdAAse = c.execute(sql3, (subId, "A")).fetchall()
                    grdBAse = c.execute(sql3, (subId, "B")).fetchall()
                    grdCAse = c.execute(sql3, (subId, "C")).fetchall()

                    self.grdAAseList.setRowCount(len(grdAAse))
                    self.grdAAseList.setColumnCount(1)
                    self.grdBAseList.setRowCount(len(grdBAse))
                    self.grdBAseList.setColumnCount(1)
                    self.grdCAseList.setRowCount(len(grdCAse))
                    self.grdCAseList.setColumnCount(1)

                    for i in range(0, len(grdAAse)):
                        self.grdAAseList.setItem(i, 0, QTableWidgetItem(grdAAse[i]))
                    for i in range(0, len(grdBAse)):
                        self.grdBAseList.setItem(i, 0, QTableWidgetItem(grdBAse[i]))
                    for i in range(0, len(grdCAse)):
                        self.grdCAseList.setItem(i, 0, QTableWidgetItem(grdCAse[i]))

        except sqlite3.IntegrityError:
            print("과목조회 문제 발생")


    #db 에서 과목 리스트 가져와서 보여주는 함수
    def returnSubList(self):
        conn = sqlite3.connect("studentManager.db")
        conn.row_factory = lambda cursor, row: row[0]
        sql = "select subName from Subject"
        subList = []

        try:    
            with conn:
                c = conn.cursor()
                subList = c.execute(sql).fetchall()
                return subList
        except sqlite3.IntegrityError:
            print("문제 발생")

    def showSub(self):
        subList = self.returnSubList()
        subListWidget = self.subListWidget
        subListWidget.clear()

        for i in range (0, len(subList)):
            subListWidget.addItem(QListWidgetItem(subList[i]))



    #과목, 평가 등급 점수, 평가 내용 db 저장 함수
    def saveSub(self):
        subTitleEdit = self.subTitleEdit.text()
        print(subTitleEdit)
        grdAEdit1 = self.grdAEdit1.text()
        grdAEdit2 = self.grdAEdit2.text()
        grdBEdit1 = self.grdBEdit1.text()
        grdBEdit2 = self.grdBEdit2.text()
        grdCEdit1 = self.grdCEdit1.text()
        grdCEdit2 = self.grdCEdit2.text()

        grdAList = []
        grdBList = []
        grdCList = []

        for i in range (0,self.grdAAseList.rowCount()):
            for j in range (0,self.grdAAseList.columnCount()):
                grdAList.append(self.grdAAseList.item(i,j).text())

        for i in range (0,self.grdBAseList.rowCount()):
            for j in range (0,self.grdBAseList.columnCount()):
                grdBList.append(self.grdBAseList.item(i,j).text())

        for i in range (0,self.grdCAseList.rowCount()):
            for j in range (0,self.grdCAseList.columnCount()):
                grdCList.append(self.grdCAseList.item(i,j).text())

        conn = sqlite3.connect("studentManager.db")

        #기존 과목 없으면 새로 생성
        try:    
            with conn:
                if(not subTitleEdit):
                    QMessageBox.about(self, "오류", "과목을 입력하세요")
                else:
                    c = conn.cursor()
                    isExist = c.execute("select * from Subject where subName = ?", (subTitleEdit,)).fetchall()
                    if(not isExist):
                        c.execute("insert into Subject(subName) values (?)", (subTitleEdit,))

                    #기존 과목을 참조하여 평가지를 새로 생성 및 수정 (먼저 다 삭제했다가 다시 새로 생성)
                    subId = c.execute("select id from Subject where subName=?", (subTitleEdit,)).fetchone()[0]
                    c.execute("delete from Assesment where subId = ?", (subId,))
                    sql = "insert into Assesment(subId, grade, content, greater, less) values (?,?,?,?,?)"
                    for i in range(0, len(grdAList)):
                        c.execute(sql, (subId, "A", grdAList[i], int(grdAEdit1), int(grdAEdit2)))
                    
                    for i in range(0, len(grdBList)):
                        c.execute(sql, (subId, "B", grdBList[i], int(grdBEdit1), int(grdBEdit2)))

                    for i in range(0, len(grdCList)):
                        c.execute(sql, (subId, "C", grdCList[i], int(grdCEdit1), int(grdCEdit2)))

                    QMessageBox.about(self, "결과", "성공")   
        except sqlite3.IntegrityError:
            print("문제 발생")
            QMessageBox.about(self, "오류", "실패")

        self.showSub()
        
    # 평가 내용 수정 함수
    def modAse(self):
        focusedTab = self.grdAseWidget.currentIndex()
        if(focusedTab == 0):
            widget = self.grdAAseList
            content = self.grdAseEdit.toPlainText()
            widget.setItem(widget.currentRow(), widget.currentColumn(), QTableWidgetItem(content))

        
        elif(focusedTab == 1):
            widget = self.grdBAseList
            content = self.grdAseEdit.toPlainText()
            widget.setItem(widget.currentRow(), widget.currentColumn(), QTableWidgetItem(content))

        elif(focusedTab == 2):
            widget = self.grdCAseList
            content = self.grdAseEdit.toPlainText()
            widget.setItem(widget.currentRow(), widget.currentColumn(), QTableWidgetItem(content))

    #평가 내용 선택하면 편집기에 해당 내용 보여줌
    def activateEdit(self):
        focusedTab = self.grdAseWidget.currentIndex()
        if(focusedTab == 0):
            widget = self.grdAAseList
            self.grdAseEdit.setPlainText(widget.item(widget.currentRow(), widget.currentColumn()).text())

        
        elif(focusedTab == 1):
            widget = self.grdBAseList
            self.grdAseEdit.setPlainText(widget.item(widget.currentRow(), widget.currentColumn()).text())

        elif(focusedTab == 2):
            widget = self.grdCAseList
            self.grdAseEdit.setPlainText(widget.item(widget.currentRow(), widget.currentColumn()).text())

    #평가 내용 항목 지우는 함수
    def delAse(self):
        focusedTab = self.grdAseWidget.currentIndex()
        
        if(focusedTab == 0):
            row = self.grdAAseList.currentRow()
            col = self.grdAAseList.currentColumn()
            self.grdAAseList.removeRow(row)
        
        elif(focusedTab == 1):
            row = self.grdBAseList.currentRow()
            col = self.grdBAseList.currentColumn()
            self.grdBAseList.removeRow(row)

        
        elif(focusedTab == 2):
            row = self.grdCAseList.currentRow()
            col = self.grdCAseList.currentColumn()
            self.grdCAseList.removeRow(row)

    #평가 내용 추가 함수
    def addAse(self):
        focusedTab = self.grdAseWidget.currentIndex()
        content = self.grdAseEdit.toPlainText()
        item = QTableWidgetItem(content)
                
        if(focusedTab == 0):
            currentRowCnt = self.grdAAseList.rowCount()
            if(currentRowCnt == 0):
                self.grdAAseList.insertRow(currentRowCnt)
                self.grdAAseList.setItem(currentRowCnt, 0, item)
            else:
                self.grdAAseList.insertRow(currentRowCnt)
                self.grdAAseList.setItem(currentRowCnt, 0, item)
        elif(focusedTab == 1):
            currentRowCnt = self.grdBAseList.rowCount()
            if(currentRowCnt == 0):
                self.grdBAseList.insertRow(currentRowCnt)
                self.grdBAseList.setItem(currentRowCnt, 0, item)
            else:
                self.grdBAseList.insertRow(currentRowCnt)
                self.grdBAseList.setItem(currentRowCnt, 0, item)
        
        elif(focusedTab == 2):
            currentRowCnt = self.grdCAseList.rowCount()
            if(currentRowCnt == 0):
                self.grdCAseList.insertRow(currentRowCnt)
                self.grdCAseList.setItem(currentRowCnt, 0, item)
            else:
                self.grdCAseList.insertRow(currentRowCnt)
                self.grdCAseList.setItem(currentRowCnt, 0, item)
        
    ##############학급추가###########################
    
    #엑셀로 불러온 학급 구성원 db 에 업로드 
    def uploadCls(self):
        conn = sqlite3.connect("studentManager.db")
        sql = "insert into Student(id, name, grade, class) values (?,?,?,?)"

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