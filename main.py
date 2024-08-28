import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget, QPushButton, QDialog, QDialogButtonBox
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtGui import QColor, QBrush, QPixmap, QIcon
from Design.first import Ui_MainWindow
from Design.register import Ui_Form_register
from Design.sign_in import Ui_Form_SignIn
from Design.user import Ui_Form_User
from Design.show_message import Ui_Form_show
from Design.sent import Ui_Form_sent
from Design.edit_message import Ui_Form_edit
from Design.write_message import Ui_Form_write
from Design.info import Ui_Form_info


class WriteMessage(QWidget, Ui_Form_write):
    def __init__(self, username, userid):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Write Message')
        self.setFixedSize(807, 540)
        self.con = sqlite3.connect('mail_server.sqlite')
        cur = self.con.cursor()
        self.q1 = cur.execute('SELECT * from Messages').fetchall()

        self.MessageEdit.setPlaceholderText('Write something...')
        self.MessageEdit.setPlainText('')
        self.FinishButton.clicked.connect(self.fin)

        self.ErrorLabel.setStyleSheet("color: red; background-color: None")
        self.ErrorLabel.setText('*')

        self.ErrorLabel_3.setStyleSheet("color: red; background-color: None")
        self.ErrorLabel_3.setText('*')

        self.ErrorLabel_4.setStyleSheet("color: red; background-color: None")
        self.ErrorLabel_4.setText('*')

        self.DeleteButton.clicked.connect(self.close)

        self.ToEdit.textChanged.connect(self.chk)
        self.HeaderEdit.textChanged.connect(self.chk1)
        self.MessageEdit.textChanged.connect(self.chk2)

        self.ErrorLabel_2.setStyleSheet("color: red; background-color: None")
        self.ErrorLabel_2.setText('* - required fields')

        self.username = username
        self.userid = userid

        self.UserName.setText(self.username)

    def chk(self):
        cur = self.con.cursor()
        le = cur.execute("select login from Users").fetchall()
        if self.ToEdit.text() != "":
            if (self.ToEdit.text(),) in le:
                self.ErrorLabel.setStyleSheet("color: green; background-color: None")
                self.ErrorLabel.setText('OK')
            else:
                self.ErrorLabel.setStyleSheet("color: red; background-color: None")
                self.ErrorLabel.setText("Wrong username")
        else:
            self.ErrorLabel.setStyleSheet('background-color: None; color: red')
            self.ErrorLabel.setText("*")

    def chk1(self):
        if self.HeaderEdit.text() == "":
            self.ErrorLabel_4.setStyleSheet('background-color: None; color: red')
            self.ErrorLabel_4.setText("*")
        else:
            self.ErrorLabel_4.setText("")

    def chk2(self):
        if self.MessageEdit.toPlainText() == "":
            self.ErrorLabel_3.setStyleSheet('background-color: None; color: red')
            self.ErrorLabel_3.setText("*")
        else:
            self.ErrorLabel_3.setText("")

    def fin(self):
        if self.ErrorLabel.text() == 'OK' and '*' not in [self.ErrorLabel_4.text(), self.ErrorLabel_3.text()]:
            cur = self.con.cursor()
            le = cur.execute(f"select id from Users where login = '{self.ToEdit.text()}'").fetchone()[0]
            self.diaa = DialogSend(self.userid, le, self.HeaderEdit.text(), self.MessageEdit.toPlainText())
            self.diaa.show()
            self.diaa.finished.connect(self.fina)

    def fina(self):
        cur = self.con.cursor()
        q2 = cur.execute('SELECT * from Messages').fetchall()
        if self.q1 != q2:
            self.con.close()
            self.close()


