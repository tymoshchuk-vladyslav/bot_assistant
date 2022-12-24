from classes import AddressBook, Birthday, Phone, Record
from colorama import Fore, Style
from notes import Notes, Note, Tag, Body
from sort import sort_fun


"""
Бот помічник.
Працює з командами (help, hello, add, change, delete_user, user_add_phone, user_delete_phone, phone, show_all, 
save_data, search, good_bye, close, exit, .)
"""


PHONE_BOOK = AddressBook()
NOTES = Notes()


def input_error(func):
    """
    Декоратор хендлера помилок.
    """
    def inner(*args, **kwargs):
        try:
            result = func(*args)
        except Exception as err:
            return err
        else:
            return result

    return inner


####################################### PHONE_BOOK #################################################


@input_error
def add(args):
    """
    Функція для додавання нового контакту до книги.
    """

    name = args[0].capitalize()
    phone = args[1:][0]

    if name in PHONE_BOOK:
        return f"{name} вже у словнику"
    else:
        PHONE_BOOK.add_record(Record(name))
        PHONE_BOOK[name].add_phone(phone)

    return f"{name} was added with {phone}"


@input_error
def add_address(args):
    """
    Функція для додавання адреси до контакту.
    :return:
    """

    name = args[0].capitalize()
    address = ' '.join(args[1:])

    if name not in PHONE_BOOK:
        return f" {name} імя не знайдено в словнику"

    if address:
        PHONE_BOOK[name].add_address(address)
        return f" {address} was added to {name}"
    else:
        user_address = input("Введіть адресу: ")
        PHONE_BOOK[name].add_address(user_address)
        return f" {user_address} was added to {name}"


@input_error
def add_phone(args):
    """
    Функція для додавання телефону до контакту.
    :return:
    """

    name = args[0].capitalize()
    phone = None
    if args[1:]:
        phone = args[1:][0]

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    if phone:
        PHONE_BOOK[name].add_phone(phone)
        return f" {phone} was added to {name}"
    else:
        user_phone = input("Введіть телефон: ")
        PHONE_BOOK[name].add_phone(user_phone)
        return f" {user_phone} was added to {name}"


@input_error
def add_birthday(args):
    """
    Функція для додавання дня народження до контакту.
    :return:
    """

    name = args[0].capitalize()
    birthday = args[1:][0]
    print(name)
    print(birthday)

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    if birthday:
        PHONE_BOOK[name].add_birthday(birthday)
        return f" {birthday} was added to {name}"
    else:
        user_birthday = input("Введіть телефон: ")
        PHONE_BOOK[name].add_birthday(user_birthday)
        return f" {user_birthday} was added to {name}"


def del_birthday(args):
    '''видаляэ день народження у контакта. приймає імя контакту'''
    name = args[0].capitalize()

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    if PHONE_BOOK[name].birthday:
        PHONE_BOOK[name].birthday = None
        return f'{name} was deleted'
    else:
        return 'no info aobout birthday'


def change_address(name):
    """
    Функція для редагування адреси контакту.
    :param name:
    :return:
    """
    name = name.title()

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    record = PHONE_BOOK[name]
    user_address = input("Введіть адресу: ")
    result = record.change_address(user_address)

    if result in "У контакту немає адреси.":
        return "У контакту немає адреси."

    return f"у контакту {name} замінено адресу на: {result}"


@input_error
def change_phone(args):
    """
    Функція для заміни телефону
    """

    name = args[0].capitalize()
    new_phone = args[1:][0]

    if name not in PHONE_BOOK:
        return f"{name} ім'я не знайдено в словнику."

    record = PHONE_BOOK[name]
    result = record.change_phone(new_phone)

    return result


def show_contact(args):
    '''Функція виводить всі контакти в книзі. Якщо передано імя виведе данні по цьому контакту'''
    separate = 30*'-'
    if args:
        name = args[0].capitalize()
        return f'{separate} \n{PHONE_BOOK.get(name, "no such name")} \n{separate}'
    else:
        result = ''
        for contact in PHONE_BOOK:
            result += f'\n{PHONE_BOOK[contact]} \n{separate}'
        return result


@input_error
def search_contacts(args):
    """
    Функція для пошуку контакту.
    """
    result = ""
    contacts = PHONE_BOOK.search_contacts(*args)
    if contacts:
        for contact in contacts:
            name = contact.name.value
            bd = contact.birthday
            address = list(map(lambda x: str(x), contact.get_addresses()))
            all_phones = list(map(lambda x: str(x), contact.get_phones()))
            result += f"{name} with:\n {', '.join(all_phones)} \n BD: {bd} \n address: {address}"
        return result
    return f"no contacts with such request: {args[0]}"


@input_error
def search_birthday(args):
    """
    Функція повертає всі контакти, в яких
    ДН через days днів
    """
    days = int(args[0])

    data = PHONE_BOOK.search_contacts_birthday(days)

    search_date = data['search_date']
    contacts = data['contacts']

    if not contacts:
        return f"У жодного з ваших контактів немає дня народження через {days} днів {search_date} числа."

    contacts_string = ", ".join(contacts)

    return f"{contacts_string} мають день народження через {days} днів {search_date} числа."


