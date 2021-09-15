import asyncio
from random import randint

from aiohttp import ClientSession
from bs4 import BeautifulSoup

HEADERS = {
    "user agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
}
HOST = "https://www.wildberries.ru"
HOST_PREF = "https:"


# PROTO_URL = f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx?targetUrl=GP"

# Main page (Oppo, A74, 19990rub): https://images.wbstatic.net/c246x328/new/26820000/26828281-1.jpg
# Product page: slider main -      https://images.wbstatic.net/big/new/26820000/26828281-1.jpg
#               slider nav  -      https://images.wbstatic.net/tm/new/26820000/26828281-1.jpg

async def get_html(url: str, session: ClientSession):
    await asyncio.sleep(5, 15)
    async with session.get(url=url, headers=HEADERS) as response:
        if response.status != "200":
            print(f"Что-то пошло не так! {response.status}")



def main():
    pass


if __name__ == '__main__':
    main()
