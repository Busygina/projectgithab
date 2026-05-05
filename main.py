import json
import os
from tkinter import *
from tkinter import ttk, messagebox

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker - Управление прочитанными книгами")
        self.root.geometry("900x600")
        self.root.resizable(True, True)

        # Файл для хранения данных
        self.data_file = "books.json"
        self.books = []
        self.filtered_books = []

        # Загрузка данных при старте
        self.load_data()

        # Создание интерфейса
        self.create_input_frame()
        self.create_filter_frame()
        self.create_books_table()
        self.create_control_buttons()

        # Обновление таблицы
        self.refresh_table()

    def create_input_frame(self):
        """Форма для ввода данных книги"""
        input_frame = LabelFrame(self.root, text="Добавить новую книгу", padx=10, pady=10, font=("Arial", 12, "bold"))
        input_frame.pack(fill="x", padx=10, pady=5)

        # Поля ввода
        labels = ["Название книги:", "Автор:", "Жанр:", "Количество страниц:"]
        self.entries = {}

        for i, label in enumerate(labels):
            Label(input_frame, text=label, font=("Arial", 10)).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            entry = Entry(input_frame, width=40, font=("Arial", 10))
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label] = entry

        # Кнопка добавления
        self.add_button = Button(input_frame, text="Добавить книгу", command=self.add_book,
                                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=20)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

    def create_filter_frame(self):
        """Фильтрация книг"""
        filter_frame = LabelFrame(self.root, text="Фильтрация", padx=10, pady=10, font=("Arial", 12, "bold"))
        filter_frame.pack(fill="x", padx=10, pady=5)

        # Фильтр по жанру
        Label(filter_frame, text="Жанр:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
        self.genre_filter_var = StringVar()
        self.genre_combo = ttk.Combobox(filter_frame, textvariable=self.genre_filter_var, width=30, font=("Arial", 10))
        self.genre_combo.grid(row=0, column=1, padx=5, pady=5)
        self.genre_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())

        # Фильтр по страницам (> 200)
        self.pages_filter_var = BooleanVar()
        self.pages_check = Checkbutton(filter_frame, text="Количество страниц > 200",
                                       variable=self.pages_filter_var, command=self.apply_filters,
                                       font=("Arial", 10))
        self.pages_check.grid(row=0, column=2, padx=20, pady=5)

        # Кнопка сброса фильтров
        self.reset_button = Button(filter_frame, text="Сбросить фильтры", command=self.reset_filters,
                                   bg="#FF9800", fg="white", font=("Arial", 9))
        self.reset_button.grid(row=0, column=3, padx=10, pady=5)

    def create_books_table(self):
        """Таблица со списком книг"""
        # Создание фрейма с прокруткой
        table_frame = Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Скроллбары
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)

        # Таблица Treeview
        columns = ("ID", "Название", "Автор", "Жанр", "Страницы")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                                 yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        self.tree.pack(fill="both", expand=True)

        # Настройка колонок
        self.tree.heading("ID", text="ID")
        self.tree.heading("Название", text="Название")
        self.tree.heading("Автор", text="Автор")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Страницы", text="Страницы")

        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Название", width=200)
        self.tree.column("Автор", width=150)
        self.tree.column("Жанр", width=120)
        self.tree.column("Страницы", width=80, anchor="center")

    def create_control_buttons(self):
        """Кнопки управления"""
        control_frame = Frame(self.root)
        control_frame.pack(fill="x", padx=10, pady=10)

        self.save_button = Button(control_frame, text="Сохранить в JSON", command=self.save_to_json,
                                  bg="#2196F3", fg="white", font=("Arial", 10), padx=20)
        self.save_button.pack(side=LEFT, padx=5)

        self.load_button = Button(control_frame, text="Загрузить из JSON", command=self.load_from_json,
                                  bg="#9C27B0", fg="white", font=("Arial", 10), padx=20)
        self.load_button.pack(side=LEFT, padx=5)

        self.delete_button = Button(control_frame, text="Удалить выбранную", command=self.delete_book,
                                    bg="#F44336", fg="white", font=("Arial", 10), padx=20)
        self.delete_button.pack(side=LEFT, padx=5)

    def validate_input(self, title, author, genre, pages):
        """Проверка корректности ввода"""
        if not title.strip():
            messagebox.showerror("Ошибка", "Название книги не может быть пустым!")
            return False
        if not author.strip():
            messagebox.showerror("Ошибка", "Автор не может быть пустым!")
            return False
        if not genre.strip():
            messagebox.showerror("Ошибка", "Жанр не может быть пустым!")
            return False
        if not pages.strip():
            messagebox.showerror("Ошибка", "Количество страниц не может быть пустым!")
            return False
        try:
            pages_num = int(pages)
            if pages_num <= 0:
                messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return False
        return True

    def add_book(self):
        """Добавление новой книги"""
        title = self.entries["Название книги:"].get()
        author = self.entries["Автор:"].get()
        genre = self.entries["Жанр:"].get()
        pages = self.entries["Количество страниц:"].get()

        if not self.validate_input(title, author, genre, pages):
            return

        # Создание новой книги
        new_id = max([book["id"] for book in self.books], default=0) + 1
        book = {
            "id": new_id,
            "title": title.strip(),
            "author": author.strip(),
            "genre": genre.strip(),
            "pages": int(pages)
        }

        self.books.append(book)
        self.refresh_table()

        # Очистка полей ввода
        for entry in self.entries.values():
            entry.delete(0, END)

        # Обновление списка жанров в фильтре
        self.update_genre_list()

        messagebox.showinfo("Успех", f"Книга \"{title}\" добавлена!")

    def delete_book(self):
        """Удаление выбранной книги"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите книгу для удаления!")
            return

        # Получение ID выбранной записи
        item = self.tree.item(selected[0])
        book_id = item["values"][0]

        # Поиск и удаление книги
        for book in self.books:
            if book["id"] == book_id:
                self.books.remove(book)
                break

        self.refresh_table()
        self.update_genre_list()
        messagebox.showinfo("Успех", "Книга удалена!")

    def apply_filters(self):
        """Применение фильтров"""
        selected_genre = self.genre_filter_var.get()
        filter_pages = self.pages_filter_var.get()

        self.filtered_books = self.books.copy()

        # Фильтр по жанру
        if selected_genre and selected_genre != "Все жанры":
            self.filtered_books = [b for b in self.filtered_books if b["genre"] == selected_genre]

        # Фильтр по страницам (> 200)
        if filter_pages:
            self.filtered_books = [b for b in self.filtered_books if b["pages"] > 200]

        self.update_table_display()

    def reset_filters(self):
        """Сброс всех фильтров"""
        self.genre_filter_var.set("")
        self.pages_filter_var.set(False)
        self.filtered_books = self.books.copy()
        self.update_table_display()

    def update_table_display(self):
        """Обновление отображения таблицы"""
        # Очистка текущих данных в таблице
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Отображение отфильтрованных книг
        for book in self.filtered_books:
            self.tree.insert("", END, values=(
                book["id"],
                book["title"],
                book["author"],
                book["genre"],
                book["pages"]
            ))

    def refresh_table(self):
        """Обновление таблицы (сброс фильтров)"""
        self.reset_filters()

    def update_genre_list(self):
        """Обновление списка жанров в фильтре"""
        genres = sorted(set(book["genre"] for book in self.books))
        genres.insert(0, "Все жанры")
        self.genre_combo["values"] = genres

    def save_to_json(self):
        """Сохранение данных в JSON файл"""
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.books, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", f"Данные сохранены в файл {self.data_file}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {str(e)}")

    def load_from_json(self):
        """Загрузка данных из JSON файла"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.books = json.load(f)
                self.refresh_table()
                self.update_genre_list()
                messagebox.showinfo("Успех", f"Данные загружены из файла {self.data_file}")
            else:
                messagebox.showwarning("Предупреждение", f"Файл {self.data_file} не найден!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки данных: {str(e)}")

    def load_data(self):
        """Автоматическая загрузка данных при запуске"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.books = json.load(f)
                self.filtered_books = self.books.copy()
                self.update_genre_list()
            except:
                self.books = []
                self.filtered_books = []

if __name__ == "__main__":
    root = Tk()
    app = BookTracker(root)
    root.mainloop()
