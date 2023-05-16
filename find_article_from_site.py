import json
from cookies_and_headers import cookie, header
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz


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
    for order_number in dict_order_numbers:

        # Системные данные для запроса
        params = {
            'page': '1',
            'rows': '36',
            'searchValue': order_number,
        }
        # Запрос
        response = requests.get(
            f'https://www.etm.ru/_next/data/{build_id_etm}/catalog.json',
            params=params,
            cookies=cookie,
            headers=header,
        ).json()
        try:
            data_goods = response.get("pageProps").get("data").get("rows")  # все данные о товаре
            mini = 50
            # Возможные способы проверки полученных данных на валидность
            for item in data_goods:
                # Сравниваем заказной номер и производителя
                if item["mnf_name"] == dict_order_numbers[order_number]["name_manufacturer"] \
                        and item["art"] == order_number:
                    all_data.append(item)
                    break
                #  Сравниваем тип изделия с номером на сайте
                elif item["name"] == dict_order_numbers[order_number]["order_type"]:
                    all_data.append(item)
                    break
                # Если нет производителя, то сравниваем тип изделия
                elif item["mnf_ser"] == dict_order_numbers[order_number]["order_type"]:
                    all_data.append(item)
                    break
                # Неточное сравнение имени (описания на сайте) с типом изделия из Eplan
                elif fuzz.WRatio(item["name"], order_number) > mini:
                    item["art"] = order_number
                    all_data.append(item)

                    break
                # Ещё один способ проверки (если буду ошибки, то можно дописать новое условие)
                elif None:
                    pass
        except Exception:
            print(f"Нет артикула")
    return all_data


def take_data_about_goods(all_data):
    """
    Функция парсит полученную с сайта простыню с данными
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


def take_data_about_unit(address_file):
    """
    Получение артикулов товара из каталога (файла xml) Eplan
    :return: лист с артикулами товаров
    """
    try:
        with open(address_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except:
        alarm_massage = "Нет файла с данными"
        print(alarm_massage)


build_id = take_unique_id_from_site()
# list_order_xml = take_data_about_unit("Example/data_goods_from_Eplan.json")  # лист с артикулами из XML
# data_about_goods_from_site = get_data_from_etm(list_order_xml, build_id)  # простыня с данными с сайта по артикулам
# XML take_data_about_goods(data_about_goods_from_site)  # Конкретные(отсортированные) данные о товарах

list_order_excel = take_data_about_unit("Example/data_goods_from_Eplan_Excel.json")  # Лист с артикулами из Excel
data_excel_about_goods_from_site = get_data_from_etm(list_order_excel, build_id)  # простыня с данными по артикулам
# Excel
take_data_about_goods(data_excel_about_goods_from_site)
