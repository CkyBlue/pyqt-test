from PyQt5.QtCore import *

from components.Canvas import Ui_MainWindow as Canvas
from components.ProtoCanvas import Ui_MainWindow as ProtoCanvas
from components.Login import Ui_Dialog as Login
from components.MsgBox import Ui_Dialog as MsgBox
from components.SaveRec import Ui_Dialog as SaveRecording
from components.Register import Ui_Dialog as Register

from utils import *

import sys

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QToolBar, QWidget
from PyQt5 import QtCore

from socket import timeout
from subprocess import Popen, PIPE
from time import sleep
import os

import json

with open('users.json', 'r') as openfile:
    usernames = json.load(openfile)

activeUser = None


class LoginWin(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Login()
        self.ui.setupUi(self)

        self.ui.login_btn.clicked.connect(self.login)
        self.ui.signup_btn.clicked.connect(self.signUp)

        self.loadCanvas = lambda _: None

    def login(self):
        username = self.ui.username_field.text()
        password = self.ui.password_field.text()

        if username in usernames.keys() and usernames[username] == password:
            global activeUser
            activeUser = username

            self.loadCanvas(0)
            self.close()

        else:
            msg = MsgBoxDlg()
            msg.setMsg("Invalid Username and Password combination.")
            msg.exec()

    def signUp(self):
        username = self.ui.username_field.text()
        password = self.ui.password_field.text()

        msg = MsgBoxDlg()
        if username in usernames.keys():
            msg.setMsg("User with username already exists.")

        else:
            usernames[username] = password

            json_object = json.dumps(usernames, indent=4)
            with open("users.json", "w") as outfile:
                outfile.write(json_object)

            msg.setMsg("Successfully registered user.")

        msg.exec()


class CanvasWin(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.handTrackingProcess = None
        self.handTrackingOutput = None

        self.setupCanvas()

        self.recordingStartDate = ""
        self.recordingStartTime = ""
        self.strokeData = {}

        self.actionClear = createAction(self, "delete_icon.png", "actionClear", self.clear)
        self.actionRecord = createAction(self, "player_record.png", "actionRecord", self.toggleRecord)

        self.recording = False
        self.pressure = 1

        self.setupToolBar()

    def startHandTracking(self):
        if (self.handTrackingProcess != None):
            self.handTrackingProcess.terminate()

        self.handTrackingProcess = Popen(["LeapTest.exe"], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        pass

    def stopHandTracking(self):
        # (output, err) = self.handTrackingProcess.communicate(input=b'\r\n')
        self.handTrackingProcess.communicate(input=b'\r\n\r\n\r\n')

        self.handTrackingProcess.kill()

        # print("Output: " + str(output))

        self.handTrackingOutput = ""

        # self.handTrackingOutput = str(str(output).replace('\\n', '\n').replace('\\r', '\r'))
        self.handTrackingProcess = None
        pass

    def setupCanvas(self):
        self.setObjectName("MainWindow")
        self.setWindowTitle("Canvas")

        # self.setGeometry(0, 0, self.frameGeometry().width(), self.frameGeometry().height())
        # self.setFixedSize(800, 600)

        geometry = app.desktop().availableGeometry()
        self.setGeometry(geometry)

        self.showMaximized()

        self.setTabletTracking(True)

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.storedImage = QImage(self.size(), QImage.Format_RGB32)

        self.image.fill(Qt.white)
        self.storedImage.fill(Qt.white)

        self.drawing = False

        self.brushSize = 4
        self.brushColor = Qt.black

        self.lastPoint = QPoint()

    def tabletEvent(self, event):
        eventType = event.type()

        data = [event.xTilt(), event.yTilt(), event.pressure()]

        if (eventType == QEvent.TabletPress):
            self.drawing = True
            self.lastPoint = event.pos()

            if self.recording:
                self.recordInstance(self.lastPoint,data)
        elif (eventType == QEvent.TabletMove and self.drawing):
            self.paintLine(self.image, self.lastPoint, event.pos())

            if self.recording:
                # self.paintLine(self.storedImage, self.lastPoint, event.pos())
                self.recordInstance(self.lastPoint, data)

            self.lastPoint = event.pos()

            self.update()
        elif eventType == QEvent.TabletRelease:
            self.drawing = False
        self.pressure = event.pressure()
        print("Tablet Event, {}".format(self.pressure))

    def setupToolBar(self):
        self.toolBar = QToolBar(self)
        self.toolBar.setObjectName("toolBar")

        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.actionClear)
        self.toolBar.addAction(self.actionRecord)

    def saveRecording(self, recordingName, difficulty):
        fileName = "{}_{}_{}_{}".format(activeUser, recordingName, self.recordingStartDate, self.recordingStartTime.replace(":", "-"))
        file = open("{}-stylus.dat".format(fileName), "w")
        file.write("Author: {}\nDifficulty: {}\nDate:{}".format(activeUser, difficulty, self.recordingStartDate))
        for key, value in self.strokeData.items():
            file.write(key + " " + value + "\n")
        file.close()

        # # open both files
        # with open('data.csv', 'r') as firstfile, open("{}-ultraleap.csv".format(fileName), 'a') as secondfile:
        #     for line in firstfile:
        #         secondfile.write(line)

        # os.rename("./data.csv", "./{}-ultraleap.csv".format(fileName))
        # # file = open("{}-ultraleap.csv".format(fileName), "w")
        # # file.write(self.handTrackingOutput)
        # # file.close()

    def toggleRecord(self):
        if self.recording:
            self.stopHandTracking()
            self.actionRecord.setIcon(getIcon("player_record.png"))
            dlg = SaveDlg(self)
            dlg.setSaveCallback(self.save)
            dlg.setCancelCallback(self.cancel)
            dlg.exec()

        else: # Start Recording
            self.startHandTracking()
            self.recordingStartDate = getDate()
            self.recordingStartTime = getTime(False)
            self.strokeData.clear()
            self.storedImage.fill(Qt.white)

            self.actionRecord.setIcon(getIcon("stop.png"))

        self.recording = not self.recording

    #TODO Remove mouse callbacks

    # TODO Compress
    def recordInstance(self, pos, data):
        self.strokeData[getTime()] = "({}, {}, {})".format(pos.x(), pos.y(), data)
        print(getTime(), pos.x(), pos.y(), data)

    def save(self, recordingName, difficulty):
        self.saveRecording(recordingName, difficulty)
        self.saveCanvas(recordingName)

        print("Save({}, {})".format(recordingName, difficulty))

    def cancel(self):
        print("Cancel")

    # TODO Maybe I need to Use Tablet Event to get rid of delay error

    def mousePressEvent(self, event):
        return
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

            if self.recording:
                self.recordInstance(self.lastPoint)

    def getBrushSize(self):
        return .5 + 5 * self.pressure

    def paintLine(self, image, pointA, pointB):
        painter = QPainter(image)
        painter.setPen(QPen(self.brushColor, self.getBrushSize(), Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawLine(pointA, pointB)

    def mouseMoveEvent(self, event):
        return
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            self.paintLine(self.image, self.lastPoint, event.pos())

            if self.recording:
                # self.paintLine(self.storedImage, self.lastPoint, event.pos())
                self.recordInstance(self.lastPoint)

            self.lastPoint = event.pos()

            self.update()

    def mouseReleaseEvent(self, event):
        return
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def saveCanvas(self, recordingName):
        filePath = "{}_{}_{}_{}.png".format(activeUser, recordingName, self.recordingStartDate, self.recordingStartTime)
        # self.storedImage.save(filePath)

    def clear(self):
        self.image.fill(Qt.white)
        self.update()

class MsgBoxDlg(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = MsgBox()
        self.ui.setupUi(self)

    def setMsg(self, msg):
        self.ui.label.setText(msg)


class SaveDlg(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = SaveRecording()
        self.ui.setupUi(self)

        self.ui.buttonBox.accepted.connect(self.save)
        self.ui.buttonBox.rejected.connect(self.cancel)

        self.saveCallback = None
        self.cancelCallback = None


    def setSaveCallback(self, callback):
        self.saveCallback = callback

    def setCancelCallback(self, callback):
        self.cancelCallback = callback

    def save(self):
        if self.saveCallback is not None:
            difficulty = int(self.ui.comboBox.currentText())
            recordingName = self.ui.lineEdit.text()

            self.saveCallback(recordingName, difficulty)
        self.close()

    def cancel(self):
        if self.cancelCallback is not None:
            self.cancelCallback()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = CanvasWin()
    win.hide()

    l = LoginWin()
    l.loadCanvas = lambda _: win.show()
    l.exec()

    # s = SaveDlg(win)
    # s.exec()

    sys.exit(app.exec())
