import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.books = []
        self.load_data()

        # Поля ввода
        tk.Label(root, text="Название книги:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Автор:").grid(row=1, column=0, padx=5, pady=5)
        self.author_entry = tk.Entry(root, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Жанр:").grid(row=2, column=0, padx=5, pady=5)
        self.genre_entry = tk.Entry(root, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Количество страниц:").grid(row=3, column=0, padx=5, pady=5)
        self.pages_entry = tk.Entry(root, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        tk.Button(root, text="Добавить книгу", command=self.add_book).grid(row=4, column=0, columnspan=2, pady=10)

        # Таблица для отображения книг
        self.tree = ttk.Treeview(root, columns=("Title", "Author", "Genre", "Pages"), show="headings")
        self.tree.heading("Title", text="Название")
        self.tree.heading("Author", text="Автор")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Pages", text="Страниц")
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Фильтры
        tk.Label(root, text="Фильтр по жанру:").grid(row=6, column=0, padx=5, pady=5)
        self.filter_genre = tk.Entry(root, width=30)
        self.filter_genre.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(root, text="Мин. количество страниц:").grid(row=7, column=0, padx=5, pady=5)
        self.filter_pages = tk.Entry(root, width=30)
        self.filter_pages.grid(row=7, column=1, padx=5, pady=5)

        tk.Button(root, text="Применить фильтр", command=self.apply_filter).grid(row=8, column=0, pady=10)
        tk.Button(root, text="Сбросить фильтр", command=self.reset_filter).grid(row=8, column=1, pady=10)

        # Кнопки сохранения/загрузки
        tk.Button(root, text="Сохранить в JSON", command=self.save_data).grid(row=9, column=0, pady=10)
        tk.Button(root, text="Загрузить из JSON", command=self.load_data).grid(row=9, column=1, pady=10)
        
    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()

        try:
            pages = int(self.pages_entry.get())
            if pages <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
            return

        if not title or not author or not genre:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        book = {"title": title, "author": author, "genre": genre, "pages": pages}
        self.books.append(book)
        self.update_table()

        # Очистка полей
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for book in self.books:
            self.tree.insert("", tk.END, values=(book["title"], book["author"], book["genre"], book["pages"]))

    def apply_filter(self):
        genre_filter = self.filter_genre.get().strip().lower()
        pages_filter = self.filter_pages.get().strip()

        filtered_books = self.books

        if genre_filter:
            filtered_books = [b for b in filtered_books if genre_filter in b["genre"].lower()]

        if pages_filter:
            try:
                min_pages = int(pages_filter)
                filtered_books = [b for b in filtered_books if b["pages"] >= min_pages]
            except ValueError:
                messagebox.showerror("Ошибка", "Минимальное количество страниц должно быть числом!")
                return

        self.update_filtered_table(filtered_books)

    def reset_filter(self):
        self.filter_genre.delete(0, tk.END)
        self.filter_pages.delete(0, tk.END)
        self.update_table()

    def update_filtered_table(self, books):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for book in books:
            self.tree.insert("", tk.END, values=(book["title"], book["author"], book["genre"], book["pages"]))
            
    def save_data(self):
        with open("books.json", "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", "Данные сохранены в books.json")

    def load_data(self):
        if os.path.exists("books.json"):
            with open("books.json", "r", encoding="utf-8") as f:
                self.books = json.load(f)
            self.update_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
