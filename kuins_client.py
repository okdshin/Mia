import sys
import subprocess
import json
from PyQt4 import QtGui
from PyQt4 import QtCore

class KuinsClient(QtGui.QWidget):
    def __init__(self):
        super(KuinsClient, self).__init__()

        self.is_connected = False
        self.setWindowTitle('Miako Connection Client')

        self.prompt_label = QtGui.QLabel('', self)
        
        self.username_label = QtGui.QLabel('username', self)
        self.username_le = QtGui.QLineEdit('', self)
        self.username_hbox = QtGui.QHBoxLayout()
        self.username_hbox.addWidget(self.username_label)
        self.username_hbox.addWidget(self.username_le)
        
        self.password_label = QtGui.QLabel('password', self)
        self.password_le = QtGui.QLineEdit('', self)
        self.password_le.setEchoMode(QtGui.QLineEdit.Password)
        self.password_hbox = QtGui.QHBoxLayout()
        self.password_hbox.addWidget(self.password_label)
        self.password_hbox.addWidget(self.password_le)
        
        self.ok_button = QtGui.QPushButton("OK Let's connect ;)", self)
        self.ok_button.clicked.connect(self.connect)

        self.main_vbox = QtGui.QVBoxLayout()
        self.main_vbox.addWidget(self.prompt_label)
        self.main_vbox.addLayout(self.username_hbox)
        self.main_vbox.addLayout(self.password_hbox)
        self.main_vbox.addWidget(self.ok_button)

        self.tray_icon = QtGui.QSystemTrayIcon(QtGui.QIcon('icon_016.png'), self)
        menu = QtGui.QMenu()
        menu.addAction("hello");
        self.tray_icon.setContextMenu(menu)
        if QtGui.QSystemTrayIcon.supportsMessages():
            self.tray_icon.show()
        
        self.setLayout(self.main_vbox)
        self.show()

        self.tray_icon.showMessage(self.tr('miako'), self.tr('connected'))

        try:
            info_file = open('info.dat', 'r')
            info_dict = json.load(info_file)
            self.username_le.setText(info_dict['username'])
            self.password_le.setText(info_dict['password'])
            self.connect()
            return
        except:
            pass

    def __del__(self):
        if not self.is_connected:
            return
        subprocess.call(['rasdial', 'kuins', '/disconnect'])

    def connect(self):
        self.is_connected = True
        if self.username_le.text() == '':
            self.prompt_label.setText('please put user name.')
            return;
        if self.password_le.text() == '':
            self.prompt_label.setText('please put password.')
            return;
        
        retcode = subprocess.call(['rasdial', 'kuins',
                str(self.username_le.text()), str(self.password_le.text()),'/phonebook:kuins.pbk'])  
        if retcode != 0:
            self.prompt_label.setText('connect failed. invalid username or password.')
            return
        info_dict = {}
        info_dict['username'] = str(self.username_le.text())
        info_dict['password'] = str(self.password_le.text())
        info_file = open('info.dat', 'w')
        json.dump(info_dict, info_file)
        info_file.close()
            
def main():
    app = QtGui.QApplication(sys.argv)
    client = KuinsClient()

    app.exec_()

if __name__ == '__main__':
    main()
