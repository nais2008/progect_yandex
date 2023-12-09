from PyQt5 import QtCore, QtWidgets, QtGui, uic
from db.db_handler import Osh, login, registr


class CheckThread(QtWidgets.QWidget):
    mysignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(CheckThread, self).__init__(parent)
        self.parent = parent

    def thr_login(self, email, passw):
        login(email, passw, self.mysignal)

    def thr_reg(self, fio, email, passw):
        registr(self.parent, fio, email, passw, self.mysignal)