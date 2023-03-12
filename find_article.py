import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 "
                  "YaBrowser/23.1.2.987 Yows er/2.5 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9"
}

with open("Catalog\sub_catalog_shop.json", "r", encoding="utf-8") as file:
    catalog = json.load(file)

# все ссылки в список
list_link = []
for link in catalog.values():
    list_link.append(link)


def find_item(all_links):
    for link in all_links:
        response = requests.get(link, headers=headers)  # Получаем ответ от сайта
        soup = BeautifulSoup(response.content, "lxml")  # Варим суп и получаем весь сайт с каталогами
        all_catalog = soup.get_text("jss198")  # ищем ссылки в основном каталоге
        print(all_catalog)


find_item(list_link)