import sys

from check_db import *
import random
from PIL import Image, ImageFilter, ImageEnhance


class AppMain(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('ui/main.ui', self)
        self.initUI()
        self.image_path = None

    def initUI(self):
        self.setWindowTitle('TEST')

        self.btn_load.clicked.connect(self.load_image)
        self.radio1.clicked.connect(self.apply_filter)
        self.radio2.clicked.connect(self.apply_filter)
        self.radio3.clicked.connect(self.apply_filter)
        self.btn_save.clicked.connect(self.save_image)

    def load_image(self):
        self.image_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)'
        )
        if self.image_path:
            self.label.setPixmap(QtGui.QPixmap(self.image_path))

    def apply_filter(self):
        if self.image_path:
            image = Image.open(self.image_path)
            if self.radio1.isChecked():
                image = image.convert('L')
            elif self.radio2.isChecked():
                image = image.filter(ImageFilter.BLUR)
            elif self.radio3.isChecked():
                image = ImageEnhance.Sharpness(image).enhance(2.0)
            image.save('temp.png')
            self.label.setPixmap(QtGui.QPixmap('temp.png'))

    def save_image(self):
        if self.image_path:
            save_path, _ = QtWidgets.QFileDialog.getSaveFileName()
            if save_path:
                Image.open('temp.png').save(save_path + '.png')


class Loading(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Загрузка...')
        self.setFixedSize(800, 600)
        self.label_animation = QtWidgets.QLabel(self)

        self.movie = QtGui.QMovie('img/loader.gif')
        self.label_animation.setMovie(self.movie)

        timer = QtCore.QTimer(self)
        self.startAnimation()
        timer.singleShot(4900 + random.randrange(500), self.stopAnimation)

        self.show()

    def startAnimation(self):
        self.movie.start()

    def stopAnimation(self):
        self.appMain = AppMain()
        self.appMain.show()

        self.movie.stop()
        self.close()


class App(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('ui/vhod.ui', self)

        self.loading_flag = False

        self.initUI()
        self.fio.setFocus()

    def initUI(self):
        self.setWindowTitle('Вход / Регестрация 🔒')
        self.setFixedSize(750, 550)

        self.reg_2.clicked.connect(self.registration)
        self.vhod_2.clicked.connect(self.auth)
        self.check_db = CheckThread(self)
        self.check_db.mysignal.connect(self.on_signal)

    def on_signal(self, text):
        if text == 'Ok':
            self.loading_flag = True
        else:
            self.loading_flag = False

    def registration(self):
        fio = self.fio.text()
        email = self.email.text()
        pas = self.pas.text()
        if not email or not pas or not fio:
            msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Заполните все поля ввода.')
            return
        self.check_db.thr_reg(fio, email, pas)

    def auth(self):
        email = self.email_2.text()
        pas = self.pas_2.text()
        if not email or not pas:
            msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Заполните все поля ввода.')
            return

        self.check_db.thr_login(email, pas)

        if self.loading_flag:
            self.loading = Loading()
            self.loading.show()
            self.close()
        else:
            msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Что-то пошло не так.')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('img/logo.png'))
    ex = App()
    ex.show()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')