class DialogDel(QDialog):
    def __init__(self, id):
        super().__init__()
        QBtn = QDialogButtonBox.Yes | QDialogButtonBox.No

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.reject)

        self.setWindowTitle('Are you sure?')

        self.layout = QVBoxLayout()
        message = QLabel("Are you sure you want to DELETE the message?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.id = id

    def ok(self):
        self.con = sqlite3.connect('mail_server.sqlite')
        cur = self.con.cursor()
        cur.execute(f"""DELETE from Messages WHERE id = {self.id}""")
        self.con.commit()
        self.con.close()
        self.close()


class DialogEdit(QDialog):
    def __init__(self, id, header, messag):
        super().__init__()
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.reject)

        self.setWindowTitle('Are you sure?')

        self.layout = QVBoxLayout()
        message = QLabel("Are you sure you want to EDIT the message?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.id = id
        self.header = header
        self.message = messag

    def ok(self):
        self.con = sqlite3.connect('mail_server.sqlite')
        cur = self.con.cursor()
        cur.execute(f"""UPDATE Messages 
                        SET header = '{self.header}', message = '{self.message}', time = datetime('now', '+3 hours') 
                        WHERE id = {self.id}""")
        self.con.commit()
        self.con.close()
        self.close()


class DialogSend(QDialog):
    def __init__(self, id, id2, header, messag):
        super().__init__()
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.reject)

        self.setWindowTitle('Are you sure?')

        self.layout = QVBoxLayout()
        message = QLabel("Are you sure you want to SEND the message?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.id = id
        self.id2 = id2
        self.header = header
        self.message = messag

    def ok(self):
        self.con = sqlite3.connect('mail_server.sqlite')
        cur = self.con.cursor()
        le = cur.execute("select * from Messages").fetchall()
        cur.execute(f"""INSERT INTO Messages (id, sender, receiver, header, message, time) 
                    VALUES (
                    {len(le) + 1}, 
                    {self.id},
                    {self.id2},
                    "{self.header}", 
                    "{self.message}",
                    datetime('now', '+3 hours'))""")
        self.con.commit()
        self.con.close()
        self.close()


class EditMessage(QWidget, Ui_Form_edit):
    def __init__(self, username, id, receiver, header, message, time):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Edit Message')
        self.setFixedSize(807, 540)

        self.BackButton.clicked.connect(self.close)

        self.con = sqlite3.connect('mail_server.sqlite')
        cur = self.con.cursor()
        self.q1 = cur.execute('SELECT * from Messages').fetchall()

        self.username = username
        self.id = id
        self.receiver = receiver
        self.header = header
        self.message = message

        self.UserName.setText(self.username)
        self.FromLabel.setText(self.username)
        self.ToLabel.setText(self.receiver)
        self.HeaderEdit.setText(self.header)
        self.MessageEdit.setPlainText(self.message.replace('\\n', '\n'))

        self.DeleteButton.clicked.connect(self.delete)
        self.FinishButton.clicked.connect(self.edit)

        self.TimeLabel.setText(time)

    def delete(self):
        self.dia = DialogDel(self.id)
        self.dia.show()
        self.dia.finished.connect(self.fin)

    def edit(self):
        self.diaa = DialogEdit(self.id, self.HeaderEdit.text(), self.MessageEdit.toPlainText())
        self.diaa.show()
        self.diaa.finished.connect(self.fin)

    def fin(self):
        cur = self.con.cursor()
        q2 = cur.execute('SELECT * from Messages').fetchall()
        if self.q1 != q2:
            self.q1 = q2
            self.close()


class SentMessages(QWidget, Ui_Form_sent):
    def __init__(self, username):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Sent Messages')
        self.setFixedSize(807, 540)

        self.username = username

        self.WriteButton.clicked.connect(self.close)

        self.UserName.setText(self.username)

        self.con = sqlite3.connect('mail_server.sqlite')
        cur = self.con.cursor()

        self.headers = ['Receiver', 'Title', 'Message', 'Edit', 'time']

        self.tableWidget.setColumnCount(5)

        self.tableWidget.setRowCount(0)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.tableWidget.setHorizontalHeaderLabels(self.headers)

        self.userid = cur.execute(f"""SELECT id 
                                             FROM Users
                                             WHERE login = 
                                             '{self.username}'""").fetchone()[0]

        res = cur.execute(f"""SELECT receiver, 
                                            header, 
                                            message,
                                            time,
                                            id
                                            FROM Messages
                                     WHERE sender = 
                                     {self.userid}""").fetchall()

        self.res1 = []
        self.buts = []
        self.buts2 = []

        font = QtGui.QFont()
        font.setFamily("Rockwell")

        for i in res:
            self.but = QPushButton('Show Message', self)
            self.but.setStyleSheet("""background-color: 
                                          qradialgradient(spread:repeat, cx:0.5, cy:0.5, 
                                          radius:0.077, fx:0.5, fy:0.5, stop:0 rgba(255, 
                                          255, 255, 255), stop:0.497326 rgba(190, 190, 190, 255), 
                                          stop:1 rgba(255, 255, 255, 255)); color: rgb(100, 0, 0)""")

            self.but2 = QPushButton('Edit', self)
            self.but2.setStyleSheet("""background-color: 
                                            qradialgradient(spread:repeat, cx:0.5, cy:0.5, 
                                            radius:0.077, fx:0.5, fy:0.5, stop:0 rgba(255, 
                                            255, 255, 255), stop:0.497326 rgba(190, 190, 190, 255), 
                                            stop:1 rgba(255, 255, 255, 255)); color: rgb(100, 0, 0)""")

            receiver = cur.execute(f"""SELECT login FROM Users WHERE id = {i[0]}""").fetchone()[0]

            font.setPointSize(11)
            self.but.setFont(font)
            self.but2.setFont(font)

            self.p = ShowMessage(self.username, i[1], i[2], receiver, i[3][0:16])
            self.p2 = EditMessage(self.username, i[4], receiver, i[1], i[2], i[3][0:16])

            self.buts.append(self.p)
            self.buts2.append(self.p2)

            self.but.clicked.connect(self.p.show)
            self.but2.clicked.connect(self.p2.show)

            kkk = (receiver, i[1], self.but, self.but2, i[3][0:16])
            self.res1.append(kkk)

        for i, row in enumerate(reversed(self.res1)):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)

            for j, elem in enumerate(row):
                if j != 2 and j != 3:
                    xx = QTableWidgetItem(elem)
                    font.setPointSize(11)
                    xx.setFont(font)
                    xx.setBackground(QBrush(QColor(220, 220, 220, 255)))

                    self.tableWidget.setItem(
                        i, j, xx)
                else:
                    self.tableWidget.setCellWidget(
                        i, j, elem
                    )

        self.tableWidget.resizeColumnsToContents()

        self.tableWidget.resizeRowsToContents()

    def show_message(self):
        pass


