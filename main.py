import sys
import sign_in

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import logging

if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        Dialog = QtWidgets.QDialog()
        ui = sign_in.Ui_Dialog_SignIn()
        ui.setupUi(Dialog)
        Dialog.show()

        sys.exit(app.exec_())
    except Exception as err:
        logging.error(str(err))
        #QMessageBox.critical(QWidget(), "Error", str(err))
        exit(1)
