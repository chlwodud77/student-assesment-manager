import sqlite3

DB_FILE = "studentManager.db"
SQL_CREATE_ASSESMENT_TABLE = """ CREATE TABLE IF NOT EXISTS "Assesment" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"subId"	INTEGER NOT NULL,
    "stndId"	INTEGER,
	"content"	TEXT,
	FOREIGN KEY("subId") REFERENCES "Subject"("id")
    FOREIGN KEY("stndId") REFERENCES "Standard"("id")
) """
SQL_CREATE_SCORE_TABLE = """ CREATE TABLE IF NOT EXISTS "Score" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"subId"	INTEGER,
	"stdId"	INTEGER,
	"score"	REAL,
	"asses"	TEXT,
	FOREIGN KEY("subId") REFERENCES "Subject"("id"),
	FOREIGN KEY("stdId") REFERENCES "Student"("id")
) """

SQL_CREATE_STANDARD_TABLE = """ CREATE TABLE IF NOT EXISTS"Standard" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"subId"	INTEGER,
	"grade"	TEXT,
	"greater"	INTEGER,
	"less"	INTEGER,
	FOREIGN KEY("subId") REFERENCES "Subject"("id")
) """

SQL_CREATE_STUDENT_TABLE = """ CREATE TABLE IF NOT EXISTS "Student" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"grade"	INTEGER NOT NULL,
	"class"	INTEGER NOT NULL,
	PRIMARY KEY("id")
) """

SQL_CREATE_SUBJECT_TABLE = """ CREATE TABLE IF NOT EXISTS "Subject" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"subName"	TEXT NOT NULL,
	"parentId"	INTEGER
) """

def createConnection(DB_FILE):
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def createTable(conn, SQL_CREATE_TABLE):
    try:
        c = conn.cursor()
        c.execute(SQL_CREATE_TABLE)
    except sqlite3.Error as e:
        print(e)

conn = createConnection(DB_FILE)

if conn is not None:
    createTable(conn, SQL_CREATE_STUDENT_TABLE)
    createTable(conn, SQL_CREATE_SUBJECT_TABLE)
    createTable(conn, SQL_CREATE_ASSESMENT_TABLE)
    createTable(conn, SQL_CREATE_SCORE_TABLE)
    createTable(conn, SQL_CREATE_STANDARD_TABLE)
    conn.commit()
    conn.close()
    

def returnAssesmentsByStandardId(stndId):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "SELECT id, content FROM Assesment WHERE stndId = ?"
            result = conn.cursor().execute(sql, (stndId,)).fetchall()
            return result
    except sqlite3.IntegrityError:
        print("과목 평가문 조회 오류")
        return False

def returnAssesmetnStandardBySubIdAndGrade(subId, grade):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "select distinct greater, less from Assesment where subId = ? and grade = ?"
            result = conn.cursor().execute(sql, (int(subId), str(grade))).fetchall()
            return result
    except sqlite3.IntegrityError:
        print("과목 평가문 조회 오류")

def returnAssesmentContentBySubIdAndGrade(subId, grade):
    sconn = sqlite3.connect("studentManager.db")
    # sconn.row_factory = lambda cursor, row: row[0]
    try:
        with sconn:
            sql = "select id, content from Assesment where subId = ? and grade = ?"
            result = sconn.cursor().execute(sql, (subId, grade)).fetchall()
            return result
    except sqlite3.IntegrityError:
        print("과목 평가문 조회 오류")
    

def returnAssesmentContentById(id):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "SELECT content FROM Assesment WHERE id = ?"
            result = conn.cursor().execute(sql, (id,)).fetchone()[0]
            return result
    except sqlite3.IntegrityError:
        print("과목 평가문 조회 오류")
        
def returnAssesmentStandardBySubId(subId):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "SELECT DISTINCT subId, grade, greater, less FROM Assesment WHERE subId = ?"
            result = conn.cursor().execute(sql, (subId,)).fetchall()
            return result
    except sqlite3.IntegrityError:
        print("과목 조회 오류")
        
