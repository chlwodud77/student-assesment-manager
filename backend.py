import pymysql
import config

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
	"score"	INTEGER,
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

def createConnection(cursor=pymysql.cursors.Cursor):
    conn = None
    try:
        conn = pymysql.connect( host = config.DATABASE_CONFIG["host"],
                                user = config.DATABASE_CONFIG["user"],
                                password = config.DATABASE_CONFIG["password"],
                                db = config.DATABASE_CONFIG["db"],
                                charset = config.DATABASE_CONFIG["charset"],
                                cursorclass = cursor )
    finally:
        return conn    

def returnAssesmentsByStandardId(stndId):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT id, content FROM Assesment WHERE stndId = %s"
            cursor.execute(sql, (stndId,))
            result = cursor.fetchall()
            return result
    finally:
        conn.close()

def returnAssesmetnStandardBySubIdAndGrade(subId, grade):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT DISTINCT greater, less FROM Assesment WHERE subId = %s AND grade = %s"
            cursor.execute(sql, (int(subId), str(grade)))
            result = cursor.fetchall()
            return result
    finally:
        conn.close()

def returnAssesmentContentBySubIdAndGrade(subId, grade):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT id, content FROM Assesment WHERE subId = %s AND grade = %s"
            cursor.execute(sql, (subId, grade))
            result = cursor.fetchall()
            return result
    finally:
        sonn.close()
    

def returnAssesmentContentById(id):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT content FROM Assesment WHERE id = %s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()[0]
            return result
    finally:
        conn.close()
        
def returnAssesmentStandardBySubId(subId):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT DISTINCT subId, grade, greater, less FROM Assesment WHERE subId = %s"
            cursor.execute(sql, (subId,))
            result = cursor.fetchall()
            return result
    finally:
        conn.close()
        
def returnAssesmentBySubId(subId):       
    conn = createConnection()                  
    try:
        with conn.cursor() as cursor:
            sql = "SELECT id, grade, content FROM Assesment WHERE subId = %s"
            cursor.execute(sql, (subId,))
            result = cursor.fetchall()
            return result
    finally:
        conn.close()
        

def returnClassAssesmentBySubId(subId, grade, classes):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT Student.name, Student.id, Score.asses FROM Student INNER JOIN Score ON Student.id = Score.stdId WHERE Score.subId = %s and Student.grade = %s and Student.class = %s"
            cursor.execute(sql, (subId, grade, classes))
            result = cursor.fetchall()
            return result
    finally:
        conn.close()

def returnClassSubList(grade, classes):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "select DISTINCT Subject.id as subId, Subject.subName, Subject.parentId FROM Subject INNER JOIN Score ON Score.subId = Subject.id INNER JOIN Student ON Score.stdId = Student.id WHERE Student.grade = %s and Student.class = %s"
            cursor.execute(sql, (grade, classes))
            result = cursor.fetchall()
            return result
    finally:
        conn.close()
        
def returnClassMemberList(grade, classes):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT name, id FROM Student WHERE grade = %s AND class = %s"
            cursor.execute(sql, (grade, classes))
            result = cursor.fetchall()
            return result
    finally:
        conn.close()

def returnClassMemberName(grade, classes):
    sconn = createConnection(pymysql.cursors.DictCursor)
    # sconn.row_factory = lambda cursor, row: row[0]

    try:
        with sconn.cursor() as cursor:
            sql = "SELECT name FROM Student WHERE grade = %s and class = %s"
            cursor.execute(sql, (grade, classes))
            result = cursor.fetchall()
            names = []
            for d in result:
                names.append(d["name"])
            return names
    finally:
        sconn.close()

def returnClassMemberNumber(grade, classes):
    sconn = createConnection(pymysql.cursors.DictCursor)
    # sconn.row_factory = lambda cursor, row: row[0]

    try:
        with sconn.cursor() as cursor:
            sql = "SELECT id FROM Student WHERE grade = %s and class = %s"
            cursor.execute(sql, (grade, classes))
            result = cursor.fetchall()
            numbers = []
            for d in result:
                numbers.append(d["id"])
            # print(result)
            return numbers
    finally:
        sconn.close()
        
