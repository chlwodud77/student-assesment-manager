from model import Assesment as As
from model import Standard as St
from model.Standard import Standard
from utils import backend


def copyChildSubject(name, srcSubId, trgParentSubId):
    try:
        trgSubId = backend.createChildSubject(name, trgParentSubId)
        orgStandards, copiedStandards = copyStandard(srcSubId, trgSubId)
        copyAssesment(srcSubId, trgSubId, orgStandards, copiedStandards)
        return True
    except Exception as e:
        print(e)


def copyStandard(srcSubId, trgSubId):
    orgStandards = St.getStandardBySubId(srcSubId)
    copiedStandards = []

    for standard in orgStandards:
        grade = standard.getGrade()
        greater = standard.getGreater()
        less = standard.getLess()

        copiedStdId = backend.createStandard(trgSubId, grade, greater, less)
        stdObj = Standard(copiedStdId, trgSubId, grade, greater, less)
        copiedStandards.append(stdObj)

    return orgStandards, copiedStandards


def copyAssesment(srcSubId, trgSubId, orgStandards, copiedStandards):
    orgAssesments = As.getAssesmentBySubId(srcSubId)

    for orgStandard, copiedStandard in zip(orgStandards, copiedStandards):
        trgStndId = copiedStandard.getId()
        orgStndId = orgStandard.getId()

        for assesment in orgAssesments:
            if orgStndId == assesment.getStandardId():
                content = assesment.getContent()
                backend.createAssesment(trgSubId, trgStndId, content)

def copyScore():
    pass