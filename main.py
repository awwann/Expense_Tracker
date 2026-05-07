import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
from datetime import datetime

# --- Конфигурация ---
CATEGORIES = ["Еда", "Транспорт", "Развлечения", "Жилье", "Здоровье"]
JSON_FILE = "data.json"

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Загрузка данных из файла
        self.expenses = self.load_expenses()

        # --- Виджеты ---
        # Фрейм ввода данных
        input_frame = tk.LabelFrame(root, text="Добавить расход", padx=10, pady=10)
        input_frame.pack(pady=10, fill='x', padx=20)

        # Сумма
        tk.Label(input_frame, text="Сумма:").grid(row=0, column=0, sticky='w')
        self.sum_entry = tk.Entry(input_frame, width=15)
        self.sum_entry.grid(row=0, column=1, padx=5)

        # Категория
        tk.Label(input_frame, text="Категория:").grid(row=0, column=2, sticky='w')
        self.category_combobox = ttk.Combobox(input_frame, values=CATEGORIES, state="readonly", width=15)
        self.category_combobox.current(0)
        self.category_combobox.grid(row=0, column=3, padx=5)

        # Дата
        tk.Label(input_frame, text="Дата:").grid(row=0, column=4, sticky='w')
        self.date_entry = DateEntry(input_frame, date_pattern='dd.mm.yyyy', width=15)
        self.date_entry.grid(row=0, column=5, padx=5)