import asyncio
from random import randint
import re

from aiohttp import ClientSession
from bs4 import BeautifulSoup

HEADERS = {
    "user agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
}
HOST = "https://www.wildberries.ru"
HOST_PREF = "https:"
PROD_ID_LIST = ["21264155", "26820000", "26301070"]


# PROTO_URL = f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx?targetUrl=GP"

# Main page (Oppo, A74, 19990rub): https://images.wbstatic.net/c246x328/new/26820000/26828281-1.jpg
# Product page: slider main -      https://images.wbstatic.net/big/new/26820000/26828281-1.jpg
#               slider nav  -      https://images.wbstatic.net/tm/new/26820000/26828281-1.jpg

fetching_data = []


async def get_html(url: str, session: ClientSession):
    await asyncio.sleep(5, 15)
    async with session.get(url=url, headers=HEADERS) as response:
        if response.status != "200":
            print(f"Что-то пошло не так! {response.status}")
        print(f"Get data from --> {url}")
        response_text = await response.text()
        fetching_data.append(response_text)
        return response_text


async def fetch_content():
    async with ClientSession() as session:
        tasks = []
        for product_id in PROD_ID_LIST:
            url = f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx?targetUrl=GP"
            task = asyncio.create_task(get_html(url, session))
            tasks.append(task)

        return await asyncio.gather(*tasks)


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    header_soup = soup.find("div", class_="same-part-kt__header-wrap")
    slider_soup = soup.find("div", class_="same-part-kt__slider-wrap j-card-left-wrap")
    price_soup = soup.find("div", class_="same-part-kt__info-wrap")
    details_soup = soup.find("div", class_="product-detail__details details")

    # header_soup
    brand = header_soup.find("h1", class_="same-part-kt__header").find_next("span").get_text()

    vendor_code = soup.find("div", class_="same-part-kt__common-info").find("span", class_="hide-desktop")
    vendor_code = vendor_code.find_next("span").get_text()

    # slider_soup
    swiper_container = slider_soup.find("ul", class_="swiper-wrapper")
    img_items = swiper_container.find_all("li")
    img_links = []
    for item in img_items[:3]:
        # <img src="//images.wbstatic.net/tm/new/26820000/26828281-1.jpg" alt=" Вид 1.">
        link = item.find("div", class_="slide__content").find("img").get("src")
        image_link = re.sub(r"/tm/", "/big/", link)
        img_links.extend(image_link)

    # price_soup
    price = price_soup.find("span", class_="price-block__final-price").get_text(strip=True)

    # details_soup
    description_text = details_soup.find("p", class_="collapsable__text").get_text()
    details_table = details_soup.find("div", class_="product-params")
    table_rows = details_table.find_all("tr", class_="product-params__row")
    specification_dict = {}
    for row in table_rows:
        ...



def main():
    pass


if __name__ == '__main__':
    main()
