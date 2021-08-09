import asyncio
import csv

from bs4 import BeautifulSoup
import aiohttp
import requests


URL = "https://www.whiskishop.com/collections/whisky-types-single-malt"
# URL = "https://www.whiskishop.com/collections/scotch-whisky-highland"

HEADERS = {
    "user agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
}

HOST = "https://www.whiskishop.com"


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_="product-container text-left product-block")
    products = [
        {
            "title": item.find("h5", class_="name").get_text(strip=True),
            "cost": item.find("span", class_="money").get_text(strip=True),
            "link": HOST + item.find("a", class_="product-name").get("href"),
        }
        for item in items
    ]

    return products


async def fetch_content(url, session, params=None):
    async with session.get(url, headers=HEADERS, params=params) as response:
        if response.status_code == 200:
            data = await response.text
            return get_content(data)
        else:
            print(f"Что-то пошло не так! {response.status_code}")


def get_pages_count(html):
    soup = BeautifulSoup(html, "html.parser")
    item = soup.find("li", class_="pagination_next").find_previous("li")
    num = item.find("a").get_text()
    return int(num) if num else 1


def save_file(data: list, filename: str):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Наименование", "Цена в фунтах", "Ссылка"])
        for item in data:
            writer.writerow([item["title"], item["cost"], item["link"]])


async def main():
    pages_count = get_pages_count()
    tasks = []
    async with aiohttp.ClientSession() as session:
        for page in range(1, pages_count+1):
            task = asyncio.create_task(fetch_content(URL, session, params={"page": page}))


if __name__ == "__main__":
    main()
