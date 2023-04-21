import json
from cookies_and_headers import cookie, header
import requests
from bs4 import BeautifulSoup


def take_unique_id_from_site():
    """
    Функция получается уникальный ID, который присваивает сайт входящему запросу
    :return: вернуть значение уникального ID
    """
    url = "https://www.etm.ru/"
    headers = header
    response = requests.get(url, headers=headers)
    content = response.content
    soup = BeautifulSoup(content, "lxml")

    data = soup.find("body").find("script")  # простыня с данными с сайта
    str_data = str(data)
    user_id = "buildId"  # Искомый тэг

    index = str_data.find(user_id)  # Индекс первого символа строки

    # Находим индекс первой кавычки после ключа "buildId"
    start_index = str_data.find('"', index + len(user_id) + 2)
    # Находим индекс второй кавычки после ключа "buildId"
    end_index = str_data.find('"', start_index + 1)
    # Извлекаем значение ключа "buildId"
    build_id_etm = str_data[start_index + 1:end_index]
    return build_id_etm


def get_data_from_etm(list_order_numbers, build_id_from_site):
    """
    Функция собирает данные о товарах на сайте ЕТМ. Поиск по артикулу товара
    :param build_id_from_site: Уникальный ID пользователя, который выдает сайт
    :type list_order_numbers: лист с данными для поиска на сайте
    :return: простыня с данными о товарах
    """
    all_data = []  # Пустой список для сбора всех данных
    for order_number in list_order_numbers:
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
        all_data = all_data + data_goods  # конечный список с данными о всех искомых товарах

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
        manufacturer = None
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
        order_list = list(data.keys())


        return order_list
    except:
        alarm_massage = "Нет файла с данными от Eplan"
        print(alarm_massage)


build_id = take_unique_id_from_site()
list_order = take_data_about_unit()  # лист с артикулами
data_about_goods_from_site = get_data_from_etm(list_order, build_id)  # простыня с данными с сайта по артикулам
take_data_about_goods(data_about_goods_from_site)  # Конкретные(отсортированные) данные о товарах
