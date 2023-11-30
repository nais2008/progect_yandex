import sys
from check_db import *


class App(QtWidgets.QMainWindow, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('ui/vhod.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Вход / Регестрация 🔒')
        self.setFixedSize(750, 550)

        self.reg_2.clicked.connect(self.registration)
        self.vhod_2.clicked.connect(self.auth)

        self.check_db = CheckThread()

    # Обработчик сигнала
    def signal_handler(self, value):
        QtWidgets.QMessageBox.about(self, 'Оповещение', value)

    def registration(self):
        fio = self.fio.text()
        email = self.email.text()
        pas = self.pas.text()
        self.check_db.thr_reg(fio, email, pas)

    def auth(self):
        email = self.email_2.text()
        pas = self.pas_2.text()
        self.check_db.thr_login(email, pas)

        self.loading = Loading(self)
        self.loading.show()
        # self.close()


class Loading(QtWidgets.QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('ui/main.ui', self)
        self.initUI()

    def initUI(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle('███░░⏳')

        self.label_animation = QtWidgets.QLabel(self)

        self.movie = QtGui.QMovie('logo/loader.gif')
        self.label_animation.setMovie(self.movie)

        timer = QtCore.QTimer(self)
        self.startAnimation()
        timer.singleShot(5000, self.stopAnimation)

        self.show()

    def startAnimation(self):
        self.movie.start()

    def stopAnimation(self):
        self.movie.stop()
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('logo/logo.png'))
    ex = App()
    widget = QtWidgets.QWidget()
    ex.show()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')