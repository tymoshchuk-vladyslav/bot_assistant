from bot_assistant.classes import AddressBook, Birthday, Phone, Record
from colorama import Fore, Style
from bot_assistant.notes import Notes, Note, Tag, Body
from bot_assistant.sort import sort_fun
import os.path


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
    if not args:
        return "Передайте ім'я контакту та номер телефону"
    elif not args[1:]:
        return "Ви не передали номер телефону"

    name = args[0].capitalize()
    phone = args[1:][0]

    if name in PHONE_BOOK:
        return f"{name} вже у словнику"

    PHONE_BOOK.add_record(Record(name))
    PHONE_BOOK[name].add_phone(phone)
    return f"{name} was added with {phone}"


@input_error
def add_address(args):
    """
    Функція для додавання адреси до контакту.
    :return:
    """
    if not args:
        raise ValueError("Не було передано жодного аргументу, ім'я та адреси")

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
    if not args:
        return "Передайте ім'я контакту та номер телефону"

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
    
    if not args:
        return "Передайте ім'я контакту та дату"

    birthday = None
    name = args[0].capitalize()
    if args[1:]:
        birthday = args[1:][0]

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    if birthday:
        PHONE_BOOK[name].add_birthday(birthday)
        return f" {birthday} was added to {name}"
    else:
        user_birthday = input("Введіть ДН: ")
        PHONE_BOOK[name].add_birthday(user_birthday)
        return f" {user_birthday} was added to {name}"


@input_error
def add_email(args):
    """
    Функція для додавання ел. пошти до контакту.
    """
    name = None

    if not args:
        print("Не було введенно жодного аргументу...")
        name = input(f"Введіть ім'я контакту: ").capitalize()

    elif args:
        name = args[0].capitalize()

    if name not in PHONE_BOOK:
        return f" {name} імя не знайдено в адресній книзі, ви можете додайте {name} ввівши команду 'add'."

    else:
        user_email = input(f"Введіть email {name}: ")
        if user_email not in PHONE_BOOK[name].get_emails():
            PHONE_BOOK[name].add_email(user_email)
            return f"У {name} додано нову ел. пошту - {user_email}."
        else:
            return f"{name} вже має ел. адресу {user_email}"


@input_error
def change_birthday(args):
    """
    Видаляє день народження у контакта. приймає імя контакту
    """
    if not args:
        return "Передайте ім'я контакту та нову дату"
    elif not args[1:]:
        return "Ви не передали нову дату"

    name = args[0].capitalize()
    new_date = args[1:][0]

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    if PHONE_BOOK[name].birthday:
        PHONE_BOOK[name].birthday.value = new_date
        return f'{name} birthday was changing to {new_date}'
    else:
        PHONE_BOOK[name].add_birthday(new_date)
        return f'{new_date} was added to {name}'


@input_error
def del_birthday(args):
    """
    Видаляє день народження у контакта. приймає імя контакту
    """
    if not args:
        return "Передайте ім'я контакту"

    name = args[0].capitalize()

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    if PHONE_BOOK[name].birthday:
        PHONE_BOOK[name].birthday = None
        return f'{name} was deleted'
    else:
        return 'no info aobout birthday'


@input_error
def change_address(args):
    """
    Функція для редагування адреси контакту.
    :param args:
    :return:
    """
    if not args:
        raise ValueError("Не було передано ім'я контакту...")

    name = args[0].capitalize()

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
    if not args:
        return "Передайте ім'я контакту та новий номер"
    elif not args[1:]:
        return "Ви не передали новий номер телефону"
    
    name = args[0].capitalize()
    new_phone = args[1:][0]

    if name not in PHONE_BOOK:
        return f"{name} ім'я не знайдено в словнику."

    record = PHONE_BOOK[name]
    result = record.change_phone(new_phone)

    return result


