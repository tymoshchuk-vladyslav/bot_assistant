from collections import UserDict
from colorama import Fore, Style
from datetime import date, timedelta
from pickle import load, dump
import re


"""
Класи бота помічника.
Record
AddressBook(UserDict)
Field
Name(Field)
Phone(Field)
Birthday(Field)
AddressContact(Field)
EmailContact(Field)
"""


class SaveData:
    """
    Клас який відповідає за сереалізацію та десереалізацію.
    """

    def __init__(self, data, path):
        self.data = data
        self.path = path

    def dump_data(self, data, path):
        """
        Метод для сереалізації даних в файл path за допомогою pickle.
        """
        self.data = data
        self.path = path

        with open(self.path, "wb") as file:
            dump(self.data, file)

    def load_data(self, path):
        """
        Метод для десереалізації даних з файлу path за допомогою pickle.
        """

        self.path = path

        with open(self.path, "rb") as file:
            new_data = load(file)
            return new_data


class AddressBook(UserDict, SaveData):
    """
    Клас книги контактів.
    Батьківський клас UserDict.
    """

    def add_record(self, record):
        """
        Додавання нового запису до книги.
        """
        self.data[record.name.value] = record

    def delete_record(self, name):
        """
        Метод для видалення запису з книги
        """
        deleted = self.data.pop(name)
        return deleted.name.value

    def search_contacts(self, search_value):
        """
        Метод для пошуку контактів серед книги.
        """

        contacts = []
        for key in self.data:
            val = self.data[key]
            if search_value[0] in key.lower():
                contacts.append(self.data[key])

            else:
                for phone in val.phones:
                    if search_value[0] in phone.value:
                        contacts.append(self.data[key])

        return contacts

    def search_contacts_birthday(self, days):
        """
        Метод, який шукає контакти в адресній книзі,
        в яких день народження через задану кулькість днів
        """
        contacts_with_birthday = []

        for contact in self.data:
            if self.data[contact].birthday:
                contacts_with_birthday.append(self.data[contact])

        today = date.today()
        contacts_to_return = {}

        if days >= 0:
            for contact in contacts_with_birthday:
                birthday_value = str(contact.birthday.value)
                splitted = birthday_value.split("-")
                counter = 0
                while counter != days + 1:
                    reference_date = today + timedelta(days=counter)
                    if date(year=reference_date.year, month=int(splitted[1]), day=int(splitted[2])) == reference_date:
                        contacts_to_return[contact.name.value] = counter
                        break
                    else:
                        counter += 1
                        continue
        elif days < 0:
            for contact in contacts_with_birthday:
                birthday_value = str(contact.birthday.value)
                splitted = birthday_value.split("-")
                counter = -1
                while counter != days - 1:
                    reference_date = today + timedelta(days=counter)
                    if date(year=reference_date.year, month=int(splitted[1]), day=int(splitted[2])) == reference_date:
                        contacts_to_return[contact.name.value] = counter
                        break
                    else:
                        counter -= 1
                        continue

        return contacts_to_return


