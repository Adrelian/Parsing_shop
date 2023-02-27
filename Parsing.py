from typing import Dict, Any

import requests
from bs4 import BeautifulSoup

# headers взял из своего браузера в запросах, нужен что бы "обмануть" сайт
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}
url_of_ETM = "https://www.etm.ru/catalog"


def check_site(site: str, head):
    """
    Функция для проверки связи с сайтом.
    :param site: Ссылка на сайт
    :param head: Заголовок для создания видимости реального запроса
    :return: функция ничего не возвращает
    """
    url = requests.get(site, headers=head)
    sts = "Неизвестно"
    if url.status_code == 200:
        sts = f'Состояние сайт {url}. Все в норме!'
    if url.status_code != 200:
        sts = f'{url}. Требуется проверка'
    return sts


def delete_unknown_chapter(counter: int, list_with_chapter: list):
    """
    Удаление не нужны элементов из каталога
    :param counter: Сколько элементов удалить
    :param list_with_chapter: Список, в котором удалять
    :return: Новый список
    """
    while counter != 0:
        list_with_chapter.pop(0)
        counter -= 1
    return list_with_chapter


def create_catalog(soup, counter_del):
    """
    Функция создания каталога изделий
    :param counter_del: Кол-во удаляемых НЕНУЖНЫХ разделов
    :param soup: Объект парсинга сайта
    :return: Возвращает словарь из разделов каталога и ссылок на эти разделы
    """
    links = []  # Лист для ссылок
    titles = []  # Лист для заголовков каталога
    for item in soup:
        link_url = item.get("href")
        links.append(link_url)
        title = item.getText("CatalogCategories_title__ahzrn")
        if title == "«Честная позиция».":
            break
        titles.append(title)

    # Удалить не нужные элементы из каталога
    titles = delete_unknown_chapter(counter_del, titles)
    links = delete_unknown_chapter(counter_del, links)
    # Создать каталог
    catalog = dict(zip(titles, links))
    for link in catalog:
        catalog[link] = "https://www.etm.ru/" + catalog[link]
    return catalog


def create_catalog_production(site: str, delete_chapter: int):
    """
    Функция создаёт основой каталог сайта в виде словаря из ключей в виде названия раздела
     и значений в виде ссылок на страницы подкаталогов
    :param delete_chapter: Удалить ненужные разделы
    :param site: Основной сайт магазина
    :return: Возвращает словарь из названия разделов и ссылок
    """
    response = requests.get(site, headers=headers)  # Получаем ответ от сайта
    soup = BeautifulSoup(response.content, "lxml")  # Варим суп и получаем весь сайт с каталогами
    all_links = soup.findAll('a')  # ищем все ссылки
    # складываем ссылки разделов и названия разделов в списки
    return create_catalog(all_links, delete_chapter)


# Проверяем сайт на отклик состояния. Если 200 всё ОК, если другое число, то читаем документацию в этому числу
status = check_site(url_of_ETM, headers)
print(status)

# Получаем общий каталог сайта
catalog_etm = create_catalog_production("https://www.etm.ru/catalog", 2)
cable = create_catalog_production(catalog_etm["Кабели, провода и изделия для прокладки кабеля"], 3)
lighting_products = create_catalog_production(catalog_etm["Светотехнические изделия"], 3)
print(cable)
# electrical_installation_products = create_catalog_production(catalog_etm["Изделия электроустановочные"], 3)
# low_voltage_equipment = create_catalog_production(catalog_etm["Оборудование низковольтное"], 3)
# panel_equipment = create_catalog_production(catalog_etm["Щитовое оборудование"], 3)
# heating_and_climate = create_catalog_production(catalog_etm["Отопление и климат"], 3)
# tools_equipment_and_protective_equipment = create_catalog_production(catalog_etm["Инструмент, оснастка и средства защиты"], 3)
# workwear_and_PPE = create_catalog_production(catalog_etm["Спецодежда и СИЗ"], 3)
# Automation_instrumentation = create_catalog_production(catalog_etm["Автоматизация, КИП"], 3)
# Equipment_6_10kV = create_catalog_production(catalog_etm["Оборудование 6-10кВ"], 3)
# Security_systems = create_catalog_production(catalog_etm["Системы безопасности"], 3)
# Telecommunication_quipment_and_SCS = create_catalog_production(catalog_etm["Телекоммуникационное оборудование и СКС"], 3)
# Bearings = create_catalog_production(catalog_etm["Подшипники"], 3)
# Hardware_and_construction_fasteners = create_catalog_production(catalog_etm["Метизы и строительный крепеж"], 3)
# Pipeline_systems = create_catalog_production(catalog_etm["Трубопроводные системы"], 3)
# Shut_off_and_control_valves = create_catalog_production(catalog_etm["Запорная и регулирующая арматура"], 3)
# Pumps_tanks_and_tanks = create_catalog_production(catalog_etm["Насосы, баки и емкости"], 3)
# Related_products = create_catalog_production(catalog_etm["Сопутствующие товары"], 3)
# Software = create_catalog_production(catalog_etm["Программное обеспечение"], 3)
