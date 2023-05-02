import mybot
from dictionary import *
from book import *

bot = mybot.bot

# бот будет обрабатывать только текст
@bot.message_handler(content_types=['text'])

def get_text_messages(message):
    print(f"Набрана команда {message.text}")
    if "ПРИВЕТ" in message.text.upper():
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, print_help(), parse_mode="Markdown")
    elif message.text == "/add_word":
        add_word(bot, message)
    elif message.text == "/check_translate":
        check_translate(bot, message)
    elif message.text == "/count_words":
        count_words(bot, message)
    elif message.text == "/add_book":
        add_book(bot, message)
    elif message.text == "/my_books":
        my_books(bot, message)
    elif "УРА" in message.text.upper():
        bot.send_message(message.from_user.id, "*Поздравляю!*", parse_mode="Markdown")
    elif "СПАСИБО" in message.text.upper():
        bot.send_message(message.from_user.id, "*Пожалуйста!*", parse_mode="Markdown")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

bot.polling(none_stop=True, interval=0)