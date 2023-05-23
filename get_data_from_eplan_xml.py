import json
import xml.etree.ElementTree as ET

xml_file = 'Example/Устройства КВТ.xml'


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
                data_unit[article_part_number] = {"Описание": desc1,
                                                  "Производитель": name_manufacturer,
                                                  "Тип изделия": article_type,
                                                  "Кол-во в упаковке": quantity_in_package}
            json.dump(data_unit, data_file, indent=4, ensure_ascii=False)
            return data_unit
    except Exception:
        print("Нет файла XML Eplan")
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


data_eplan_xml = take_data_from_xml_eplan(xml_file)  # Данные из XML файла eplan (В ДАННЫЙ МОМЕНТ СОХРАНЯЕМ В JSON)
