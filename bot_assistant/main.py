from classes import AddressBook, Birthday, Phone, Record
from colorama import Fore, Style
from notes import Notes, Note
from sort import sort_fun


"""
Бот помічник.
Працює з командами (help, hello, add, change, delete_user, user_add_phone, user_delete_phone, phone, show_all, 
save_data, search, good_bye, close, exit, .)
"""


PHONE_BOOK = AddressBook()
NOTES = Notes()


def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args)
        except Exception as err:
            return err
        else:
            return result

    return inner
#################################

    
        


@input_error
def add(args):
  
    name = args[0].capitalize()
    phone = args[1:][0]
    
    if name in PHONE_BOOK:
        return f"{name} вже у словнику"
    else:
        PHONE_BOOK.add_record(Record(name))
        PHONE_BOOK[name].add_phone(phone)
    
    return f'{name} was added with {phone}'
    

@input_error
def add_address(args):
    """
    Функція для додавання адреси до контакту.
    :return:
    """

    name = args[0].capitalize()
    address = ' '.join(args[1:])
    

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    if address:
        PHONE_BOOK[name].add_address(address)
        return f' {address} was added to {name}'
    else:
        user_address = input("Введіть адресу: ")
        PHONE_BOOK[name].add_address(user_address)
        return f' {user_address} was added to {name}'
    

@input_error
def add_phone(args):
    """
    Функція для додавання телефону до контакту.
    :return:
    """

    name = args[0].capitalize()
    phone = args[1:][0]
    print(name)
    print(phone)


    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    if phone:
        PHONE_BOOK[name].add_phone(phone)
        return f' {phone} was added to {name}'
    else:
        user_phone = input("Введіть телефон: ")
        PHONE_BOOK[name].add_phone(user_phone)
        return f' {user_phone} was added to {name}'