@input_error
def change_email(name):
    """
    Функція для редагування електронної пошти контакту.
    """

    if not name:
        return "Не було введенно жодного аргументу..."
    
    name = name[0].title()

    if name not in PHONE_BOOK:
        return f" {name} імя не знайдено в адресній книзі, ви можете додайте {name} ввівши команду 'add'."
    else:
        record = PHONE_BOOK[name]
        user_email = input(f"Введіть нову ел. пошту {name}: ")
        result = record.change_email(user_email)
        return result


@input_error
def show_contact(args):
    """
    Функція виводить всі контакти в книзі. Якщо передано імя виведе данні по цьому контакту
    """
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

    if not args:
        return show_contact(args)
        
    result = ""
    contacts = PHONE_BOOK.search_contacts(*args)
    if contacts:
        for contact in contacts:
            name = contact.name.value
            bd = contact.birthday
            address = list(map(lambda x: str(x), contact.get_addresses()))
            all_phones = list(map(lambda x: str(x), contact.get_phones()))
            result += f"{name} with:\n Phones:{', '.join(all_phones)} \n BD: {bd} \n address: {address}\n"
        return result
    return f"no contacts with such request: {args[0]}"


@input_error
def search_birthday(args):
    """
    Функція повертає всі контакти, в яких
    ДН через days днів
    """
    if not args:
        return "Введіть будь ласка дні"

    try:
        days = int(args[0])
    except:
        return "Введіть будь ласка числове значення"

    data = PHONE_BOOK.search_contacts_birthday(days)

    if not data:
        if days > 0:
            return f"У жодного з ваших контактів немає дня народження впродовж {days} днів."
        elif days < 0:
            return f"У жодного з ваших контактів не було дня народження {days * (-1)} днів назад"

    to_return = []
    sorted_data = dict(sorted(data.items(), key=lambda x: x[1]))

    for contact in sorted_data:
        if sorted_data[contact] == 0:
            to_return.append(
                f"У {contact} сьогодні день народження")
        elif sorted_data[contact] > 0:
            to_return.append(
                f"{contact} має день народження через {data[contact]} дні")
        elif sorted_data[contact] < 0:
            to_return.append(
                f"В {contact} був день народження {data[contact] * (-1)} днів назад")

    return "\n".join(to_return)


@input_error
def delete_address(args):
    """
    Функція для видалення адреси у контакта.
    """
    if not args:
        raise ValueError("Не було введено ім'я контакту для видалення адреси.")

    name = args[0].capitalize()

    if name not in PHONE_BOOK:
        return f"{name} ім'я не знайдено у словнику"

    record = PHONE_BOOK[name]
    result = record.delete_address()

    return result


@input_error
def delete_phone(args):
    """
    функція для видалення номеру телефона
    """
    if not args:
        return "Введіть будь ласка І'мя"
    
    name = args[0].capitalize()

    if name not in PHONE_BOOK:
        return f"{name} ім'я не знайдено у словнику"

    record = PHONE_BOOK[name]
    result = record.delete_phone()

    return result


@input_error
def delete_email(name):
    """
    функція для видалення вибраної ел. пошти у контакта
    """

    if not name:
        return "Не було введенно жодного аргументу..."

    name = name[0].title()

    if name not in PHONE_BOOK:
        return f" {name} імя не знайдено в адресній книзі, ви можете додати {name} ввівши команду add."

    else:
        record = PHONE_BOOK[name]
        result = record.delete_email()
        return result


