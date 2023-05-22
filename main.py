# Основные библиотеки
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog

# мои программы
from get_data_from_eplan_excel import take_data_from_excel_eplan

Form, Window = uic.loadUiType("Qtdesigner/design_programm.ui")

app = QApplication(sys.argv)
window = Window()
window.setFixedSize(640, 480)  # Блокируем изменение размера окна
form = Form()
form.setupUi(window)
window.show()


# Тело программы
def open_file():
    """
    Функция открывает файл Excel со спецификацией
    :return: Путь к файлу в виде строки
    """
    file_path = QFileDialog.getOpenFileName(None, "Выберите файл", "",
                                            "Excel Files (*.xlsx *.xls)")[0]  # Получить только первый выбранный файл
    data_excel = take_data_from_excel_eplan(file_path)
    for key, value in data_excel.items():
        form.text_info_excel.insertPlainText(key, ":", value + "\n")
    print("Без ошибок")
    return file_path


form.open_button_excel.clicked.connect(open_file)


app.exec_()