@input_error
def delete_phone(args):
    """
    функція для видалення номеру телефона
    """

    name = args[0].capitalize()

    if name not in PHONE_BOOK:
        return f"{name} ім'я не знайдено у словнику"

    record = PHONE_BOOK[name]
    result = record.delete_phone()

    return result


def good_bye(*args):
    """
    Функція для завершення роботи бота.
    """
    save()
    print("See you latter")
    quit()


def helps(*args):
    """
    Функція повертає список команд на які реагує бот.
    """

    commands = [f'{Fore.GREEN}add{Style.RESET_ALL} - will adding new contact to you addressbook in format add: [Name][Phone]',
                f'{Fore.GREEN}add phone{Style.RESET_ALL} - will adding phone to contact in format add: [Name] [Phone]',
                f'{Fore.GREEN}add address{Style.RESET_ALL} - will adding new address to contact in format: [Name] [address]',
                f'{Fore.GREEN}add email{Style.RESET_ALL} - will adding new address to contact in format: [Name] [email]',
                f'{Fore.GREEN}add birthday{Style.RESET_ALL} - will adding new address to contact in format: [Name] [birthday]',
                f'{Fore.GREEN}change address{Style.RESET_ALL} - will change address of you contact. format for change: [Name] [New address]',
                f'{Fore.GREEN}search contacts{Style.RESET_ALL} - will search all contacts by name or phone number. format: [searching text]',
                f'{Fore.GREEN}show contact{Style.RESET_ALL} - will show all contacts. Show without name will show all contacts. format: [searching text]',
                f'{Fore.GREEN}delete birthday{Style.RESET_ALL} - will delete contact Bday. format [name]',
                #f'{Fore.GREEN}phone{Style.RESET_ALL} - will show all phone numbers of your contacts. format [name]',
                #f'{Fore.GREEN}upcoming_birthday{Style.RESET_ALL} - will show you upcoming Bday in  "n" days. format [quantity of days]',
                f'{Fore.GREEN}save{Style.RESET_ALL} - will save you addressbook and notes',
                f'{Fore.GREEN}load{Style.RESET_ALL} - will load you addressbook and notes',
                f'{Fore.GREEN}sort{Style.RESET_ALL} - will make magik and sort you files. Give only dir ;)',

                f'{Fore.BLUE}add note{Style.RESET_ALL} - will adding new note',
                f'{Fore.BLUE}del note{Style.RESET_ALL} - will delete note. format: [record number]',
                f'{Fore.BLUE}change note{Style.RESET_ALL} - will changing note. format: [record number] [new text]',
                f'{Fore.BLUE}change tag{Style.RESET_ALL} - will add or delete tag to you note',
                f'{Fore.BLUE}show notes{Style.RESET_ALL} - will show you all notes',
                f'{Fore.BLUE}sort notes{Style.RESET_ALL} - will show you note with sort. 1/-1 to asc/desc sorting',
                f'{Fore.BLUE}search notes{Style.RESET_ALL} - will searching note for you by text',
                f'{Fore.BLUE}search tag{Style.RESET_ALL} - will searching note for you by tag',

                f'{Fore.RED}good_bye{Style.RESET_ALL} - for exit',
                ]

    return '\n'.join(commands)


def break_f(*args):
    """
    Коли користувач введе щось інше крім команд повертається строка про неправильний ввід команди.
    """
    return f"Wrong enter... Try Help"


####################################### NOTES #################################################


@input_error
def add_note(*args):
    """
    Функція викликає окремій юзерінпут і створює Нотатку з тегами.
    """

    while True:
        body = input("Введіть текст нотатки:\n")
        if not body:
            print("введіть текст або оберіть cansel")
        elif body == "cansel":
            return
        else:
            break

    while True:
        tag = input("додайте теги:\n")
        if not tag:
            print("введіть текст або оберіть cansel")
        elif tag == "cansel":
            return
        else:
            break

    NOTES.add_record(Note(tag, body))

    return "Нотатку створено"


@input_error
def del_note(args):
    """
    На вході приймає номери нотатків які треба видалити, при наявності таких видаляє.
    """
    number = args
    print(number)
    del_numbers = []
    for i in number:
        try:
            del NOTES[int(i)-1]  # нотатки виводятся з 1
        except IndexError:
            print(f"немає нотатки з таким номером {int(i)}")
        else:
            del_numbers.append(int(i)-1)

    return f"нотатки {del_numbers} були видалені"


@input_error
def change_note(args):
    """
    Приймає номер нотатку і новий текст. міняє.
    """

    number = int(args[0])
    new_text = ' '.join(args[1:])

    if not new_text:
        new_text = input("Введіть новий текст:\n")

    NOTES.cahange_note_text(number-1, new_text)  # нотатки виводятся з 1

    return f"Нотатка №{number} була змінена"


