# kanban_desc.py
import os

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from typing import Optional
from kanban_logic import add_task, change_status, delete_task, export_tasks_to_file

from datetime import datetime


# Экспорт созданного файла в папку
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVE_DIR = os.path.join(BASE_DIR, "saved_files")
os.makedirs(SAVE_DIR, exist_ok=True)  # создаёт, если нет директории


# Создаем класс заголовка с окнами
class ProjectHeader(tk.Frame):
    def __init__(self, master):
        super().__init__(master, padx=20, pady=20, bg="Forest Green")
        self.pack(fill="x")

        # Настройка стиля для DateEntry
        style = ttk.Style()
        style.configure("Custom.TLabel", font=("Arial", 16))
        style.configure("Custom.TEntry", font=("Arial", 16))

        # Название проекта
        tk.Label(self, text="Название проекта:", bg="Forest Green", fg="cornsilk1", font=("Arial", 16)) \
            .grid(row=0, column=0, columnspan=4, sticky="n", pady=(0, 5))

        self.project_name = tk.Entry(self, width=30, bg="Beige", fg="green", font=("Arial", 16), justify="center")
        self.project_name.grid(row=1, column=0, columnspan=4, sticky="n", pady=(0, 10))

        # Сроки реализации проекта
        ttk.Label(self, text="Срок реализации проекта:", font=("Arial", 16)).grid(row=2, column=0, columnspan=5,
                                                                              sticky="n", pady=(0, 5))
        # Объединенный фрейм для дат
        date_frame = tk.Frame(self, bg="Forest Green")
        date_frame.grid(row=3, column=0, columnspan=5, pady=(5, 0))

        tk.Label(date_frame, text="С:", bg="Forest Green", fg="cornsilk1", font=("Arial", 16)).pack(side="left", padx=(10, 2))
        self.date_from = DateEntry(date_frame, width=12, date_pattern='dd.mm.yyyy', font=("Arial", 16))
        self.date_from.pack(side="left", padx=(2, 10))

        tk.Label(date_frame, text="По:", bg="Forest Green", fg="cornsilk1", font=("Arial", 16)).pack(side="left", padx=(10, 2))
        self.date_to = DateEntry(date_frame, width=12, date_pattern='dd.mm.yyyy', font=("Arial", 16))
        self.date_to.pack(side="left", padx=(2, 10))

        self.grid_columnconfigure(1, weight=1)


# Глобальная переменная
active_listbox: Optional[tk.Listbox] = None


# Глобальные функции модуля:
# Визуальное оформление интерфейса: объект Style из модуля ttk
def configure_styles():
    style = ttk.Style()
    style.configure("Custom.TLabel", font=("Arial", 16)) # стиль меток
    style.configure("Custom.TEntry", font=("Arial", 16)) # стиль полей ввода


# Извлекаем текст задачи из поля ввода task_entry, передаём его в add_task() получаем обратно структуру с ID и текстом и добавляем его в список задач task_listBox, очищаем поле ввода.
def gui_add_task():
    task = task_entry.get("1.0", tk.END).strip()
    if task:
        task_data = add_task(task) # логика из kanban_logi
        task_listBox.insert(tk.END, f"{task_data['id']}. {task_data['text']}")
        task_entry.delete("1.0", tk.END)
        task_entry.focus_set()


#  Перемещает выбранную задачу из списка "Задачи" в статус "В работе"
def send_to_execution():
    selected = task_listBox.curselection()
    if selected:
        index = selected[0]
        raw_text = task_listBox.get(index)
        task_listBox.delete(index)

        task_id = raw_text.partition(".")[0]
        updated = change_status(task_id, "executing")
        if updated:
            executing_listBox.insert(tk.END, f"{updated['id']}. {updated['text']} ({updated['timestamp']})")


