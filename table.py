from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class TableModel(QAbstractTableModel):
    def rowCount(self, parent):
        return len(rows)
    def columnCount(self, parent):
        return len(headers)
    def data(self, index, role):
        if role != Qt.DisplayRole:
            return QVariant()
        return rows[index.row()][index.column()]
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return QVariant()
        return headers[section]

app = QApplication([])
model = TableModel()
view = QTableView()
view.setModel(model)
view.show()
app.exec_()