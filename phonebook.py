import json
from typing import List, Dict, Union


class PhoneBook:
    
    """
    Класс представляет собой Телефонную записную книжку с набором функционала в виде методов.
    """
    
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.data = self.load_data()
        
    def load_data(self) -> List[Dict[str, Union[str, int]]]:
        """
        Метод служит для прочтения JSON файла и дальнейшей работы в нем. Принимает на вход путь к файлу
        который указывается при инициализации класса.

        Возвращает:
            List[Dict[str, Union[str, int]]]: Возвращает все имеющиеся контакты или информацию, что файл не найден
        """
        try:
            with open(self.file_path, "r", encoding='utf-8') as file:
                data = json.load(file)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            print("Файл не найден или содержит некорректные данные. Создание нового телефонного справочника...")
            return []

    def save_data(self) -> Exception | None:
        """
        Метод служит для записи данных в JSON файл, с помощью которого был инициализирован класс.

        Возвращает:
            Exception | None:
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
        except Exception as error:
            return error
            
    def display_contacts(self, page: int = 1, contacts_per_page: int = 15) -> None:
        """
        Метод для постраничного отображения списка контактов

        Аргументы:
            page (int, optional): Номер страницы, по умолчанию начинаем с 1.
            contacts_per_page (int, optional): Количество записей на странице, по умолчанию 15.
        """
        start_index = (page - 1) * contacts_per_page
        end_index = start_index + contacts_per_page
        contacts = self.data[start_index:end_index]
        if len(contacts) == 0:
            print("Вы достигли последней страницы.")
            return
    
        for contact in contacts:
            print("--------------------")
            print(f"Номер записи: {contact['id']}")
            print(f"Фамилия: {contact['Фамилия']}")
            print(f"Имя: {contact['Имя']}")
            print(f"Отчество: {contact['Отчество']}")
            print(f"Компания: {contact['Компания']}")
            print(f"Рабочий номер: {contact['Рабочий номер']}")
            print(f"Личный номер: {contact['Личный номер']}")

    def add_contact(self) -> None:
        """
        Метод служит для записи новых контактов в книгу. Формирует словарь с определенными ключами, 
        сортирует в алфавитном порядке, по ключу "Фамилия" все записи и добавляет новый контакт.
        """
        contact = {}
        contact['id'] = self.count_contact() + 1
        contact["Фамилия"] = input("Фамилия контакта: ")
        contact["Имя"] = input("Имя контакта: ")
        contact["Отчество"] = input("Отчество контакта: ")
        contact["Компания"] = input("Компания контакта: ")
        contact["Личный номер"] = input("Введите личный номер телефона: ")
        contact["Рабочий номер"] = input("Введите рабочий номер телефона: ")
        self.data.append(contact)
        self.data.sort(key=lambda x: x["Фамилия"])
        self.save_data()
        print("Запись успешно добавлена.")
        
    def edit_contact(self, index: int) -> None:
        """
        Метод служит для редактирования уже имеющихся контактов
        Реализован поиск по номеру записи конкретного контакта, изменение всех его полей и сохранения в файл.

        Аргументы:
            index (int): Номер записи контакта (id)
        """
        contact = self.search_contacs(index)
        if not contact:
            print("Контакта не существует!")
        else:
            print(f"Вы хотите отредактировать эту запись?\n {contact}")
            answer = int(input("1 - Да \n0 - Нет\n "))
            if answer == 1:
                print("Редактирование записи:")
                contact["Фамилия"] = input("Введите фамилию: ")
                contact["Имя"] = input("Введите имя: ")
                contact["Отчество"] = input("Введите отчество: ")
                contact["Компания"] = input("Введите название компании: ")
                contact["Личный номер"] = input("Введите личный номер телефона: ")
                contact["Рабочий номер"] = input("Введите рабочий номер телефона: ")
                self.data.sort(key=lambda x: x["Фамилия"]) 
                self.save_data()
                print("Запись успешно отредактирована!")
            elif answer == 0:
                print("Выберете другую запись")
            else:
                print("Вы выбрали несуществующий вариант, начните сначала")
            
    def count_contact(self) -> int:
        """
        Метод служит для подсчета общего количества контактов в записной книге

        Возвращает:
            int: Возвращает число равное количеству записей
        """
        return (len(self.data))

    def search_contacs(self, search_criteria: dict) -> Dict[str, str | int] | list:
        """
        Метод служит для поиска определенных записией. В зависимсоти от сценария принимает разные аргументы

        Args:
            search_criteria (_type_): Принимает словарь с полями по которым будет осуществлен поиск.
            Каждое поле является не обязательным, но необходимо указать хотя бы одно.

        Returns:
            Dict[str, str | int] | list: Возвращает один или несколько результатов в зависимости от сценария
        """
        matching_records = []
        for record in self.data:
            match = True
            if "id" in search_criteria:
                if search_criteria["id"] == record["id"]:
                    return record
            else:
                for key, value in search_criteria.items():
                    if value.lower() and key in record and record[key].lower() != value.lower():
                        match = False
                        break
                if match:
                    matching_records.append(record)
        return matching_records
    
    def book_menu(self) -> None:
        """
        Метод служит для навигации и определения сценария всего класса
        """
        page_num = 1
        records_per_page = 5

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
                if len(self.data) <= page_num * records_per_page:
                    print("Вы достигли последней страницы.")
                    self.book_menu()
                page_num += 1
            elif choice == "2":
                self.add_contact()
            elif choice == "3":
                try:
                    search_criteria = {
                        "id": int(input("Введите номер записи: "))
                    }
                    self.edit_contact(search_criteria)
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