# Перемещает выбранную задачу из списка "В работе" в статус "Тестирование"
def send_to_testing():
    selected = executing_listBox.curselection()
    if selected:
        index = selected[0]
        raw_text = executing_listBox.get(index)
        executing_listBox.delete(index)
        task_id = raw_text.partition(".")[0]
        updated = change_status(task_id, "testing")
        if updated:
            testing_listBox.insert(tk.END, f"{updated['id']}. {updated['text']} ({updated['timestamp']})")


# Перемещает выбранную задачу из списка "Тестирование" в статус "Завершено"
def mark_completed():
    selected = testing_listBox.curselection()
    if selected:
        index = selected[0]
        raw_text = testing_listBox.get(index)
        testing_listBox.delete(index)
        task_id = raw_text.partition(".")[0]
        updated = change_status(task_id, "done")
        if updated:
            completed_listBox.insert(tk.END, f"{updated['id']}. {updated['text']} ({updated['timestamp']})")


# Удаляет выбранную задачу из активного списка и из логики
def gui_delete_task():
    global active_listbox
    if isinstance(active_listbox, tk.Listbox):
        selected = active_listbox.curselection()
        if selected:
            raw_text = active_listbox.get(selected[0])
            task_id = raw_text.partition(".")[0]
            active_listbox.delete(selected[0])
            delete_task(task_id)  # ← вызов из kanban_logic


# Устанавливает активный Listbox для операций (удаление, перемещение и т.д.)
# в глобальную переменную active_listbox, чтобы другие функции могли работать
# с текущим выбранным списком задач, независимо от его статуса
def set_active_listbox(lb):
    global active_listbox
    active_listbox = lb


# Открываем всплывающее окно с полной информацией о выбранной задаче
# двойным кликом мыши
def show_full_task(event):
    widget = event.widget
    if isinstance(widget, tk.Listbox):
        selection = widget.curselection()
        if selection:
            index = selection[0]
            raw_text = widget.get(index)
            top = tk.Toplevel()
            top.title("Полная задача")
            top.configure(bg="Beige")
            tk.Label(top, text=raw_text, wraplength=500, justify="left",
                     bg="Beige", fg="darkgreen", font=("Arial", 14)).pack(padx=20, pady=20)


# Экспорт в txt файл
def export_export():
    print("Кнопка нажата — экспорт начат")
    # Экспорт в фиксированный файл (для отладки или резервной копии)
    export_tasks_to_file("kanban_export.txt")
    print("Экспорт завершён.")

    # Формируем имя файла с меткой времени
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"kanban_export_{timestamp}.txt"
    full_path = os.path.join(SAVE_DIR, filename)

    # Повторный экспорт в файл с уникальным именем
    export_tasks_to_file(full_path)
    # Уведомляем об успешном экспорте
    messagebox.showinfo("Экспорт", f"Задачи сохранены в:\n{filename}")

# Инициализируем главное окно интерфейса
root = tk.Tk()
root.title("Kanban-доска проекта")
root.configure(background="Forest Green")

# Применяем стили
configure_styles()
header = ProjectHeader(root) # Заголовок проекта

# Ввод задачи
text1 = tk.Label(root, text="Ввод задачи", bg="Forest Green", fg="cornsilk1", font=("Arial", 16))
text1.pack(pady=5)

task_entry = tk.Text(root, height=3, width=50, bg="Beige", fg="green", font=("Arial", 14))
task_entry.pack(pady=10, padx=10)
task_entry.focus_set()


# Добавляем виджет для мыши с контекстным меню
def show_context_menu(event):
    widget = event.widget
    context_menu = tk.Menu(widget, tearoff=0)
    context_menu.add_command(label="Вырезать", command=lambda: widget.event_generate("<<Cut>>"))
    context_menu.add_command(label="Копировать", command=lambda: widget.event_generate("<<Copy>>"))
    context_menu.add_command(label="Вставить", command=lambda: widget.event_generate("<<Paste>>"))
    context_menu.tk_popup(event.x_root, event.y_root)

task_entry.bind("<Button-3>", show_context_menu)


