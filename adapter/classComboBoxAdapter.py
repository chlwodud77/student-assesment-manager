import backend


# 학급 리스트 출력 함수
def insertClassComboBox(combobox):
    combobox.clear()
    classes = backend.returnClassList()
    for i in range(0, len(classes)):
        combobox.addItem(str(classes[i][0]) + "학년 " + str(classes[i][1]) + "반")
