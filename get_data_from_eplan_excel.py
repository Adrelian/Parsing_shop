import json
import xlrd

excel_file = 'C:/Games/python/Parsing_Shop/Example/Спецификация Электрика.xls'
data_from_eplan_to_json = "Example/data_goods_Eplan_Excel.json"


def take_data_from_excel_eplan(adress_file_excel):
    """
    Функция собирает данные из файла Excel Eplan. И сохраняет полученные данные в json
    :param adress_file_excel: Адрес файла Excel со спецификацией
    :return: словарь с данными об изделиях
    """
    try:
        excel_data = xlrd.open_workbook(adress_file_excel)  # Открыть файл
        page = excel_data.sheet_by_index(0)  # Открыть первый лист

        with open("C:/Games/python/Parsing_Shop/Example/data_goods_from_eplan_excel.json", 'w', encoding='utf-8') as data_file:
            data_unit = {}  # Пустой словарь для сбора данных об изделиях

            for column in range(3, page.nrows):
                # Номер для заказа
                article = page.cell_value(column, 1)
                # Производитель
                manufacturer = page.cell_value(column, 2)
                # Тип изделия
                number_type = page.cell_value(column, 3)
                # Кол-во изделий
                quantity = page.cell_value(column, 4)
                # Описание изделий
                description_item = page.cell_value(column, 5)
                # Создание словаря
                data_unit[article] = dict(name=description_item,
                                          order_type=number_type,
                                          name_manufacturer=manufacturer,
                                          price_retail="",
                                          price_max_discount="",
                                          quantity=quantity)
            json.dump(data_unit, data_file, indent=4, ensure_ascii=False)
        return data_unit

    except FileNotFoundError:
        print("Нет файла Excel")
        return None


def save_data_eplan_excel(file_excel):
    """
    Функция сохраняет полученные данные с сайта в файл Excel со спецификацией
    :return:
    """
    with open("Example/data_goods_from_ETM.json", "r", encoding='utf-8') as data:
        data_etm = json.load(data)
    workbook = xlrd.open_workbook(file_excel)
    sheet = workbook["Закупка оборудования"]

    for row in range(sheet.nrows):
        for col in range(sheet.ncols):
            if sheet.cell(row, col).value == 'Изделие: Обозначение 1':
                column = col


# Получить данные из Excel спецификации (В ДАННЫЙ МОМЕНТ СОХРАНЯЕМ В JSON)
data_eplan_excel = take_data_from_excel_eplan(excel_file)

save_data_eplan_excel(excel_file)  # Сохранить новые данные из интернета в Excel
