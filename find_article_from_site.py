import json
from cookies_and_headers import cookie, header
import requests
from bs4 import BeautifulSoup


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


def get_data_from_etm(dict_order_numbers, build_id_from_site):
    """
    Функция собирает данные о товарах на сайте ЕТМ. Поиск по артикулу товара
    :param dict_order_numbers: Словарь с данными обо всех товарах
    :param build_id_from_site: Уникальный ID пользователя, который выдает сайт
    :return: простыня с данными о товарах
    """
    all_data = []  # Пустой список для сбора всех данных
    for order_number in dict_order_numbers.keys():

        # Системные данные для запроса
        params = {
            'page': '1',
            'rows': '12',
            'searchValue': order_number,
        }
        # Запрос
        response = requests.get(
            f'https://www.etm.ru/_next/data/{build_id_from_site}/catalog.json',
            params=params,
            cookies=cookie,
            headers=header,
        ).json()
        data_goods = response.get("pageProps").get("data").get("rows")  # все данные о товаре

        # Каждый элемент в data_goods - словарь, нужно проверять производителя
        for item in data_goods:
            if item["mnf_name"] == "КВТ":
                print(item)
        # all_data = all_data + data_goods  # конечный список с данными о всех искомых товарах

    return all_data


def take_data_about_goods(object_data_goods):
    """
    Функция парсит полученную с сайта простыню с данными
    :param object_data_goods: Простыня с данным о товаре
    :return: Словарь с основным ключом артикулом и остальной информацией в подсловарях
    """
    with open("example/data_goods_from_etm.json", 'w', encoding='utf-8') as data_file:
        data_unit = {}  # пустой словарь для сбора данных
        # сбор определённых значений о товаре
        for item in object_data_goods:
            name = item.get("name")  # описание товара
            price = item.get("price98")  # розничная цена
            sale_price = item.get("price")  # цена со всеми скидками
            code = item.get("code")  # код заказа етм
            manufacturer_name = item.get("mnf_name")  # производитель
            article_number = item.get("art")  # заказной номер

            data_unit[article_number] = {"name": name, "manufacturer_name": manufacturer_name, "etm_code": code,
                                         "price_retail": price, "price_max_discount": sale_price}

        json.dump(data_unit, data_file, indent=4, ensure_ascii=False)


def take_data_about_unit():
    """
    Получение артикулов товара из каталога (файла xml) Eplan
    :return: лист с артикулами товаров
    """
    try:
        with open("Example/data_goods_from_Eplan.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except:
        alarm_massage = "Нет файла с данными от Eplan"
        print(alarm_massage)


build_id = take_unique_id_from_site()
list_order = take_data_about_unit()  # лист с артикулами
data_about_goods_from_site = get_data_from_etm(list_order, build_id)  # простыня с данными с сайта по артикулам
take_data_about_goods(data_about_goods_from_site)  # Конкретные(отсортированные) данные о товарах
