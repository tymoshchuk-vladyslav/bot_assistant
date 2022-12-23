from classes import AddressBook, Birthday
from classes import AddressBook, Record, Phone
from colorama import Fore, Style
from sort import sort_fun


"""
Бот помічник.
Працює з командами (help, hello, add, change, delete_user, user_add_phone, user_delete_phone, phone, show_all, 
save_data, search, good_bye, close, exit, .)
"""


PHONE_BOOK = AddressBook()


def add_address(name):
    """
    Функція для додавання адреси до контакту.
    :return:
    """
    name = name.title()

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    record = PHONE_BOOK[name]
    user_address = input("Введіть адресу: ")
    record.add_address(user_address)
    return f"Адрес {user_address}. Додано до контакту {name}."


def add(name, phone):

    if name in PHONE_BOOK:
        return f"{name} вже у словнику"

    record = Record(name)

    if not Phone(phone).value:
        PHONE_BOOK.add_record(record)
        return f"{name} був доданий до словника, але телефон неправильного формату"

    else:
        PHONE_BOOK.add_record(record)
        record.add_phone(name, phone, PHONE_BOOK)
        return f"{name} з телефоном {phone} було додано до словника "


def good_bye():
    quit()


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


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError, ValueError, TypeError, KeyError):
            return "Try again, please"

    return inner


def helps():
    commands = [f'{Fore.GREEN}add{Style.RESET_ALL} - will adding new contact to you addressbook in format add: [Name][Phone]',
                f'{Fore.GREEN}change{Style.RESET_ALL} - will change one of you contact. format for change: [Name][Phone][New phone]',
                f'{Fore.GREEN}delete{Style.RESET_ALL} - will delete contact. format [name]',
                f'{Fore.GREEN}phone{Style.RESET_ALL} - will show all phone numbers of your contacts. format [name]',
                f'{Fore.GREEN}upcoming_birthday{Style.RESET_ALL} - will show you upcoming Bday in  "n" days. format [quantity of days]',
                f'{Fore.GREEN}save{Style.RESET_ALL} - will save you addressbook',
                f'{Fore.GREEN}load{Style.RESET_ALL} - will load you addressbook',
                f'{Fore.GREEN}add_address{Style.RESET_ALL} - will adding new address to contact in format add_address [Name]']

    return '\n'.join(commands)


def break_f():
    """
    Коли користувач введе щось інше крім команд повертається строка про неправильний ввід команди.
    """
    return f"Wrong enter... "


USER_COMMANDS = {
    'sort': sort_fun,
    'add_address': add_address
}


def main():
    """
    Логіка роботи бота помічника
    """

    while True:
        user_input = input(
            "Введіть будь ласка команду: (або використай команду help)\n")
        result = change_input(user_input)
        print(result)
        if result == "Good Bye!":
            break


if __name__ == "__main__":
    main()
