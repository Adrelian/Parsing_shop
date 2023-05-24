# pip install beautifulsoup
# pip install fuzzywuzzy
# pip install
# pip install python-Levenshtein
# pip3 install soupsieve

import json
from cookies_and_headers import cookie, header
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

from get_data_from_eplan_excel import take_data_from_excel_eplan


def take_unique_id_from_site():
    """
    Функция получается уникальный ID, который присваивает сайт входящему запросу
    :return: вернуть значение уникального ID
    """
    # Создание супа
    url = "https://www.etm.ru/"
    headers = header
    response = requests.get(url, headers=headers)
    content = response.content
    soup = BeautifulSoup(content, "lxml")
    # Поиск Id
    data = soup.find("body").find("script").text  # простыня с данными с сайта в виде текста
    data_dict = json.loads(data)  # Превратить в словарь
    build_id_etm = data_dict['buildId']  # Найти Id

    return build_id_etm


def get_data_from_etm(dict_order_numbers, build_id_etm):
    """
    Функция собирает данные о товарах на сайте ЕТМ. Поиск по артикулу товара
    :param dict_order_numbers: Словарь с данными обо всех товарах
    :param build_id_etm: Уникальный ID пользователя, который выдает сайт
    :return: простыня с данными о товарах
    """
    all_data = []  # Пустой список для сбора всех данных

    for order_number in dict_order_numbers:  # Запрос на сайт по артикулу
        # Системные данные для запроса
        params = {
            'page': '1',
            'rows': '36',
            'searchValue': order_number,
        }
        # Запрос
        print(requests.get(f'https://www.etm.ru/_next/data/{build_id_etm}/catalog.json'))
        response = requests.get(
            f'https://www.etm.ru/_next/data/{build_id_etm}/catalog.json',
            params=params,
            cookies=cookie,
            headers=header,
        ).json()
        # Попытка прочитать с сайта данные по артикулу
        try:
            data_goods = response.get("pageProps").get("data").get("rows")  # все данные о товаре

            # Возможные способы проверки полученных данных на валидность
            for item in data_goods:
                # Сравниваем артикул сайта с номером для заказа EPLAN (и производителей)
                if item["art"] == order_number \
                        and item["mnf_name"] == dict_order_numbers[order_number]["name_manufacturer"]:
                    item["art"] = order_number
                    all_data.append(item)
                    break

                # Сравниваем тип изделия сайта и тип изделия Eplan (и производителей)
                elif item["mnf_ser"] == dict_order_numbers[order_number]["order_type"] \
                        and dict_order_numbers[order_number]["name_manufacturer"] == item["mnf_name"]:
                    item["art"] = order_number
                    all_data.append(item)
                    break

                # Неточное сравнение имени (описания на сайте) с номером для заказа из Eplan (и производителя)
                elif fuzz.WRatio(item["name"], order_number) > 70 \
                        and fuzz.WRatio(dict_order_numbers[order_number]["name_manufacturer"], item["mnf_name"]) > 90:
                    print(f"Алгоритм fuzzy сработал с переменной для {order_number}")
                    item["art"] = order_number
                    all_data.append(item)
                    break

                # Неточное сравнение имени (описания на сайте) с типом изделия из Eplan и производителя
                elif fuzz.WRatio(item["name"], order_number) > 70 \
                        and dict_order_numbers[order_number]["name_manufacturer"] == "":
                    a = fuzz.WRatio(item["name"], order_number)
                    print(a)
                    print(f"Алгоритм fuzzy  с числом сработал для {order_number}")
                    item["art"] = order_number
                    all_data.append(item)
                    break

                # Ещё один способ проверки (если буду ошибки, то можно дописать новое условие)
                elif None:
                    pass

        except Exception:
            print(f"Нет данных на сайте по этому артикулу{dict_order_numbers[order_number]}")

    return all_data


def take_data_about_goods(all_data):
    """
    Функция парсит полученную с сайта простыню с данными и создает JSON файл с данными об изделиях
    :param all_data: Простыня с данным о товаре
    :return: Словарь с основным ключом артикулом и остальной информацией в словарях
    """
    with open("example/data_goods_from_etm.json", 'w', encoding='utf-8') as data_file:
        data_unit = {}  # пустой словарь для сбора данных
        # сбор определённых значений о товаре
        for item in all_data:
            name = item.get("name")  # описание товара
            quantity_in_package = item.get("pack")  # кол-во изделий в паковке
            price = item.get("price98")  # розничная цена
            sale_price = item.get("price")  # цена со всеми скидками
            code = item.get("code")  # код заказа етм
            name_manufacturer = item.get("mnf_name")  # производитель
            article_number = item.get("art")  # заказной номер

            data_unit[article_number] = {"name": name, "name_manufacturer": name_manufacturer,
                                         "quantity_in_package": quantity_in_package, "etm_code": code,
                                         "price_retail": price, "price_max_discount": sale_price}

        json.dump(data_unit, data_file, indent=4, ensure_ascii=False)


def take_data_about_unit():
    """
    Получить данные об изделиях из спецификации Eplan
    :return: Словарь с данными о товарах
    """
    data = take_data_from_excel_eplan('C:/Games/python/Parsing_Shop/Example/Спецификация Электрика.xls')
    print(data)
    for item in data:
        print(item)
    return data


