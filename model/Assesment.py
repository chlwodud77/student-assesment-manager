import backend

class Assesment:
    def setId(self, id):
        self.id = id
    
    def setSubId(self, subId):
        self.subId = subId
    
    def setStandardId(self, standardId):
        self.standardId = standardId

    def setContent(self, content):
        self.content = content
    
    def getId(self):
        return self.id
    
    def getSubId(self):
        return self.subId
    
    def getStandardId(self):
        return self.standardId

    def getContent(self):
        return self.content

def getAssesmentBySubId(subId):
    try:
        assesments = backend.returnAssesmentBySubId(subId)
        assesmentObjectArray = []

        for assesment in assesments:
            assesId, subId, stndId, content = assesment
            assesmentObj = Assesment()
            assesmentObj.setId(assesId)
            assesmentObj.setSubId(subId)
            assesmentObj.setStandardId(stndId)
            assesmentObj.setContent(content)
            assesmentObjectArray.append(assesmentObj)
        
        return assesmentObjectArray
    except Exception as e:
        print(e)
        return []