
from PyQt5 import QtCore, QtGui, QtWidgets
import random
import string
import os, sys
import pandas as pd
from functools import partial

def send_email(text,address, title):
    #os.system("echo \"" +  text + " \" | mutt -s \"" +title + "\" " + address)
    print("emailserf")
def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
def checklogin (usernames, passwords):
    df = pd.read_csv("users.csv")
    user_data = df[df["username"] == usernames]
    if (user_data.empty):
        print("Username Not Found")
        return "notfound"
    else:
        pas = user_data["password"].values[0]
        if (pas == passwords):
            print("right pass")
            return "right"
        else:
            print("Wrong Pass")
            return "wrong"

global state
global text_username
global text_password
global state

class Register():
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")

        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(410, 40, 611, 551))

        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.title = QtWidgets.QLabel(self.frame)
        self.title.setText("PyAuction: Register")

        font = QtGui.QFont()
        font.setPointSize(50)
        self.title.setFont(font)


        self.username = QtWidgets.QLineEdit(self.frame)
        self.username.setGeometry(QtCore.QRect(90, 160, 421, 51))
        self.username.setStyleSheet("background-color: rgb(213, 213, 213);")
        self.username.setInputMask("")
        self.username.setText("")
        self.username.setReadOnly(False)
        self.username.setObjectName("lineEdit")

        self.email = QtWidgets.QLineEdit(self.frame)
        self.email.setGeometry(QtCore.QRect(90, 240, 421, 51))
        self.email.setStyleSheet("background-color: rgb(213, 213, 213);")
        self.email.setObjectName("lineEdit_4")

        self.radioButton = QtWidgets.QRadioButton(self.frame)
        self.radioButton.setGeometry(QtCore.QRect(100, 340, 411, 31))

        self.radioButton.setObjectName("radioButton")

        self.submitbutton = QtWidgets.QPushButton(self.frame)
        self.submitbutton.setGeometry(QtCore.QRect(90, 440, 421, 51))
        font = QtGui.QFont()
        font.setPointSize(16)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        submit_a = partial(self.submit, Dialog)
        self.submitbutton.clicked.connect(submit_a)

    def submit (self, Dialog):
        text_user = self.username.text()
        text_email = self.email.text()
        text_pass = randomString()

        print(text_pass)

        with open('users.csv', 'a+') as fd:
            fd.write(text_user +","+ text_email +","+ text_pass+'\n')
            send_email(text_pass, text_email, "PyAuction Password")
            fd.write(' \n')
        DialogR.accept()
        print("Saved")


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.username.setPlaceholderText(_translate("Dialog", "Username"))
        self.email.setPlaceholderText(_translate("Dialog", "Email"))
        self.radioButton.setText(_translate("Dialog", "I Agree with Terms and Conditions"))
        self.submitbutton.setText(_translate("Dialog", "Sign Up"))

class Login(QtWidgets.QDialog):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")

        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(410, 40, 611, 551))

        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.title = QtWidgets.QLabel(self.frame)
        self.title.setText("PyAuction: Login")

        font = QtGui.QFont()
        font.setPointSize(50)
        self.title.setFont(font)


        self.username = QtWidgets.QLineEdit(self.frame)
        self.username.setGeometry(QtCore.QRect(90, 160, 421, 51))
        self.username.setStyleSheet("background-color: rgb(213, 213, 213);")
        self.username.setInputMask("")
        self.username.setText("")
        self.username.setReadOnly(False)
        self.username.setObjectName("lineEdit")

        self.password = QtWidgets.QLineEdit(self.frame)
        self.password.setGeometry(QtCore.QRect(90, 240, 421, 51))
        self.password.setStyleSheet("background-color: rgb(213, 213, 213);")
        self.password.setObjectName("lineEdit_4")
        self.loginbutton = QtWidgets.QPushButton(self.frame)
        self.loginbutton.setGeometry(QtCore.QRect(90, 340, 421, 51))

        self.registerbutton = QtWidgets.QPushButton(self.frame)
        self.registerbutton.setGeometry(QtCore.QRect(90, 400, 421, 51))

        font = QtGui.QFont()
        font.setPointSize(16)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        log = partial(self.login, Dialog)
        reg = partial(self.register, Dialog)

        self.loginbutton.clicked.connect(log)
        self.registerbutton.clicked.connect(reg)

    def login (self, Dialog):
        global text_username, text_password, state
        state = "login"
        text_username = self.username.text()
        text_password = self.password.text()
        Dialog.accept()

    def register (self, Dialog):
        global state
        state = "register"
        Dialog.reject()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.username.setPlaceholderText(_translate("Dialog", "Username"))
        self.password.setPlaceholderText(_translate("Dialog", "Password"))
        self.registerbutton.setText(_translate("Dialog", "Sign Up"))
        self.loginbutton.setText(_translate("Dialog", "Login"))


# def main():
global state
#state = "init"
app = QtWidgets.QApplication(sys.argv)
Dialog = QtWidgets.QDialog()
ui = Login()
ui.setupUi(Dialog)
appR = QtWidgets.QApplication(sys.argv)
DialogR = QtWidgets.QDialog()
uiR = Register()
uiR.setupUi(DialogR)

while True:
    print("start loop")
    Dialog.show()
    result = app.exec_()
    if (state == "login"):
        everythingOK = checklogin(text_username, text_password)
        print(everythingOK)
        if everythingOK == "right":
            break
    if (state == "register"):
        DialogR.show()
        appR.exec_()
        print("state changed")
        state = "login"
    #if (state == "init"):
    #    result = app.exec_()


import auctionsite
print("dome")
auctionsite.main(text_username)
print("a")

