from utils import backend


class Score:
    def __init__(self, id=None, subId=None, stdId=None, score=None, asses=None):
        self.id = id
        self.subId = subId
        self.stdId = stdId
        self.score = score
        self.asses = asses

    def setId(self, id):
        self.id = id

    def setSubId(self, subId):
        self.subId = subId

    def setStdId(self, stdId):
        self.stdId = stdId

    def setScore(self, score):
        self.score = score

    def setAsses(self, asses):
        self.asses = asses

    def getId(self):
        return self.id

    def getSubId(self):
        return self.subId

    def getStdId(self):
        return self.stdId

    def getScore(self):
        return self.score

    def getAsses(self):
        return self.asses

def getScoreBySubId(subId):
    try:
        scores = backend.returnScoreBySubId(subId)
        scoreObjectArray = []

        for score in scores:
            scoreId, subId, stdId, score, asses = score
            scoreObj = Score(scoreId, subId, stdId, score, asses)
            scoreObjectArray.append(scoreObj)

        return scoreObjectArray
    except Exception as e:
        print(e)


def getScoreBySubIdAndClass(subId, grade, classes):
    try:
        scores = backend.returnScoreBySubIdAndClass(subId, grade, classes)
        scoreObjectArryay = []

        # print(scores)

        for score in scores:
            scoreId = score[0]
            stdId = score[1]
            scoreNum = score[2]
            asses = score[3]
            scoreObj = Score()
            scoreObj.setId(scoreId)
            scoreObj.setSubId(subId)
            scoreObj.setStdId(stdId)
            scoreObj.setScore(scoreNum)
            scoreObj.setAsses(asses)
            scoreObjectArryay.append(scoreObj)

        return scoreObjectArryay
    except Exception as e:
        print(e)
        return []


def saveScore(subId, stdId, score, asses):
    try:
        result = backend.saveScore(subId, stdId, score, asses)
        if result:
            return True
        else:
            return False
    except Exception as e:
        print(e)


def updateScore(subId, stdId, score, asses):
    try:
        result = backend.updateScoreAndAssesBySubIdAndStdId(subId, stdId, score, asses)
        if result:
            return True
        else:
            return False
    except Exception as e:
        print(e)


def isScoreExist(subId, stdId):
    try:
        result = backend.returnScore(subId, stdId)
        if result is None: return True
        return False
    except Exception as e:
        print(e)