def returnStudentAssesmentBySubId(subId, stdId):
    sconn = createConnection(pymysql.cursors.DictCursor)
    # sconn.row_factory = lambda cursor, row: row[0]
    try:
        with sconn.cursor() as cursor:
            sql = "SELECT Score.asses FROM Student INNER JOIN Score ON Student.id = Score.stdId WHERE Score.subId = %s and Student.id = %s"
            cursor.execute(sql, (subId, stdId))
            result = cursor.fetchall()
            return result
    finally:
        sconn.close()

def returnClassList():
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT DISTINCT grade, class from Student"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        conn.close()

def returnParentSubject():
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM Subject where parentId is NULL"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        conn.close()

def returnChildSubjectsFromParentId(parentId):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM Subject WHERE parentId = %s"
            cursor.execute(sql, (parentId,))
            result = cursor.fetchall()
            return result
    finally:
        conn.close()

def returnChildSubjectId(name, parentId):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT id FROM Subject WHERE subName = %s and parentId = %s"
            cursor.execute(sql, (name, parentId))
            result = cursor.fetchone()[0]
            return result
    finally:
        conn.close()

def returnScore(subId, stdId):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT id, score, asses FROM Score WHERE subId = %s and stdId = %s"
            cursor.execute(sql, (int(subId), int(stdId),))
            result = cursor.fetchone()
            return result
    finally:
        conn.close()

def returnScoreBySubIdAndClass(subId, grade, classes):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT Score.stdId, Score.score FROM Student INNER JOIN Score ON Student.id = Score.stdId AND Score.subId = %s AND Student.grade = %s AND Student.class = %s"
            cursor.execute(sql, (int(subId), int(grade), int(classes)))
            result = cursor.fetchall()
            return result
    finally:
        conn.close()

def returnSubNameBySubId(subId):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT subName FROM Subject WHERE id = %s"
            cursor.execute(sql, (subId,))
            result = cursor.fetchone()[0]
            return result
    finally:
        conn.close()
        
def returnSubList():
    conn = createConnection()
    try:    
        with conn.cursor() as cursor:
            sql = "SELECT id, subName, parentId FROM Subject"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        conn.close()
        
def returnStandardBySubId(subId):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT id, subId, grade, greater, less FROM Standard Where subId = %s"
            cursor.execute(sql, (subId,))
            result = cursor.fetchall()
            return result
    finally:
        conn.close()

def returnStandardById(stndId):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT grade, greater, less FROM Standard WHERE id = %s"
            cursor.execute(sql, (stndId,))
            result = cursor.fetchone()
            return result
    finally:
        conn.close()

def returnIfStudentSubjectScoreExist(subId, stdId):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            result = []
            sql = "SELECT score, asses FROM Score WHERE subId = %s AND stdId = %s"
            cusor.execute(sql, (subId, stdId))
            result = cursor.fetchone()
            return result
    finally:
        conn.close()

