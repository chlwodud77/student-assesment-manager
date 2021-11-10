from utils import backend


class Assesment:
    def __init__(self, id=None, subId=None, stndId=None, content=None):
        self.id = id
        self.subId = subId
        self.stndId = stndId
        self.content = content

    def setId(self, id):
        self.id = id

    def setSubId(self, subId):
        self.subId = subId

    def setStandardId(self, stndId):
        self.stndId = stndId

    def setContent(self, content):
        self.content = content

    def getId(self):
        return self.id

    def getSubId(self):
        return self.subId

    def getStandardId(self):
        return self.stndId

    def getContent(self):
        return self.content


def getAssesmentBySubId(subId):
    try:
        assesments = backend.returnAssesmentBySubId(subId)
        assesmentObjectArray = []

        for assesment in assesments:
            assesId, subId, stndId, content = assesment
            assesmentObj = Assesment(assesId, subId, stndId, content)

            assesmentObjectArray.append(assesmentObj)
        return assesmentObjectArray
    except Exception as e:
        print(e)
        return []
