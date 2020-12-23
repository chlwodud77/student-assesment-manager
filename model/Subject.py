import backend


class Subject:
    def setId(self, id):
        self.id = id

    def setName(self, name):
        self.name = name

    def setParentId(self, parentId):
        self.parentId = parentId

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getParentId(self):
        return self.parentId


def getSubjectBySubId(subId):
    try:
        subject = backend.returnSubjectBySubId(subId)
        name = subject[1]
        parentId = subject[2]
        subjectObj = Subject()
        subjectObj.setId(subId)
        subjectObj.setName(name)
        subjectObj.setParentId(parentId)

        return subjectObj
    except Exception as e:
        print(e)
        return []
