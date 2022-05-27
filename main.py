from components.Canvas import Ui_MainWindow as Canvas
from components.ProtoCanvas import Ui_MainWindow as ProtoCanvas
from components.Login import Ui_Dialog as Login
from components.MsgBox import Ui_Dialog as MsgBox
from components.Register import Ui_Dialog as Register

import sys

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton

# class Window(QMainWindow):
#     """Main window."""
#     def __init__(self, parent=None):
#         """Initializer."""
#         super().__init__(parent)
#         # Use a QPushButton for the central widget
#         self.centralWidget = QPushButton("Employee...")
#         # Connect the .clicked() signal with the .onEmployeeBtnClicked() slot
#         self.centralWidget.clicked.connect(self.onEmployeeBtnClicked)
#         self.setCentralWidget(self.centralWidget)
#
#     # Create a slot for launching the employee dialog
#     def onEmployeeBtnClicked(self):
#         """Launch the employee dialog."""
#         dlg = EmployeeDlg(self)
#         dlg.exec()
#

usernames = {"SK": "A!ML@B"}
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
            msg.setMsg("Successfully registered user.")

        msg.exec()


class CanvasWin(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Canvas()
        self.ui.setupUi(self)


class MsgBoxDlg(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = MsgBox()
        self.ui.setupUi(self)

    def setMsg(self, msg):
        self.ui.label.setText(msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = ProtoCanvas()
    win.hide()

    l = LoginWin()
    l.loadCanvas = lambda _: win.show()
    l.exec()

    sys.exit(app.exec())
