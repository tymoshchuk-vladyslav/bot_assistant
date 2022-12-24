from collections import UserList
from pickle import dump, load
import re


class Notes(UserList):
    ''' Загальний клас в якому зберігаються всі нотатки як екземплври класу Record'''

    def add_record(self, record):
        '''метод додає новий єекземпляр класу'''
        self.data.append(record)

    def cahange_note_text(self, number: int, new_value):
        '''змінює текст нотатку, на вході приймає № нотатку та нове значення'''
        self.data[number].change(new_value)

    def cahange_tag(self, number: int, action, tag):
        '''змінює текст нотатку, на вході приймає № нотатку, дію(додати/видалит) та нове значення'''
        if action == 'add':
            self.data[number].add_tag(tag)
        elif action in ['del', 'dell', 'delete']:
            self.data[number].del_tag(tag)
        else:
            return 'no such tag'

    def search_by_tag(self, tag):
        '''шукає нотатки за тегом та виводить їх відсортовано по зростанню, приймає тег'''
        result = ''
        sorted_list = sorted(self.data, key=lambda record: record.tag.value)
        for idx, record in enumerate(sorted_list, start=1):

            if tag.lower() in record.tag.value:
                result += f'---note №{idx}---\n{str(record)}\n'
        return result

    def search(self, search_text):
        ''' пошук по тексту, приймає текст для пошуку'''
        result = ''
        for idx, record in enumerate(self.data, start=1):
            # print(idx, record)

            if search_text in record.body.value:
                # print(record)
                result += f'---note №{idx}---\n{str(record)}\n'
        return result

    def get_notes(self):
        '''технічна функція для вивдення всіх нотатків'''
        result = ''
        for idx, record in enumerate(self.data, start=1):
            result += f'---note №{idx}---\n{str(record)}\n'
        return result

    def sort_notes(self, way=1):
        '''функція сортуввання. для реверсного сортування потрібно передати -1
        повертае всі ноаттки'''
        if way == 1:
            self.data.sort(key=lambda record: record.tag.value)
        else:
            self.data.sort(key=lambda record: record.tag.value, reverse=True)

        return self.get_notes()

    def save_notes(self):
        '''серіалізує'''
        filename = r"save_notes.bin"
        with open(filename, "wb") as file:
            dump(self.data, file)

    def load_notes(self):
        '''десереалізує'''
        filename = r"save_notes.bin"
        try:
            with open(filename, "rb") as file:
                self.data = load(file)
        except FileNotFoundError:
            return


class Note:
    '''1 екземпляр класу = 1 нотатка, в середені має текст і тегі'''

    def __init__(self, tag, body):
        self.tag = Tag(tag)
        self.body = Body(body)

    def change(self, new_value):
        '''змінює текст нотатки, приймає новий текст'''
        self.body.value = new_value

    def add_tag(self, new_tag):
        '''додає тег, приймає новий тег'''
        splited = sorted(re.split('\W', new_tag))
        self.tag.value.extend([i.lower() for i in splited if bool(i) == True])
        self.tag.value.sort()

    def del_tag(self, tag):
        '''видаляє тег, приймає тег. Повертає текст помилки якщо такого тегу немає без помилки'''
        try:
            self.tag.value.remove(tag.lower())
        except:
            return 'no such tag'

    def __str__(self):
        return f'{self.tag.value}\n {self.body.value}\n' + 50*'-'  # + '\n'

    # def __repr__(self):
    #     return f'{self.tag.value[:3]}...\n {self.body.value[:50]}...\n' + 50*'-' +'\n'


class Field:
    def __init__(self, value):
        self.value = value


class Tag(Field):
    def __init__(self, value):
        splited = sorted(re.split('\W', value))
        self.value = [i.lower() for i in splited if bool(i) == True]


class Body(Field):
    pass

