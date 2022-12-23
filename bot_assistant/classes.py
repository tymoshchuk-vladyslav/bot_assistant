from collections import UserDict
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

    def add_address(self, address):
        """
        Метод для додавання нового адресу до рекорда.
        :param address:
        :return:
        """
        self.address.append(AddressContact(address))

    def change_address(self, address):
        """
        Метод для редагування адресу у контакта.
        :param address:
        :return:
        """

        if len(self.address) == 0:
            return f"У контакта немає адреси."

        elif len(self.address) == 1:
            self.address[0] = AddressContact(address)
            return f"{address}"

        elif len(self.address) > 1:
            i = -1
            print(f"Виберіть адресу контакту для редагування.")
            for adr in self.address:
                i += 1
                print(f"№  {i}  :  {adr.value}")
            inp_user = int(input(f"Введіть №..."))
            self.address[inp_user] = AddressContact(address)
            return f"{address}"


class AddressBook(UserDict):
    """
    Клас книги контактів.
    Батьківський клас UserDict.
    """

    def add_record(self, record):
        self.data[record.name.value] = record


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
            self.__value = None
        else:
            self.__value = new_value


class Birthday(Field):
    """
    День народження контакта.
    Додається до списку birthday, який створюється при ініціалізації класу Record.
    """
    pass


class AddressContact(Field):
    """
    Адрес контакта.
    Додається до списку address, який створюється при ініціалізації класу Record.
    """

    @Field.value.setter
    def value(self, value: str):
        """
        Сетер для адреси.
        :param value:
        :return:
        """
        if not value.isalnum():
            raise ValueError('Невірний адрес, введіть адрес в текстовому форматі.')
        self.__value = value


class EmailContact(Field):
    """
    Email контакта.
    Додається до списку email_contact, який створюється при ініціалізації класу Record.
    """
    pass
