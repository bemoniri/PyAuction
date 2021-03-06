from PyQt5 import QtCore, QtGui, QtWidgets
import time
import datetime
import os, sys
from datetime import datetime
import pandas as pd
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication)
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

global rows
global oldornew
oldornew = 0

from functools import partial

headers = ["Auction", "Price", "Time", "Username"]


class TableModel(QAbstractTableModel):
    def rowCount(self, parent):
        global rows
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


global profile_view
global username
global state
global text_username
global text_password
global state
global is_add
global error_mess
global profile_error_mess
global want_to_see_my_bids
global is_ref
global buttpress

is_ref = 0
want_to_see_my_bids = 0
profile_error_mess = ""
error_mess = ""
is_add = 0
profile_view = 0

def accepts():
    model = TableModel()
    view = QTableView()
    view.setModel(model)
    view.show()

class SurfViewer(QtWidgets.QDialog):

    def bid(self, obj, name, Dialog):
        global username
        global error_mess

        bid_df = pd.read_csv("bids.csv")
        text = obj.text()
        auctionDF = pd.read_csv('auctions.csv')

        listofauctions = auctionDF[auctionDF["Name"] == name]
        auctiontype = listofauctions["Type"].values[0]
        try:
            bid_price = int(text)
        except:
            error_mess = "Wrong Value for Price"
            return
        # extbid = listofauctions["FirstBid"].values[0]

        bids_data = pd.read_csv('bids.csv')
        bids_data = bids_data[bids_data["Auction"] == name]


        if int(auctiontype) == 1:
            extbid = max(bids_data["Price"])
            if int(bid_price) >= int(extbid):
                s = pd.Series([name, int(text), datetime.now(), username], index=["Auction", "Price", "Time", "User"])
                bid_df = bid_df.append(s, ignore_index=True)
                bid_df.to_csv('bids.csv', index=False)
                error_mess = "Completed"
            else:

                error_mess = "Bid Higher!"
        else:
            extbid = min(bids_data["Price"])
            if int(bid_price) <= int(extbid):
                s = pd.Series([name, int(text), datetime.now(), username], index=["Auction", "Price", "Time", "User"])
                bid_df = bid_df.append(s, ignore_index=True)
                bid_df.to_csv('bids.csv', index=False)
                error_mess = "Completed"
            else:
                error_mess = "Bid Lower!"
        global is_add
        is_add = -1
        Dialog.accept()

    def refresh_func(self, Dialog):
        global is_add
        is_add = -1
        Dialog.accept()

    def logout(self):
        # exec(open("login.py").read())
        os.system("python login.py")
        quit()

    def done(self, butt, Dialog):
        global buttpress
        global is_add
        is_add = 0
        buttpress = butt
        Dialog.accept()

    def my_bids(self, Dialog):
        global want_to_see_my_bids
        global oldornew
        oldornew = 1
        want_to_see_my_bids = 1
        Dialog.accept()

    def my_oldbids(self, Dialog):
        global want_to_see_my_bids
        global oldornew
        oldornew = -1
        want_to_see_my_bids = 1
        Dialog.accept()

    def create_auction(self, obj1, obj2, obj3, obj4, obj5, Dialog):
        global username
        global is_add
        global error_mess
        name = obj1.text()
        type = obj2.text()
        detail = obj3.text()
        first_bid = obj4.text()

        duration = float(obj5.text())

        fin_time = time.time() + duration * 60
        # fin_time = datetime.fromtimestamp(fin_time).strftime('%c')

        auction_df = pd.read_csv('auctions.csv')
        s = pd.Series([name, int(type), detail, first_bid, fin_time],
                      index=["Name", "Type", "Details", "FirstBid", "Time"])
        auction_df = auction_df.append(s, ignore_index=True)
        auction_df.to_csv('auctions.csv', index=False)
        is_add = 1

        bid_df = pd.read_csv("bids.csv")
        s = pd.Series([name, first_bid, datetime.now(), "Init"], index=["Auction", "Price", "Time", "User"])
        bid_df = bid_df.append(s, ignore_index=True)
        bid_df.to_csv('bids.csv', index=False)
        error_mess = "Created!"
        Dialog.accept()

    def see_profile(self, Dialog):
        global profile_view
        global profile_error_mess
        profile_error_mess = ""
        profile_view = 1
        Dialog.accept()

    def exit_function(self, Dialog):
        global profile_view
        profile_view = 0
        Dialog.accept()

    def change_pass_function(self, old, new, repnew, Dialog):
        global profile_error_mess
        old = old.text()
        new = new.text()
        repnew = repnew.text()
        df = pd.read_csv("users.csv")
        real_pass = str(df[df["username"] == username].password.values[0])

        if (real_pass == old):
            if (new == repnew):
                # df[df["username"] == username].password = new
                df.loc[df["username"] == username, 'password'] = new
                profile_error_mess = "Password Changed!"
            else:
                profile_error_mess = "Passwords do not match!"

        else:
            profile_error_mess = "Wrong Password!"
        df.to_csv("users.csv", index=False)
        Dialog.accept()

    def setupProfile(self, Dialog):
        # global username

        df = pd.read_csv("users.csv")
        email = str(df[df["username"] == username].email.values[0])
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(100, 100, 1000, 500)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.exitbutton = QtWidgets.QPushButton(self.frame)
        self.exitbutton.setText("Back")
        self.exitbutton.setGeometry(QtCore.QRect(0, 0, 100, 51))

        exit_partial = partial(self.exit_function, Dialog)
        self.exitbutton.clicked.connect(exit_partial)

        self.title1 = QtWidgets.QLabel(self.frame)
        self.title1.setText("Email:   " + email)
        self.title1.setGeometry(QtCore.QRect(150, 0, 200, 30))

        self.title = QtWidgets.QLabel(self.frame)
        self.title.setText("Username:   " + username)
        self.title.setGeometry(QtCore.QRect(150, 30, 200, 30))

        # Change Password

        self.old_t = QtWidgets.QLabel(self.frame)
        self.old_t.setText("Old Password")
        self.old_t.setGeometry(QtCore.QRect(150, 100, 100, 51))

        self.new_t = QtWidgets.QLabel(self.frame)
        self.new_t.setText("New Password")
        self.new_t.setGeometry(QtCore.QRect(145 + 150, 100, 100, 51))

        self.repnew_t = QtWidgets.QLabel(self.frame)
        self.repnew_t.setText("Repeat Password")
        self.repnew_t.setGeometry(QtCore.QRect(135 + 300, 100, 150, 51))

        self.old = QtWidgets.QLineEdit(self.frame)
        self.old.setGeometry(QtCore.QRect(150, 150, 100, 51))
        self.old.setStyleSheet("background-color: rgb(213, 213, 213);")
        self.old.setInputMask("")
        self.old.setText("")
        self.old.setReadOnly(False)
        self.old.setObjectName("lineEdit")

        self.new = QtWidgets.QLineEdit(self.frame)
        self.new.setGeometry(QtCore.QRect(300, 150, 100, 51))
        self.new.setStyleSheet("background-color: rgb(213, 213, 213);")
        self.new.setInputMask("")
        self.new.setText("")
        self.new.setReadOnly(False)
        self.new.setObjectName("lineEdit")

        self.repnew = QtWidgets.QLineEdit(self.frame)
        self.repnew.setGeometry(QtCore.QRect(450, 150, 100, 51))
        self.repnew.setStyleSheet("background-color: rgb(213, 213, 213);")
        self.repnew.setInputMask("")
        self.repnew.setText("")
        self.repnew.setReadOnly(False)
        self.repnew.setObjectName("lineEdit")

        self.changebutton = QtWidgets.QPushButton(self.frame)
        self.changebutton.setText("Change")
        self.changebutton.setGeometry(QtCore.QRect(0, 150, 100, 51))
        cpf_partial = partial(self.change_pass_function, self.old, self.new, self.repnew, Dialog)
        self.changebutton.clicked.connect(cpf_partial)

        # global error_mess
        global profile_error_mess
        self.warning = QtWidgets.QLabel(self.frame)
        self.warning.setText(profile_error_mess)
        self.warning.setGeometry(QtCore.QRect(300 + 100, 250, 200, 301))
        font = QtGui.QFont()
        font.setFamily("Free Serif")
        font.setPixelSize(20)
        font.setBold(True)
        self.warning.setFont(font)

        self.see_mybids = QtWidgets.QPushButton(self.frame)
        self.see_mybids.setText("Active Bids")
        self.see_mybids.setGeometry(QtCore.QRect(0, 250, 250, 51))

        self.see_otherbids = QtWidgets.QPushButton(self.frame)
        self.see_otherbids.setText("My Old Bids")
        self.see_otherbids.setGeometry(QtCore.QRect(300, 250, 250, 51))

        mybids_partial = partial(self.my_bids, Dialog)
        self.see_mybids.clicked.connect(mybids_partial)

        myoldbids_partial = partial(self.my_oldbids, Dialog)
        self.see_otherbids.clicked.connect(myoldbids_partial)

    def setupUi(self, Dialog):
        finish = QAction("Quit", self)
        finish.triggered.connect(self.closeEvent)

        def closeEvent(self, event):
            global buttpress
            buttpress = ""
            close = QMessageBox.question(self,
                                         "QUIT",
                                         "Sure?",
                                         QMessageBox.Yes | QMessageBox.No)
            if close == QMessageBox.Yes:
                event.accept()

            else:
                event.ignore()

        self.butpress = 0
        Dialog.setObjectName("Dialog")

        super(SurfViewer, self).__init__()
        self.frame = QtWidgets.QFrame(Dialog)

        self.frame.setGeometry(100, 100, 1100, 530)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        df = pd.read_csv("auctions.csv")

        df1 = df[df["Type"] == 1]
        df2 = df[df["Type"] == 0]

        i = -1

        self.Refresh = QtWidgets.QPushButton(self.frame)
        self.Refresh.setText("Refresh")
        self.Refresh.setGeometry(QtCore.QRect(0, 0, 100, 31))
        refresh_partial = partial(self.refresh_func, Dialog)
        self.Refresh.clicked.connect(refresh_partial)

        self.addAuction = QtWidgets.QPushButton(self.frame)
        self.addAuction.setText("Add Auction")
        self.addAuction.setGeometry(QtCore.QRect(0, 50, 100, 51))

        self.profile = QtWidgets.QPushButton(self.frame)
        self.profile.setText("Profile")
        self.profile.setGeometry(QtCore.QRect(450 + 450, 50, 100, 51))

        prof_partial = partial(self.see_profile, Dialog)
        # self.addAuction.clicked.connect(make_auction)
        self.profile.clicked.connect(prof_partial)

        self.logoutobj = QtWidgets.QPushButton(self.frame)
        self.logoutobj.setText("Logout")
        self.logoutobj.setGeometry(QtCore.QRect(450 + 450, 110, 100, 51))

        log = partial(self.logout)
        self.logoutobj.clicked.connect(log)

        self.un = QtWidgets.QLabel(self.frame)
        self.un.setText("Username: " + "\n" + username)
        self.un.setGeometry(QtCore.QRect(450 + 450, 0, 100, 51))

        self.title1 = QtWidgets.QLabel(self.frame)
        self.title1.setText("Name")
        self.title1.setGeometry(QtCore.QRect(175, 0, 100, 51))

        self.title2 = QtWidgets.QLabel(self.frame)
        self.title2.setText("Monaghese (0)" + "\n" + "Mozayedeh (1)")
        self.title2.setGeometry(QtCore.QRect(150 + 150, 0, 100, 51))

        self.title3 = QtWidgets.QLabel(self.frame)
        self.title3.setText("Detail")
        self.title3.setGeometry(QtCore.QRect(175 + 300, 0, 100, 51))

        self.title4 = QtWidgets.QLabel(self.frame)
        self.title4.setText("First Bid")
        self.title4.setGeometry(QtCore.QRect(175 + 450, 0, 100, 51))

        self.title5 = QtWidgets.QLabel(self.frame)
        self.title5.setText("Duration")
        self.title5.setGeometry(QtCore.QRect(175 + 600, 0, 100, 51))

        global error_mess
        self.warning = QtWidgets.QLabel(self.frame)
        self.warning.setText(error_mess)
        self.warning.setGeometry(QtCore.QRect(300 + 100, 350, 200, 301))
        font = QtGui.QFont()
        font.setFamily("Free Serif")
        font.setPixelSize(20)

        font.setBold(True)
        self.warning.setFont(font)

        self.textbox1 = QtWidgets.QLineEdit(self.frame)
        self.textbox1.setGeometry(QtCore.QRect(150, 50, 100, 51))
        self.textbox1.setStyleSheet("background-color: rgb(213, 213, 213);")
        self.textbox1.setInputMask("")
        self.textbox1.setText("")
        self.textbox1.setReadOnly(False)
        self.textbox1.setObjectName("lineEdit")

        self.textbox2 = QtWidgets.QLineEdit(self.frame)
        self.textbox2.setGeometry(QtCore.QRect(300, 50, 100, 51))
        self.textbox2.setStyleSheet("background-color: rgb(213, 213, 213);")
        self.textbox2.setInputMask("")
        self.textbox2.setText("")
        self.textbox2.setReadOnly(False)
        self.textbox2.setObjectName("lineEdit")

        self.textbox3 = QtWidgets.QLineEdit(self.frame)
        self.textbox3.setGeometry(QtCore.QRect(450, 50, 100, 51))
        self.textbox3.setStyleSheet("background-color: rgb(213, 213, 213);")
        self.textbox3.setInputMask("")
        self.textbox3.setText("")
        self.textbox3.setReadOnly(False)
        self.textbox3.setObjectName("lineEdit")

        self.textbox4 = QtWidgets.QLineEdit(self.frame)
        self.textbox4.setGeometry(QtCore.QRect(600, 50, 100, 51))
        self.textbox4.setStyleSheet("background-color: rgb(213, 213, 213);")
        self.textbox4.setInputMask("")
        self.textbox4.setText("")
        self.textbox4.setReadOnly(False)
        self.textbox4.setObjectName("lineEdit")

        self.textbox5 = QtWidgets.QLineEdit(self.frame)
        self.textbox5.setGeometry(QtCore.QRect(750, 50, 100, 51))
        self.textbox5.setStyleSheet("background-color: rgb(213, 213, 213);")
        self.textbox5.setInputMask("")
        self.textbox5.setText("")
        self.textbox5.setReadOnly(False)
        self.textbox5.setObjectName("lineEdit")

        make_auction = partial(self.create_auction, self.textbox1, self.textbox2, self.textbox3, self.textbox4,
                               self.textbox5, Dialog)
        self.addAuction.clicked.connect(make_auction)

        for index, row in df1.iterrows():
            i += 1
            name = row['Name']
            bids_data = pd.read_csv('bids.csv')
            bids_data = bids_data[bids_data["Auction"] == name]
            price = max(bids_data["Price"])

            # price = row['FirstBid']
            time = row['Time']
            time = datetime.fromtimestamp(int(time)).strftime('%c')

            self.title = QtWidgets.QLabel(self.frame)
            self.title.setText("Name: " + name + "\n" + "Max Price: " + str(price) + "\n" + "Time: " + str(time))
            self.title.setGeometry(QtCore.QRect(150, 160 + 110 * i, 250, 51))

            self.textbox = QtWidgets.QLineEdit(self.frame)
            self.textbox.setGeometry(QtCore.QRect(150, 220 + 110 * i, 100, 31))
            self.textbox.setStyleSheet("background-color: rgb(213, 213, 213);")
            self.textbox.setInputMask("")
            self.textbox.setText("")
            self.textbox.setReadOnly(False)
            self.textbox.setObjectName("lineEdit")

            self.button = QtWidgets.QPushButton(self.frame)
            self.button.setText("See Bids")
            self.button.setGeometry(QtCore.QRect(0, 160 + 110 * i, 100, 51))
            display_a = partial(self.done, name, Dialog)
            self.button.clicked.connect(display_a)

            self.bidbutton = QtWidgets.QPushButton(self.frame)
            self.bidbutton.setText("Bid")
            self.bidbutton.setGeometry(QtCore.QRect(0, 220 + 110 * i, 100, 31))
            bid_auction = partial(self.bid, self.textbox, name, Dialog)
            self.bidbutton.clicked.connect(bid_auction)

            bids_df = pd.read_csv("bids.csv")

        i = -1
        for index, row in df2.iterrows():
            i += 1
            name = row['Name']
            bids_data = pd.read_csv('bids.csv')
            bids_data = bids_data[bids_data["Auction"] == name]
            price = min(bids_data["Price"])
            time = row['Time']
            time = datetime.fromtimestamp(int(time)).strftime('%c')

            self.title = QtWidgets.QLabel(self.frame)
            self.title.setText("Name: " + name + "\n" + "Min Price: " + str(price) + "\n" + "Time: " + str(time))
            self.title.setGeometry(QtCore.QRect(150 + 530, 160 + 110 * i, 250, 51))

            self.button = QtWidgets.QPushButton(self.frame)
            self.button.setText("See Bids")
            self.button.setGeometry(QtCore.QRect(0 + 530, 160 + 110 * i, 100, 51))
            display_a = partial(self.done, name, Dialog)
            self.button.clicked.connect(display_a)

            self.textbox = QtWidgets.QLineEdit(self.frame)
            self.textbox.setGeometry(QtCore.QRect(530 + 150, 220 + 110 * i, 100, 31))
            self.textbox.setStyleSheet("background-color: rgb(213, 213, 213);")
            self.textbox.setInputMask("")
            self.textbox.setText("")
            self.textbox.setReadOnly(False)
            self.textbox.setObjectName("lineEdit")

            self.bidbutton = QtWidgets.QPushButton(self.frame)
            self.bidbutton.setText("Bid")
            self.bidbutton.setGeometry(QtCore.QRect(0 + 530, 220 + 110 * i, 100, 31))

            bid_auction = partial(self.bid, self.textbox, name, Dialog)
            self.bidbutton.clicked.connect(bid_auction)

            bids_df = pd.read_csv("bids.csv")