class Record:
    """
    Клас Record, який відповідає за логіку додавання/видалення/редагування необов'язкових полів та зберігання
    обов'язкового поля Name.
    При ініціалізації класу створюється ім'я класу Name, та список номерів телефоні, в який будуть записані номери
    телефонів класу Phone. Поле Birthday створюється пустим, поле Email створюється порожній список в якому будуть
    екземпляри класу EmailContact, поле
    """

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.address = []
        self.birthday = None
        self.email_list = []

    def __str__(self):
        return f'{Fore.BLUE}    Name:{Style.RESET_ALL}{self.name.value} \n' \
               f'{Fore.BLUE}  Phones:{Style.RESET_ALL}{self.get_information(self.phones)} \n' \
               f'{Fore.BLUE} Address:{Style.RESET_ALL}{self.get_information(self.address)} \n' \
               f'{Fore.BLUE}Birthday:{Style.RESET_ALL}{self.birthday} \n' \
               f'{Fore.BLUE}   Email:{Style.RESET_ALL}{self.get_information(self.email_list)}'

    @staticmethod
    def add_information(list_info, field):
        """
        Метод для додавання інформації до списків phones, address, email_list.
        """
        list_info.append(field)

    def add_birthday(self, birthday):
        """
        Метод для додавання дн до рекорду.
        Додається як екземпляр класу Birthday.
        """
        self.birthday = Birthday(birthday)

    @staticmethod
    def get_information(field):
        """
        Метод для повернення списку відповідно переданого поля.
        """
        all_info = [info.value for info in field]
        return all_info

    @staticmethod
    def change_information(new_info, field):
        """
        Метод для редагування phone, address, email.
        """
        if not field:
            return f"У контакту немає адреси."

        elif len(field) == 1:
            field[0] = new_info
            return f"{new_info}"

        elif len(field) > 1:
            i = -1
            print(f"Виберіть адресу контакту для редагування.")
            for f in field:
                i += 1
                print(f"№  {i}  :  {f.value}")
            inp_user = int(input(f"Введіть №..."))

            if inp_user not in range(0, i + 1):
                raise ValueError("Такого номеру немає в списку адрес.")

            field[inp_user] = new_info
            return f"{new_info.value}"

    def delete_information(self, field):
        """
        Метод для видалення адреси у контакту.
        """
        if not field:
            return f"{self.name.value} не має даних"

        if len(field) == 1:
            info_to_delete = field.pop(0)
            return f"Значення: {info_to_delete.value}, був видалений для контакту {self.name.value}"

        else:
            i = -1
            print("Виберіть з списку що хочете видалити")
            for f in field:
                i += 1
                print(f"№ {i} : {f.value}")
            inp_user = int(input(f"Введіть №..."))

            if inp_user not in range(0, i + 1):
                raise ValueError("Такого номеру немає в списку.")

            info_to_delete = field.pop(inp_user)
            return f"Значення: {info_to_delete.value}, був видалений для контакту {self.name.value}"


class Field:
    """
    Батьківський клас для Name, Phone, Birthday, AddressContact, EmailContact.
    """

    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        """getter
        повертає значення self.__value"""
        return self.__value

    @value.setter
    def value(self, new_value):
        """
        setter
        змінює значення self.__value
        """
        self.__value = new_value


class Name(Field):
    """
    Ім'я контакта.
    """
    pass


class Phone(Field):
    """
    Номер телефону контакта.
    Додається до списку phones, який створюється при ініціалізації класу Record.
    """

    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        """
        setter, щоб
        номер телефону був такого формату
        +380000000000
        """
        check_match = re.search(r"\+\d{12}", new_value)
        if not check_match:
            raise Exception("phone must be in +380CCXXXXXXX format")
        else:
            self.__value = new_value


class Birthday(Field):
    """
    День народження контакта.
    Додається до списку birthday, який створюється при ініціалізації класу Record.
    """

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if re.search(r"\b\d{2}[.]\d{2}[.]\d{4}", value):
            value_splitted = value.split(".")
            self.__value = date(year=int(value_splitted[2]), month=int(
                value_splitted[1]), day=int(value_splitted[0]))
        else:
            raise Exception("Birthday must be in DD.MM.YYYY format")

    def __str__(self) -> str:
        return self.__value.strftime("%d.%m.%Y")


class AddressContact(Field):
    """
    Адрес контакту.
    Додається до списку address, який створюється при ініціалізації класу Record.
    """

    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if not new_value:
            raise ValueError("Адрес не повинен бути пустий...")
        self.__value = new_value


class EmailContact(Field):
    """
    Email контакту.
    Додається до списку email_contact, який створюється при ініціалізації класу Record.
    """

    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        """
        EmailContact setter.
        """
        if not re.findall(r"\b[A-Za-z][\w+.]+@\w+[.][a-z]{2,3}", value):
            raise ValueError(
                '''Невірний формат ел. пошти. 
                 Приклад вводу - "****@ukr.net"
                 ''')
        self.__value = value
