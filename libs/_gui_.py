#!/mnt/e/winProgs/Python/python.exe
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from _sql_functions_ import sqlVerifyUserLogin, sqlAddUserAccount
from _sql_functions_ import *



current_user = None;
rows = None;
class PageWindow(QtWidgets.QMainWindow):
    gotoSignal = QtCore.pyqtSignal(str)
    def goto(self, name):
        self.gotoSignal.emit(name)


class ListWindow(PageWindow):
    def __init__(self):
        super(ListWindow,self).__init__()
        uic.loadUi('UIs/list_page.ui',self)
        self.height = self.geometry().height()
        self.width = self.geometry().width()
        self.scroll_area.setGeometry(QtCore.QRect(5, 5, self.height-10, self.width-10))
        self.scroll_area.setWidgetResizable(True)
        self.pushButton.clicked.connect(self.btn)
    def btn(self):
        global rows
        for r in rows:
            print(r)
            self.pushButton = QtWidgets.QPushButton(self.scroll_area_contents)
            self.pushButton.setText(r[9])
            self.verticalLayout.addWidget(self.pushButton)

class MainMenuWindow(PageWindow):
    def __init__(self):
        super(MainMenuWindow, self).__init__()
        uic.loadUi('UIs/main.ui', self)
        self.height = self.geometry().height()
        self.width = self.geometry().width()
        self.all_actions.clicked.connect(self.all_actions_clicked);
        self.unique_applications.clicked.connect(self.unique_applications_clicked);
    def all_actions_clicked(self):
        global rows
        rows = sqlGetActionsByUser(current_user)
        self.goto("list")
    def unique_applications_clicked(self):
        global rows;
        for row in (sqlGetUniqueApplicationsByUser(current_user)):
            print(row)



class LoginWindow(PageWindow, QtWidgets.QDialog):
    def __init__(self):
        super(LoginWindow, self).__init__()
        uic.loadUi("UIs/login_page.ui", self)
        self.height = self.geometry().height()
        self.width = self.geometry().width()
        self.submit_button.clicked.connect(self.btn_click)
        self.invalid_message.setVisible(False)
        self.password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_entry.returnPressed.connect(self.btn_click)

    def btn_click(self):
        global current_user;
        username = self.username_entry.text()
        password = self.password_entry.text()
        verify_flag = sqlVerifyUserLogin(username, password)
        if verify_flag == 1:#user found
            current_user = username
            self.goto('main_menu')
        else:
            self.invalid_message.setVisible(True)
            self.password_entry.clear()


class WindowStack(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)#init parent attributes
        self.stacked_widget = QtWidgets.QStackedWidget()#stack of widgets
        self.setCentralWidget(self.stacked_widget)
        self.m_pages = {}#dictionary k: window name __ v: widget
        self.register(MainMenuWindow(), "main_menu")#register widgets to the stack
        self.register(LoginWindow(), "login")##
        self.register(ListWindow(), "list")
        self.goto("login")#set the page to start the stack

    def register(self, widget, name):#register a widget to the stack
        self.m_pages[name] = widget#add name:widget to pages dict
        self.stacked_widget.addWidget(widget)#add it to the widget stack
        if isinstance(widget, PageWindow):#if widget is the correct type :: PageWindow
            widget.gotoSignal.connect(self.goto)#override the goto signal of pages

    @QtCore.pyqtSlot(str)
    def goto(self, name):#set a widget as the active page
        if name in self.m_pages:#if the name passed is in the stack
            widget = self.m_pages[name]#get the widget from the pages dict
            self.stacked_widget.setCurrentWidget(widget)#pull it up from the widget stack
            self.resize(widget.height, widget.width)
            self.setWindowTitle(widget.windowTitle())#update the window title to the widgets window title


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = WindowStack()
    w.show()
    sys.exit(app.exec_())