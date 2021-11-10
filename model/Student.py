from utils import backend


class Student:
    def setId(self, id):
        self.id = id

    def setName(self, name):
        self.name = name

    def setGrade(self, grade):
        self.grade = grade

    def setClass(self, classes):
        self.classes = classes

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getGrade(self):
        return self.grade

    def getClass(self):
        return self.classes


def getStudentsByGradeAndClass(grade, classes):
    try:
        students = backend.returnClassMemberList(grade, classes)
        studentObjectArray = []

        for student in students:
            name = student[0]
            stdId = student[1]
            studentObj = Student()
            studentObj.setId(stdId)
            studentObj.setName(name)
            studentObj.setGrade(grade)
            studentObj.setClass(classes)
            studentObjectArray.append(studentObj)

        return studentObjectArray
    except Exception as e:
        print(e)
        return []
