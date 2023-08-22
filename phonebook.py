from itertools import count
import json
import random

from constants import *


class PhoneBook:
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.data = self.load_data()
        
    def load_data(self):
        try:
            with open(self.file_path, "r", encoding='utf-8') as file:
                data = json.load(file)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            print("Файл не найден или содержит некорректные данные. Создание нового телефонного справочника...")
            return []

    def save_data(self):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
        except Exception as error:
            return error
            
    def display_contacts(self, page: int = 1, contacts_per_page: int = 15):
        start_index = (page - 1) * contacts_per_page
        end_index = start_index + contacts_per_page
        contacts = self.data[start_index:end_index]
        for contact in contacts:
            print(f"Фамилия: {contact['Фамилия']}")
            print(f"Имя: {contact['Имя']}")
            print(f"Компания: {contact['Компания']}")
            print(f"Телефонный номер: {contact['Телефонный номер']}")
            print("--------------------")

    def add_contact(self):
        print(self.count_contact())
        contact = {}
        contact['id'] = self.count_contact() + 1
        contact["Фамилия"] = input("Фамилия контакта: ")
        contact["Имя"] = input("Имя контакта: ")
        contact["Компания"] = input("Компания контакта: ")
        contact["Телефонный номер"] = int(input("Телефонный номер контакта: "))
        self.data.append(contact)
        self.data.sort(key=lambda x: x["Фамилия"])
        self.save_data()
        print("Запись успешно добавлена.")
        
    def edit_record(self, index):
        if index < 1 or index > len(self.data):
            print("Недопустимый индекс записи!")
        else:
            record = self.data[index - 1]
            print("Редактирование записи:")
            record["Фамилия"] = input("Введите фамилию: ")
            record["Имя"] = input("Введите имя: ")
            record["Компания"] = input("Введите название компании: ")
            record["Телефонный номер"] = input("Введите телефон: ")
            self.data.sort(key=lambda x: x["Фамилия"]) 
            self.save_data()
            print("Запись успешно отредактирована!")
            
    def count_contact(self):
        return (len(self.data))

    def search_contacs(self, search_criteria):
        matching_records = []
        for record in self.data:
            match = True
            for key, value in search_criteria.items():
                if value.lower() and key in record and record[key].lower() != value.lower():
                    match = False
                    break
            if match:
                matching_records.append(record)
        return matching_records
    
    def book_menu(self):
        page_num = 1
        records_per_page = 10

        while True:
            print("Меню:")
            print(f"1. Показать записи {page_num} страницы")
            print("2. Добавить запись")
            print("3. Редактировать запись")
            print("4. Поиск записей")
            print("0. Выйти")

            choice = input("Введите номер выбранного действия: ")

            if choice == "1":
                self.display_contacts(page_num, records_per_page)
                page_num += 1
            elif choice == "2":
                self.add_contact()
            elif choice == "3":
                try:
                    index = int(input("Введите индекс контакта для редактирования: "))
                    self.edit_record(index)
                except ValueError:
                    print("Недопустимое значение индекса!")
            elif choice == "4":
                search_criteria = {
                    "Фамилия": input("Введите фамилию: "),
                    "Имя": input("Введите имя: "),
                    "Телефонный номер": input("Введите номер: ")
                }
                matching_contacts = self.search_contacs(search_criteria)
                if len(matching_contacts) > 0:
                    print("Найденные контакты:")
                    for contact in matching_contacts:
                        print(contact)
                        print("-----------------------")
                else:
                    print("Записей не найдено.")
            elif choice == "0":
                break
            else:
                print("Неверный выбор. Пожалуйста, повторите.")


if __name__ == "__main__":
    book = PhoneBook("phonebook.json")
    book.book_menu()