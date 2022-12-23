from classes import AddressBook


"""
Бот помічник.
Працює з командами (help, hello, add, change, delete_user, user_add_phone, user_delete_phone, phone, show_all, 
save_data, search, good_bye, close, exit, .)
"""

PHONE_BOOK = AddressBook()


def change_input(user_input):
    """
    Функція для обробки введених даних від користувача
    """
    new_input = user_input
    data = ''
    for key in USER_COMMANDS:
        if user_input.strip().lower().startswith(key):
            new_input = key
            data = user_input[len(new_input)+1:]
            break
    if data:
        return handler(new_input)(data)
    return handler(new_input)()


def handler(commands):
    return USER_COMMANDS.get(commands, break_f)


def helps():
    return f"Команди на які відповідає помічник: \n"\
           "help\n"\
           "good_bye, close, exit, .\n"


def break_f():
    """
    Коли користувач введе щось інше крім команд повертається строка про неправильний ввід команди.
    """
    return f"Wrong enter... "


USER_COMMANDS = {
None
}


def main():
    """
    Логіка роботи бота помічника
    """

    while True:
        user_input = input("Введіть будь ласка команду: (або використай команду help)\n")
        result = change_input(user_input)
        print(result)
        if result == "Good Bye!":
            break


if __name__ == "__main__":
    main()
