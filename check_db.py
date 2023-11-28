from PyQt5 import uic, QtCore, QtGui, QtWidgets
from db.db_handler import *


class CheckThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)

    def thr_login(self, email, passw):
        login(email, passw, self.mysignal)

    def thr_reg(self, fio, email, passw):
        registr(fio, email, passw, self.mysignal)