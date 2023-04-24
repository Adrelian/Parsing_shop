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
            quantity_in_package = part_data.attrib.get("quantity/package")  # Количество/упаковка
            ETM_code = part_data.attrib.get("")  # ОПРЕДЕЛИТЬСЯ С ТИПОМ ПЕРЕМЕННОЙ В EPLAN
            code_second_site = part_data.attrib.get("")  # ОПРЕДЕЛИТЬСЯ С ТИПОМ ПЕРЕМЕННОЙ В EPLAN
            code_third_site = part_data.attrib.get("")  # ОПРЕДЕЛИТЬСЯ С ТИПОМ ПЕРЕМЕННОЙ В EPLAN

            # Сбор данных об изделии в один словарь
            data_unit[article_part_number] = dict(name=desc1, order_type=article_type,
                                                  name_manufacturer=name_manufacturer, price=price,
                                                  price_with_discount=price_with_discount, weight=weight,
                                                   quantity_in_package=quantity_in_package, ETM_code=ETM_code,
                                                  code_second_site=code_second_site, code_third_site=code_third_site)

        json.dump(data_unit, data_file, indent=4, ensure_ascii=False)

        return data_unit


def compare_data_from_site_with_date_from_eplan(eplan_data, etm_date, site_date_1=None, site_date_2=None,
                                                site_date_3=None):
    pass


def send_data_to_Eplan():
    """
    Берём данные полученные с сайта и сохраняем в файл для Eplan
    :return:
    """
    with open("Example/data_goods_from_ETM.json", 'r', encoding='utf-8') as finish_data_file:
        data = json.load(finish_data_file)
        for item in data.values():
            print(item)


data_from_eplan = take_data_from_xml_eplan(xml_file)
send_data_to_Eplan()
