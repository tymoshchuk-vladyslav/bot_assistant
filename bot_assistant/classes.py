from collections import UserDict
from datetime import date
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


class AddressBook(UserDict):
    """
    Клас книги контактів.
    Батьківський клас UserDict.
    """

    def add_record(self, record):
        self.data[record.name.value] = record

    def search_contacts(self, search_value):
        contacts = []
        for key, val in self.data.items():
            if search_value in key.lower():
                contacts.append(self.data[key])
            else:
                for phone in val.get_phones():
                    if search_value in phone:
                        contacts.append(self.data[key])

        return contacts


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

    def add_address(self, address):
        self.address.append(AddressContact(address))
        
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def get_phones(self):
        all_phones = [phone.value for phone in self.phones]
        return all_phones
    
    def get_addresses(self):
        all_address = [address.value for address in self.address]
        return all_address


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
    Адрес контакта.
    Додається до списку address, який створюється при ініціалізації класу Record.
    """
    pass
   


class EmailContact(Field):
    """
    Email контакта.
    Додається до списку email_contact, який створюється при ініціалізації класу Record.
    """
    pass


# PB = AddressBook()
# PB.add_record(Record('Tim'))
# PB['Tim'].add_phone('+380998887744')
# PB['Tim'].add_address('dfghdfgdf')
# PB.add_record(Record('Bil'))
# PB['Bil'].add_phone('+380112223344')
# PB['Bil'].add_phone('+380555555555')
# PB['Bil'].add_address('klklklkk')
# PB['Bil'].add_birthday('11.01.2000')

# print(PB['Tim'].name.value)
# print(PB['Tim'].phones[0].value)
# print(PB['Tim'].address[0].value)
# print(PB['Bil'].name.value)
# print(PB['Bil'].phones[0].value)
# print(PB['Bil'].address[0].value)
# print(PB['Bil'].phones[1].value)
# print(PB['Bil'].birthday)


# print(PB.search_contacts('44')[1].name.value)
