import json
import xml.etree.ElementTree as ET

xml_file = 'Example/Устройства КВТ.xml'


def take_data_from_xml_eplan(address_file):
    """
    Функция собирает нужные данные из xml файла для последующего поиска этих данных на сайте
    :param address_file: ссылка на файл XML
    :return:
    """
    # Создаём дерево файла для парсинга
    tree = ET.parse(address_file)
    root = tree.getroot()

    # Перебираем файл для получения нужно информации
    with open("Example/data_goods_from_Eplan.json", 'w', encoding='utf-8') as data_file:
        data_unit = {}  # Пустой словарь для сбора данных об изделиях

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
            data_unit[article_part_number] = dict(name=desc1, order_type=article_type,
                                                  name_manufacturer=name_manufacturer, price_retail=price,
                                                  price_max_discount=price_with_discount, weight=weight,
                                                  quantity_in_package=quantity_in_package, ETM_code=ETM_code,
                                                  code_second_site=code_second_site, code_third_site=code_third_site)

        json.dump(data_unit, data_file, indent=4, ensure_ascii=False)

        return data_unit


def find_different_between_eplan_and_etm():
    """Функция получает данные из файлов JSON и переносит данные одного файла в другой"""
    with open("Example/data_goods_from_ETM.json", 'r', encoding='utf-8') as etm_data_file:
        data_from_etm = json.load(etm_data_file)
    with open("Example/data_goods_from_Eplan.json", "r", encoding='utf-8') as eplan_data_file:
        data_from_eplan = json.load(eplan_data_file)

    eplan_article_number = list(data_from_eplan.keys())  # Заказные номера из Eplan
    etm_article_number = list(data_from_etm.keys())  # Заказные номера и ETM

    fault_search = set()  # Множество ошибок поиска

    # Поиск отличий между Eplan и ETM
    for article_number in eplan_article_number:
        if article_number not in etm_article_number:
            fault_search.add(article_number)

    return fault_search


def send_data_to_eplan(address_file):
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
                print(f"Артикул файла ЕТМ {item_with_price} равен артикулу Eplana {item_eplan.attrib.get('P_ARTICLE_ORDERNR')}")
                price1 = data_etm[item_with_price]["price_retail"]  # Цена 1
                item_eplan.set("P_ARTICLE_PURCHASEPRICE_1", str(price1))
                price2 = data_etm[item_with_price]["price_max_discount"]  # Цена 2
                item_eplan.set("P_ARTICLE_PURCHASEPRICE_2", str(price2))

    # Записываем в XML полученные изменения
    tree.write("output.xml", encoding='utf-8')


data_eplan = take_data_from_xml_eplan(xml_file)  # Данные из XML файла eplan (В ДАННЫЙ МОМЕНТ СОХРАНЯЕМ В JSON)
fault_find_article = find_different_between_eplan_and_etm()  # Список с артикулами, которые не смог найти
send_data_to_eplan("Example/Устройства КВТ.xml")