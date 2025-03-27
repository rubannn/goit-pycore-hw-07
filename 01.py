"""
================================
    Технiчний опис завдання
================================
Розробіть систему для управління адресною книгою.

Сутності:
    Field: Базовий клас для полів запису.
    Name: Клас для зберігання імені контакту. Обов'язкове поле.
    Phone: Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
    Record: Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
    AddressBook: Клас для зберігання та управління записами.

Функціональність:
    AddressBook:Додавання записів.
    Пошук записів за іменем.
    Видалення записів за іменем.
    Record:Додавання телефонів.
    Видалення телефонів.
    Редагування телефонів.
    Пошук телефону.

================================
    Критерії оцінювання
================================
Клас AddressBook:
    Реалізовано метод add_record, який додає запис до self.data.
    Реалізовано метод find, який знаходить запис за ім'ям.
    Реалізовано метод delete, який видаляє запис за ім'ям.

Клас Record:
    Реалізовано зберігання об'єкта Name в окремому атрибуті.
    Реалізовано зберігання списку об'єктів Phone в окремому атрибуті.
    Реалізовано методи для
        додавання - add_phone/
        видалення - remove_phone/
        редагування - edit_phone/
        пошуку об'єктів Phone - find_phone.

Клас Phone:
    Реалізовано валідацію номера телефону (має бути перевірка на 10 цифр).
"""

from collections import UserDict
import re
from datetime import datetime, date

from colorama import init, Fore

init(autoreset=True)
ERROR = Fore.RED

DATE_FORMAT = "%d.%m.%Y"


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r"\d{10}", value):
            print(
                ERROR
                + f'You input: {value}\nError: "Phone number format <only 10 digits>."'
            )
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, DATE_FORMAT).date()
        except ValueError:
            # raise ValueError("Invalid date format. Use DD.MM.YYYY")
            print(ERROR + "Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime(DATE_FORMAT) if self.value else "---"


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        """Додавання телефонів"""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """Видалення телефонів"""
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        """Редагування телефонів"""
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = Phone(new_phone).value
                return
        print(
            ERROR + f'You want to change: {old_phone}\nError: "Phone number not found."'
        )

    def find_phone(self, search_phone):
        """Пошук телефону"""
        for phone in self.phones:
            if phone.value == search_phone:
                return phone
        return None

    def add_birthday(self, birthday):
        """Додавання дня народження"""
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday if self.birthday else '---'}"


class AddressBook(UserDict):
    def add_record(self, record):
        """Додавання записів"""
        self.data[record.name.value] = record

    def find(self, name):
        """Пошук записів за іменем"""
        return self.data.get(name, None)

    def delete(self, name):
        """Видалення записів за іменем"""
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        result = []
        today = datetime.today().date()
        for record in self.data.values():
            if record.birthday:
                name = record.name.value
                birthday = record.birthday.value
                birthday_this_year = date(today.year, birthday.month, birthday.day)
                birthday_next_year = date(today.year + 1, birthday.month, birthday.day)
                delta = (birthday_this_year - today).days
                delta_next = (birthday_next_year - today).days
                if 0 <= delta <= 7:
                    result.append(
                        {
                            "name": name,
                            "congratulation_date": birthday_this_year.strftime(
                                DATE_FORMAT
                            ),
                        }
                    )
                elif 0 <= delta_next <= 7:
                    result.append(
                        {
                            "name": name,
                            "congratulation_date": birthday_next_year.strftime(
                                DATE_FORMAT
                            ),
                        }
                    )
        return result

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())


def input_error(func):
    """Декоратор для обробки помилок введення користувача."""

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return ERROR + f"\tGive me name and phone please. Format: <name> <phone>"
        except KeyError:
            return ERROR + f"\tContact not found."
        except IndexError:
            return ERROR + f"\tNot enough arguments provided."

    return inner


@input_error
def parse_input(user_input):
    """Розбирає введений користувачем рядок на команду та аргументи."""

    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book):
    """Змінює телефон існуючого контакту."""

    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        return record.edit_phone(old_phone, new_phone)
    return ERROR + "Contact not found."


@input_error
def show_phone(args, book):
    """Показує телефон контакту."""

    name = args[0]
    record = book.find(name)
    if record:
        return f"{name}: {', '.join(p.value for p in record.phones)}"
    return ERROR + "Contact not found."


@input_error
def add_birthday(args, book):
    """Додає день народження до контакту."""

    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    return ERROR + "Contact not found."


@input_error
def show_birthday(args, book):
    """Повертає дату дня народження контакту."""

    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"
    return ERROR + "Birthday not found."


@input_error
def birthdays(book):
    """Повертає список контактів із днями народження на наступний тиждень."""

    upcoming = book.get_upcoming_birthdays()
    if upcoming:
        return "Upcoming birthdays:\n" + "\n".join(
            f"{item['name']}: {item['congratulation_date']}" for item in upcoming
        )
    return "No upcoming birthdays."


def show_all(book):
    """Повертає всі контакти у книзі."""

    if not book:
        return "No contacts saved."
    return "\n".join(f"{record}" for record in book.data.values())


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
