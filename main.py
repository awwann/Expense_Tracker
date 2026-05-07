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