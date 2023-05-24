# Основные библиотеки
import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog
# мои программы

from get_data_from_eplan_excel import take_data_from_excel_eplan
from find_article_from_site import *

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
    Функция открывает файл Excel со спецификацией, и результат записывает в JSON (temp)
    :return: Словарь с данными об изделиях
    """
    file_path = QFileDialog.getOpenFileName(None, "Выберите файл", "",
                                            "Excel Files (*.xlsx *.xls)")[0]  # Получить только первый выбранный файл
    data_excel = take_data_from_excel_eplan(file_path)  # Данные из Excel файла
    # Вывод на печать
    for key, value in data_excel.items():
        form.text_info_excel.insertPlainText("Артикул: " + key + "\n")
        for sub_key, sub_value in value.items():
            if sub_value:
                form.text_info_excel.insertPlainText(sub_key + ": " + sub_value + "\n")
        form.text_info_excel.insertPlainText("----------------------------------------------------" + "\n")
    # Создаем директорию для временных файлов
    try:
        os.mkdir("Temp")
    except:
        form.text_info_excel.insertPlainText("Системная ошибка: Не могу создать временную папку")
    # Результат сбора данных из Excel записываем во временную переменную
    try:
        with open("Temp/excel.json", "w", encoding='utf-8') as file:
            json.dump(data_excel, file, ensure_ascii=False, indent=4)
    except:
        form.text_info_excel.insertPlainText("Системная ошибка: Не могу создать временный файл со спецификацией")


def parsing():
    try:
        id_etm = take_unique_id_from_site()  # Уникальный ID  сайта ETM
    except:
        form.text_info_excel.insertPlainText("Системная ошибка: Нет доступа к сайту ETM")

    try:
        with open("Temp/excel.json") as data:
            data = json.load(data)
    except FileNotFoundError:
        form.text_info_excel.insertPlainText("Системная ошибка: Нет временного файла")
    print(id_etm)
    data_from_etm = get_data_from_etm(data, id_etm)  # Получить данные по спецификации с сайта ETM
    # print(data_from_etm)


form.open_button_excel.clicked.connect(open_file)  # Вывести спецификацию в программу

form.parsing_button_excel.clicked.connect(parsing)

app.exec_()
