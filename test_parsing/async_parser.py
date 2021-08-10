import asyncio
import csv

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from stuff import HEADERS, HOST, URL


"""
async get & fetch_content, multithread parse, save results
"""


async def get_html(session: ClientSession, url: str) -> str:
    async with session.get(url=url, headers=HEADERS) as response:
        if response.status == 200:
            print(f"Получаю данные с {url}")
            return response.text()





if __name__ == "__main__":
    ...
