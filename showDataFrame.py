import sys
import pandas as pd
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QAbstractTableModel, Qt
from pandasModel import PandasModel


# df = pd.DataFrame({'a': ['Mary', 'Jim', 'John'],
#                 'b': [100, 200, 300],
#                 'c': ['a', 'b', 'c']})
# df = pd.read_excel("test.xlsx", sheet_name="Sheet2")
class ShowDataFrame():
    def __init__(self):
        super().__init__()

    def show(self, dfList, classList):
        dialog = QDialog(self)
        tabwidget = QTabWidget()

        for df, classText in zip(dfList, classList):
            tab = QWidget()
            model = PandasModel(df)
            view = QTableView(tab)
            view.setModel(model)
            header = view.horizontalHeader()
            header.setSectionResizeMode(4, QHeaderView.Stretch)
            view.resize(800,600)
            tabwidget.addTab(tab, classText)

        vbox = QVBoxLayout()
        vbox.addWidget(tabwidget)
        dialog.setLayout(vbox)
        dialog.resize(800,600)
        dialog.exec_()
        
