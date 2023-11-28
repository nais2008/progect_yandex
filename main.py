import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QTimer
from des import *
from check_db import *



class App(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/vhod.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Вход / Регестрация 🔒')
        self.setFixedSize(750, 550)

        self.reg_2.clicked.connect(self.registration)
        self.vhod_2.clicked.connect(self.auth)
        self.base_line_edit0 = [self.fio, self.email, self.pas]
        self.base_line_edit1 = [self.email_2, self.pas_2]

    def check_input1(funct):
        def wrapper(self):
            for i in self.base_line_edit0:
                if len(i.text) == 0:
                    return
            funct(self)
        return wrapper

    def check_input2(funct):
        def wrapper(self):
            for i in self.base_line_edit1:
                if len(i.text) == 0:
                    return
            funct(self)
        return wrapper

    @check_input1
    def registration(self):
        self.loading = Loading(self)
        self.loading.show()
        self.close()

    @check_input2
    def auth(self):
        email = self.ui.email_2.text()
        pas = self.ui.pas_2.text()

        self.loading = Loading(self)
        self.loading.show()
        self.close()


class Loading(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('ui/main.ui', self)
        self.initUI()

    def initUI(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle('███░░⏳')

        self.label_animation = QLabel(self)

        self.movie = QMovie('logo/loader.gif')
        self.label_animation.setMovie(self.movie)

        timer = QTimer(self)
        self.startAnimation()
        timer.singleShot(10000, self.stopAnimation)

        self.show()

    def startAnimation(self):
        self.movie.start()

    def stopAnimation(self):
        self.movie.stop()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    widget = QWidget()
    ex.show()
    sys.exit(app.exec())