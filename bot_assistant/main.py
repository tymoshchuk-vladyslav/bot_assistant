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
            f"{Fore.GREEN}Введіть будь ласка команду: (або використай команду help){Style.RESET_ALL}\n").lower()
        fun, args = parser(user_input)
        # print(fun, args)
        text = fun_name(fun)(args)
        print(text)


if __name__ == "__main__":
    main()