def returnScoreRangeAndContentBySubId(subId):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT Assesment.subId, Standard.greater, Standard.less, Assesment.content
                FROM Assesment INNER JOIN Standard
                ON Assesment.subId = Standard.subId AND Assesment.stndId = Standard.id
                WHERE Standard.subId = %s
                """
            cursor.execute(sql, (subId,))
            result = cursor.fetchall()
            return result
    finally:
        conn.close()

def deleteAssesmentById(id):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM Assesment WHERE id = %s"
            cursor.execute(sql, (id,))
            conn.commit()
            return True
    finally:
        conn.close()
        
def deleteAssesmentBySubId(subId):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM Assesment WHERE subId = %s"
            cursor.execute(sql, (subId,))
            conn.commit()
            return True
    finally:
        conn.close()

def deleteAssesmentByStndId(stndId):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM Assesment WHERE stndId = %s"
            cursor.execute(sql, (stndId,))
            conn.commit()
            return True
    finally:
        conn.close()

def deleteClass(grade, classes):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM Student WHERE grade = %s and class = %s"
            cursor.execute(sql, (grade, classes))
            conn.commit()
            return True
    finally:
        conn.close()

def deleteScoreById(id):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM Score WHERE id = %s"
            cursor.execute(sql, (id,))
            conn.commit()
            return True
    finally:
        conn.close()
        
def deleteSubById(subId):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql1 = "DELETE FROM Subject WHERE parentId = %s"
            sql2 = "DELETE FROM Subject WHERE id = %s"
            sql3 = "DELETE FROM Assesment WHERE subId = %s"
            cursor.execute(sql1, (subId,))
            cursor.execute(sql2, (subId,))
            cursor.execute(sql3, (subId,))
            conn.commit()
            return True  
    finally:
        conn.close()

def deleteStandradById(stndId):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM Standard WHERE id = %s"
            cursor.execute(sql, (stndId,))
            conn.commit()
            return True
    finally:
        conn.close()
        
def saveScore(subId, stdId, score, asses):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT into Score(subId, stdId, score, asses) VALUES (%s,%s,%s,%s)"
            cursor.execute(sql, (subId, stdId, score, asses))
            conn.commit()
            return True
    finally:
        conn.close()
        
def createAssesment(subId, stndId, content):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT into Assesment(subId, stndId, content) VALUES (%s,%s,%s)"
            cursor.execute(sql, (subId, stndId, content))
            conn.commit()
            return True
    finally:
        conn.close()
        
def createChildSubject(name, parentId):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT into Subject(subName, parentId) VALUES (%s,%s)"
            cursor.execute(sql, (name, parentId))
            lastrowId = cursor.lastrowid
            conn.commit()
            return lastrowId
    finally:
        conn.close()

def createParentSubject(name):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT into Subject(subName) VALUES (%s)"
            cursor.execute(sql, (name,))
            lastrowId = cursor.lastrowid
            conn.commit()
            return lastrowId
    finally:
        conn.close()
        
def createStandard(subId, grade, greater, less):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT into Standard(subId, grade, greater, less) VALUES (%s,%s,%s,%s)"
            cursor.execute(sql, (subId, grade, greater, less))
            conn.commit()
            return True
    finally:
        conn.close()

def saveStudent(id, name, grade, classes):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO Student(id, name, grade, class) VALUES (%s,%s,%s,%s)"
            cursor.execute(sql, (id, name, grade, classes))
            conn.commit()
            return True  
    finally:
        conn.close()
    
def updateSubNameBySubId(id, name):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE Subject SET subName = %s WHERE id = %s"
            cursor.execute(sql, (name, id))
            conn.commit()
            return True  
    finally:
        conn.close()
    
def updateAssesment(assesId, content):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE Assesment SET content = %s WHERE id = %s"
            cursor.execute(sql, (content, assesId))
            conn.commit()
            return True
    finally:
        conn.close()

def updateStandard(stndId, grade, greater, less):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE Standard SET grade = %s, greater = %s, less = %s WHERE id = %s"
            cursor.execute(sql, (grade, greater, less, stndId))
            conn.commit()
            return True
    finally:
        conn.close()

def updateScoreById(scoreId, score, asses):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE Score SET score = %s, asses = %s WHERE id = %s" 
            cursor.execute(sql, (score, asses, scoreId))
            conn.commit()
            return True
    finally:
        conn.close()

def updateScoreAssesBySubIdAndStdId(subId, stdId, asses):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE Score SET asses = %s WHERE subId = %s AND stdId = %s"
            cursor.execute(sql, (asses, subId, stdId))
            conn.commit()
            return True
    finally:
        conn.close()

def updateScoreAndAssesBySubIdAndStdId(subId, stdId, score, asses):
    conn = createConnection()
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE Score SET score = %s, asses = %s WHERE subId = %s AND stdId = %s"
            cursor.execute(sql, (score, asses, subId, stdId))
            conn.commit()
            return True
    finally:
        conn.close()