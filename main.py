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
    :return: Словарь с данными об изделиях
    """
    file_path = QFileDialog.getOpenFileName(None, "Выберите файл", "",
                                            "Excel Files (*.xlsx *.xls)")[0]  # Получить только первый выбранный файл
    data_excel = take_data_from_excel_eplan(file_path)
    for key, value in data_excel.items():
        form.text_info_excel.insertPlainText("Артикул: " + key + "\n")
        for sub_key, sub_value in value.items():
            if sub_value:
                form.text_info_excel.insertPlainText(sub_key + ": " + sub_value + "\n")
        form.text_info_excel.insertPlainText("----------------------------------------------------" + "\n")
    print(data_excel)
    return data_excel


def parsing(list_order):
    from find_article_from_site import take_unique_id_from_site
    id_etm = take_unique_id_from_site()  # Уникальный ID  сайта ETM
    from find_article_from_site import get_data_from_etm
    data_from_etm = get_data_from_etm(list_order, id_etm)  # Получить данные по спецификации с сайта ETM
    print(data_from_etm)


data_from_excel = form.open_button_excel.clicked.connect(open_file)  # Вывести спецификацию в программу
form.parsing_button_excel.clicked.connect(parsing(data_from_excel))

app.exec_()