@input_error
def delete_contact(args):
    """
    Функція видалення контакта з книги
    """
    if not args:
        return "Введіть будь ласка І'мя"
    
    name = args[0].capitalize()

    if name not in PHONE_BOOK:
        return f"Контакту {name} немає у словнику."

    contact = PHONE_BOOK.delete_record(name)
    return f"{contact} був видалений з книги"


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
                f'{Fore.GREEN}change email{Style.RESET_ALL} - will change email of you contact. format for change: [Name] [New email]',
                f'{Fore.GREEN}change phone{Style.RESET_ALL} - will change old phone with new value. format for change: [Name] [New phone]',
                f'{Fore.GREEN}search contacts{Style.RESET_ALL} - will search all contacts by name or phone number. format: [searching text]',
                f'{Fore.GREEN}show contact{Style.RESET_ALL} - will show all contacts. Show without name will show all contacts. format: [searching text]',
                f'{Fore.GREEN}change birthday{Style.RESET_ALL} - will change contact Bday. format [name][new date]',   
                f'{Fore.GREEN}delete birthday{Style.RESET_ALL} - will delete contact Bday. format [name]',
                f'{Fore.GREEN}delete contact{Style.RESET_ALL} - will delete contact. format [name]',
                f'{Fore.GREEN}delete address{Style.RESET_ALL} - will delete address. format [name]',
                f'{Fore.GREEN}delete email{Style.RESET_ALL} - will delete selected contact email. format [Name] [email]',
                #f'{Fore.GREEN}phone{Style.RESET_ALL} - will show all phone numbers of your contacts. format [name]',
                f'{Fore.GREEN}search birthday{Style.RESET_ALL} - will show you upcoming Bday in  "n" days. format [quantity of days]',
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

    if not os.path.isdir("save_data"):
        os.mkdir("save_data")

    NOTES.save_notes()
    PHONE_BOOK.dump_data()

    return f"{Fore.RED}data saved{Style.RESET_ALL}"


@input_error
def load(*args):
    """
    Функція завантаження нотаток.
    """
    if os.path.isfile("save_data/save_notes.bin"):
        NOTES.load_notes()

    if os.path.isfile("save_data/save_data.bin"):
        PHONE_BOOK.load_data()

    return f"{Fore.RED}data loaded{Style.RESET_ALL}"


def parser(text):
    """
    Функція формує кортеж із назви функції і аргументів для неї.
    """

    if text:
        normalise_text = text.replace(
            "good bye", "good_bye").replace("show all", "show_all").replace("upcoming birthday", "upcoming_birthday")\
            .replace("add address", "add_address").replace("add birthday", "add_birthday")\
            .replace("add bd", "add_birthday").replace("add bday", "add_birthday")\
            .replace("search contacts", "search_contacts").replace("add phone", "add_phone")\
            .replace("change phone", "change_phone").replace("change phones", "change_phone")\
            .replace("change address", "change_address").replace("change adr", "change_address")\
            .replace("delete phone", "delete_phone").replace("del phone", "delete_phone")\
            .replace("add note", "add_note").replace("del note", "del_note").replace("delete note", "del_note")\
            .replace("change note", "change_note").replace("change tag", "change_tag")\
            .replace("sort notes", "sort_notes").replace("search notes", "search_notes").replace("search note", "search_notes")\
            .replace("search tag", "search_tag").replace("search tags", "search_tag").replace("show notes", "show_notes")\
            .replace("del birthday", "del_birthday").replace("delete birthday", "del_birthday").replace("del bd", "del_birthday")\
            .replace("delete bd", "del_birthday").replace("delete bday", "del_birthday").replace("del bday", "del_birthday")\
            .replace("add email", "add_email").replace("change email", "change_email").replace("delete email", "delete_email")\
            .replace("search birthday", "search_birthday").replace("search bd", "search_birthday")\
            .replace("show contact", "show_contact").replace("show contacts", "show_contact")\
            .replace("delete contact", "delete_contact").replace("del contact", "delete_contact")\
            .replace("delete address", "delete_address").replace("del address", "delete_address")\
            .replace("save", "save").replace("load", "load")\
            .replace("change birthday", "change_birthday").replace("change bd", "change_birthday").replace("change bday", "change_birthday")


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
        "show_contact": show_contact,
        "add_email": add_email,
        "change_email": change_email,
        "delete_email": delete_email,
        "search_birthday": search_birthday,
        "delete_contact": delete_contact,
        "delete_address": delete_address,
        "change_birthday": change_birthday
    }

    return fun_dict.get(fun, break_f)


def main():
    """
    Логіка роботи бота помічника
    """

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
