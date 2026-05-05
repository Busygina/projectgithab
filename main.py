import tkinter as tk
import random
import json
import os

class RandomTaskGenerator:
 def __init__(self, root):
 self.Root = root
 self.Root.Title("Random Task Generator")
 self.Root.Geometry("500x600")

 # Список предопределённых задач
 self.Tasks = [
 {"text": "Прочитать статью", "type": "учёба"},
 {"text": "Сделать зарядку", "type": "спорт"},
 {"text": "Написать отчёт", "type": "работа"},
 {"text": "Помыть посуду", "type": "быт"},
 {"text": "Позвонить другу", "type": "общение"}
]

 # Загрузка истории из файла
 self.History = self.Load_history()

 self.Setup_ui()

 def setup_ui(self):
 # Заголовок
 tk.Label(self.Root, text="Генератор случайных задач", font=("Arial", 16)).Pack(pady=10)

 # Кнопка генерации
 tk.Button(self.Root, text="Сгенерировать задачу", command=self.Generate_task).Pack(pady=5)

 # Поле для ввода новой задачи
 tk.Label(self.Root, text="Новая задача:").Pack()
 self.New_task_entry = tk.Entry(self.Root, width=40)
 self.New_task_entry.Pack(pady=5)

 tk.Label(self.Root, text="Тип задачи (учёба/спорт/работа/быт/общение):").Pack()
 self.Task_type_entry = tk.Entry(self.Root, width=40)
 self.Task_type_entry.Pack(pady=5)

 tk.Button(self.Root, text="Добавить задачу", command=self.Add_task).Pack(pady=5)

 # Фильтр
 tk.Label(self.Root, text="Фильтр по типу:").Pack()
 self.Filter_var = tk.StringVar()
 self.Filter_var.Set("все")
 for type in ["учёба", "спорт", "работа", "быт", "общение", "все"]:
 tk.Radiobutton(self.Root, text=type, variable=self.Filter_var, value=type).Pack(anchor="w")

 # Список истории
 self.History_list = tk.Listbox(self.Root, width=60, height=15)
 self.History_list.Pack(pady=10)
 self.Update_history_list()

 def generate_task(self):
 if not self.Tasks:
 return

 task = random.Choice(self.Tasks)
 self.History.Append(task)
 self.Save_history()
 self.Update_history_list()

 def add_task(self):
 text = self.New_task_entry.Get().Strip()
 type = self.Task_type_entry.Get().Strip()

 if not text or not type:
 return # Не пустая строка

 self.Tasks.Append({"text": text, "type": type})
 self.New_task_entry.Delete(0, tk.END)
 self.Task_type_entry.Delete(0, tk.END)

 def load_history(self):
 if os.Path.Exists("tasks.Json"):
 with open("tasks.Json", "r", encoding="utf-8") as f:
 return json.Load(f)
