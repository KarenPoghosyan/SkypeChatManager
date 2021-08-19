# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5.QtWidgets import QApplication,QMainWindow, QWidget, QCheckBox,\
    QLabel, QVBoxLayout, QListWidget, QHBoxLayout, QListWidgetItem
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

import json
import skype_handler
import urllib.request


class QCustomQWidget (QWidget):
    def __init__ (self, parent = None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QVBoxLayout()
        self.textUpQLabel    = QLabel()
        self.textDownQLabel  = QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout  = QHBoxLayout()
        self.iconQLabel      = QLabel()
        self.chBox = QCheckBox()
        self.allQHBoxLayout.addWidget(self.chBox, 0)
        self.allQHBoxLayout.addWidget(self.iconQLabel, 1)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 2)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')
        self.textDownQLabel.setStyleSheet('''
            color: rgb(255, 0, 0);
        ''')

    def setTextUp (self, text):
        self.textUpQLabel.setText(text)

    def setTextDown (self, text):
        self.textDownQLabel.setText(text)

    def setIcon (self, imagePath):
        pixmap = QPixmap(imagePath)
        pixmap2 = pixmap.scaled(64, 64)
        self.iconQLabel.setPixmap(pixmap2)

    def unsetChBox(self):
            self.chBox.setCheckState(QtCore.Qt.Unchecked)

    def setChBox(self):
            self.chBox.setCheckState(QtCore.Qt.Checked)

class exampleQMainWindow (QMainWindow):
    def __init__ (self):
        super(exampleQMainWindow, self).__init__()
        # Create QListWidget

    def createList(self, lst):
        self.myQListWidget = QListWidget(self)

        for c in lst:
            #print(c)

            # Create QCustomQWidget
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextUp(str(c.name))
            myQCustomQWidget.setTextDown("ccccc")
            #if c.avatar:
            #    local_filename, headers = urllib.request.urlretrieve(c.avatar)
            #    myQCustomQWidget.setIcon(local_filename)
            myQCustomQWidget.setChBox()

            # Create QListWidgetItem
            #myQListWidgetItem = QListWidgetItem(self.myQListWidget)
            # Set size hint
            #myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            # Add QListWidgetItem into QListWidget
            #self.myQListWidget.addItem(myQListWidgetItem)
            #self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        self.setCentralWidget(self.myQListWidget)





class Ui_MainWindow(object):
    password = ""
    login = ""

    map_lstID2contact = {}
    map_lstID2chat = {}
    skip_contacts = []

    contacts_list = []
    chats_list = []
    sk = None

    def get_contacts_list(self):

        chats_list = json.load(open("./chats_list.json"))

        for c in self.sk.get_contacts():
            if c.id in self.skip_contacts:
                continue
            if "contacts_only" in chats_list:
                if c.id not in chats_list["contacts_only"]:
                    continue

            self.contacts_list.append(c)

    def create_contacts_list(self):
        self.get_contacts_list()
        #sort
        self.contacts_list.sort(key=lambda r: r.raw['creation_time'], reverse=True)

        for c in self.contacts_list:

            # print(c.id + " " + str(c.name) + " " + c.raw['creation_time'])
            self.map_lstID2contact[self.listWidget.count()] = c

            # Create QCustomQWidget
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextUp(str(c.name))
            myQCustomQWidget.setTextDown(c.raw['creation_time'])
            if c.avatar:
                local_filename, headers = urllib.request.urlretrieve(c.avatar)
                myQCustomQWidget.setIcon(local_filename)
            myQCustomQWidget.unsetChBox()

            # Create QListWidgetItem
            myQListWidgetItem = QListWidgetItem(self.listWidget)
            # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            # Add QListWidgetItem into QListWidget
            self.listWidget.addItem(myQListWidgetItem)
            self.listWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)

            self.listWidget.item(0).setSelected(True)




    def create_chat_list(self):
        chats_list = json.load(open("./chats_list.json"))

        for chat_id in chats_list["chats_only"]:
            chat = self.sk.get_chat(chat_id)

            self.map_lstID2chat[self.listWidget_2.count()] = chat

            # Create QCustomQWidget
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextUp(str(chat.topic))
            myQCustomQWidget.setTextDown("ccccc")
            #if hasattr(chat, "picture"):
            #    local_filename, headers = urllib.request.urlretrieve(chat.picture)
            #    myQCustomQWidget.setIcon(local_filename)
            myQCustomQWidget.unsetChBox()

            # Create QListWidgetItem
            myQListWidgetItem = QListWidgetItem(self.listWidget_2)
            # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            # Add QListWidgetItem into QListWidget
            self.listWidget_2.addItem(myQListWidgetItem)
            self.listWidget_2.setItemWidget(myQListWidgetItem, myQCustomQWidget)

    def add_contacts(self):
        for user_index in range(self.listWidget.count()):
            it = self.listWidget.itemWidget(self.listWidget.item(user_index))
            if it.chBox.isChecked():
                for chat_index in range(self.listWidget_2.count()):
                    it2 = self.listWidget_2.itemWidget(self.listWidget_2.item(chat_index))
                    if it2.chBox.isChecked():
                        if self.map_lstID2contact[user_index].id not in self.map_lstID2chat[chat_index].userIds:
                            print(self.map_lstID2contact[user_index].id + "-> " + self.map_lstID2chat[chat_index].topic)
                            self.map_lstID2chat[chat_index].addMember(self.map_lstID2contact[user_index].id)
                        else:
                            print("User " + self.map_lstID2contact[user_index].id + " is already in chat"
                                  + self.map_lstID2chat[chat_index].topic) + ", SKIPPING"

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 768)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 10, 1011, 711))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget = QtWidgets.QListWidget(self.horizontalLayoutWidget)
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout.addWidget(self.listWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton_add = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_add.setObjectName("pushButton_add")
        self.verticalLayout.addWidget(self.pushButton_add)
        self.pushButton_remove = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_remove.setObjectName("pushButton_remove")
        self.verticalLayout.addWidget(self.pushButton_remove)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.listWidget_2 = QtWidgets.QListWidget(self.horizontalLayoutWidget)
        self.listWidget_2.setObjectName("listWidget_2")
        self.horizontalLayout.addWidget(self.listWidget_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton_add.clicked.connect(self.add_contacts)
        #print(self.password)
        #print(self.login)



        try:
            self.sk = skype_handler.SkypeHandler()
            self.sk.connect(self.login, self.password)
        except Exception as err:
            QMessageBox.critical(QWidget(), "Connection Error", str(err))
            exit(1)

        self.skip_contacts = ["0d5d6cff-595d-49d7-9cf8-973173f5233b"]
        self.create_contacts_list()
        self.create_chat_list()




    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Skype Chat Manager"))
        self.pushButton_add.setText(_translate("MainWindow", "Add -->"))
        self.pushButton_remove.setText(_translate("MainWindow", "Remove <--X"))