@input_error
def change_tag(args):
    """Функція дізнається у користувача що саме він хоче зробити, додати чи видалити тег, номер і тег.
    Відповідно до вибору видалить чи додасть тег до обранної нотатки."""

    while True:
        action = input("Оберіть дію add/del:\n")
        print(action)
        if action == "cancel":
            return
        elif not action or action not in ['add', 'del']:
            print("не коректне значення, для того щоб відмінити дію - оберіть cancel")
        else:
            break

    while True:
        number = input("Введіть номер нотатки:\n")
        if number == "cancel":
            return
        elif not number or not number.isdigit():
            print("не коректне значення, для того щоб відмінити дію - оберіть cancel")
        else:
            break

    while True:
        tag = input("Введіть новий тег:\n")
        if tag == "cancel":
            return
        elif not tag:
            print("не коректне значення, для того щоб відмінити дію - оберіть cancel")
        else:
            break

    if action == "add":
        NOTES[int(number) - 1].add_tag(tag)
    else:
        NOTES[int(number) - 1].del_tag(tag)


@input_error
def sort_notes(args):
    """
    Функція для сортування нотаток.
    """
    if args:
        number = int(args[0])
        if number not in [1, -1]:
            return "1 чи порожньо для сортування, -1 для зворотнього сортування"
        return NOTES.sort_notes(number)
    else:
        return NOTES.sort_notes()


def show_notes(args):
    return NOTES.get_notes()


@input_error
def search_notes(args):
    """
    Функція для пошуку нотатки.
    """
    text = ' '.join(args)
    return NOTES.search(text)


@input_error
def search_tag(args):
    """
    Функція для пошуку нотатки за тегом.
    """

    search_args = args

    if search_args:
        result = ""
        for i in search_args:
            print(i)
            result += NOTES.search_by_tag(i)
        if result:
            return result
        else:
            return "нотаток не виявлено"
    else:
        return "ви не вибрали жотдного тегу"


@input_error
def save(*args):
    """
    Функція збереження нотаток.
    """
    NOTES.save_notes()
    ####### тут місце під сейв адресбуку  ########

    return "saved"


@input_error
def load(*args):
    """
    Функція завантаження нотаток.
    """
    NOTES.load_notes()

    ####### тут місце під лоад адресбуку  ########

    return "loaded"


def parser(text):
    """
    Функція формує кортеж із назви функції і аргументів для неї.
    """

    if text:
        normalise_text = text.replace(
            "good bye", "good_bye").replace("show all", "show_all").replace("upcoming birthday", "upcoming_birthday")\
            .replace("add address", "add_address").replace("add birthday", "add_birthday")\
            .replace("add bd", "add_birthday").replace("add bday", "add_birthday").replace("add email", "add_email")\
            .replace("search contacts", "search_contacts").replace("add phone", "add_phone")\
            .replace("change phone", "change_phone").replace("change phones", "change_phone")\
            .replace("delete phone", "delete_phone").replace("del phone", "delete_phone")\
            .replace("add note", "add_note").replace("del note", "del_note").replace("delete note", "del_note")\
            .replace("change note", "change_note").replace("change tag", "change_tag")\
            .replace("sort notes", "sort_notes").replace("search notes", "search_notes").replace("search note", "search_notes")\
            .replace("search tag", "search_tag").replace("search tags", "search_tag").replace("show notes", "show_notes")\
            .replace("del birthday", "del_birthday").replace("delete birthday", "del_birthday").replace("del bd", "del_birthday")\
            .replace("delete bd", "del_birthday").replace("delete bday", "del_birthday").replace("del bday", "del_birthday")\
            .replace("show contact", "show_contact").replace("show contacts", "show_contact")

        # формуємо кортеж із назви функції і аргументів для неї
        return normalise_text.split()[0], normalise_text.split()[1:]


def fun_name(fun):
    """
    Хендлер команд від користувача.
    """

    fun_dict = {
        "hello": helps,
        "help": helps,
        "good_bye": good_bye,
        "close": good_bye,
        "exit": good_bye,
        "add": add,
        "add_phone": add_phone,
        "add_address": add_address,
        "add_birthday": add_birthday,
        "del_birthday": del_birthday,
        "change_address": change_address,
        "search_contacts": search_contacts,
        "sort": sort_fun,
        "add_note": add_note,
        "del_note": del_note,
        "change_note": change_note,
        "change_tag": change_tag,
        "sort_notes": sort_notes,
        "show_notes": show_notes,
        "search_notes": search_notes,
        "search_tag": search_tag,
        "save": save,
        "load": load,
        "change_phone": change_phone,
        "delete_phone": delete_phone,
        "show_contact": show_contact
    }

    return fun_dict.get(fun, break_f)


def main():
    """
    Логіка роботи бота помічника
    """

    while True:
        user_input = input(
            "Введіть будь ласка команду: (або використай команду help)\n").lower()
        fun, args = parser(user_input)
        # print(fun, args)
        text = fun_name(fun)(args)
        print(text)


if __name__ == "__main__":
    main()
