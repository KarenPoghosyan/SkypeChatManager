# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5.QtWidgets import QWidget, QCheckBox,\
    QLabel, QVBoxLayout, QHBoxLayout, QListWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

import json
import skype_handler
import urllib.request
import os
import logging
import pathlib


working_dir = "."

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
            color: rgb(0, 0, 0);
        ''')
        self.textUpQLabel.setFont(QtGui.QFont("Arial", 12))

        self.textDownQLabel.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')

    def setTextUp (self, text):
        self.textUpQLabel.setText(text)

    def setTextDown (self, text):
        self.textDownQLabel.setText(text)

    def setAvatar_image (self, local_filename):
        pixmap = QPixmap(local_filename)
        pixmap2 = pixmap.scaled(64, 64)
        self.iconQLabel.setPixmap(pixmap2)

    def setAvatar_default (self, text):
        pixmap = QPixmap(64, 64)
        painter = QtGui.QPainter(pixmap)
        pen = QtGui.QPen()
        pen.setWidth(0)
        pen.setColor(QtGui.QColor.fromRgb(0, 44, 51))
        painter.setPen(pen)
        font = QtGui.QFont("Arial", 18)
        font.setBold(True)
        painter.setFont(font)
        painter.setBrush(QtGui.QBrush(QtGui.QColor.fromRgb(0, 44, 51), QtCore.Qt.SolidPattern))

        rect = QtCore.QRect(0, 0, 64, 64)
        painter.drawEllipse(rect)

        pen.setColor(QtGui.QColor.fromRgb(0, 120, 212))
        painter.setPen(pen)
        painter.drawText(rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, text.upper())
        painter.end()
        self.iconQLabel.setPixmap(pixmap)



    def unsetChBox(self):
            self.chBox.setCheckState(QtCore.Qt.Unchecked)

    def setChBox(self):
            self.chBox.setCheckState(QtCore.Qt.Checked)


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

        working_dir = str(pathlib.Path(__file__).parent.resolve())

        chats_list = json.load(open(working_dir + "/chats_list.json"))

        for c in self.sk.get_contacts():
            if c.id in self.skip_contacts:
                continue
            if "contacts_only" in chats_list:
                if c.id not in chats_list["contacts_only"]:
                    continue

            self.contacts_list.append(c)

    def clean_dt(self, date_time_str):
        ret_str = date_time_str.replace('T', ' ')
        ind = ret_str.rfind('.')
        return ret_str[:ind]

    def create_contacts_list(self):
        try:
            logging.info('Creating contacts list')
            self.get_contacts_list()
            #sort
            self.contacts_list.sort(key=lambda r: r.raw['creation_time'], reverse=True)

            for c in self.contacts_list:
                #print(c.gid + " " + str(c.name) + " " + c.raw['creation_time'])

                self.map_lstID2contact[self.listWidget.count()] = c

                # Create QCustomQWidget
                myQCustomQWidget = QCustomQWidget()

                if c.name:
                    logging.debug(str(c.name))
                    myQCustomQWidget.setTextUp(str(c.name))
                else:
                    logging.debug(str(c.id))
                    myQCustomQWidget.setTextUp(str(c.id))

                myQCustomQWidget.setTextDown("Created on: " + self.clean_dt(c.raw['creation_time']))
                if c.avatar:
                    #pass
                    local_filename, headers = urllib.request.urlretrieve(c.avatar)
                    myQCustomQWidget.setAvatar_image(local_filename)
                else:
                    lst = str(c.name).split(' ')
                    if len(lst) > 1:
                        myQCustomQWidget.setAvatar_default(lst[0][0] + lst[1][0])
                    else:
                        myQCustomQWidget.setAvatar_default(str(c.name)[0: 2])



                myQCustomQWidget.unsetChBox()

                # Create QListWidgetItem
                myQListWidgetItem = QListWidgetItem(self.listWidget)
                # Set size hint
                myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
                # Add QListWidgetItem into QListWidget
                self.listWidget.addItem(myQListWidgetItem)
                self.listWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)

                self.listWidget.item(0).setSelected(True)
        except Exception as err:
            logging.critical('Contacts lists creation failed: ' + str(err))
            QMessageBox.critical(QWidget(), "Contacts creation failed", str(err))
            exit(1)




    def create_chat_list(self):
        try:
            logging.info('Creating chats list')
            working_dir = str(pathlib.Path(__file__).parent.resolve())
            chats_list = json.load(open(working_dir + "/chats_list.json"))

            # get Recent chats
            logging.debug("Recent chats ")
            rc_chats = self.sk.get_chats()
            if hasattr(rc_chats, 'skype'):
                for chat_id, val in rc_chats.skype.chats.cache.items():
                    if str(chat_id).startswith("19:"):
                        if str(chat_id) not in chats_list["chats_only"]:
                            logging.debug('"' + str(chat_id) + '": "' + str(val.topic) + '"')
                            #chats_list["chats_only"][str(chat_id)] = str(val.topic)


            for chat_id in chats_list["chats_only"].keys():

                chat = self.sk.get_chat(chat_id)

                logging.debug(str(chat_id) + ": " + str(chat.topic))

                self.map_lstID2chat[self.listWidget_2.count()] = chat

                # Create QCustomQWidget
                myQCustomQWidget = QCustomQWidget()
                myQCustomQWidget.setTextUp(str(chat.topic))
                myQCustomQWidget.setTextDown("Creator: " + str(chat.creator.name))
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

        except Exception as err:
            logging.critical('Chats lists creation failed: ' + str(err))
            QMessageBox.critical(QWidget(), "Chats creation failed", str(err))
            exit(1)



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

        self.pushButton_remove.hide()

        working_dir = str(pathlib.Path(__file__).parent.resolve())

        abs_path = os.path.abspath(working_dir + '/ChatManager.log')
        logging.basicConfig(filename=abs_path, encoding='utf-8', level=logging.DEBUG, force=True)

        try:
            self.sk = skype_handler.SkypeHandler()
            self.sk.connect(self.login, self.password)
            logging.debug("Connected")
        except Exception as err:
            logging.critical('Connection Error: ' + str(err))
            QMessageBox.critical(QWidget(), "Connection Error", str(err))
            exit(1)

        try:
            self.skip_contacts = ["0d5d6cff-595d-49d7-9cf8-973173f5233b", "echo123", "concierge"]
            self.create_contacts_list()
            self.create_chat_list()
        except Exception as err:
            logging.critical('Lists creation failed: ' + str(err))
            QMessageBox.critical(QWidget(), "Lists creation failed", str(err))
            exit(1)




    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("DA Skype Manager")
        self.pushButton_add.setText("Add -->")
        self.pushButton_remove.setText("Remove <--X")
