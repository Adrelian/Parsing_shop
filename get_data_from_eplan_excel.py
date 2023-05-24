import xlrd


def take_data_from_excel_eplan(adress_file_excel):
    """
    Функция собирает данные из файла Excel Eplan. И сохраняет полученные данные в json
    :param adress_file_excel: Адрес файла Excel со спецификацией
    :return: словарь с данными об изделиях
    """
    try:
        excel_data = xlrd.open_workbook(adress_file_excel)  # Открыть файл
        page = excel_data.sheet_by_index(0)  # Открыть первый лист

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
            data_unit[article] = {"Описание": description_item,
                                  "Производитель": manufacturer,
                                  "Тип изделия": number_type,
                                  "Кол-во": quantity}
        return data_unit
    except FileNotFoundError:
        print("Файл со спецификацией не найдем")


def save_data_eplan_excel(path_file_to_save):
    """
    Функция сохраняет полученные данные с сайта в файл Excel со спецификацией
    :param path_file_to_save: Путь для сохранения данных после парсинга сайта
    :return:
    """
    pass




