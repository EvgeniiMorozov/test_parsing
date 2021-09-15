import asyncio
from concurrent.futures import ThreadPoolExecutor
from random import randint

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from main import save_to_xlsx
import requests
from stuff import HEADERS

# URL = "https://www.wildberries.ru/catalog/elektronika/smartfony-i-telefony/vse-smartfony"
URL = "https://www.wildberries.ru/catalog/elektronika/smartfony-i-telefony/vse-smartfony?sort=popular&page=1&fbrand=5789%3B6049%3B5786%3B5779%3B16111%3B10883%3B28380%3B132943%3B5772"
HOST = "https://www.wildberries.ru"

"""
async get-request & fetch_content, multithread parse, save results
"""
fetching_data: list[str] = []
img_links = []
prod_links = []


async def get_html(session: ClientSession, page: int):
    await asyncio.sleep(randint(3, 6))
    url = URL + f"?page={page}"
    async with session.get(url=url, headers=HEADERS) as response:
        if response.status != 200:
            print(f"Что-то пошло не так! {response.status=}")
        print(f"Получаю данные с {url}")
        response_text = await response.read()
        # fetching_data.append(response_text)
        with open(f"source/page_content/page_{page}.txt", "wb") as file:
            file.write(response_text)

        return response_text


async def fetch_content():
    async with ClientSession() as session:
        response = await session.get(url=URL, headers=HEADERS)
        # Важно помнить, библиотека  BS4 не асинхронная !!!
        # soup = BeautifulSoup(await response.text(), "html.parser")
        # num = soup.find("li", class_="pagination_next").find_previous("li").find("a").get_text()
        # pages_count = int(num) if num else 1
        pages_count = 6

        tasks = []

        for page in range(1, pages_count + 1):
            task = asyncio.create_task(get_html(session, page))
            tasks.append(task)

        return await asyncio.gather(*tasks)


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_="product-card__wrapper")

    data = []
    for item in items:
        prod_link = HOST + item.find("a", class_="product-card__main j-open-full-product-card").get("href")
        img_link = item.find("img", class_="j-thumbnail thumbnail").get("src")
        img_links.extend(img_link)
        description = item.find("a", class_="product-card__main j-open-full-product-card").get("alt")
        prod_links.extend(prod_link)
        brand_div = item.find("div", class_="product-card__brand-name")
        brand = brand_div.find("strong", class_="brand-name").get_text()
        spec_proto = brand_div.find("span", class_="goods-name").get_text()

        data.extend({
            "brand": brand,
            "product_link": prod_link,
            "img_link": img_link,
            "description": description
        })

    return data


def get_image(url):
    data = requests.get(url, headers=HEADERS).content
    with open("source/img/{filename}.jpg", "wb", encoding="UTF-8") as file:
        file.write(data)


def parse(data: list[str]):
    encoding_data: list[dict] = []
    with ThreadPoolExecutor() as executor:
        for chunk in data:
            future = executor.submit(get_content, chunk)
            encoding_data.extend(future.result())

    return encoding_data


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_content())
    # print(len(fetching_data))
    # result = parse(fetching_data)
    # # save_to_xlsx(result, "async_result.xlsx")
    # with open("source/img_links.txt", "w", encoding="UTF-8") as file:
    #     [file.write(link) for link in img_links]
    # with open("source/prod_links.txt", "w", encoding="UTF-8") as file:
    #     [file.write(link) for link in prod_links]
