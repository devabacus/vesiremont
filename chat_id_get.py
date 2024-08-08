import telebot
from config import API_TOKEN



bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Напиши мне что-нибудь, и я скажу тебе chat_id.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    chat_id = message.chat.id
    bot.reply_to(message, f"Chat ID: {chat_id}")

bot.polling()
