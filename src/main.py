from PyQt5 import uic
from PyQt5.QtWidgets import *
from Crypto.PublicKey import RSA, DSA
from Crypto.Util import Counter
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

import crypto
from controller import *


class UiWindow(QMainWindow):
    def __init__(self):
        super(UiWindow, self).__init__()
        uic.loadUi('interface.ui', self)
        self.privateButton = self.findChild(QToolButton, 'privateButton')
        self.publicButton = self.findChild(QToolButton, 'publicButton')
        self.encryptButton = self.findChild(QPushButton, 'encryptButton')
        self.decryptButton = self.findChild(QPushButton, 'decryptButton')
        self.genButton = self.findChild(QPushButton, 'genButton')

        self.privatePath = self.findChild(QLineEdit, 'privatePath')
        self.publicPath = self.findChild(QLineEdit, 'publicPath')

        self.encModeBox = self.findChild(QComboBox, 'encModeBox')
        self.password = self.findChild(QLineEdit, 'password')
        self.genPass = self.findChild(QLineEdit, 'genPass')

        self.privateButton.clicked.connect(self.choosePrivateKeyFile)
        self.publicButton.clicked.connect(self.choosePublicKeyFile)
        self.encryptButton.clicked.connect(self.encrypt)
        self.decryptButton.clicked.connect(self.decrypt)
        self.genButton.clicked.connect(self.genKeys)

        self.show()

        self.controller = Controller()

    def showPopup(self, text, icon=QMessageBox.Critical):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setText(text)
        msg.exec()

    def choosePrivateKeyFile(self):
        self.privatePath.setText(QFileDialog.getOpenFileName(self, 'Podaj ścieżkę do klucza prywatnego')[0])

    def choosePublicKeyFile(self):
        self.publicPath.setText(QFileDialog.getOpenFileName(self, 'Podaj ścieżkę do klucza publicznego')[0])

    def genKeys(self):
        self.publicPath.setText(QFileDialog.getSaveFileName(self, 'Zapisz klucz publiczny')[0])
        self.privatePath.setText(QFileDialog.getSaveFileName(self, 'Zapisz klucz prywatny')[0])
        self.password.setText(self.genPass.text())
        if self.controller.generate_keys(self.publicPath.text(), self.privatePath.text(), self.password.text()):
            self.showPopup('Wygenerowano pomyślnie', QMessageBox.Information)
        else:
            self.showPopup('Podaj poprawne ścieżki do zapisu wygenerowanych kluczy')
            self.publicPath.setText('')
            self.privatePath.setText('')
            self.password.setText('')

    def encrypt(self):
        if self.controller.load_public(self.publicPath.text()) is None:
            return self.showPopup('Zła ścieżka pliku z kluczem')

        inputPath = Path(QFileDialog.getOpenFileName(self, 'Wybierz plik')[0])
        if inputPath.is_file():
            if self.controller.encrypt(self.encModeBox.currentText(), str(inputPath), QFileDialog.getSaveFileName(self, 'Zapisz zaszyfrowany plik')[0]):
                self.showPopup('Zaszyfrowano pomyślnie', QMessageBox.Information)
        else:
            self.showPopup('Zła ścieżka pliku do szyfrowania')

    def decrypt(self):
        try:
            if self.controller.load_private(self.privatePath.text(), self.password.text()) is None:
                return self.showPopup('Zła ścieżka pliku z kluczem')
        except:
            return self.showPopup('Błąd odczytu klucza')

        inputPath = Path(QFileDialog.getOpenFileName(self, 'Wybierz plik')[0])
        if inputPath.is_file():
            try:
                if self.controller.decrypt(str(inputPath), QFileDialog.getSaveFileName(self, 'Zapisz odszyfrowany plik')[0]):
                    self.showPopup('Odszyfrowano pomyślnie', QMessageBox.Information)
            except:
                return self.showPopup('Błędny format pliku')
        else:
            self.showPopup('Zła ścieżka pliku do odszyfrowania')


app = QApplication([])
window = UiWindow()
app.exec_()
