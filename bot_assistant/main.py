from classes import AddressBook
from colorama import Fore, Style


"""
Бот помічник.
Працює з командами (help, hello, add, change, delete_user, user_add_phone, user_delete_phone, phone, show_all, 
save_data, search, good_bye, close, exit, .)
"""

PHONE_BOOK = AddressBook()




def helps():
    commands = [f'{Fore.GREEN}add{Style.RESET_ALL} - will adding new contact to you addressbook in format add: [Name][Phone]',
           f'{Fore.GREEN}change{Style.RESET_ALL} - will change one of you contact. format for change: [Name][Phone][New phone]',
           f'{Fore.GREEN}delete{Style.RESET_ALL} - will delete contact. format [name]',
           f'{Fore.GREEN}phone{Style.RESET_ALL} - will show all phone numbers of your contacts. format [name]',
           f'{Fore.GREEN}upcoming_birthday{Style.RESET_ALL} - will show you upcoming Bday in  "n" days. format [quantity of days]',
           f'{Fore.GREEN}save{Style.RESET_ALL} - will save you addressbook',
           f'{Fore.GREEN}load{Style.RESET_ALL} - will load you addressbook']

    return '\n'.join(commands)


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
