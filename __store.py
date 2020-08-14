
class subjectStore:
    def __init__(self):
        self.standard        = []
        self.newStandard     = []
        self.assesment       = []
        self.newAssesment    = []
        self.deleteAssesment = []

    def getStandard(self):
        return self.standard
    
    def addStandard(self, subId ="", grade="", greater="", less=""):
        container = dict(subId=subId, grade=grade, greater=greater, less=less)
        if(container not in self.standard):
            self.standard.append(container)
            
    def modifyStandard(self, subId, grade, greater, less):
        pass
    
    def getDeleteAssesment(self):
        return self.deleteAssesment
    
    def delNewAsssesment(self, assesId="", subId="", grade="", greater="", less="", content=""):
        container = dict(assesId=assesId, subId=subId, grade=grade,
                        greater=greater, less=less, content=content)
        if(container in self.newAssesment):
            self.newAssesment.remove(container)
        
    def getNewAssesment(self):
        return self.newAssesment
    
    def addnewAssesment(self, container):
        if(container not in self.newAssesment):
            self.newAssesment.append(container)
    
    def addDeleteAssesment(self, container):
        if(container not in self.deleteAssesment):
            self.deleteAssesment.append(container)
    
    def findAssesment(self, assesId):
        for asses in self.assesment:
            if(str(asses["assesId"]) == str(assesId)):
                return asses
    
    def findAssesmentsBySubId(self, subId):
        assesments = []
        for asses in self.assesment:
            if(asses["subId"] == subId):
                assesments.append(asses)
        return assesments
                
            
    def findAssesmentBySubIdAndGrade(self, subId, grade):
        for asses in self.assesment:
            if(str(asses["subId"]) == str(subId) and str(asses["grade"]) == str(grade)):
                return asses
    
    def getAssesment(self):
        return self.assesment
    
    def addAssesment(self, assesId="", subId="", grade="", greater="", less="", content=""):
        container = dict(assesId=assesId, subId=subId, grade=grade,
                        greater=greater, less=less, content=content)
        if(container not in self.assesment):
            self.assesment.append(container)
    
    def delAssesment(self, container):
        if(container in self.assesment):
            self.assesment.remove(container)
            print("assesments : ",self.assesment)
            
    def modifyNewAssesment(self, subId, grade, content, newContent):
        for asses in self.newAssesment:
            if(asses["subId"] == subId and asses["grade"] == grade and asses["content"] == content):
                asses["content"] = newContent
    
    def modifyAssesment(self, assesId, content):
        for asses in self.assesment:
            if(asses["assesId"] == assesId):
                asses["content"] = content
        print("assesments: ",self.assesment)
    
    def reset(self):
        self.standard  = []
        self.assesment = []
        self.newAssesment = []
        self.deleteAssesment = []