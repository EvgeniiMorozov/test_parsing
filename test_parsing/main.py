from bs4 import BeautifulSoup
import requests


# URL = "https://www.whiskishop.com/collections/whisky-types-single-malt?page=1"
URL = "https://www.whiskishop.com/collections/whisky-types-single-malt"
# URL = "https://www.whiskishop.com/collections/scotch-whisky-highland"

HEADERS = {
    "user agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
}

HOST = "https://www.whiskishop.com"


def get_html(url, params=None):
    """
    Возвращает результат GET-запроса
    """
    return requests.get(url, headers=HEADERS, params=None)


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")

    # Задаём параметры поиска - div и  его class

    # Так не работает
    # items = soup.find_all("div", class_="product-container")
    # Так работает
    items = soup.find_all("div", class_="product-container text-left product-block")
    # Проверим, что на выходе будет
    # print(items)
    # создаём список, куда будем складывать результаты парсинга
    products = []
    for item in items:
        products.append({
            "title": item.find("h5", class_="name").get_text(strip=True),
            "cost": item.find("span", class_="money").get_text(strip=True),
            # "rating": item.find("span", class_="spr-badge").get("data-rating"),
            "review": item.found("span", class_="spr-badge-caption").get_text(strip=True),
            "link": HOST + item.find("a", class_="product-name").get("href")
        })
    # Смотрим, результат и обращаем внимание на кол-во элементов в списке. Их должно быть 9, как и карточек на экране
    print(products)
    print(len(products))
    return products


def main():
    html = get_html(URL)
    # print(html)
    # print(html.text)
    # print(html.status_code)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print(f"Что-то пошло не так! {html.status_code=}")


if __name__ == "__main__":
    main()