def returnAssesmentBySubId(subId):       
    conn = createConnection(DB_FILE)                  
    try:
        with conn:
            sql = "SELECT id, grade, content FROM Assesment WHERE subId = ?"
            result = conn.cursor().execute(sql, (subId,)).fetchall()
            return result
    except sqlite3.IntegrityError:
        print("과목 평가문 조회 오류")
        

def returnClassAssesmentBySubId(subId, grade, classes):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "SELECT Student.name, Student.id, Score.asses FROM Student INNER JOIN Score ON Student.id = Score.stdId WHERE Score.subId = ? and Student.grade = ? and Student.class = ?"
            result = conn.cursor().execute(sql, (subId, grade, classes)).fetchall()
            return result
    except sqlite3.IntegrityError:
        print("과목 조회 오류")

def returnClassSubList(grade, classes):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "select DISTINCT Subject.id as subId, Subject.subName, Subject.parentId FROM Subject INNER JOIN Score ON Score.subId = Subject.id INNER JOIN Student ON Score.stdId = Student.id WHERE Student.grade = ? and Student.class = ?"
            result = conn.cursor().execute(sql, (grade, classes)).fetchall()
            return result
    except sqlite3.IntegrityError:
        print("과목 조회 오류")
        
def returnClassMemberList(grade, classes):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "SELECT name, id FROM Student WHERE grade = ? and class = ?"
            result = conn.cursor().execute(sql, (grade, classes)).fetchall()
            return result
    except sqlite3.IntegrityError:
        print("학급 구성원 조회 오류")

def returnClassMemberName(grade, classes):
    sconn = createConnection(DB_FILE)
    sconn.row_factory = lambda cursor, row: row[0]

    try:
        with sconn:
            sql = "SELECT name FROM Student WHERE grade = ? and class = ?"
            result = sconn.cursor().execute(sql, (grade, classes)).fetchall()
            return result
    except sqlite3.IntegrityError:
        print("학급 구성원 조회 오류")

def returnClassMemberNumber(grade, classes):
    sconn = createConnection(DB_FILE)
    sconn.row_factory = lambda cursor, row: row[0]

    try:
        with sconn:
            sql = "SELECT id FROM Student WHERE grade = ? and class = ?"
            result = sconn.cursor().execute(sql, (grade, classes)).fetchall()
            return result
    except sqlite3.IntegrityError:
        print("학급 구성원 조회 오류")
        
def returnStudentAssesmentBySubId(subId, stdId):
    sconn = createConnection(DB_FILE)
    sconn.row_factory = lambda cursor, row: row[0]
    try:
        with sconn:
            sql = "SELECT Score.asses FROM Student INNER JOIN Score ON Student.id = Score.stdId WHERE Score.subId = ? and Student.id = ?"
            result = sconn.cursor().execute(sql, (subId, stdId)).fetchall()
            return result
    except sqlite3.IntegrityError:
        print("평가문 조회 오류")

def returnClassList():
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "SELECT DISTINCT grade, class from Student"
            result = conn.cursor().execute(sql).fetchall()
            return result
    except sqlite3.IntegrityError:
        print("학급 조회 오류")

def returnParentSubject():
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "SELECT * FROM Subject where parentId is NULL"
            result = conn.cursor().execute(sql).fetchall()
            return result
    except sqlite3.IntegrityError:
        print("상위 과목 불러오기 오류")

def returnChildSubjectsFromParentId(parentId):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "SELECT * FROM Subject WHERE parentId = ?"
            result = conn.cursor().execute(sql, (parentId,)).fetchall()
            return result
    except sqlite3.IntegrityError:
        print("하위 과목 불러오기 오류")

def returnChildSubjectId(name, parentId):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "SELECT id FROM Subject WHERE subName = ? and parentId = ?"
            result = conn.cursor().execute(sql, (name, parentId)).fetchone()[0]
            return result
    except sqlite3.IntegrityError:
        print("점수 저장 오류")

def returnScore(subId, stdId):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "SELECT id, score, asses FROM Score WHERE subId = ? and stdId = ?"
            result = conn.cursor().execute(sql, (int(subId), int(stdId),)).fetchone()
            return result
    except sqlite3.IntegrityError:
        print("점수 조회 오류")

