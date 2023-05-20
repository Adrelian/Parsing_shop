from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("Моя программа")
        self.setGeometry(400, 400, 600, 600)  # Первые два числа это смещение по X и Y, вторые это размеры окна

        self.main_text = QtWidgets.QLabel(self)
        self.main_text.setText("Это базовый текст")
        self.main_text.move(100, 100)
        self.main_text.adjustSize()

        btn = QtWidgets.QPushButton(self)
        btn.move(70, 150)
        btn.setText("Кнопка")
        btn.setFixedWidth(200)
        btn.clicked.connect(add_label)


def add_label():
    print("add")


def application():
    app = QApplication(sys.argv)  # Запуск программы на компьютере и передаем те настройки, которые связаны именно с
    # этим компьютером
    window = QMainWindow()  # Основное окно программы



    window.show()  # открытие программы
    sys.exit(app.exec_())  # Закрытие программы


application()
