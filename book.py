book_dict = {}

def add_book(bot, message):
    def get_name(message):
        global book_dict, name
        name = message.text
        if name in book_dict:
            if book_dict[name]['link'] is None:
                link = "Не указана"
            else:
                link = f"[Кликабельная ссылка]({book_dict[name]['link']})"
            bot.send_message(message.from_user.id,
                             f"""Информация о книге {name} уже добавлена:
Ссылка: {link}
Рейтинг (из 10): {book_dict[name]['rating']}
Хотите исправить информацию?""", parse_mode="Markdown")
            bot.register_next_step_handler(message, get_y_n)
        else:
            bot.send_message(message.from_user.id, f"Вставьте ссылку на книгу {name}:")
            bot.register_next_step_handler(message, get_link)

    def get_y_n(message):
        if "ДА" in message.text.upper() or "Y" in message.text.upper():
            bot.send_message(message.from_user.id, f"Вставьте ссылку на книгу {name}:")
            bot.register_next_step_handler(message, get_link)

    def get_link(message):
        global book_dict, name
        link = message.text
        book_dict[name] = {}
        book_dict[name]['name'] = name
        book_dict[name]['link'] = None
        if 'http' in link or 'www' in link:
            book_dict[name]['link'] = link
        else:
            book_dict[name]['link'] = None
        bot.send_message(message.from_user.id, "Добавьте рейтинг (от 0 до 10):")
        bot.register_next_step_handler(message, get_rating)

    def get_rating(message):
        global book_dict, name
        book_dict[name]['rating'] = int(message.text)
        # TODO add checker
        # while book_dict[name]['rating'] is None:
        #     try:
        #         book_dict[name]['rating'] = int(message.text)
        #         break
        #     except ValueError:
        #         bot.send_message(message.from_user.id, "Рейтинг лучше ввести цифрами")
        #         bot.register_next_step_handler(message, get_rating)
        if book_dict[name]['link'] is None:
            link = "Не указана"
        else:
            link = f"[Кликабельная ссылка]({book_dict[name]['link']})"
        bot.send_message(message.from_user.id,
                         f"""Добавлена информация о книге {name}:
Ссылка: {link}
Рейтинг (из 10): {book_dict[name]['rating']}""", parse_mode="Markdown")

    bot.send_message(message.from_user.id, "Введите название книги, о которой хотите написать")
    bot.register_next_step_handler(message, get_name)


def my_books(bot, message):
    if len(book_dict) == 0:
        bot.send_message(message.from_user.id, "Информация о книгах ещё не добавлена")
    else:
        for name in book_dict:
            if book_dict[name]['link'] is None:
                link = "Не указана"
            else:
                link = f"[Кликабельная ссылка]({book_dict[name]['link']})"
            bot.send_message(message.from_user.id,
                             f"""Книге {name}:
Ссылка: {link}
Рейтинг (из 10): {book_dict[name]['rating']}""", parse_mode="Markdown")
