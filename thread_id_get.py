import telebot
from config import *



bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Напиши мне что-нибудь, и я скажу тебе chat_id и thread_id, если это тема.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    chat_id = message.chat.id
    thread_id = message.message_thread_id if hasattr(message, 'message_thread_id') else None
    bot.reply_to(message, f"Chat ID: {chat_id}, Thread ID: {thread_id}")

bot.polling()