# if __name__ == '__main__':
def main(username_input):
    print("Auction Site")
    global username
    global is_add
    username = username_input
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    DialogP = QtWidgets.QDialog()

    apps = QApplication([])
    ui = SurfViewer()
    ui.setupUi(Dialog)
    headers = ["Auction", "Price", "Time", "Username"]
    # model = TableModel()
    # view = QTableView()
    # view.setModel(model)

    ui.setupUi(Dialog)
    Dialog.show()
    result = app.exec_()
    global rows
    global want_to_see_my_bids
    global oldornew

    while 1:
        global profile_view
        if (profile_view):
            while True:
                DialogP = QtWidgets.QDialog()
                ui_p = SurfViewer()
                ui_p.setupProfile(DialogP)
                DialogP.show()
                result = app.exec_()
                if (want_to_see_my_bids == 1):
                    if (oldornew == 1):
                        # global username
                        df = pd.read_csv("bids.csv")
                        rows = df[df["User"] == username].values.tolist()
                        model = TableModel()
                        view = QTableView()
                        view.setModel(model)
                        view.show()
                        want_to_see_my_bids = 0
                    else:
                        df = pd.read_csv("old_bids.csv")
                        rows = df[df["User"] == username].values.tolist()
                        model = TableModel()
                        view = QTableView()
                        view.setModel(model)
                        view.show()
                        want_to_see_my_bids = 0

                if (profile_view == 0):
                    break

                del ui_p
                del DialogP
            ui = SurfViewer()
            ui.setupUi(Dialog)
            Dialog.show()
            result = app.exec_()

        else:
            del ui
            del Dialog
            Dialog = QtWidgets.QDialog()
            ui = SurfViewer()
            ui.setupUi(Dialog)
            Dialog.show()

            if (is_add == 0):
                # global rows
                df = pd.read_csv("bids.csv")
                rows = df[df["Auction"] == buttpress].values.tolist()
                model = TableModel()
                view = QTableView()
                view.setModel(model)
                view.show()
            # if(is_add = -1):

            is_add = 0
            result = app.exec_()
