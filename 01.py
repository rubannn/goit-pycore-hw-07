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

from colorama import init, Fore

init(autoreset=True)
ERROR = Fore.RED


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


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

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

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


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

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())


class Birthday(Field):
    def __init__(self, value):
        try:
            # Додайте перевірку коректності даних
            # та перетворіть рядок на об'єкт datetime
            ...
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None


# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")
