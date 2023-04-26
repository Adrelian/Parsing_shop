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
            price = part_data.attrib.get("P_ARTICLE_PRICEUNIT")  # Стоимость: Цена единицы
            price_with_discount = part_data.attrib.get(
                "P_ARTICLE_PURCHASEPRICE_1")  # Стоимость товара со всеми скидками: Закупочная цена/Единица цены
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


def take_data_from_json():
    """Функция получает данные из файлов JSON и переносит даные одного файла в другой"""
    with open("Example/data_goods_from_ETM.json", 'r', encoding='utf-8') as etm_data_file:
        data_from_etm = json.load(etm_data_file)
    with open("Example/data_goods_from_Eplan.json", "r", encoding='utf-8') as eplan_data_file:
        data_from_eplan = json.load(eplan_data_file)
    for item in data_from_etm.values():
        for item2 in data_from_eplan.values():
            print(item2)


def send_data_to_eplan():
    """
    Берём данные полученные с сайта и сохраняем в файл для Eplan
    :return:
    """
    None


data_eplan = take_data_from_xml_eplan(xml_file)
take_data_from_json()