def returnScoreBySubIdAndClass(subId, grade, classes):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "SELECT Score.stdId, Score.score FROM Student INNER JOIN Score ON Student.id = Score.stdId AND Score.subId = ? AND Student.grade = ? AND Student.class = ?"
            result = conn.cursor().execute(sql, (int(subId), int(grade), int(classes))).fetchall()
            return result
    except sqlite3.IntegrityError:
        print("점수 조회 오류")

def returnSubNameBySubId(subId):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "SELECT subName FROM Subject WHERE id = ?"
            result = conn.cursor().execute(sql, (subId,)).fetchone()[0]
            return result
    except sqlite3.IntegrityError:
        print("과목 조회 오류")
        
def returnSubList():
    conn = createConnection(DB_FILE)
    try:    
        with conn:
            sql = "select id, subName, parentId from Subject"
            result = conn.cursor().execute(sql).fetchall()
            return result
    except sqlite3.IntegrityError:
        print("문제 발생")
        
def returnStandardBySubId(subId):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "SELECT id, subId, grade, greater, less FROM Standard Where subId = ?"
            result = conn.cursor().execute(sql, (subId,)).fetchall()
            return result
    except sqlite3.IntegrityError:
        print("평가 기준 불러오기 오류")
        return False

def returnStandardById(stndId):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "SELECT grade, greater, less FROM Standard WHERE id = ?"
            result = conn.cursor().execute(sql, (stndId,)).fetchone()
            return result
    except sqlite3.IntegrityError:
        print("평가 기준 불러오기 오류")
        return False

def returnIfStudentSubjectScoreExist(subId, stdId):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            result = []
            sql = "SELECT score, asses FROM Score WHERE subId = ? AND stdId = ?"
            result = conn.cursor().execute(sql, (subId, stdId)).fetchone()
            return result
    except sqlite3.IntegrityError:
        print("점수 확인 오류")
        return False

def returnScoreRangeAndContentBySubId(subId):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = """
                SELECT Assesment.subId, Standard.greater, Standard.less, Assesment.content
                FROM Assesment INNER JOIN Standard
                ON Assesment.subId = Standard.subId AND Assesment.stndId = Standard.id
                WHERE Standard.subId = ?
                """
            result = conn.cursor().execute(sql, (subId,)).fetchall()
            return result
    except sqlite3.IntegrityError:
        print("과목 점수별 평가문 불러오기 오류")
        return False

def deleteAssesmentById(id):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "DELETE FROM Assesment WHERE id = ?"
            conn.cursor().execute(sql, (id,))
            return True
    except sqlite3.IntegrityError:
        print("평가 삭제 오류") 
        return False
        
def deleteAssesmentBySubId(subId):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "DELETE FROM Assesment WHERE subId = ?"
            conn.cursor().execute(sql, (subId,))
            return True
    except sqlite3.IntegrityError:
        print("점수 삭제 오류") 
        return False

def deleteAssesmentByStndId(stndId):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "DELETE FROM Assesment WHERE stndId = ?"
            conn.cursor().execute(sql, (stndId,))
            return True
    except sqlite3.IntegrityError:
        print("평가문 삭제 오류")
        return False

def deleteClass(grade, classes):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "DELETE FROM Student WHERE grade = ? and class = ?"
            conn.cursor().execute(sql, (grade, classes))
            return True
    except sqlite3.IntegrityError:
        print("학급 삭제 오류") 
        return False

def deleteStudent(id):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "DELETE FROM Student WHERE id = ?"
            conn.cursor().execute(sql, (id,))
            return True
    except sqlite3.IntegrityError:
        print("학생 삭제 오류")
        return False

def deleteScoreById(id):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "DELETE FROM Score WHERE id = ?"
            conn.cursor().execute(sql, (id,))
            return True
    except sqlite3.IntegrityError:
        print("점수 삭제 오류")
        return False
        
def deleteSubById(subId):
    conn = createConnection(DB_FILE)
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

