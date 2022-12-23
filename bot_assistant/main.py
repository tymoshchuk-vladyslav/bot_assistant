from classes import AddressBook


"""
Бот помічник.
Працює з командами (help, hello, add, change, delete_user, user_add_phone, user_delete_phone, phone, show_all, 
save_data, search, good_bye, close, exit, .)
"""


def input_error(func):
    """Декоратор для обробки помилок користувача"""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError, ValueError, TypeError, KeyError):
            return "Try again, please"

    return inner


PHONE_BOOK = AddressBook()


def helps():
    return f"Команди на які відповідає помічник: \n"\
           "help\n"\
           "good_bye, close, exit, .\n"


USER_COMMANDS = {
    None
}


def main():
    """
    Логіка роботи бота помічника
    """

    pass


if __name__ == "__main__":
    main()
