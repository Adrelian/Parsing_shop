import requests
from bs4 import BeautifulSoup
import pandas as pd

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


check_site(url_of_ETM, headers)

response = requests.get(url_of_ETM, headers=headers)  # Получаем ответ от сайта
soup = BeautifulSoup(response.content, "lxml")  # Варим суп и получаем весь сайт с каталогами

data_link_catalog = soup.findAll("div", class_="CatalogCategories_wrapper__aOgzT")  # ищу все разделы сайта

all_links = soup.findAll('a') # ищем все ссылки
list_link = []
list_title = []
# два списка с заголовками и ссылками
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

def  chapter_catalog():











# data_schity_title = soup.findAll("div", class_ = "CatalogCategories_card__Y8sOG") # заголовки разделов
# print(data_schity_title)

# data = soup.find("div", class_="jss173")
# print(data)
# # name = data.find("div", class_="jss195").text.replace("\n", "")