def deleteStandradById(stndId):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "DELETE FROM Standard WHERE id = ?"
            conn.cursor().execute(sql, (stndId,))
            return True
    except sqlite3.IntegrityError:
        print("점수 기준 삭제 오류")
        return False
        
def saveScore(subId, stdId, score, asses):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "INSERT into Score(subId, stdId, score, asses) VALUES (?,?,?,?)"
            conn.cursor().execute(sql, (subId, stdId, score, asses))
            return True
    except sqlite3.IntegrityError:
        print("점수 저장 오류")
        return False
        
def createAssesment(subId, stndId, content):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "INSERT into Assesment(subId, stndId, content) VALUES (?,?,?)"
            conn.cursor().execute(sql, (subId, stndId, content))
            return True
    except sqlite3.IntegrityError:
        print("하위 과목 저장 오류")
        return False
        
def createChildSubject(name, parentId):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            cursor = conn.cursor()
            sql = "INSERT into Subject(subName, parentId) VALUES (?,?)"
            cursor.execute(sql, (name, parentId))
            lastrowId = cursor.lastrowid
            return lastrowId
    except sqlite3.IntegrityError:
        print("하위 과목 저장 오류")
        return False

def createParentSubject(name):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            cursor = conn.cursor()
            sql = "INSERT into Subject(subName) VALUES (?)"
            cursor.execute(sql, (name,))
            lastrowId = cursor.lastrowid
            return lastrowId
    except sqlite3.IntegrityError:
        print("상위 과목 저장 오류")
        return False
        
def createStandard(subId, grade, greater, less):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            cursor = conn.cursor()
            sql = "INSERT into Standard(subId, grade, greater, less) VALUES (?,?,?,?)"
            cursor.execute(sql, (subId, grade, greater, less))
            return True
    except sqlite3.IntegrityError:
        print("점수 기준 저장 오류")
        return False

def saveStudent(id, name, grade, classes):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "insert into Student(id, name, grade, class) values (?,?,?,?)"
            conn.cursor().execute(sql, (id, name, grade, classes))
            return True  
    except sqlite3.IntegrityError:
        print("과목 저장 문제 발생")
        return False
    
def updateSubNameBySubId(id, name):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "UPDATE Subject SET subName = ? WHERE id = ?"
            conn.cursor().execute(sql, (name, id))
            return True  
    except sqlite3.IntegrityError:
        print("과목 저장 문제 발생")
        return False
    
def updateAssesment(assesId, content):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "UPDATE Assesment SET content = ? WHERE id = ?"
            conn.cursor().execute(sql, (content, assesId))
            return True
    except sqlite3.IntegrityError:
        print("하위 과목 저장 오류")
        return False

def updateStandard(stndId, grade, greater, less):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "UPDATE Standard SET grade = ?, greater = ?, less = ? WHERE id = ?"
            conn.cursor().execute(sql, (grade, greater, less, stndId))
            return True
    except sqlite3.IntegrityError:
        print("등급 기준 업데이트 오류")
        return False

def updateScoreById(scoreId, score, asses):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "UPDATE Score SET score = ?, asses = ? WHERE id = ?" 
            conn.cursor().execute(sql, (score, asses, scoreId))
            return True
    except sqlite3.IntegrityError:
        print("점수 업데이트 오류")
        return False

def updateScoreAssesBySubIdAndStdId(subId, stdId, asses):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "UPDATE Score SET asses = ? WHERE subId = ? AND stdId = ?"
            conn.cursor().execute(sql, (asses, subId, stdId))
            return True
    except sqlite3.IntegrityError:
        print("점수 업데이트 오류")
        return False

def updateScoreAndAssesBySubIdAndStdId(subId, stdId, score, asses):
    conn = createConnection(DB_FILE)
    try:
        with conn:
            sql = "UPDATE Score SET score = ?, asses = ? WHERE subId = ? AND stdId = ?"
            conn.cursor().execute(sql, (score, asses, subId, stdId))
            return True
    except sqlite3.IntegrityError:
        print("점수 평가 업데이트 오류")
        return False