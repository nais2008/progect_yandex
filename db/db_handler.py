import sqlite3
from PyQt5 import uic, QtCore, QtGui, QtWidgets


class Osh(QtWidgets.QDialog):
    def __init__(self, danget_text: str):
        super().__init__()
        uic.loadUi('ui/osh.ui', self)

        self.pushButton.clicked.connect(self.close)
        self.danget_text = danget_text

        self.initUI()

    def initUI(self):
        self.label.setText(self.danget_text)


def login(email, passw, signal):
    con = sqlite3.connect('db/db.sqlite')
    cur = con.cursor()

    # Проверка на существование аккаунта
    cur.execute(f'SELECT * FROM user WHERE email="{email}";')
    value = cur.fetchall()

    if value != [] and value[0][3] == passw:
        signal.emit('Ok')
        print('Авторизован')
    else:
        signal.emit('Неправильно введет логин или пароль')
        print('не авторизован')

    cur.close()
    con.close()


def registr(_self, fio, email, passw, signal):
    con = sqlite3.connect('db/db.sqlite')
    cur = con.cursor()

    cur.execute(f'SELECT * FROM user WHERE email="{email}";')
    value = cur.fetchall()

    if value:
        _self.osh = Osh('Аккаунт с этим email уже используется')
        _self.osh.exec()

    else:
        cur.execute(f"INSERT INTO user (fio, email, password) VALUES ('{fio}', '{email}', '{passw}')")
        print(f"Зарегистрирован: {_self.fio.text()}")
        _self.fio.clear()
        _self.email.clear()
        _self.pas.clear()
        _self.email_2.setFocus()

        con.commit()

    cur.close()
    con.close()