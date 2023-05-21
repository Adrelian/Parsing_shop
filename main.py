# Основные библиотеки
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QPushButton

# мои программы
from get_data_from_eplan_excel import take_data_from_excel_eplan

Form, Window = uic.loadUiType("Qtdesigner/design_programm.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()
# Тело программы
def open_file():
    file_path = QFileDialog.getOpenFileName()[0]
    print(file_path)
    return file_path



excel_path = open_file()

a = form.open_button_excel.clicked.connect(open_file)



app.exec()