# Добавляем ручную вставку текста: Ctrl+V
# работает только при латинской раскладке клавиатуры
# (tkinter отслеживает символ, а не физическую клавишу)
def paste_clipboard(_=None):
    try:
        text = root.clipboard_get()
        task_entry.insert(tk.INSERT, text)
    except tk.TclError:
        pass

# Бинды для Ctrl+V — вызывают встроенное событие вставки
task_entry.bind("<Control-v>", paste_clipboard)
task_entry.bind("<Control-V>", paste_clipboard)

task_entry.bind("<FocusIn>", lambda e: task_entry.config(bg="lightyellow"))
task_entry.bind("<FocusOut>", lambda e: task_entry.config(bg="Beige"))


# Кнопка для теста вставки вручную
tk.Button(root, text="Вставить", command=paste_clipboard).pack()


# Кнопки
button_frame = tk.Frame(root, bg="Forest Green")
button_frame.pack(pady=5)

tk.Button(button_frame, text="Добавить", bg="cadetblue1", command=gui_add_task).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Выполнение", bg="lightblue", command=send_to_execution).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Тестирование", bg="lightsteelblue", command=send_to_testing).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Выполнено", bg="chartreuse2", command=mark_completed).grid(row=0, column=3, padx=5)
tk.Button(button_frame, text="Удалить", bg="coral", command=gui_delete_task).grid(row=0, column=4, padx=5)
tk.Button(button_frame, text="Сохранить в файл", bg="lightblue", command=export_export).grid(row=0, column=6, padx=5)

# Основной фрейм со списками (4)
lists_frame = tk.Frame(root, bg="Forest Green")
lists_frame.pack(fill="both", expand=True, padx=10, pady=10)


def create_list_row(parent, title, bg_color, fg_color):
    # Горизонтальный блок: метка + список задач с прокруткой
    row_frame = tk.Frame(parent, bg="Forest Green")
    row_frame.pack(fill="x", pady=5)

    # Заголовок списка слева
    label = tk.Label(row_frame, text=title, bg="Forest Green", fg=fg_color, font=("Arial", 16), width=18, anchor="w")
    label.grid(row=0, column=0, sticky="w", padx=(10, 5))

    # Контейнер для списка задач и вертикальной прокрутки
    list_frame = tk.Frame(row_frame)
    list_frame.grid(row=0, column=1, sticky="ew")

    listbox = tk.Listbox(list_frame, height=6, bg=bg_color, fg="black", font=("Arial", 14), width=80)
    listbox.grid(row=0, column=0, sticky="ew")

    # Вертикальная прокрутка для списка
    scrollbar = tk.Scrollbar(list_frame, orient= "vertical", command=listbox.yview, width=14)
    scrollbar.grid(row=0, column=1, sticky="ns")
    listbox.config(yscrollcommand=scrollbar.set)

    # Адаптируем ширину колонок для равномерного распределения
    row_frame.grid_columnconfigure(0, weight=1)
    row_frame.grid_columnconfigure(1, weight=1)

    return listbox


# Создаём четыре списка задач по статусам:
task_listBox = create_list_row(lists_frame, "Список задач", "LightSeaGreen", "plum2")
executing_listBox = create_list_row(lists_frame, "Выполнение", "lightgoldenrod", "lightyellow")
testing_listBox = create_list_row(lists_frame, "Тестирование", "lavender", "lightblue")
completed_listBox = create_list_row(lists_frame, "Выполнено", "lightgray", "lightgreen")


#  Назначаем обработчики для каждого списка:
# - при фокусе сохраняем активный список
# - при двойном клике открываем задачу во всплывающем окне
for lb in [task_listBox, executing_listBox, testing_listBox, completed_listBox]:
    lb.bind("<FocusIn>", lambda e, lb=lb: set_active_listbox(lb))
    lb.bind("<Double-Button-1>", show_full_task)


# Запускаем главный цикл интерфейса
root.mainloop()
