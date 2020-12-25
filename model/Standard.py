from utils import backend


class Standard:
    def __init__(self, id=None, subId=None, grade=None, greater=None, less=None):
        self.id = id
        self.subId = subId
        self.grade = grade
        self.greater = greater
        self.less = less

    def setId(self, id):
        self.id = id

    def setSubId(self, subId):
        self.subId = subId

    def setGrade(self, grade):
        self.grade = grade

    def setGreater(self, greater):
        self.greater = greater

    def setLess(self, less):
        self.less = less

    def getId(self):
        return self.id

    def getSubId(self):
        return self.subId

    def getGrade(self):
        return self.grade

    def getGreater(self):
        return self.greater

    def getLess(self):
        return self.less


def getStandardBySubId(subId):
    try:
        standards = backend.returnStandardBySubId(subId)
        standardOjbectArray = []

        for standard in standards:
            stndId, subId, grade, greater, less = standard
            standardObj = Standard(stndId, subId, grade, greater, less)
            standardOjbectArray.append(standardObj)
        return standardOjbectArray
    except Exception as e:
        print(e)
        return []
