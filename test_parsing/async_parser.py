import asyncio
from concurrent.futures import ThreadPoolExecutor

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from main import save_to_xlsx
from stuff import HEADERS, HOST, URL


"""
async get-request & fetch_content, multithread parse, save results
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
        return response_text


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


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_="product-container text-left product-block")

    return [
        {
            "title": item.find("h5", class_="name").get_text(strip=True),
            "cost": item.find("span", class_="money").get_text(strip=True),
            "link": HOST + item.find("a", class_="product-name").get("href"),
        }
        for item in items
    ]


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
    print(len(fetching_data))
    result = parse(fetching_data)
    save_to_xlsx(result, "async_result.xlsx")
