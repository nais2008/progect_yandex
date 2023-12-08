import sqlite3
from PyQt5 import uic, QtCore, QtGui, QtWidgets


class Osh(QtWidgets.QWidget):
    def __init__(self, danget_text: str):
        super().__init__()
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi('ui/osh.ui', self)
        self.initUI()

    def initUI(self):
        self.label.setText(self.danget_text)
        self.app = App(self)
        self.pushButton.clicked.connect(self.app)

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


def registr(fio, email, passw, signal):
    con = sqlite3.connect('db/db.sqlite')
    cur = con.cursor()

    cur.execute(f'SELECT * FROM user WHERE email="{email}";')
    value = cur.fetchall()

    if value != []:
        signal.emit('Аккаунт с этим email уже используется')
        print('не зареган')
        osh = Osh('Аккаунт с этим email уже используется')
        osh.show()
    elif value == []:
        cur.execute(f"INSERT INTO user (fio, email, password) VALUES ('{fio}', '{email}', '{passw}')")
        print("Зарегистрирован")
        con.commit()

    cur.close()
    con.close()