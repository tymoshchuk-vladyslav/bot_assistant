from colorama import Fore, Style
from bot_assistant.bot_logic import show_logo, load, parser, fun_name


def main():
    """
    Логіка роботи бота помічника
    """
    show_logo()
    load()

    while True:
        user_input = input(
            "Введіть будь ласка команду: (або використай команду help)\n").lower()
        fun, args = analyze_fun(user_input)
        # print(fun, '-------', args)
        text = fun_name(fun)(args)
        print(text)


if __name__ == "__main__":
    main()