class ShowMessage(QWidget, Ui_Form_show):
    def __init__(self, sender, header, message, username, time):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Show Message')
        self.setFixedSize(807, 540)
        self.sender = sender

        self.header = header

        self.message = message

        self.username = username

        self.time = time

        self.TimeLabel.setText(self.time)
        self.label_3.setText(self.header)
        self.UserName.setText(self.username)
        self.plainTextEdit.setPlainText(self.message.replace('\\n', '\n'))
        self.FromLabel.setText(self.sender)
        self.ToLabel.setText(self.username)

        self.BackButton.clicked.connect(self.close)


class UserWindow(QWidget, Ui_Form_User):
    def __init__(self, username):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(f'{username} page')
        self.setFixedSize(807, 540)

        self.LogOutButton.clicked.connect(self.close)

        self.username = username

        self.UserName.setText(self.username)

        self.con = sqlite3.connect('mail_server.sqlite')
        cur = self.con.cursor()

        self.headers = ['Sender', 'Title', 'Message', 'time']

        self.tableWidget.setColumnCount(4)

        self.tableWidget.setRowCount(0)

        self.UpdateButton.setIcon(QIcon('files/update.png'))
        self.UpdateButton.setIconSize(QSize(41, 41))
        self.UpdateButton.clicked.connect(self.upd)

        self.WriteButton.clicked.connect(self.write)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.tableWidget.setHorizontalHeaderLabels(self.headers)

        self.userid = cur.execute(f"""SELECT id 
                                     FROM Users
                                     WHERE login = 
                                     '{self.username}'""").fetchone()[0]

        res = cur.execute(f"""SELECT sender, 
                                    header, 
                                    message,
                                    time
                                    FROM Messages
                             WHERE receiver = 
                             {self.userid}""").fetchall()

        self.res1 = []

        self.buts = []

        font = QtGui.QFont()
        font.setFamily("Rockwell")

        for i in res:
            self.but = QPushButton('Show Message', self)
            self.but.setStyleSheet("""background-color: 
                                      qradialgradient(spread:repeat, cx:0.5, cy:0.5, 
                                      radius:0.077, fx:0.5, fy:0.5, stop:0 rgba(255, 
                                      255, 255, 255), stop:0.497326 rgba(190, 190, 190, 255), 
                                      stop:1 rgba(255, 255, 255, 255)); color: rgb(100, 0, 0)""")

            font.setPointSize(11)
            self.but.setFont(font)

            sender = cur.execute(f"""SELECT login FROM Users WHERE id = {i[0]}""").fetchone()[0]

            self.p = ShowMessage(sender, i[1], i[2], self.username, i[3][0:16])
            self.buts.append(self.p)
            self.but.clicked.connect(self.p.show)

            kkk = (sender, i[1], self.but, i[3][0:16])
            self.res1.append(kkk)

        for i, row in enumerate(reversed(self.res1)):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)

            for j, elem in enumerate(row):

                if j != 2:
                    xx = QTableWidgetItem(elem)
                    font.setPointSize(11)
                    xx.setFont(font)
                    xx.setBackground(QBrush(QColor(220, 220, 220, 255)))

                    self.tableWidget.setItem(
                        i, j, xx)
                else:
                    self.tableWidget.setCellWidget(
                        i, j, elem
                    )

        self.tableWidget.resizeColumnsToContents()

        self.tableWidget.resizeRowsToContents()

        self.SentButton.clicked.connect(self.sent)

    def show_message(self):
        pass

    def sent(self):
        self.sss = SentMessages(self.username)
        self.sss.show()

    def upd(self):
        cur = self.con.cursor()
        res = cur.execute(f"""SELECT sender, 
                                            header, 
                                            message,
                                            time
                                            FROM Messages
                                     WHERE receiver = 
                                     {self.userid}""").fetchall()

        self.res1 = []

        self.buts = []

        font = QtGui.QFont()
        font.setFamily("Rockwell")

        for i in res:
            self.tableWidget.setRowCount(0)
            self.but = QPushButton('Show Message', self)
            self.but.setStyleSheet("""background-color: 
                                              qradialgradient(spread:repeat, cx:0.5, cy:0.5, 
                                              radius:0.077, fx:0.5, fy:0.5, stop:0 rgba(255, 
                                              255, 255, 255), stop:0.497326 rgba(190, 190, 190, 255), 
                                              stop:1 rgba(255, 255, 255, 255)); color: rgb(100, 0, 0)""")

            font.setPointSize(11)
            self.but.setFont(font)

            sender = cur.execute(f"""SELECT login FROM Users WHERE id = {i[0]}""").fetchone()[0]

            self.p = ShowMessage(sender, i[1], i[2], self.username, i[3][0:16])
            self.buts.append(self.p)
            self.but.clicked.connect(self.p.show)

            kkk = (sender, i[1], self.but, i[3][0:16])
            self.res1.append(kkk)

        for i, row in enumerate(reversed(self.res1)):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)

            for j, elem in enumerate(row):

                if j != 2:
                    xx = QTableWidgetItem(elem)
                    font.setPointSize(11)
                    xx.setFont(font)
                    xx.setBackground(QBrush(QColor(220, 220, 220, 255)))

                    self.tableWidget.setItem(
                        i, j, xx)
                else:
                    self.tableWidget.setCellWidget(
                        i, j, elem
                    )
        self.tableWidget.update()

    def write(self):
        self.wr = WriteMessage(self.username, self.userid)
        self.wr.show()


