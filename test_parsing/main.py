from bs4 import BeautifulSoup
import requests


# URL = "https://www.whiskishop.com/collections/whisky-types-single-malt?page=1"
URL = "https://www.whiskishop.com/collections/whisky-types-single-malt"

HEADERS = {
    "user agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}


def get_html(url, params=None):
    response = requests.get(url, headers=HEADERS, params=None)
    print(response.status_code)
    print(response.content)
    return response


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_="product-container")
    print(items)
    # создаём список, куда будем складывать результаты парсинга
    products = []


def main():
    html = get_html(URL)
    if html == 200:
        get_content(html.text)
    else:
        print(f"Что-то пошло не так! {html.status_code=}")


if __name__ == "__main__":
    main()
