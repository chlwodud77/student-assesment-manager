import backend


class Standard:
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
            standardObj = Standard()
            standardObj.setId(stndId)
            standardObj.setSubId(subId)
            standardObj.setGrade(grade)
            standardObj.setGreater(greater)
            standardObj.setLess(less)
            standardOjbectArray.append(standardObj)

        return standardOjbectArray
    except Exception as e:
        print(e)
        return []
