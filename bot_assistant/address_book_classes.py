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

    # def dump_data(self):
    #     """
    #     Метод для сереалізації даних в файл save_data.bin за допомогою pickle.
    #     """
    #     with open("save_data/save_data.bin", "wb") as file:
    #         dump(self.data, file)
    #
    # def load_data(self):
    #     """
    #     Метод для десереалізації даних з файлу save_data.bin за допомогою pickle.
    #     """
    #     with open("save_data/save_data.bin", "rb") as file:
    #         new_data = load(file)
    #         self.data = new_data

    def search_contacts(self, search_value):
        """
        Метод для пошуку контактів серед книги.
        """
        contacts = []
        for key, val in self.data.items():
            if search_value in key.lower():
                contacts.append(self.data[key])
            else:
                for phone in val.get_phones():
                    if search_value in phone:
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
               f'{Fore.BLUE}  Phones:{Style.RESET_ALL}{self.get_phones()} \n' \
               f'{Fore.BLUE} Address:{Style.RESET_ALL}{self.get_addresses()} \n' \
               f'{Fore.BLUE}Birthday:{Style.RESET_ALL}{self.birthday} \n' \
               f'{Fore.BLUE}   Email:{Style.RESET_ALL}{self.get_emails()}'

    def add_address(self, address):
        """
        Метод для додавання нового адресу до рекорду.
        Додається до списку як екземпляр класу AddressContact.
        :param address:
        :return:
        """
        self.address.append(AddressContact(address))

    def add_birthday(self, birthday):
        """
        Метод для додавання дн до рекорду.
        Додається як екземпляр класу Birthday.
        """
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        """
        Метод для додавання номера телефону до рекорду.
        Додається до списку як екземпляр класу Phone.
        """
        self.phones.append(Phone(phone))

    def add_email(self, email):
        """
        Метод для додавання нової ел. пошти до контакта.
        """
        self.email_list.append(EmailContact(email))

    def get_phones(self):
        """
        Метод для певернення списку всіх номерів телефонів.
        """
        all_phones = [phone.value for phone in self.phones]
        return all_phones

    def get_addresses(self):
        """
        Метод для повернення списку всіх адрес.
        """
        all_address = [address.value for address in self.address]
        return all_address

    def get_emails(self):
        all_emails = [email.value for email in self.email_list]
        return all_emails

    def change_address(self, address):
        """
        Метод для редагування адрес у контакту.
        :param address:
        :return:
        """

        if not self.address:
            return f"У контакту немає адреси."

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

            if inp_user not in range(0, i + 1):
                raise ValueError("Такого номеру немає в списку адрес.")

            self.address[inp_user] = AddressContact(address)
            return f"{address}"

    def change_phone(self, new_phone):
        """
        метод заміни номеру телефона
        """
        if not self.phones:
            self.phones.append(Phone(new_phone))
            return f"{new_phone} був доданий до словника для контакту {self.name.value}"

        if len(self.phones) == 1:
            old_phone = self.phones[0].value
            self.phones[0] = Phone(new_phone)
            return f"{old_phone} був замінений на {new_phone} для контакту {self.name.value}"

        if len(self.phones) > 1:
            i = -1
            print("Виберіть телефон для заміни на новий.")
            for phone in self.phones:
                i += 1
                print(f"№ {i} : {phone.value}")
            inp_user = int(input(f"Введіть №..."))

            if inp_user not in range(0, i + 1):
                raise ValueError("Такого номеру немає в списку телефонів.")

            old_phone = self.phones[inp_user].value
            self.phones[inp_user] = Phone(new_phone)
            return f"{old_phone} був замінений на {new_phone} для контакту {self.name.value}"

    def change_email(self, new_email):
        """
        Метод для редагування ел. пошти у контакта.
        """
        if not self.email_list:
            return f"{self.name.value} ще не має ел. пошти."
        elif len(self.email_list) == 1:
            old_email = self.email_list[0].value
            self.email_list[0] = EmailContact(new_email)
            return f"{old_email} був замінений на {new_email} для контакту {self.name.value}"
        else:
            print("Виберіть ел. пошту, для редагування.")
            i = -1
            for e_mail in self.email_list:
                i += 1
                print(f"№  {i}  :  {e_mail.value}")

            user_choice = int(input("Виберіть № для заміни: "))

            if user_choice not in range(0, i + 1):
                return f"Такого номеру немає в списку емейлів..."

            elif user_choice in range(0, i + 1):
                old_email = self.email_list[user_choice].value
                self.email_list[user_choice] = EmailContact(new_email)

                return f"{old_email} був замінений на {new_email} для контакту {self.name.value}"
            else:
                return "Ви ввели невірне значення. Спробуйте ще раз."

    def delete_address(self):
        """
        Метод для видалення адреси у контакту.
        """
        if not self.address:
            return f"{self.name.value} не має адреси"

        if len(self.address) == 1:
            address_to_delete = self.address.pop(0)
            return f"Адрес: {address_to_delete.value}, був видалений для контакту {self.name.value}"

        else:
            i = -1
            print("Виберіть який телефон хочете видалити")
            for adr in self.address:
                i += 1
                print(f"№ {i} : {adr.value}")
            inp_user = int(input(f"Введіть №..."))

            if inp_user not in range(0, i + 1):
                raise ValueError("Такого номеру немає в списку адрес.")

            address_to_delete = self.address.pop(inp_user)
            return f"Адрес: {address_to_delete.value}, був видалений для контакту {self.name.value}"

    def delete_phone(self):
        """
        метод для видалення номеру телефона
        """
        if not self.phones:
            return f"{self.name.value} не має няіких номерів"

        if len(self.phones) == 1:
            phone_to_delete = self.phones.pop(0)
            return f"{phone_to_delete.value} був видалений для контакту {self.name.value}"

        else:
            i = -1
            print("Виберіть який телефон хочете видалити")
            for phone in self.phones:
                i += 1
                print(f"№ {i} : {phone.value}")
            inp_user = int(input(f"Введіть №..."))

            if inp_user not in range(0, i + 1):
                raise ValueError("Такого номеру немає в списку телефонів.")

            phone_to_delete = self.phones.pop(inp_user)
            return f"{phone_to_delete.value} був видалений для контакту {self.name.value}"

    def delete_email(self):
        """
        Метод для видалення ел. пошти у контакта.
        """
        if not self.email_list:
            return f"{self.name.value} не має ел. пошти, для видалення."

        elif len(self.email_list) == 1:
            deleting_email = self.email_list.pop(0)
            return f"{deleting_email.value} був видалений для контакту {self.name.value}"

        else:
            print("Виберіть необхідну для видалення ел. пошту.")
            i = -1

            for e_mail in self.email_list:
                i += 1
                print(f"№  {i}  :  {e_mail.value}")

            user_choice = int(input("Введіть № - "))

            if user_choice not in range(0, i + 1):
                return f"Такого номеру немає в списку емейлів..."

            if user_choice in range(0, i + 1):
                deleting_email = self.email_list.pop(user_choice)
                return f"{deleting_email.value} був видалений для контакту {self.name.value}"

            else:
                return "Ви ввели невірне значення. Спробуйте ще раз."


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
    pass


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
