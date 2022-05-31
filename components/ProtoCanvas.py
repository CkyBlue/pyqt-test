# importing libraries
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, QtGui, QtCore

from utils import *


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        pass

    # TODO Compress
    def recordInstance(self, pos):
        self.strokeData[getTime()] = "({}, {})".format(pos.x(), pos.y())
        print(getTime(), pos.x(), pos.y())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

            if self.recording:
                self.recordInstance(self.lastPoint)

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)

            painter.setPen(QPen(self.brushColor, self.brushSize,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.setRenderHint(QPainter.Antialiasing)

            painter.drawLine(self.lastPoint, event.pos())

            self.lastPoint = event.pos()

            if self.recording:
                self.recordInstance(self.lastPoint)

            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def saveCanvas(self, recordingName):
        filePath = "canvas.png"
        self.image.save(filePath)

    def clear(self):
        self.image.fill(Qt.white)
        self.update()

# window class
# class Ui_MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle("Canvas")
#
#         self.setGeometry(100, 100, 800, 600)
#         self.setFixedSize(700, 500)
#
#         self.setTabletTracking(True)
#
#         self.image = QImage(self.size(), QImage.Format_RGB32)
#
#         self.image.fill(Qt.white)
#
#         self.drawing = False
#
#         self.brushSize = 4
#         self.brushColor = Qt.black
#
#         self.lastPoint = QPoint()
#
#         # mainMenu = self.menuBar()
#         # fileMenu = mainMenu.addMenu("File")
#
#         # b_size = mainMenu.addMenu("Brush Size")
#         #
#         # saveAction = QAction("Save", self)
#         # saveAction.setShortcut("Ctrl + S")
#         # fileMenu.addAction(saveAction)
#         # saveAction.triggered.connect(self.save)
#
#         # clearAction = QAction("Clear", self)
#         # clearAction.setShortcut("Ctrl + C")
#         # fileMenu.addAction(clearAction)
#         # clearAction.triggered.connect(self.clear)
#
#         # pix_4 = QAction("4px", self)
#         # b_size.addAction(pix_4)
#         # pix_4.triggered.connect(self.Pixel_4)
#         #
#         # pix_7 = QAction("7px", self)
#         # b_size.addAction(pix_7)
#         # pix_7.triggered.connect(self.Pixel_7)
#         #
#         # pix_9 = QAction("9px", self)
#         # b_size.addAction(pix_9)
#         # pix_9.triggered.connect(self.Pixel_9)
#
#         MainWindow = self
#
#         MainWindow.setObjectName("MainWindow")
#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#         MainWindow.setCentralWidget(self.centralwidget)
#
#         self.menubar = QtWidgets.QMenuBar(MainWindow)
#         self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
#         self.menubar.setObjectName("menubar")
#         self.menuActions = QtWidgets.QMenu(self.menubar)
#         self.menuActions.setObjectName("menuActions")
#         MainWindow.setMenuBar(self.menubar)
#         self.statusbar = QtWidgets.QStatusBar(MainWindow)
#         self.statusbar.setObjectName("statusbar")
#         MainWindow.setStatusBar(self.statusbar)
#         self.toolBar = QtWidgets.QToolBar(MainWindow)
#         self.toolBar.setObjectName("toolBar")
#         MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
#         self.actionClear = QAction("Clear", self)
#
#         icon = QtGui.QIcon()
#         icon.addPixmap(QtGui.QPixmap("delete_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         self.actionClear.setIcon(icon)
#
#         self.actionClear.setObjectName("actionClear")
#         self.actionClear.triggered.connect(self.clear)
#
#         self.actionSave = QtWidgets.QAction(MainWindow)
#         icon1 = QtGui.QIcon()
#         icon1.addPixmap(QtGui.QPixmap("save_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         self.actionSave.setIcon(icon1)
#         self.actionSave.setObjectName("actionSave")
#         self.menuActions.addAction(self.actionClear)
#         self.menuActions.addAction(self.actionSave)
#         self.menubar.addAction(self.menuActions.menuAction())
#         self.toolBar.addAction(self.actionClear)
#         self.toolBar.addAction(self.actionSave)
#
#     def clear(self):
#         print("Clear")
#
#     def tabletEvent(self, QTabletEvent):
#         print("Tablet Event")
#
#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.drawing = True
#             self.lastPoint = event.pos()
#
#     def mouseMoveEvent(self, event):
#         if (event.buttons() & Qt.LeftButton) & self.drawing:
#             painter = QPainter(self.image)
#
#             painter.setPen(QPen(self.brushColor, self.brushSize,
#                                 Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
#             painter.setRenderHint(QPainter.Antialiasing)
#
#             painter.drawLine(self.lastPoint, event.pos())
#
#             self.lastPoint = event.pos()
#             self.update()
#
#     def mouseReleaseEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.drawing = False
#
#     def paintEvent(self, event):
#         canvasPainter = QPainter(self)
#         canvasPainter.drawImage(self.rect(), self.image, self.image.rect())
#
#     # method for saving canvas
#     def save(self):
#         # filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
#         #                                           "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
#         #
#         # if filePath == "":
#         #     return
#         # self.image.save(filePath)
#         pass
#
#     def clear(self):
#         self.image.fill(Qt.white)
#         self.update()
#
#     def Pixel_4(self):
#         self.brushSize = 4
#
#     def Pixel_7(self):
#         self.brushSize = 7
#
#     def Pixel_9(self):
#         self.brushSize = 9
#
#     def Pixel_12(self):
#         self.brushSize = 12


if __name__ == "__main__":
    import sys

    App = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(App.exec())
