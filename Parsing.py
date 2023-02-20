import requests
from bs4 import BeautifulSoup
import pandas as pd


url = "https://www.etm.ru/catalog"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}


response = requests.get(url, headers=headers)
print(response)
soup = BeautifulSoup(response.content, "html.parser")  # 'html.parser' вместо "lxml"

data = soup.find("div", class_="jss543")

name = data.find("div", class_="jss560").text.replace("\n", "")