class RegisterWindow(QWidget, Ui_Form_register):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Registration')
        self.setFixedSize(496, 481)
        self.pushButton.clicked.connect(self.reg)
        self.login.textChanged.connect(self.chk)
        self.con = sqlite3.connect('mail_server.sqlite')

    def sdfs(self):
        pass

    def chk(self):
        cur = self.con.cursor()
        le = cur.execute("select login from Users").fetchall()
        if self.login.text() != "":
            if (self.login.text(),) in le:
                self.CheckLabel.setStyleSheet("color: red; background-color: None")
                self.CheckLabel.setText('This login already exists')
            else:
                self.CheckLabel.setStyleSheet("color: green; background-color: None")
                self.CheckLabel.setText('OK')
        else:
            self.CheckLabel.setStyleSheet('background-color: None')
            self.CheckLabel.setText("")

    def reg(self):
        cur = self.con.cursor()
        if self.CheckLabel.text() == 'OK':
            le = cur.execute("select * from Users").fetchall()
            cur.execute(f"""INSERT INTO Users (id, login, password) 
            VALUES (
            {len(le) + 1}, 
            "{self.login.text()}", 
            "{self.password.text()}")""")
            self.close()
            self.con.commit()
            self.con.close()


class SignInWindow(QWidget, Ui_Form_SignIn):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Sign In')
        self.setFixedSize(496, 481)
        self.con = sqlite3.connect('mail_server.sqlite')
        self.pushButton.clicked.connect(self.run)

    def run(self):
        cur = self.con.cursor()
        res = cur.execute(f"""SELECT login, 
                             password FROM Users
                             WHERE login = "{self.login.text()}" 
                             and password = '{self.password.text()}'""").fetchone()
        if not res:
            self.error_label.setStyleSheet("color: red; background-color: None")
            self.error_label.setText("Incorrect login or password")
        else:
            self.close()
            self.userwindow = UserWindow(self.login.text())
            self.userwindow.show()


class InfoWindow(QWidget, Ui_Form_info):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Info')
        self.setFixedSize(807, 540)
        self.tx = open('files/info.txt', 'r', encoding='utf-8')
        self.t = "".join(self.tx.readlines())
        self.plainTextEdit.setPlainText(self.t)
        self.BackButton.clicked.connect(self.close)
        self.label2 = QLabel(self)
        self.pixmap = QPixmap('files/mail.jpg')
        self.pixmap = self.pixmap.scaled(307, 204)
        self.label2.setPixmap(self.pixmap)
        self.label2.move(30, 90)
        self.label2.resize(307, 204)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Nikita Mail v0.0.1')
        self.RegisterButton.clicked.connect(self.open_register)
        self.SignButton.clicked.connect(self.open_signin)
        self.SignButton_2.clicked.connect(self.info)
        self.serv = []
        self.setFixedSize(807, 540)

    def open_register(self):
        self.win = RegisterWindow()
        self.win.show()

    def open_signin(self):
        self.op = SignInWindow()
        self.op.show()
        self.serv.append(self.op)

    def info(self):
        self.inf = InfoWindow()
        self.inf.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
