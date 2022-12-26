# BOT-ASSISTANT

“Персональний помічник” може:
зберігати контакти з іменами, адресами, номерами телефонів, email та днями народження до книги контактів;
виводити список контактів, у яких день народження через задану кількість днів від поточної дати;
перевіряти правильність введеного номера телефону та email під час створення або редагування запису та повідомляти користувача у разі некоректного введення;
здійснювати пошук контактів серед контактів книги;
редагувати та видаляти записи з книги контактів;
зберігати нотатки з текстовою інформацією;
проводити пошук за нотатками;
редагувати та видаляти нотатки;
додавати в нотатки "теги", ключові слова, що описують тему та предмет запису;
здійснювати пошук та сортування нотаток за ключовими словами (тегами);
сортувати файли у зазначеній папці за категоріями (зображення, документи, відео та ін.).

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [License](#license)

## Install

This project uses [Python 3.10](https://www.python.org/). Go check them out if you don't have them locally installed.

Download all files.
Requires pip to install.

```sh
$ pip install [folder path pyproject.toml]
```

## Usage

console script

```sh
    help - show all comand
    add - will adding new contact to you addressbook in format add: [Name][Phone]
    add phone - will adding phone to contact in format add: [Name] [Phone]
    add address - will adding new address to contact in format: [Name] [address]
    add email - will adding new address to contact in format: [Name] [email]
    add birthday - will adding new address to contact in format: [Name] [birthday]
    change address - will change address of you contact. format for change: [Name] [New address]
    change email - will change email of you contact. format for change: [Name] [New email]
    change phone - will change old phone with new value. format for change: [Name] [New phone]
    change birthday - will change birthday with new value. format for change: [Name] [New birthday]
    search contacts - will search all contacts by name or phone number. format: [searching text]
    show contact - will show all contacts. Show without name will show contact. format: [searching text]
    delete birthday - will delete contact Bday. format [name]
    delete contact - will delete contact. format [name]
    delete address - will delete address. format [name]
    delete email - will delete selected contact email. format [Name] [email]
    search birthday - will show you upcoming Bday in  "n" days. format [quantity of days]
    save - will save you addressbook and notes
    load - will load you addressbook and notes
    sort - will make magik and sort you files. Give only dir ;)
    
    add note - will adding new note
    del note - will delete note. format: [record number]
    change note - will changing note. format: [record number] [new text]
    change tag - will add or delete tag to you note
    show notes - will show you all notes
    sort notes - will show you note with sort. 1/-1 to asc/desc sorting
    search notes - will searching note for you by text
    search tag - will searching note for you by tag
    
    good_bye - for exit
```

## License

[MIT](LICENSE) © Vladislav Timoshcuk, Anton Holovin, Andrew Subotin, Sergii Kashpurenko