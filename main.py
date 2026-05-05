import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

# Настройки
HISTORY_FILE = "tasks.json"
DEFAULT_TASKS = [
    {"text": "Прочитать статью", "type": "учёба"},
    {"text": "Сделать зарядку", "type": "спорт"},
    {"text": "Написать отчёт", "type": "работа"},
    {"text": "Посмотреть обучающее видео", "type": "учёба"},
    {"text": "Разобрать почту", "type": "работа"},
    {"text": "Погулять на свежем воздухе", "type": "отдых"},
]

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных задач")
        self.root.geometry("500x500")

        # Загрузка данных
        self.tasks = self.load_tasks()
        self.filtered_tasks = self.tasks.copy()

        # Текущая задача
        self.current_task_label = tk.Label(
            root, text="Нажмите «Сгенерировать задачу»",
            font=("Arial", 12),
            wraplength=450,
            justify="center",
            pady=10
        )
        self.current_task_label.pack()

        # Кнопка генерации
        tk.Button(
            root,
            text="Сгенерировать задачу",
            command=self.generate_task,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10),
            padx=10,
            pady=5
        ).pack(pady=10)

        # Фильтр по типу
        filter_frame = tk.Frame(root)
        filter_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(filter_frame, text="Фильтр по типу:").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar(value="все")
        filter_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=["все", "учёба", "работа", "спорт", "отдых"],
            state="readonly",
            width=10
        )
        filter_combo.pack(side=tk.LEFT, padx=5)
        filter_combo.bind("<<ComboboxSelected>>", self.apply_filter)

        # История задач
        history_frame = tk.Frame(root)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.history_listbox = tk.Listbox(history_frame, height=10)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_listbox.yview)

        # Добавление новых задач
        add_frame = tk.Frame(root)
        add_frame.pack(fill=tk.X, padx=20, pady=5)

        self.new_task_entry = tk.Entry(add_frame, width=30)
        self.new_task_entry.pack(side=tk.LEFT, expand=True)

        self.new_task_type = ttk.Combobox(
            add_frame,
            values=["учёба", "работа", "спорт", "отдых"],
            state="readonly",
            width=10
        )
        self.new_task_type.set("работа")
        self.new_task_type.pack(side=tk.LEFT, padx=5)

        tk.Button(
            add_frame,
            text="Добавить в список",
            command=self.add_new_task
        ).pack(side=tk.LEFT)

        self.update_history_list()

    def load_tasks(self):
        """Загрузка задач из JSON или создание файла с дефолтными задачами."""
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return DEFAULT_TASKS.copy()
        else:
            # Создаём файл с дефолтными задачами
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(DEFAULT_TASKS, f, ensure_ascii=False, indent=2)
            return DEFAULT_TASKS.copy()

    def save_tasks(self):
        """Сохранение задач в JSON."""
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def update_history_list(self):
        """Обновление списка истории."""
        self.history_listbox.delete(0, tk.END)
        for task in self.filtered_tasks:
            self.history_listbox.insert(tk.END, f"{task['text']} ({task['type']})")

    def apply_filter(self, event=None):
        """Применение фильтра по типу задачи."""
        selected_filter = self.filter_var.get()
        if selected_filter == "все":
            self.filtered_tasks = self.tasks
        else:
            self.filtered_tasks = [task for task in self.tasks if task['type'] == selected_filter]
        self.update_history_list()

    def generate_task(self):
        """Генерация случайной задачи."""
        if not self.tasks:
            messagebox.showwarning("Предупреждение", "Список задач пуст! Добавьте новые задачи.")
            return

        selected_task = random.choice(self.tasks)

        # Отображаем задачу в главном лейбле
        self.current_task_label.config(
            text=f"Задача: {selected_task['text']}\nТип: {selected_task['type'].capitalize()}",
            bg="#f0f0f0",
            relief="solid"
        )

        # Добавляем в историю
        self.filtered_tasks.append(selected_task)
        self.
