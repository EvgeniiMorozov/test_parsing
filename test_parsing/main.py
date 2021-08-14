import csv

from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
import requests
from stuff import HEADERS, HOST, URL


def get_html(url, params=None):
    """
    Возвращает результат GET-запроса
    """
    return requests.get(url, headers=HEADERS, params=None)


def get_pages_count(html):
    """
    Возвращает номер последней страницы

    В объекте супа ищем тэг li с классом pagination_next и записываем в переменную,
    затем с помощью метода find_previous() находим, предыдущий тэг li и извлекаем из него текст,
    преобразуем в число и подаём на выход функции
    """
    soup = BeautifulSoup(html, "html.parser")
    item = soup.find("li", class_="pagination_next").find_previous("li")
    # print(item)
    num = item.find("a").get_text()
    # print(num)
    return int(num) if num else 1


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")

    # Задаём параметры поиска - div и  его class
    # Так не работает
    # items = soup.find_all("div", class_="product-container")
    # Так работает (надо задавать полное имя класса)
    items = soup.find_all("div", class_="product-container text-left product-block")
    """
    Метод find_all() отдает список строк и ниже по этому списку мы будем итерировать
    """
    # print(items)
    products = []
    for item in items:
        """
        Список items представляет собой список строк, каждая строка это контент из определённой карточки товара.
        В каждой строке мы ищем интересующую нас информацию и записываем в отдельный словарь, далее этот словарь
        складываем результирующий список.
        """
        products.append(
            {
                "title": item.find("h5", class_="name").get_text(strip=True),
                "cost": item.find("span", class_="money").get_text(strip=True),
                # "rating": item.find("span", class_="spr-badge").get("data-rating"),
                # "review": item.found("span", class_="spr-badge-caption").get_text(strip=True),
                "link": HOST + item.find("a", class_="product-name").get("href"),
            }
        )
    # Смотрим, результат и обращаем внимание на кол-во элементов в списке. Их должно быть 9, как и карточек на экране
    # print(products)
    # print(len(products))
    return products


def save_file(data: list, filename: str):
    """
    Сохраняет данные в csv-формате
    """
    with open(filename, "w", encoding="UTF-8", newline="") as file:
        # Чтоб полученный открылся в Exel`е, не обходимо указать разделитель ';'
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Наименование", "Цена в фунтах", "Ссылка"])
        for item in data:
            writer.writerow([item["title"], item["cost"], item["link"]])


def save_to_xlsx(data: list, filename: str):
    # создаём объект книги Excel
    book = Workbook()
    # выбираем лист книги
    sheet = book.active
    # "обзываем" его
    sheet.title = "Parse_results"
    # Делаем оглавление шапки таблицы результатов
    sheet["A1"] = "Наименование"
    sheet["B1"] = "Цена в фунтах"
    sheet["C1"] = "Ссылка на продукт"

    # заполняем таблицу данными
    for row, chunk in enumerate(data, start=2):
        sheet[row][0].value = chunk["title"]
        sheet[row][1].value = chunk["cost"]
        sheet[row][2].value = chunk["link"]

    # сохраняем файл
    book.save(filename)
    # закрываем книгу Excel
    book.close()





def main():
    html = get_html(URL)
    # print(html)
    # print(html.text)
    # print(html.status_code)

    if html.status_code == 200:
        result = []
        pages = get_pages_count(html.text)

        for page in range(1, pages + 1):
            print(f"Парсим страницу {page} из {pages}...")
            # Для каждой страницы формируем url-ссылку
            url = URL + f"?page={page}"
            html = get_html(url)
            print(html.url)
            result.extend(get_content(html.text))

        print(f"Получено {len(result)} наименований")

        # Сохраняем результаты
        save_file(result, "result_csv.csv")
        save_to_xlsx(result, "result_excel.xlsx")
    else:
        print(f"Что-то пошло не так! {html.status_code=}")


if __name__ == "__main__":
    main()
