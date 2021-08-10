import asyncio
import csv

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from stuff import HEADERS, HOST, URL


"""
async get & fetch_content, multithread parse, save results
"""


async def get_html(session: ClientSession, page: int) -> str:
    url = URL + f"?page={page}"
    async with session.get(url=url, headers=HEADERS) as response:
        if response.status == 200:
            print(f"Получаю данные с {url}")
            return response.text()


async def fetch_content() -> list[str]:
    async with ClientSession() as session:
        response = await session.get(url=URL, headers=HEADERS)
        # Важно помнить, библиотека  BS4 не асинхронная !!!
        soup = BeautifulSoup(await response.text(), "html.parser")
        num = soup.find("li", class_="pagination_next").find_previous("li").find("a").get_text()
        pages_count = int(num) if num else 1

        tasks = []

        for page in range(1, pages_count + 1):
            task = asyncio.create_task(get_html(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    ...
