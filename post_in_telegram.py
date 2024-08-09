import os
import telebot
from config import *
import time

bot = telebot.TeleBot(API_TOKEN)

# Функция для отправки PDF файлов
def send_pdfs():
    manual_folder = 'manuals/massa'  # Папка, где хранятся PDF файлы
    for pdf_file in os.listdir(manual_folder):
            file_path = os.path.join(manual_folder, pdf_file)
            try:
                with open(file_path, 'rb') as file:
                    print(f"Отправка файла '{pdf_file}' в чат {CHAT_ID} с thread_id {THREAD_ID}")
                    bot.send_document(CHAT_ID, file, message_thread_id=THREAD_ID)
                print(f"Файл '{pdf_file}' успешно отправлен.")
                # Добавляем задержку между отправками
                time.sleep(1)
            except telebot.apihelper.ApiException as e:
                if e.result.status_code == 429:
                    retry_after = int(e.result.json().get('parameters', {}).get('retry_after', 60))
                    print(f"Превышен лимит запросов. Повтор через {retry_after} секунд.")
                    time.sleep(retry_after)
                    # Повторяем отправку после ожидания
                    with open(file_path, 'rb') as file:
                        bot.send_document(CHAT_ID, file, message_thread_id=THREAD_ID)
                    print(f"Файл '{pdf_file}' успешно отправлен после ожидания.")
                else:
                    print(f"Не удалось отправить файл '{pdf_file}': {e}")

if __name__ == '__main__':
    send_pdfs()