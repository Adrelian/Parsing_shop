import json
import xml.etree.ElementTree as ET
import xlrd


xml_file = 'Example/Устройства КВТ.xml'
excel_file = 'Example/Спецификация Электрика.xls'
data_from_eplan_to_json = "Example/data_goods_Eplan_Excel.json"


def take_data_from_xml_eplan(address_file_xml):
    """
    Функция собирает нужные данные из xml файла для последующего поиска этих данных на сайте
    :param address_file_xml: ссылка на файл XML
    :return: найденные данные из XML файла Eplan
    """
    try:
        # Создаём дерево файла для парсинга
        tree = ET.parse(address_file_xml)
        root = tree.getroot()
        # Перебираем файл для получения нужно информации
        with open("Example/data_goods_from_Eplan_xml.json", 'w', encoding='utf-8') as data_file:
            data_unit = {}  # Пустой словарь для сбора данных об изделиях
            # Сбор данных из XML файла
            for part_data in root:
                desc1 = part_data.attrib.get("P_ARTICLE_DESCR1")[6:][:-1]  # Описание: Обозначение 1
                article_type = part_data.attrib.get("P_ARTICLE_TYPENR")  # Тип изделия: Номер типа
                article_part_number = part_data.attrib.get("P_ARTICLE_ORDERNR")  # Артикул: Номер для заказа
                name_manufacturer = part_data.attrib.get("P_ARTICLE_MANUFACTURER")  # Имя производителя: Производитель
                price = part_data.attrib.get("P_ARTICLE_PURCHASEPRICE_1")  # Закупочная цена/единица цены (Валюта 1)
                price_with_discount = part_data.attrib.get(
                    "P_ARTICLE_PURCHASEPRICE_2")  # Закупочная цена/единица цены (Валюта 2)
                weight = part_data.attrib.get("P_ARTICLE_WEIGHT")  # Вес
                quantity_in_package = part_data.attrib.get("P_ARTICLE_PACKAGINGQUANTITY")  # Количество/упаковка
                ETM_code = part_data.attrib.get("")  # ОПРЕДЕЛИТЬСЯ С ТИПОМ ПЕРЕМЕННОЙ В EPLAN
                code_second_site = part_data.attrib.get("")  # ОПРЕДЕЛИТЬСЯ С ТИПОМ ПЕРЕМЕННОЙ В EPLAN
                code_third_site = part_data.attrib.get("")  # ОПРЕДЕЛИТЬСЯ С ТИПОМ ПЕРЕМЕННОЙ В EPLAN

                # Сбор данных об изделии в один словарь
                data_unit[article_part_number] = dict(name=desc1,
                                                      order_type=article_type,
                                                      name_manufacturer=name_manufacturer,
                                                      price_retail=price,
                                                      price_max_discount=price_with_discount,
                                                      weight=weight,
                                                      quantity_in_package=quantity_in_package,
                                                      ETM_code=ETM_code,
                                                      code_second_site=code_second_site,
                                                      code_third_site=code_third_site
                                                      )

            json.dump(data_unit, data_file, indent=4, ensure_ascii=False)
            return data_unit
    except Exception:
        print("Нет файла XML Eplan")
        return None


def take_data_from_excel_eplan(adress_file_excel, file_json_for_data_excel):
    """
    Функция собирает данные из файла Excel Eplan. И сохраняет полученные данные в json
    :param adress_file_excel: Адрес файла Excel со спецификацией
    :param file_json_for_data_excel: 
    :return: словарь с данными об изделиях
    """
    try:
        excel_data = xlrd.open_workbook(adress_file_excel)  # Открыть файл
        page = excel_data.sheet_by_index(0)  # Открыть первый лист

        with open(file_json_for_data_excel, 'w', encoding='utf-8') as data_file:
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

    except Exception:
        print("Нет файла Excel")
        return None


def send_data_to_eplan_xml(address_file):
    """
    Берём данные полученные с сайта и сохраняем в файл для Eplan
    :return:
    """
    # Создаём дерево файла для парсинга
    tree = ET.parse(address_file)
    root = tree.getroot()

    # Открытие файла с найденными ценами
    with open("Example/data_goods_from_ETM.json", "r", encoding='utf-8') as data:
        data_etm = json.load(data)

    # Перенос цен в файл XML
    for item_with_price in data_etm:
        for item_eplan in root.iter("part"):
            if item_with_price == item_eplan.attrib.get("P_ARTICLE_ORDERNR"):
                price1 = data_etm[item_with_price]["price_retail"]  # Цена 1
                item_eplan.set("P_ARTICLE_PURCHASEPRICE_1", str(price1))
                price2 = data_etm[item_with_price]["price_max_discount"]  # Цена 2
                item_eplan.set("P_ARTICLE_PURCHASEPRICE_2", str(price2))

    # Записываем в XML полученные изменения
    tree.write("output.xml", encoding='utf-8')


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
    workbook.inser_cols(column)






data_eplan_excel = take_data_from_excel_eplan(excel_file, data_from_eplan_to_json) # Получить данные из Excel спецификации (В ДАННЫЙ МОМЕНТ СОХРАНЯЕМ В JSON)
data_eplan_xml = take_data_from_xml_eplan(xml_file)  # Данные из XML файла eplan (В ДАННЫЙ МОМЕНТ СОХРАНЯЕМ В JSON)
save_data_eplan_excel(excel_file)
