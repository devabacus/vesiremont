import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# URL страницы
url = "https://www.scale.ru/support/"

# Запрос к странице
response = requests.get(url)

# Проверка успешности запроса
if response.status_code == 200:
    # Парсинг содержимого страницы
    soup = BeautifulSoup(response.content, "html.parser")

    # Поиск всех ссылок
    links = soup.find_all("a")

    # Фильтрация ссылок на PDF файлы
    pdf_links = [(link.get("href"), link.text.strip()) for link in links if link.get("href") and ".pdf" in link.get("href")]

    # Создание директории для сохранения PDF файлов
    if not os.path.exists("pdfs"):
        os.makedirs("pdfs")

    # Исключаемые слова
    excluded_words = ["описание типа", "сертификат", "Брошюра", "Буклет", "Презентация", "Свидетельство"]

    # Скачивание всех PDF файлов
    for pdf_link, link_text in pdf_links:
        # Проверка на наличие исключаемых слов
        if any(word in link_text.lower() for word in excluded_words):
            print(f"Файл '{link_text}' исключен из скачивания.")
            continue

        # Полный URL файла
        pdf_url = urljoin(url, pdf_link)

        # Формирование имени файла
        pdf_name = f"{link_text}.pdf"
        pdf_name = pdf_name.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')  # Замена недопустимых символов

        try:
            # Запрос к PDF файлу
            pdf_response = requests.get(pdf_url)
            pdf_response.raise_for_status()  # Проверка статуса ответа

            # Сохранение PDF файла
            with open(os.path.join("pdfs", pdf_name), "wb") as pdf_file:
                pdf_file.write(pdf_response.content)

            print(f"Файл '{pdf_name}' успешно скачан.")
        except requests.exceptions.RequestException as e:
            print(f"Не удалось скачать файл '{pdf_name}': {e}")

    print("Все доступные PDF файлы успешно скачаны.")
else:
    print(f"Не удалось получить доступ к странице. Код ошибки: {response.status_code}")
