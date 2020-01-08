
from PyQt5 import QtCore, QtGui, QtWidgets
import random
import string
import os, sys
from datetime import  datetime
import pandas as pd
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication)
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
global rows
from functools import partial
#rows =    [("Newton", "1643-01-04", "Classical mechanics"),
#           ("Einstein", "1879-03-14", "Relativity"),
#           ("Darwin", "1809-02-12", "Evolution"),("Darwin", "1809-02-12", "Evolution"),("Darwin", "1809-02-12", "Evolution")]
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


global username
username = "Trump"
global state
global text_username
global text_password
global state
global is_add
global error_mess
error_mess = ""
is_add = 0

def accepts():
    model = TableModel()
    view = QTableView()
    view.setModel(model)
    view.show()

global buttpress
class SurfViewer(QtWidgets.QDialog):

    def bid (self, obj, name, Dialog):
        global username
        bid_df = pd.read_csv("bids.csv")
        text = obj.text()
        auctionDF = pd.read_csv('auctions.csv')

        listofauctions = auctionDF[auctionDF["Name"] == name]
        auctiontype = listofauctions["Type"].values[0]
        bid_price = int(text)
        #extbid = listofauctions["FirstBid"].values[0]

        bids_data = pd.read_csv('bids.csv')
        bids_data = bids_data[bids_data["Auction"] == name]

        global error_mess
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




    def logout(self):
        #exec(open("login.py").read())
        os.system("python login.py")
        quit()

    def done(self, butt, Dialog):
        global buttpress
        global is_add
        is_add = 0
        buttpress = butt
        Dialog.accept()

    def create_auction(self, obj1, obj2, obj3, obj4, Dialog):
        global username
        global is_add
        global error_mess
        name = obj1.text()
        type = obj2.text()
        detail = obj3.text()
        first_bid = obj4.text()
        time = datetime.now()
        auction_df = pd.read_csv('auctions.csv')
        s = pd.Series([name, int(type), detail, first_bid, time], index=["Name", "Type", "Details", "FirstBid", "Time"])
        auction_df = auction_df.append(s, ignore_index=True)
        auction_df.to_csv('auctions.csv', index=False)
        is_add = 1

        bid_df = pd.read_csv("bids.csv")
        s = pd.Series([name, first_bid, datetime.now(), "Init"], index=["Auction", "Price", "Time", "User"])
        bid_df = bid_df.append(s, ignore_index=True)
        bid_df.to_csv('bids.csv', index=False)
        error_mess = "Created!"
        Dialog.accept()


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
        #self.frame.setGeometry(QtCore.QRect(500, 500, 500, 500))
        self.frame.setGeometry(100, 100, 1000, 500)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        df = pd.read_csv("auctions.csv")

        df1 = df[df["Type"] == 1]
        df2 = df[df["Type"] == 0]

        i = -1
        self.addAuction = QtWidgets.QPushButton(self.frame)
        self.addAuction.setText("Add Auction")
        self.addAuction.setGeometry(QtCore.QRect(0, 40, 100, 51))

        self.profile = QtWidgets.QPushButton(self.frame)
        self.profile.setText("Profile")
        self.profile.setGeometry(QtCore.QRect(450+450, 50, 100, 51))

        self.logoutobj = QtWidgets.QPushButton(self.frame)
        self.logoutobj.setText("Logout")
        self.logoutobj.setGeometry(QtCore.QRect(450 + 450, 110, 100, 51))

        log = partial(self.logout)
        self.logoutobj.clicked.connect(log)


        self.un = QtWidgets.QLabel(self.frame)
        self.un.setText("Username: " + "\n" + username)
        self.un.setGeometry(QtCore.QRect(450+450, 0, 100, 51))

        self.title1 = QtWidgets.QLabel(self.frame)
        self.title1.setText("Name")
        self.title1.setGeometry(QtCore.QRect(175, 0, 100, 51))

        self.title2 = QtWidgets.QLabel(self.frame)
        self.title2.setText("Monaghese (0)"+ "\n" + "Mozayedeh (1)")
        self.title2.setGeometry(QtCore.QRect(150+150, 0, 100, 51))

        self.title3 = QtWidgets.QLabel(self.frame)
        self.title3.setText("Detail")
        self.title3.setGeometry(QtCore.QRect(175+300, 0, 100, 51))

        self.title4 = QtWidgets.QLabel(self.frame)
        self.title4.setText("First Bid")
        self.title4.setGeometry(QtCore.QRect(175+450, 0, 100, 51))

        global error_mess
        self.warning = QtWidgets.QLabel(self.frame)
        self.warning.setText(error_mess)
        self.warning.setGeometry(QtCore.QRect(300 + 100, 200, 100, 51))


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

        make_auction = partial(self.create_auction, self.textbox1, self.textbox2, self.textbox3, self.textbox4, Dialog)
        self.addAuction.clicked.connect(make_auction)

        for index, row in df1.iterrows():
            i += 1
            name = row['Name']
            bids_data = pd.read_csv('bids.csv')
            bids_data = bids_data[bids_data["Auction"] == name]
            price = max(bids_data["Price"])

            #price = row['FirstBid']
            time = row['Time']

            self.title = QtWidgets.QLabel(self.frame)
            self.title.setText("Name:" + name + "\n" + "Max Price:" + str(price) + "\n" + "Time:" + str(time))
            self.title.setGeometry(QtCore.QRect(0, 160 + 110*i, 100, 51))

            self.textbox = QtWidgets.QLineEdit(self.frame)
            self.textbox.setGeometry(QtCore.QRect(0, 220 + 110 * i, 100, 31))
            self.textbox.setStyleSheet("background-color: rgb(213, 213, 213);")
            self.textbox.setInputMask("")
            self.textbox.setText("")
            self.textbox.setReadOnly(False)
            self.textbox.setObjectName("lineEdit")

            self.button = QtWidgets.QPushButton(self.frame)
            self.button.setText("See Bids")
            self.button.setGeometry(QtCore.QRect(200, 160 + 110 * i, 100, 51))
            display_a = partial(self.done, name, Dialog)
            self.button.clicked.connect(display_a)

            self.bidbutton = QtWidgets.QPushButton(self.frame)
            self.bidbutton.setText("Bid")
            self.bidbutton.setGeometry(QtCore.QRect(200, 220 + 110 * i, 100, 31))
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

            self.title = QtWidgets.QLabel(self.frame)
            self.title.setText("Name:" + name + "\n" + "Min Price:" + str(price) + "\n" + "Time:" + str(time))
            self.title.setGeometry(QtCore.QRect(90+530, 160 + 110 * i, 100, 51))

            self.button = QtWidgets.QPushButton(self.frame)
            self.button.setText("See Bids")
            self.button.setGeometry(QtCore.QRect(210+530, 160 + 110 * i, 100, 51))
            display_a = partial(self.done, name, Dialog)
            self.button.clicked.connect(display_a)

            self.textbox = QtWidgets.QLineEdit(self.frame)
            self.textbox.setGeometry(QtCore.QRect(530+90, 220 + 110 * i, 100, 31))
            self.textbox.setStyleSheet("background-color: rgb(213, 213, 213);")
            self.textbox.setInputMask("")
            self.textbox.setText("")
            self.textbox.setReadOnly(False)
            self.textbox.setObjectName("lineEdit")

            self.bidbutton = QtWidgets.QPushButton(self.frame)
            self.bidbutton.setText("Bid")
            self.bidbutton.setGeometry(QtCore.QRect(210+530, 220 + 110 * i, 100, 31))

            bid_auction = partial(self.bid, self.textbox, name, Dialog)
            self.bidbutton.clicked.connect(bid_auction)

            bids_df = pd.read_csv("bids.csv")

#if __name__ == '__main__':
def main(username_input):
    print("auction site")
    global username
    global is_add
    username= username_input
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()

    apps = QApplication([])
    ui = SurfViewer()
    ui.setupUi(Dialog)
    headers = ["Auction", "Price", "Time", "Username"]
    #model = TableModel()
    #view = QTableView()
    #view.setModel(model)
    ui.setupUi(Dialog)
    Dialog.show()
    result = app.exec_()
    while 1:
        del ui
        del Dialog
        Dialog = QtWidgets.QDialog()
        ui = SurfViewer()
        ui.setupUi(Dialog)
        Dialog.show()

        if(is_add == 0):
            global rows
            df = pd.read_csv("bids.csv")
            rows= df[df["Auction"]==buttpress].values.tolist()
            model = TableModel()
            view = QTableView()
            view.setModel(model)
            view.show()
        #if(is_add = -1):

        is_add = 0
        print('hop')
        result = app.exec_()

        #view.show()
        #ui.setupUi(Dialog)
        #Dialog.show()
        #apps.exec_()
