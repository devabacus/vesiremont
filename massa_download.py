import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests

# Настройка Selenium и запуск браузера
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

main_page = 'https://massa.ru'

# Переход на страницу с документами
documents_url = 'https://massa.ru/support/documents/'

# Ввод логина и пароля
username = 'massa'
password = 'slcte489'

driver.get(documents_url)
time.sleep(2)  # Ожидание загрузки страницы

driver.find_element(By.NAME, 'USER_LOGIN').send_keys(username)
driver.find_element(By.NAME, 'USER_PASSWORD').send_keys(password)
driver.find_element(By.NAME, 'USER_PASSWORD').send_keys(Keys.RETURN)

# Ожидание после авторизации
time.sleep(3)

# Получение HTML-кода страницы
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Получение cookies
cookies = driver.get_cookies()
driver.quit()

# Найти все ссылки на категории
category_links = soup.find_all('a', href=True)
category_links = [(link.text.strip().replace('/', '_'), link['href']) for link in category_links if '/support/documents/' in link['href']]

# Создание основной папки для документации
base_path = 'manuals/massa'
os.makedirs(base_path, exist_ok=True)

# Начало сессии requests для скачивания файлов
session = requests.Session()

# Установка заголовков
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Referer': documents_url
}

for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])

# Скачивание файлов из каждой категории
for category_name, category_url in category_links:
    # Создание папки для категории
    category_path = os.path.join(base_path, category_name)
    os.makedirs(category_path, exist_ok=True)
    
    # Запрос страницы категории
    full_url = main_page + category_url
    category_response = session.get(full_url, headers=headers)
    
    if category_response.status_code != 200:
        print(f"Не удалось получить доступ к {full_url}")
        continue
    
    category_soup = BeautifulSoup(category_response.content, 'html.parser')
    
    # Найти блок div с классом 'card-group group'
    div_block = category_soup.find('div', class_='card-group group')
    
    if div_block:
        # Найти все ссылки на файлы в этом блоке
        file_links = div_block.find_all('a', href=True)
        file_links = [(link.text.strip(), main_page + link['href'] if link['href'].startswith('/') else link['href']) for link in file_links]
        
        for file_name, link in file_links:
            # Определение расширения файла из ссылки
            file_extension = os.path.splitext(link)[1]
            
            # Удаление недопустимых символов из имени файла
            safe_file_name = file_name.replace('/', '_').replace('\\', '_').replace(' ', '_')
            filename = os.path.join(category_path, f"{safe_file_name}{file_extension}")
            
            # Скачивание файла
            file_response = session.get(link, headers=headers)
            
            if file_response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(file_response.content)
                
                print(f"Скачан файл: {filename}")
            else:
                print(f"Не удалось скачать файл: {link}")
    else:
        print(f"Блок с классом 'card-group group' не найден на странице {full_url}")

print("Скачивание завершено")
          