@input_error
def add_birthday(args):
    """
    Функція для додавання телефону до контакту.
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
        return f' {birthday} was added to {name}'
    else:
        user_birthday = input("Введіть телефон: ")
        PHONE_BOOK[name].add_birthday(user_birthday)
        return f' {user_birthday} was added to {name}'


@input_error
def search_contacts(args):
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


def good_bye(*args):
    print('See you latter')
    quit()
    

def helps(*args):
    commands = [f'{Fore.GREEN}add{Style.RESET_ALL} - will adding new contact to you addressbook in format add: [Name][Phone]',
                f'{Fore.GREEN}change{Style.RESET_ALL} - will change one of you contact. format for change: [Name][Phone][New phone]',
                f'{Fore.GREEN}delete{Style.RESET_ALL} - will delete contact. format [name]',
                f'{Fore.GREEN}phone{Style.RESET_ALL} - will show all phone numbers of your contacts. format [name]',
                f'{Fore.GREEN}upcoming_birthday{Style.RESET_ALL} - will show you upcoming Bday in  "n" days. format [quantity of days]',
                f'{Fore.GREEN}save{Style.RESET_ALL} - will save you addressbook',
                f'{Fore.GREEN}load{Style.RESET_ALL} - will load you addressbook',
                f'{Fore.GREEN}add_address{Style.RESET_ALL} - will adding new address to contact in format add_address [Name]']

    return '\n'.join(commands)







def break_f(*args):
    """
    Коли користувач введе щось інше крім команд повертається строка про неправильний ввід команди.
    """
    return f"Wrong enter... Try Help"

####################################### NOTES #################################################


@input_error
def add_note(*args):
    ''' Функція викликає окремій юзерінпут і створює Нотатку з тегами'''
    while True:
        body = input('Введіть текст нотатки:\n')
        if not body:
            print('введіть текст або оберіть cansel')
        elif body == 'cansel':
            return
        else:
            break
    
    while True:
        tag = input('додайте теги:\n')
        if not tag:
            print('введіть текст або оберіть cansel')
        elif tag == 'cansel':
            return
        else:
            break
    
 
    NOTES.add_record(Note(tag, body))
    return 'Нотатку створено'
 

@input_error
def del_note(args):
    '''на вході приймає номери нотатків які треба видалити, при наявності таких видаляє'''
    number = args
    print(number)
    del_numbers = []
    for i in number:
        try:
            del NOTES[int(i)-1] # нотатки виводятся з 1
        except IndexError:
            print(f'немає нотатки з таким номером {int(i)}')
        else:
            del_numbers.append(int(i)-1)
    
    return f'нотатки {del_numbers} були видалені'
           

@input_error
def change_note(args):
    '''приймає номер нотатку і новий текст. міняє'''
    number = int(args[0])
    new_text = ' '.join(args[1:])
    if not new_text:
        new_text = input('Введіть новий текст:\n')
        
    NOTES.cahange_note_text(number-1, new_text) #нотатки виводятся з 1
    return f'Нотатка №{number} була змінена'


@input_error
def change_tag(args):
    '''функція дізнається у користувача що саме він хоче зробити, додати чи видалити тег, номер і тег. 
    відповідно до вибору видалить чи додасть тег до обранної нотатки '''
    while True:
        action = input('Оберіть дію add/del:\n')
        print(action)
        if action == 'cancel':
            return
        elif not action or action not in ['add', 'del']:
            print('не коректне значення, для того щоб відмінити дію - оберіть cancel')
        else:
            break

    while True:
        number = input('Введіть номер нотатки:\n')
        if number == 'cancel':
            return
        elif not number or not number.isdigit():
            print('не коректне значення, для того щоб відмінити дію - оберіть cancel')
        else:
            break

    while True:
        tag = input('Введіть новий тег:\n')
        if tag == 'cancel':
            return
        elif not tag:
            print('не коректне значення, для того щоб відмінити дію - оберіть cancel')
        else:
            break

    if action == 'add':
        NOTES[int(number) - 1].add_tag(tag)
    else:
        NOTES[int(number) - 1].del_tag(tag)
    

@input_error
def sort_notes(args):
    if args:
        number = int(args[0])
        if number not in [1, -1]:
            return '1 чи порожньо для сортування, -1 для зворотнього сортування'
        return NOTES.sort_notes(number)
    else:
        return NOTES.sort_notes()
    
 
    
def parser(text):
    if text:
        normalise_text = text.replace(
            "good bye", "good_bye").replace("show all", "show_all").replace("upcoming birthday", "upcoming_birthday")\
            .replace("add address", "add_address").replace("add birthday", "add_birthday")\
            .replace("add bd", "add_birthday").replace("add bday", "add_birthday").replace("add email", "add_email")\
            .replace("search contacts", "search_contacts").replace('add phone', 'add_phone')\
            .replace('add note', 'add_note').replace('del note', 'del_note').replace('delete note', 'del_note')\
            .replace('change note', 'change_note').replace('change tag', 'change_tag')\
            .replace('sort notes', 'sort_notes').replace('search notes', 'search_notes').replace('search tag', 'search_tag')
        # формуємо кортеж із назви функції і аргументів для неї
        return normalise_text.split()[0], normalise_text.split()[1:]
    
def fun_name(fun):
    fun_dict = {
        "hello": helps,
        "help": helps,
        "good_bye": good_bye,
        "close": good_bye,
        "exit": good_bye,
        'add': add,
        'add_phone': add_phone,
        'add_address': add_address,
        'add_birthday': add_birthday,
        'search_contacts': search_contacts,
        'sort': sort_fun,
        'add_note': add_note,
        'del_note': del_note,
        'change_note': change_note,
        'change_tag': change_tag,
        'sort_notes': sort_notes,
        
        # 'search_notes': search_notes,
        # 'search_tag': search_tag
        

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
        print(fun, args)
        text = fun_name(fun)(args)
        print(text)
        
       


if __name__ == "__main__":
    main()
