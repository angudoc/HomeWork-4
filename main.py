import requests
from lxml import html
import csv

# URL сайта, который содержит таблицу
URL = "https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm"

# Заголовок, чтобы имитировать запрос из браузера
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

try:
    # Отправляем HTTP GET-запрос
    response = requests.get(URL, headers=HEADERS)
    response.raise_for_status()  # Проверяем успешность запроса

    # Парсим содержимое страницы как HTML
    tree = html.fromstring(response.content)

    # XPath для выбора строк таблицы (замените на подходящий путь для вашей страницы)
    rows = tree.xpath('//table//tr')

    # Проверяем, нашлись ли строки таблицы
    if not rows:
        raise ValueError("Таблица не найдена на указанной странице.")

    # Извлекаем данные таблицы
    table_data = []
    for row in rows:
        cells = row.xpath('.//th/text() | .//td/text()')  # Получаем текст из ячеек
        table_data.append([cell.strip() for cell in cells])  # Удаляем лишние пробелы

    # Проверяем, что таблица не пуста
    if len(table_data) < 2:  # Предполагаем, что первая строка — это заголовки
        raise ValueError("Данных в таблице недостаточно для сохранения.")

    # Сохраняем данные в CSV-файл
    output_file = "table_data.csv"
    with open(output_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(table_data)

    print(f"Данные успешно сохранены в файл: {output_file}")

except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении HTTP-запроса: {e}")
except ValueError as e:
    print(f"Ошибка в данных: {e}")
except Exception as e:
    print(f"Непредвиденная ошибка: {e}")
00