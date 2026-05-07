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

        # Кнопка добавления
        add_button = tk.Button(input_frame, text="Добавить расход", command=self.add_expense)
        add_button.grid(row=0, column=6, padx=15)

        # Фрейм с таблицей и фильтрами
        main_frame = tk.Frame(root)
        main_frame.pack(fill='both', expand=True, padx=20)

        # Фильтры
        filter_frame = tk.Frame(main_frame)
        filter_frame.pack(fill='x', pady=(10, 0))

        # Фильтр по категории
        tk.Label(filter_frame, text="Фильтр по категории:").pack(side='left')
        self.filter_category = ttk.Combobox(filter_frame, values=["Все"] + CATEGORIES, state="readonly", width=15)
        self.filter_category.current(0)
        self.filter_category.pack(side='left', padx=(5, 20))

        # Фильтр по дате (от/до)
        tk.Label(filter_frame, text="Фильтр по дате:").pack(side='left')

        filter_date_subframe = tk.Frame(filter_frame)
        filter_date_subframe.pack(side='left')

        tk.Label(filter_date_subframe, text="с").pack(side='left')
        self.filter_date_from = DateEntry(filter_date_subframe, date_pattern='dd.mm.yyyy', width=10)
        self.filter_date_from.pack(side='left', padx=(2, 5))

        tk.Label(filter_date_subframe, text="по").pack(side='left')
        self.filter_date_to = DateEntry(filter_date_subframe, date_pattern='dd.mm.yyyy', width=10)
        self.filter_date_to.pack(side='left', padx=(2, 5))

        filter_btn = tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        filter_btn.pack(side='left', padx=(20, 0))

        # Таблица расходов (Treeview)
        columns = ("id", "sum", "category", "date")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings")

        # Настройка ширины колонок и заголовков
        self.tree.column("sum", width=80, anchor='e')
        self.tree.column("category", width=150)
        self.tree.column("date", width=120)
        self.tree.heading("sum", text="Сумма")
        self.tree.heading("category", text="Категория")
        self.tree.heading("date", text="Дата")

        self.tree.pack(fill='both', expand=True, pady=(10, 0))

        # Полоса прокрутки для таблицы
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Фрейм для анализа (сумма за период)
        analysis_frame = tk.LabelFrame(root, text="Анализ расходов", padx=10, pady=10)
        analysis_frame.pack(pady=10, fill='x', padx=20)

        tk.Label(analysis_frame, text="Период:").grid(row=0, column=0, sticky='w')

        period_subframe = tk.Frame(analysis_frame)
        period_subframe.grid(row=1, column=0, sticky='w')

        tk.Label(period_subframe, text="с").pack(side='left')
        self.analysis_date_from = DateEntry(period_subframe, date_pattern='dd.mm.yyyy', width=10)
        self.analysis_date_from.pack(side='left', padx=(2, 5))

        tk.Label(period_subframe, text="по").pack(side='left')
        self.analysis_date_to = DateEntry(period_subframe, date_pattern='dd.mm.yyyy', width=10)
        self.analysis_date_to.pack(side='left', padx=(2, 5))

        calc_btn = tk.Button(analysis_frame, text="Посчитать сумму", command=self.calculate_sum_period)
        calc_btn.grid(row=2, column=0, pady=(5, 0))

        self.sum_result_label = tk.Label(analysis_frame, text="Сумма: 0 ₽", font=('Arial', 12))
        self.sum_result_label.grid(row=3, column=0)

    def load_expenses(self):
        """Загружает расходы из файла JSON."""
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_expenses(self):
        """Сохраняет расходы в файл JSON."""
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.expenses, f, ensure_ascii=False, indent=2)

    def display_expenses(self):
       """Отображает расходы в таблице."""
        for row in self.tree.get_children():
           self.tree.delete(row)

        for expense in self.expenses:
           self.tree.insert("", "end", values=(expense["id"], expense["sum"], expense["category"], expense["date"]))

    def add_expense(self):
       """Обрабатывает добавление нового расхода."""
       try:
           sum_value = float(self.sum_entry.get())
           if sum_value <= 0:
               raise ValueError("Сумма должна быть положительной.")

           category = self.category_combobox.get()
           date_str = self.date_entry.get_date().strftime('%d.%m.%Y')

           new_expense = {
              "id": len(self.expenses) + 1,
              "sum": sum_value,
              "category": category,
              "date": date_str
           }

           self.expenses.append(new_expense)
           self.save_expenses()
           self.display_expenses()

           # Очистка полей после успешного добавления
           self.sum_entry.delete(0, 'end')
           messagebox.showinfo("Успех", "Расход добавлен!")

       except ValueError as e:
           messagebox.showerror("Ошибка ввода", str(e))
       except Exception as e:
           messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка: {e}")

    def apply_filter(self):
       """Применяет фильтры к таблице."""
       filtered_cat = self.filter_category.get()
       date_from = self.filter_date_from.get_date()
       date_to = self.filter_date_to.get_date()
