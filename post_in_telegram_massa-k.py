import os
import telebot
from config import *
import time

bot = telebot.TeleBot(API_TOKEN)

# Функция для отправки файлов
def send_files():
    base_folder = 'manuals'  # Папка, где хранятся файлы
    
    for root, dirs, files in os.walk(base_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            
            # Создаем относительный путь, убирая "manuals" и само имя файла из пути
            relative_path = os.path.relpath(root, base_folder)
            caption = relative_path
            
            try:
                with open(file_path, 'rb') as file:
                    print(f"Отправка файла '{file_name}' в чат {CHAT_ID} с thread_id {THREAD_ID}")
                    bot.send_document(CHAT_ID, file, caption=caption, message_thread_id=THREAD_ID)
                print(f"Файл '{file_name}' успешно отправлен.")
                # Добавляем задержку между отправками
                time.sleep(1)
            except telebot.apihelper.ApiException as e:
                if e.result.status_code == 429:
                    retry_after = int(e.result.json().get('parameters', {}).get('retry_after', 60))
                    print(f"Превышен лимит запросов. Повтор через {retry_after} секунд.")
                    time.sleep(retry_after)
                    # Повторяем отправку после ожидания
                    with open(file_path, 'rb') as file:
                        bot.send_document(CHAT_ID, file, caption=caption, message_thread_id=THREAD_ID)
                    print(f"Файл '{file_name}' успешно отправлен после ожидания.")
                else:
                    print(f"Не удалось отправить файл '{file_name}': {e}")
            except Exception as ex:
                print(f"Произошла ошибка: {ex}")

if __name__ == '__main__':
    send_files()
