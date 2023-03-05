import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import json

# headers взял из своего браузера в запросах, нужен, что бы "обмануть" сайт
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 "
                  "YaBrowser/23.1.2.987 Yows er/2.5 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9"
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


def push_button_open_catalog(site):
    """
    Функция нажимает на кнопки для открытия свёрнутых подкаталогов. Кнопка "Ещё(кол-во элементов)"
    :param site: Ссылка на страницу каталога
    :return:
    """
    my_driver_for_open_site = Service("C:\\Games\\python\\Parsing_Shop\\ChromeDriver\\chromedriver.exe")
    driver_site = webdriver.Chrome(service=my_driver_for_open_site)

    driver_site.get(site)
    time.sleep(1)
    list_with_find_button = driver_site.find_elements(By.CLASS_NAME, "CatalogCategories_link__k1wbv")
    for button in list_with_find_button:
        button.click()
        time.sleep(1)
    page_source = driver_site.page_source
    return page_source


def create_catalog(all_catalog, type_catalog=1):
    """
    Функция создания каталога изделий
    :param type_catalog: Тип каталога, type_catalog=1 - основной каталог, type_catalog=2 - подкаталоги
    :param all_catalog: Объект парсинга сайта
    :return: Возвращает словарь из разделов каталога и ссылок на эти разделы.
    """
    titles = []  # Лист для заголовков каталога
    links = []  # Лист для ссылок

    # Перебираем все элементы soup для поиска ссылок и названий раздела каталога

    for item in all_catalog:
        item_text = item.text
        item_href = item.find("a").get("href")
        try:
            titles.append(item_text)
            links.append(item_href)
        except:
            pass
    # Создать каталог
    catalog = dict(zip(titles, links))
    # Если ссылка не имела слова catalog вначале, 2о нужно его добавить
    for link in catalog:
        if type_catalog != 1:
            catalog[link] = "https://www.etm.ru/catalog/" + catalog[link]  # ссылки на подкаталоги
        else:
            catalog[link] = "https://www.etm.ru" + catalog[link]  # ссылки на основной каталог
    return catalog


def create_soup_for_catalog_production(site: str, type_catalog=1):
    """
    Функция создаёт основой каталог сайта в виде словаря из ключей в виде названия раздела
     и значений в виде ссылок на страницы подкаталогов
    :param type_catalog: Тип каталога, type_catalog=1 - основной каталог, type_catalog=2 - подкаталоги
    :param site: Основной сайт магазина
    :return: возвращает словарь из названия разделов и ссылок
    """

    # response = requests.get(site, headers=headers)  # Получаем ответ от сайта
    # soup = BeautifulSoup(response.content, "lxml")  # Варим суп и получаем весь сайт с каталогами
    # all_links = soup.findAll('a')  # ищем все ссылки

    if type_catalog == 1:
        response = requests.get(site, headers=headers)  # Получаем ответ от сайта
        soup = BeautifulSoup(response.content, "lxml")  # Варим суп и получаем весь сайт с каталогами
        all_catalog = soup.findAll(class_ = "CatalogCategories_card__Y8sOG")  # ищем все ссылки в основном каталоге

    else:
        create_page = push_button_open_catalog(site)
        soup = BeautifulSoup(create_page, "lxml")
        all_catalog = soup.findAll(class_="CatalogCategories_titleThirdCategory__NgjiL")  # ищем все ссылки в подкаталоге
    return create_catalog(all_catalog, type_catalog)


# Проверяем сайт на отклик состояния. Если 200 всё ОК, если другое число, то читаем документацию в этому числу
status = check_site(url_of_ETM, headers)

# Получаем общий каталог сайта
catalog_etm = create_soup_for_catalog_production("https://www.etm.ru/catalog", 1)
# cable = create_soup_for_catalog_production(catalog_etm["Кабели, провода и изделия для прокладки кабеля"], 2)
# lighting_products = create_soup_for_catalog_production(catalog_etm["Светотехнические изделия"], 2)
# electrical_installation_products = create_soup_for_catalog_production(catalog_etm["Изделия электроустановочные"], 2)
with open("Catalog/catalog_etm.json", "w") as file:
    json.dump(catalog_etm, file, indent=4, ensure_ascii=False)
# low_voltage_equipment = create_soup_for_catalog_production(catalog_etm["Оборудование низковольтное"], 2)
# panel_equipment = create_soup_for_catalog_production(catalog_etm["Щитовое оборудование"], 2)
# heating_and_climate = create_soup_for_catalog_production(catalog_etm["Отопление и климат"], 2)
# tools_equipment_and_protective_equipment = create_soup_for_catalog_production(catalog_etm["Инструмент, оснастка и средства защиты"], 2)
# workwear_and_PPE = create_soup_for_catalog_production(catalog_etm["Спецодежда и СИЗ"], 2)
# Automation_instrumentation = create_soup_for_catalog_production(catalog_etm["Автоматизация, КИП"], 2)
# Equipment_6_10kV = create_soup_for_catalog_production(catalog_etm["Оборудование 6-10кВ"], 2)
# Security_systems = create_soup_for_catalog_production(catalog_etm["Системы безопасности"], 2)
# Telecommunication_quipment_and_SCS = create_soup_for_catalog_production(catalog_etm["Телекоммуникационное оборудование и СКС"], 2)
# Bearings = create_soup_for_catalog_production(catalog_etm["Подшипники"], 2)
# Hardware_and_construction_fasteners = create_soup_for_catalog_production(catalog_etm["Метизы и строительный крепеж"], 2)
# Pipeline_systems = create_soup_for_catalog_production(catalog_etm["Трубопроводные системы"], 2)
# Shut_off_and_control_valves = create_soup_for_catalog_production(catalog_etm["Запорная и регулирующая арматура"], 2)
# Pumps_tanks_and_tanks = create_soup_for_catalog_production(catalog_etm["Насосы, баки и емкости"], 2)
# Related_products = create_soup_for_catalog_production(catalog_etm["Сопутствующие товары"], 2)
# Software = create_catalog_production(create_soup_for_catalog_production["Программное обеспечение"], 2)
