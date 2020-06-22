import sqlite3

conn = sqlite3.connect("studentManager.db")


def returnAssesmetnStandardBySubIdAndGrade(subId, grade):
    try:
        with conn:
            sql = "select distinct greater, less from Assesment where subId = ? and grade = ?"
            return conn.cursor().execute(sql, (int(subId), str(grade))).fetchall()
    except sqlite3.IntegrityError:
        print("과목 평가문 조회 오류")

def returnAssesmentContentBySubIdAndGrade(subId, grade):
    sconn = sqlite3.connect("studentManager.db")
    sconn.row_factory = lambda cursor, row: row[0]
    try:
        with sconn:
            sql = "select content from Assesment where subId = ? and grade = ?"
            return sconn.cursor().execute(sql, (subId, grade)).fetchall()
    except sqlite3.IntegrityError:
        print("과목 평가문 조회 오류")
    

def returnAssesmentContentById(id):
    try:
        with conn:
            sql = "SELECT content FROM Assesment WHERE id = ?"
            return conn.cursor().execute(sql, (id,)).fetchone()[0]
    except sqlite3.IntegrityError:
        print("과목 평가문 조회 오류")
        
def returnAssementStandardBySubId(subId):
    try:
        with conn:
            sql = "SELECT DISTINCT grade, greater, less FROM Assesment WHERE subId = ?"
            return conn.cursor().execute(sql, (subId,)).fetchall()
    except sqlite3.IntegrityError:
        print("과목 조회 오류")
        
def returnAssesmentBySubId(subId):                         
    try:
        with conn:
            sql = "SELECT id, grade, content FROM Assesment WHERE subId = ?"
            return conn.cursor().execute(sql, (subId,)).fetchall()
    except sqlite3.IntegrityError:
        print("과목 평가문 조회 오류")
        

def returnClassAssesmentBySubId(subId, grade, classes):
    try:
        with conn:
            sql = "SELECT Student.name, Student.id, Score.asses FROM Student INNER JOIN Score ON Student.id = Score.stdId WHERE Score.subId = ? and Student.grade = ? and Student.class = ?"
            return conn.cursor().execute(sql, (subId, grade, classes)).fetchall()
    except sqlite3.IntegrityError:
        print("과목 조회 오류")

def returnClassSubList(grade, classes):
    try:
        with conn:
            sql = "select DISTINCT Subject.id as subId, Subject.subName, Subject.parentId FROM Subject INNER JOIN Score ON Score.subId = Subject.id INNER JOIN Student ON Score.stdId = Student.id WHERE Student.grade = ? and Student.class = ?"
            return conn.cursor().execute(sql, (grade, classes)).fetchall()
    except sqlite3.IntegrityError:
        print("과목 조회 오류")
        
def returnClassMemberList(grade, classes):
    try:
        with conn:
            sql = "SELECT name, id FROM Student WHERE grade = ? and class = ?"
            return conn.cursor().execute(sql, (grade, classes)).fetchall()
    except sqlite3.IntegrityError:
        print("학급 구성원 조회 오류")
        
def returnClassList():
    try:
        with conn:
            sql = "SELECT DISTINCT grade, class from Student"
            return conn.cursor().execute(sql).fetchall()
    except sqlite3.IntegrityError:
        print("학급 조회 오류")

def returnChildSubjectId(name, parentId):
    try:
        with conn:
            sql = "SELECT id FROM Subject WHERE subName = ? and parentId = ?"
            return conn.cursor().execute(sql, (name, parentId)).fetchone()[0]
    except sqlite3.IntegrityError:
        print("점수 저장 오류")

def returnScore(subId, stdId):
    try:
        with conn:
            sql = "SELECT id, score, asses FROM Score WHERE subId = ? and stdId = ?"
            return conn.cursor().execute(sql, (int(subId), int(stdId),)).fetchone()
    except sqlite3.IntegrityError:
        print("점수 조회 오류")

def returnSubNameBySubId(subId):
    try:
        with conn:
            sql = "SELECT subName FROM Subject WHERE id = ?"
            return conn.cursor().execute(sql, (subId,)).fetchone()[0]
    except sqlite3.IntegrityError:
        print("과목 조회 오류")
        
def returnSubList():
    try:    
        with conn:
            sql = "select id, subName, parentId from Subject"
            return conn.cursor().execute(sql).fetchall()
    except sqlite3.IntegrityError:
        print("문제 발생")
        
def deleteAssesmentBySubId(subId):
    try:
        with conn:
            sql = "DELETE FROM Assesment WHERE subId = ?"
            conn.cursor().execute(sql, (subId,))
            return True
    except sqlite3.IntegrityError:
        print("점수 삭제 오류") 
        return False

def deleteScoreById(id):
    try:
        with conn:
            sql = "DELETE FROM Score WHERE id = ?"
            conn.cursor().execute(sql, (id,))
    except sqlite3.IntegrityError:
        print("점수 삭제 오류")
        
def deleteSubById(subId):
    try:
        with conn:
            sql1 = "delete from Subject where parentId = ?"
            sql2 = "delete from Subject where id = ?"
            sql3 = "delete from Assesment where subId = ?"
            c = conn.cursor()
            c.execute(sql1, (subId,))
            c.execute(sql2, (subId,))
            c.execute(sql3, (subId,))
            return True  
    except sqlite3.IntegrityError:
        print("과목 삭제 문제 발생")
        return False
        
def saveScore(subId, stdId, score, asses):
    try:
        with conn:
            sql = "INSERT into Score(subId, stdId, score, asses) VALUES (?,?,?,?)"
            conn.cursor().execute(sql, (subId, stdId, score, asses))
            return True
    except sqlite3.IntegrityError:
        print("점수 저장 오류")
        return False
        
def createAssesment(subId, grade, content, greater, less):
    try:
        with conn:
            sql = "INSERT into Assesment(subId, grade, content, greater, less) VALUES (?,?,?,?,?)"
            conn.cursor().execute(sql, (subId, grade, content, greater, less))
            return True
    except sqlite3.IntegrityError:
        print("하위 과목 저장 오류")
        return False
        
def createChildSubject(name, parentId):
    try:
        with conn:
            sql = "INSERT into Subject(subName, parentId) VALUES (?,?)"
            conn.cursor().execute(sql, (name, parentId))
            return True
    except sqlite3.IntegrityError:
        print("하위 과목 저장 오류")
        return False

def createParentSubject(name):
    try:
        with conn:
            sql = "INSERT into Subject(subName) VALUES (?)"
            conn.cursor().execute(sql, (name,))
            return True
    except sqlite3.IntegrityError:
        print("상위 과목 저장 오류")
        return False
        
def saveStudent(name, grade, classes):
    try:
        with conn:
            sql = "insert into Student(name, grade, class) values (?,?,?)"
            conn.cursor().execute(sql, (name, grade, classes))
            return True  
    except sqlite3.IntegrityError:
        print("과목 저장 문제 발생")
        QMessageBox.about(self, "결과", "학생 저장 실패.")
        return False
