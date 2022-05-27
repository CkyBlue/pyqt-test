# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/Canvas.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("Canvas")

        MainWindow.setGeometry(100, 100, 800, 600)
        MainWindow.setFixedSize(700, 500)

        self.image = QImage(MainWindow.size(), QImage.Format_RGB32)

        self.image.fill(Qt.white)

        self.drawing = False

        self.brushSize = 4
        self.brushColor = Qt.black

        self.lastPoint = QPoint()

        mainMenu = MainWindow.menuBar()
        fileMenu = mainMenu.addMenu("File")

        b_size = mainMenu.addMenu("Brush Size")

        saveAction = QAction("Save", MainWindow)
        saveAction.setShortcut("Ctrl + S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        clearAction = QAction("Clear", MainWindow)
        clearAction.setShortcut("Ctrl + C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

        pix_4 = QAction("4px", MainWindow)
        b_size.addAction(pix_4)
        pix_4.triggered.connect(self.Pixel_4)

        pix_7 = QAction("7px", MainWindow)
        b_size.addAction(pix_7)
        pix_7.triggered.connect(self.Pixel_7)

        pix_9 = QAction("9px", MainWindow)
        b_size.addAction(pix_9)
        pix_9.triggered.connect(self.Pixel_9)


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)

            painter.setPen(QPen(self.brushColor, self.brushSize,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

            painter.drawLine(self.lastPoint, event.pos())

            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    # method for saving canvas
    def save(self):
        # filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
        #                                           "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        #
        # if filePath == "":
        #     return
        # self.image.save(filePath)
        pass

    def clear(self):
        self.image.fill(Qt.white)
        self.update()

    def Pixel_4(self):
        self.brushSize = 4

    def Pixel_7(self):
        self.brushSize = 7

    def Pixel_9(self):
        self.brushSize = 9

    def Pixel_12(self):
        self.brushSize = 12

class Ui_MainWindow2(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setTabletTracking(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        self.menuConfigs = QtWidgets.QMenu(self.menubar)
        self.menuConfigs.setObjectName("menuConfigs")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionClear = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap("UI/../delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClear.setIcon(icon)
        self.actionClear.setObjectName("actionClear")
        self.actionLog_Out = QtWidgets.QAction(MainWindow)
        self.actionLog_Out.setObjectName("actionLog_Out")
        self.actionChange_Sampling_Rate = QtWidgets.QAction(MainWindow)
        self.actionChange_Sampling_Rate.setObjectName("actionChange_Sampling_Rate")
        self.menuOptions.addAction(self.actionClear)
        self.menuOptions.addAction(self.actionLog_Out)
        self.menuConfigs.addAction(self.actionChange_Sampling_Rate)
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuConfigs.menuAction())
        self.toolBar.addAction(self.actionClear)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuOptions.setTitle(_translate("MainWindow", "Options"))
        self.menuConfigs.setTitle(_translate("MainWindow", "Configs"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionClear.setText(_translate("MainWindow", "Clear"))
        self.actionLog_Out.setText(_translate("MainWindow", "Log Out"))
        self.actionChange_Sampling_Rate.setText(_translate("MainWindow", "Change Sampling Rate"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
