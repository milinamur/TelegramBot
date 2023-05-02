import pandas as pd
import random as r

def print_help():
    text = """Я помогу тебе с изучением английских слов.

Ты можешь использовать следующие команды:

*Перевод английских слов*
/add\_word - добавить новое слово в словарь
/check\_translate - проверить себя
/count\_words - вывести количество слов в словаре

*Информация о литературе*
/add\_book - добавить информацию о книге
/my\_books - вывести информацию о литературе
"""
    return text


df = pd.read_excel('data/eng_rus_dict.xlsx', header=None, names=['eng', 'rus'])
new_words_counter = 0
properly_counter = 0
check_word_count = 0
check_list = []
index = 0

def add_word(bot, message):
    def get_eng(message):
        global word_eng
        word_eng = message.text
        if word_eng in df['eng'].tolist():
            ind = df['eng'].tolist().index(word_eng)
            translate = df.iloc[ind]['rus']
            bot.send_message(message.from_user.id,
                             f"Слово {word_eng} уже есть в словаре.\n\nЗначения: {translate}.\nХотите добавить?")
            bot.register_next_step_handler(message, get_y_n)
        else:
            bot.send_message(message.from_user.id, f"Напишите перевод слова {word_eng}:")
            bot.register_next_step_handler(message, get_rus)

    def get_y_n(message):
        if "ДА" in message.text.upper() or "Y" in message.text.upper():
            bot.send_message(message.from_user.id, f"Напишите перевод слова {word_eng}:")
            bot.register_next_step_handler(message, get_rus_exist)

    def get_rus_exist(message):
        global word_rus, word_eng
        word_rus = message.text
        ind = df['eng'].tolist().index(word_eng)
        translate = df.iloc[ind]['rus']
        df.iloc[ind]['rus'] = translate + ', ' + word_rus
        bot.send_message(message.from_user.id, f"Добавлен перевод: {word_eng} - {word_rus}")

    def get_rus(message):
        global word_rus, new_words_counter
        word_rus = message.text
        df.loc[len(df)] = [word_eng, word_rus]
        new_words_counter += 1
        bot.send_message(message.from_user.id, f"Добавлен перевод: {word_eng} - {word_rus}")

    bot.send_message(message.from_user.id, "Введите слово, которое хотите добавить в словарь:")
    bot.register_next_step_handler(message, get_eng)


def count_words(bot, message):
    count = df.shape[0]
    bot.send_message(message.from_user.id, f"Сейчас в словаре {count} слов, из них добавлено {new_words_counter}.")


def check_translate(bot, message):
    def check_counter(message):
        global properly_counter, check_word_count, index
        check_word_count = int(message.text)
        # TODO add checker
        # while check_word_count == 0:
        #     try:
        #         check_word_count = int(message.text)
        #         break
        #     except ValueError:
        #         bot.send_message(message.from_user.id, "Количество лучше ввести цифрами")
        #         bot.register_next_step_handler(message, check_counter)
        print(check_word_count)
        print_word()

    def print_word():
        global properly_counter, check_word_count, index
        if check_word_count > 0:
            index = r.randint(0, df.shape[0])
            word_eng = df.iloc[index]['eng']
            bot.send_message(message.from_user.id, f"Напишите перевод слова {word_eng}")
            check_word_count -= 1
            bot.register_next_step_handler(message, check_word)
        else:
            # print("Отвечено")
            bot.send_message(message.from_user.id, f"Правильно введено {properly_counter}")
            properly_counter = 0
            check_word_count = 0

    def check_word(message):
        global properly_counter, index
        answer = message.text
        word_rus = df.iloc[index]['rus']
        if answer.upper() in word_rus.upper():
            properly_counter += 1
            # print("Ответ верный")
        # else:
            # print("Неверно")
        print_word()

    bot.send_message(message.from_user.id, "Сколько слов хотите проверить?")
    bot.register_next_step_handler(message, check_counter)
