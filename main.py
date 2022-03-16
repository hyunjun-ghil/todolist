import sys, os, time, datetime


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, QtCore, uic
from random import *
from functools import partial
import googleCalendar


# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
global curItem
gCalendar = []


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

main_class = uic.loadUiType(resource_path("main.ui"))[0]
addCalendar_class = uic.loadUiType(resource_path("addCalendar.ui"))[0]
wiseSayingFile = resource_path("wisesaying.txt")

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

        self.refreshGCalendar()

        self.saveMenu.triggered.connect(self.saveMenuClicked)

        self.gCalendarBtn.clicked.connect(self.refreshGCalendar)
        self.gCalendar_addBtn.clicked.connect(self.gCalendar_addBtnClicked)

        self.addListBtn.clicked.connect(self.addListBtnClicked)
        self.doneListBtn.clicked.connect(self.doneListBtnClicked)
        self.deleteListBtn.clicked.connect(self.deleteListBtnClicked)

        self.moveUpBtn.clicked.connect(self.moveUpBtnClicked)
        self.moveDownBtn.clicked.connect(self.moveDownBtnClicked)
        self.moveRightBtn.clicked.connect(self.moveRightBtnClicked)
        self.moveLeftBtn.clicked.connect(self.moveLeftBtnClicked)

        self.mainList.itemClicked.connect(self.listClicked)
        self.calendarWidget.clicked.connect(self.calendarClicked)

        wiseSayingList = []
        f = open(wiseSayingFile, 'r', encoding='utf8')
        while True:
            fline = f.readline()
            if not fline: break
            wiseSayingList.append(fline.replace("\n", ""))

        i = randint(0, len(wiseSayingList))
        self.wiseLabel.setText(wiseSayingList[i])

    def gCalendar_addBtnClicked(self):
        gCalendarAdd = gCalendarAddDialog()
        gCalendarAdd.exec_()
        self.refreshGCalendar()

    def gCalendar_delete(self, id):
        response = QMessageBox.question(self, 'save', '삭제하시겠습니까?', QMessageBox.Yes | QMessageBox.No)
        if response == QMessageBox.Yes:
            googleCalendar.delete(id)
        else:
            self.close()
        self.refreshGCalendar()


    def saveMenuClicked(self):
        curdatetime = str(datetime.date.today()) + ".txt"
        file = open(curdatetime, "w")
        for i in range(0, self.mainList.count()):
            ts = str(self.mainList.item(i).checkState()) + ":" + self.mainList.item(i).text() + "\n"
            file.write(ts)
        file.close()
        QMessageBox.information(self, "result", "저장되었습니다.")

    def showTime(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm:ss')
        self.timeLabel.setText(label_time)

    def refreshGCalendar(self):
        gCalendar = []
        gCalendar.append(googleCalendar.main())

        for i in reversed(range(self.verticalLayout.count())):
            self.verticalLayout.itemAt(i).widget().setParent(None)

        i = 0
        if gCalendar[0]:
            for data in gCalendar[0]:
                i = i + 1
                checkboxdata = data
                print(checkboxdata)
                globals()["self.calendar_list{}".format(i)] = QPushButton(
                    checkboxdata[0] + '\n' + checkboxdata[1] + "\n" + checkboxdata[2])
                globals()["self.calendar_list{}".format(i)].setStyleSheet("font-size:15px; background-color:bisque;")
                globals()["self.calendar_list{}".format(i)].clicked.connect(partial(self.gCalendar_delete, checkboxdata[3]))
                self.verticalLayout.addWidget(globals()["self.calendar_list{}".format(i)])
        else:
            self.NoDataLabel = QLabel("No Events Today :)")
            self.NoDataLabel.setAlignment(Qt.AlignCenter)
            self.verticalLayout.addWidget(self.NoDataLabel)



    def addListBtnClicked(self):
        item = QtWidgets.QListWidgetItem("New List Added:) Write Here")
        item.setFont(QFont("맑은 고딕", 13))
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEditable)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.mainList.addItem(item)

    def doneListBtnClicked(self):
        currentRow = self.mainList.currentItem()
        if currentRow.checkState() == Qt.Checked:
            currentRow.setCheckState(QtCore.Qt.Unchecked)
            currentRow.setBackground(Qt.white)
        else:
            currentRow.setCheckState(QtCore.Qt.Checked)
            currentRow.setBackground(Qt.gray)

    def deleteListBtnClicked(self):
        currentRow = self.mainList.currentRow()
        self.mainList.takeItem(currentRow)


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

    def listClicked(self):
        global curItem
        curItem = self.mainList.currentItem()

    def calendarClicked(self):
        today = self.calendarWidget.selectedDate().toString(Qt.DefaultLocaleLongDate)
        self.todayLabel.setText(today)
        self.mainList.clear()
        textFile = "./" + str(self.calendarWidget.selectedDate().toString(Qt.ISODate)) + ".txt"
        try:
            f = open(textFile, 'r')
        except OSError as e:
            messagebox = TimerMessageBox(1, self, "저장된 TodoList가 없습니다. 그렇다고 굳이 파일을 생성하지 않으셔도 됩니다.")
            messagebox.exec_()
            return
        while True:
            line = f.readline()
            if not line: break
            column = line.split(":")
            if column[0] == '2':
                item = QtWidgets.QListWidgetItem(column[1].replace("\n", ""))
                item.setFont(QFont("맑은 고딕", 13))
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEditable)
                item.setCheckState(QtCore.Qt.Checked)
                item.setBackground(Qt.gray)
                self.mainList.addItem(item)
            else:
                item = QtWidgets.QListWidgetItem(column[1].replace("\n", ""))
                item.setFont(QFont("맑은 고딕", 13))
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                item.setCheckState(QtCore.Qt.Unchecked)
                self.mainList.addItem(item)

class gCalendarAddDialog(QDialog, addCalendar_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("AddCalendar")
        self.setWindowIcon(QIcon("titleimage.png"))
        self.gCalendar_popup_saveBtn.clicked.connect(self.gCalendar_popup_save_clicked)

        self.dateEdit.setDate(datetime.datetime.today())
        self.timeEdit_2.setTime(QTime.currentTime())

    def gCalendar_popup_save_clicked(self):
        googleCalendar.save(self.dateEdit.date(), self.timeEdit_2.time(), self.lineEdit.text(), self.lineEdit_2.text())
        self.close()
        # return event


class TimerMessageBox(QMessageBox):
    def __init__(self, timeout=1, parent=None, text=""):
        super(TimerMessageBox, self).__init__(parent)
        self.setWindowTitle("info")
        self.time_to_wait = timeout
        self.setText(text)
        self.setStandardButtons(QMessageBox.NoButton)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.changeContent)
        self.timer.start()

    def changeContent(self):
        self.time_to_wait -= 1
        if self.time_to_wait <= 0:
            self.close()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()



if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()