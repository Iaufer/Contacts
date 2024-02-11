import csv
import os
import re
from typing import List, Any, Dict

class Contact:
    def __init__(self, last_name: str, first_name: str, middle_name: str, name_org: str, work_phone: str, personal_phone: str) -> None:
        """
        Класс, представляющий контакт в телефонном справочнике.

        Args:
            last_name (str): Фамилия контакта.
            first_name (str): Имя контакта.
            middle_name (str): Отчество контакта.
            name_org (str): Название организации контакта.
            work_phone (str): Рабочий телефон контакта (без кода страны).
            personal_phone (str): Личный телефон контакта (без кода страны).
        """
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.name_org = name_org
        self.work_phone = work_phone
        self.personal_phone = personal_phone

    @classmethod
    def create_contact(cls) -> 'Contact':
        """
        Создает новый контакт, запрашивая у пользователя необходимую информацию.

        Returns:
            Contact: Созданный контакт.
        """
        print("Введите фамилию: ")
        last_name = input().strip()

        print("Введите имя: ")
        first_name = input().strip()
        
        print("Введите отчество: ")
        middle_name = input().strip()
        
        print("Введите название организации: ")
        name_org = input().strip()
        
        work_phone = input_phone("Введите рабочий телефон(без кода страны): ")
        personal_phone = input_phone("Введите личный телефон(без кода страны): ")
        
        return cls(last_name, first_name, middle_name, name_org, work_phone, personal_phone)

def input_phone(prompt: str) -> str:
    """
    Запрашивает у пользователя ввод телефонного номера и проверяет его формат.

    Args:
        prompt (str): Подсказка для пользователя.

    Returns:
        str: Введенный телефонный номер.
    """
    while True:
        phone = input(prompt).strip()
        if re.match(r'^\d{10}$', phone):
            return phone
        else:
            print("Некорректный формат номера телефона. Повторите ввод.")

class CSVFileManager:
    def __init__(self, file_name: str) -> None:
        """
        Инициализирует объект для работы с файлом CSV.

        Args:
            file_name (str): Имя CSV-файла.
        """
        self.file_name = file_name
    
    def add_contact(self, contact: Contact) -> None:
        """
        Добавляет новый контакт в файл CSV.

        Args:
            contact (Contact): Контакт для добавления.
        """
        with open(self.file_name, "r", newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if contact.work_phone == row[4] or contact.personal_phone == row[5]:
                    print("Контакт с таким номером телефона уже существует.")
                    return
        row = [contact.last_name, contact.first_name, contact.middle_name, contact.name_org, contact.work_phone, contact.personal_phone]
        with open(self.file_name, "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)
        print("Контакт успешно добавлен в справочник.")
    
    def edit_contact(self, last_name: str, first_name: str) -> None:
        """
        Изменяет информацию о контакте.

        Args:
            last_name (str): Фамилия контакта.
            first_name (str): Имя контакта.
        """
        temp_file = self.file_name + ".tmp"
        with open(self.file_name, "r", newline='') as csvfile, open(temp_file, "w", newline='') as tempcsvfile:
            reader = csv.reader(csvfile)
            writer = csv.writer(tempcsvfile)
            updated = False
            for row in reader:
                if last_name == row[0] and first_name == row[1]:
                    print("Выберите, какое поле контакта вы хотите изменить:")
                    print("1. Фамилия")
                    print("2. Имя")
                    print("3. Отчество")
                    print("4. Название организации")
                    print("5. Рабочий телефон")
                    print("6. Личный телефон")
                    choice = int(input().strip())
                    if choice == 1:
                        row[0] = input("Новая фамилия: ").strip()
                    elif choice == 2:
                        row[1] = input("Новое имя: ").strip()
                    elif choice == 3:
                        row[2] = input("Новое отчество: ").strip()
                    elif choice == 4:
                        row[3] = input("Новое название организации: ").strip()
                    elif choice == 5:
                        row[4] = input_phone("Новый рабочий телефон(без кода страны): ")
                    elif choice == 6:
                        row[5] = input_phone("Новый личный телефон(без кода страны): ")
                    updated = True
                writer.writerow(row)
        if updated:
            os.replace(temp_file, self.file_name)
            print("Контакт успешно изменен.")
        else:
            os.remove(temp_file)
            print("Контакт не найден.")

    def find_contact(self, **kwargs: str) -> List[Contact]:
        """
        Находит контакты по заданным атрибутам.

        Args:
            **kwargs (str): Атрибуты для поиска контактов.

        Returns:
            List[Contact]: Список найденных контактов.
        """
        found_contacts = []
        with open(self.file_name, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                contact = Contact(*row)
                if all(getattr(contact, attr, None).lower() == value.lower() for attr, value in kwargs.items()):
                    found_contacts.append(contact)
        return found_contacts

    def display_contacts(self, page_num: int, page_size: int = 10) -> None:
        """
        Выводит список контактов постранично.

        Args:
            page_num (int): Номер страницы для отображения.
            page_size (int, optional): Размер страницы. По умолчанию 10.
        """
        with open(self.file_name, 'r') as f:
            reader = csv.reader(f)
            contacts = list(reader)
            total_pages = len(contacts) // page_size + (1 if len(contacts) % page_size != 0 else 0)
            if page_num < 1 or page_num > total_pages:
                print("Недопустимый номер страницы.")
                return
            start = (page_num - 1) * page_size
            end = min(start + page_size, len(contacts))
            contacts = contacts[start:end]
            for contact in contacts:
                print(contact)

        print(f"Страница {page_num}/{total_pages}")
        print("Выберите действие:")
        print("1. Предыдущая страница")
        print("2. Следующая страница")
        print("3. Вернуться в меню")
        choice = input().strip()
        if choice == '1' and page_num > 1:
            self.display_contacts(page_num - 1, page_size)
        elif choice == '2' and page_num < total_pages:
            self.display_contacts(page_num + 1, page_size)
        elif choice == '3':
            return
        else:
            print("Неверный выбор.")
            self.display_contacts(page_num, page_size)

csvfm = CSVFileManager("data.csv")

while True:
    print("Выберите действие:")
    print("1. Создать контакт")
    print("2. Изменить контакт")
    print("3. Найти контакт")
    print("4. Вывести контакты")
    
    choice = input().strip()
    
    if choice == '1':
        print("Создание нового контакта:")
        con = Contact.create_contact()
        csvfm.add_contact(con)
    elif choice == '2':
        print("Изменение контакта:")
        last_name = input("Введите фамилию контакта, которого вы хотите изменить: ").strip()
        first_name = input("Введите имя контакта, которого вы хотите изменить: ").strip()
        csvfm.edit_contact(last_name, first_name)
    elif choice == '3':
        print("Поиск контакта:")
        last_name = input("Введите фамилию контакта, который вы хотите найти: ").strip()
        first_name = input("Введите имя контакта, который вы хотите найти: ").strip()
        found_contacts = csvfm.find_contact(last_name=last_name, first_name=first_name)
        if found_contacts:
            print("Найденные контакты:")
            for contact in found_contacts:
                print(contact.__dict__)
        else:
            print("Контакт не найден.")
    elif choice == '4':
        print("Вывод контактов:")
        page_num = int(input("Введите номер страницы для отображения: ").strip())
        csvfm.display_contacts(page_num)
        
    print("Хотите продолжить? (Y/n)")
    ans = input().strip().lower()
    if ans != 'y':
        break
