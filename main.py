import sys
import skype_handler
import urllib.request
import MainWindow
import sign_in
import json
import time

from PyQt5.QtWidgets import QApplication,QMainWindow, QWidget, QCheckBox,\
    QLabel, QVBoxLayout, QListWidget, QHBoxLayout, QListWidgetItem
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets

from MainWindow import Ui_MainWindow


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
        self.iconQLabel.setPixmap(QPixmap(imagePath))

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



class Ui_Dialog(object):
    def openWindow(self):

        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        Dialog.close()
        self.window.show()

    def setupUi(self,Dialog):
        Dialog.setObjectName("Dialog_SignIn")
        Dialog.resize(220, 136)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 100, 191, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 211, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_login = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_login.setObjectName("label_login")
        self.horizontalLayout.addWidget(self.label_login)
        spacerItem = QtWidgets.QSpacerItem(33, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_password = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_password.setObjectName("label_password")
        self.horizontalLayout_2.addWidget(self.label_password)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.openWindow)
        self.buttonBox.rejected.connect(QtCore.QCoreApplication.instance().quit)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog_SignIn", "Sign-In"))
        self.label_login.setText(_translate("Dialog_SignIn", "Login:"))
        self.label_password.setText(_translate("Dialog_SignIn", "Password:"))




if __name__ == '__main__':


    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = sign_in.Ui_Dialog_SignIn()
    ui.setupUi(Dialog)
    Dialog.show()

    sys.exit(app.exec_())


    #window = exampleQMainWindow()


