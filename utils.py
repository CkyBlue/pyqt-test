from datetime import datetime
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QAction

# Avoid '/' since time used in export names
def getDate():
    return datetime.now().strftime("%d-%m-%Y")

def getTime(millis = True):
    if (millis):
        return datetime.now().strftime("%H:%M:%S.%f")
    return datetime.now().strftime("%H:%M:%S")

def getIcon(path):
    icon = QIcon()
    icon.addPixmap(QPixmap(path), QIcon.Normal, QIcon.Off)
    return icon

def createAction(window, iconPath, actionName, callback):
    action = QAction(window)

    action.setIcon(getIcon(iconPath))
    action.setObjectName(actionName)

    if callback is not None:
        action.triggered.connect(callback)

    return action