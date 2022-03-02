import sys, os, time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, QtCore, uic
from functools import partial

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
global curItem


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

main_class = uic.loadUiType(resource_path("main.ui"))[0]

class MainWindow(QMainWindow, main_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("ToDoList")
        self.setWindowIcon(QIcon("titleimage.png"))

        today = QDate.currentDate().toString(Qt.DefaultLocaleLongDate)
        self.todayLabel.setText(today)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(200)

        self.addListBtn.clicked.connect(self.saveBtnClicked)

        self.moveRightBtn.clicked.connect(self.moveRightBtnClicked)
        self.moveLeftBtn.clicked.connect(self.moveLeftBtnClicked)
        self.moveUpBtn.clicked.connect(self.moveUpBtnClicked)
        self.moveDownBtn.clicked.connect(self.moveDownBtnClicked)

        self.mainList.itemClicked.connect(self.listClicked)
        self.calendarWidget.clicked.connect(self.calendarClicked)

    def saveBtnClicked(self):
        item = QtWidgets.QListWidgetItem("New List Added:) Write Here")
        item.setFont(QFont("맑은 고딕", 13))
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEditable)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.mainList.addItem(item)

    def listClicked(self):
        global curItem
        curItem = self.mainList.currentItem()

    def moveUpBtnClicked(self):
        currentRow = self.mainList.currentRow()
        currentItem = self.mainList.takeItem(currentRow)
        self.mainList.insertItem(currentRow - 1, currentItem)
        self.mainList.setCurrentRow(currentRow - 1)
        self.mainList.setFocus()

    def moveDownBtnClicked(self):
        currentRow = self.mainList.currentRow()
        currentItem = self.mainList.takeItem(currentRow)
        self.mainList.insertItem(currentRow + 1, currentItem)
        self.mainList.setCurrentRow(currentRow + 1)
        self.mainList.setFocus()

    def moveRightBtnClicked(self):
        global curItem
        curItemText = "    " + curItem.text()
        self.mainList.currentItem().setText(curItemText)

    def moveLeftBtnClicked(self):
        global curItem
        curItemText = curItem.text().replace("    ", "", 1)
        self.mainList.currentItem().setText(curItemText)

    def calendarClicked(self):
        today = self.calendarWidget.selectedDate().toString(Qt.DefaultLocaleLongDate)
        self.todayLabel.setText(today)

    def showTime(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm:ss')
        self.timeLabel.setText(label_time)


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()

