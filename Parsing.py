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
    if url.status_code == 200:
        print(f'Состояние сайт {url}. Все в норме!')
    if url.status_code != 200:
        print(f'{url}. Требуется проверка')


def create_catalog_all_production(site: str):
    """
    Функция создаёт основой каталог сайта в виде словаря из ключей в виде названия раздела и значений в виде ссылок на страницы подкаталогов
    :param site: Основной сайт магазина
    :return: Возвращает словарь из названия разделов и ссылок
    """
    response = requests.get(site, headers=headers)  # Получаем ответ от сайта
    soup = BeautifulSoup(response.content, "lxml")  # Варим суп и получаем весь сайт с каталогами

    all_links = soup.findAll('a')  # ищем все ссылки
    list_link = []  # cписок для ссылок
    list_title = []  # список для названия разделов каталога
    # складываем ссылки разделов и названия разделов в списки
    for link in all_links:
        link_url = link.get("href")
        list_link.append(link_url)
        title_url = link.getText("CatalogCategories_title__ahzrn")
        list_title.append(title_url)
        if title_url == "Программное обеспечение":
            break
    # Удаляем лишние ссылки
    list_title.pop(0)
    list_title.pop(0)
    list_link.pop(0)
    list_link.pop(0)
    # Создаём словарь из заголовков и ссылок
    title_and_link = dict(zip(list_title, list_link))
    for value in title_and_link:
        title_and_link[value] = "https://www.etm.ru" + title_and_link[value]
    return title_and_link


def del_unknown(number: int, list_with_something):  # ПРОВЕРИТЬ РАБОТУ
    if number > 0:
        list_with_something.pop()
        number = number - 1


def chapter_catalog(main_catalog: dict, end_parsing: str, index: int):
    """
    Функция парсит по разделам каталога, которые уже созданы выше, для получения названия и ссылок подкаталога
    :param index: Индекс словаря
    :param end_parsing: Заголовок раздела, после которого останавливаем парсинг (последний раздел)
    :param main_catalog: Основной каталог товаров
    :return: возвращает словарь из названия разделов и их ссылок
    """
    index = 0  # для движения по словарю
    for chapter in main_catalog:
        resp = requests.get(main_catalog[index], headers=headers) # Запрос на сайт
        soup_chapter = BeautifulSoup(resp.content, "lxml") # Получение информации со всего сайта по запросу выше
        links = soup_chapter.findAll('a')  # ищем все ссылки на элементы
        main_catalog.setdefault(__key=[], []).
    # пустые списки для ссылок и заголовков разделов
    title_chapter = []
    link_chapter = []

    # перебираем все ссылки и заголовки, складываем в списки созданные ранее
    for url in links:
        link_ch = url.get("href")
        link_chapter.append(link_ch)
        title_ch = url.getText("CCatalogCategories_cardSubCategory__urEmp")
        title_chapter.append(title_ch)
        if title_ch == end_parsing:
            break

    # Удаляем не нужны ссылки
    link_chapter.pop(0)
    link_chapter.pop(0)
    link_chapter.pop(0)
    title_chapter.pop(0)
    title_chapter.pop(0)
    title_chapter.pop(0)

    # Создаём словарь из названия разделов и ссылок
    data_dictionary = dict(zip(title_chapter, link_chapter))
    for value in data_dictionary:
        data_dictionary[value] = "https://www.etm.ru/catalog/" + data_dictionary[value]
    return data_dictionary


def get_name_and_price(chapter: str, tag: str):  # ФУНКЦИЯ НЕ ГОТОВАЯ. ТРЕБУЕТСЯ ПРОВЕРКА
    resp = requests.get(chapter, headers=headers)
    soup_chapter = BeautifulSoup(resp.content, "lxml")
    print(soup_chapter)


# Проверяем сайт на отклик состояния. Если 200 всё ОК, если другое число, то читаем документацию в этому числу
check_site(url_of_ETM, headers)

# Получаем общий каталог сайта
catalog_etm = create_catalog_all_production("https://www.etm.ru/catalog")

# # Раздел с проводами
# cable = chapter_catalog(title_and_link["Кабели, провода и изделия для прокладки кабеля"], "Промышленные электрические соединители")
# f = list(cable.values())[0]
#
# get_name_and_price(f, "js397")
# # Раздел со светотехникой
# light = chapter_catalog(title_and_link["Светотехнические изделия"], "Аксессуары Системы Управления Освещеним (адаптеры, выключатели т.д.)")
