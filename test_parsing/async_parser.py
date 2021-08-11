import asyncio
from concurrent.futures import ThreadPoolExecutor
import csv
from typing import Coroutine

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from stuff import HEADERS, HOST, URL
from main import get_content, save_file


"""
async get & fetch_content, multithread parse, save results
"""
fetching_data: list[str] = []

async def get_html(session: ClientSession, page: int):
    url = URL + f"?page={page}"
    async with session.get(url=url, headers=HEADERS) as response:
        if response.status != 200:
            print(f"Что-то пошло не так! {response.status=}")
        print(f"Получаю данные с {url}")
        response_text = await response.text()
        fetching_data.append(response_text)


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

        return await asyncio.gather(*tasks)


def parse(data: list[str]):
    encoding_data: list[dict] = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        future = executor.submit(get_content([chunk for chunk in data]))
        encoding_data.extend(future.result())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_content())
    print(len(fetching_data))
    result = parse(fetching_data)
    print(result)
