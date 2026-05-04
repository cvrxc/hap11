import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Имя файла для хранения данных
DATA_FILE = 'books.json'

# Загрузка данных из файла
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Сохранение данных в файл
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Инициализация главного окна
root = tk.Tk()
root.title("Book Tracker")

# Общий список книг
books = load_data()

# ----------- Ввод Полей -----------

frame_input = tk.Frame(root, padx=10, pady=10)
frame_input.pack()

tk.Label(frame_input, text="Название книги").grid(row=0, column=0, sticky='w')
entry_title = tk.Entry(frame_input, width=30)
entry_title.grid(row=0, column=1)

tk.Label(frame_input, text="Автор").grid(row=1, column=0, sticky='w')
entry_author = tk.Entry(frame_input, width=30)
entry_author.grid(row=1, column=1)

tk.Label(frame_input, text="Жанр").grid(row=2, column=0, sticky='w')
entry_genre = tk.Entry(frame_input, width=30)
entry_genre.grid(row=2, column=1)

tk.Label(frame_input, text="Кол. страниц").grid(row=3, column=0, sticky='w')
entry_pages = tk.Entry(frame_input, width=10)
entry_pages.grid(row=3, column=1)

# ----------- Таблица книг -----------

columns = ('Название', 'Автор', 'Жанр', 'Страниц')
tree = ttk.Treeview(root, columns=columns, show='headings', height=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(padx=10, pady=10)

# ----------- Функции -----------

def add_book():
    title = entry_title.get().strip()
    author = entry_author.get().strip()
    genre = entry_genre.get().strip()
    pages = entry_pages.get().strip()

    # Проверка заполнения
    if not title or not author or not genre or not pages:
        messagebox.showwarning("Внимание", "Все поля должны быть заполнены")
        return
    if not pages.isdigit():
        messagebox.showwarning("Внимание", "Количество страниц должно быть числом")
        return

    book = {
        'title': title,
        'author': author,
        'genre': genre,
        'pages': int(pages)
    }
    books.append(book)
    refresh_table()
    # Очистить поля
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_pages.delete(0, tk.END)

def refresh_table(filtered_books=None):
    for item in tree.get_children():
        tree.delete(item)
    data = filtered_books if filtered_books is not None else books
    for b in data:
        tree.insert('', tk.END, values=(b['title'], b['author'], b['genre'], b['pages']))

def save_books():
    save_data(books)
    messagebox.showinfo("Успех", "Данные сохранены!")

def load_books():
    global books
    books = load_data()
    refresh_table()

def filter_books():
    genre_filter = entry_genre_filter.get().strip().lower()
    pages_filter = entry_pages_filter.get().strip()

    filtered = books
    if genre_filter:
        filtered = [b for b in filtered if genre_filter in b['genre'].lower()]
    if pages_filter:
        if pages_filter.isdigit():
            filtered = [b for b in filtered if b['pages'] > int(pages_filter)]
        else:
            messagebox.showwarning("Внимание", "Параметр фильтра по страницам должен быть числом")
            return
    refresh_table(filtered)

def reset_filters():
    entry_genre_filter.delete(0, tk.END)
    entry_pages_filter.delete(0, tk.END)
    refresh_table()

# ----------- Кнопки -----------

btn_frame = tk.Frame(root, padx=10, pady=10)
btn_frame.pack()

tk.Button(btn_frame, text="Добавить книгу", command=add_book).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Сохранить", command=save_books).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Загрузить", command=load_books).grid(row=0, column=2, padx=5)

# ----------- Фильтр -----------

filter_frame = tk.Frame(root, padx=10, pady=10, bd=1, relief=tk.SOLID)
filter_frame.pack()

tk.Label(filter_frame, text="Фильтр по жанру").grid(row=0, column=0, sticky='w')
entry_genre_filter = tk.Entry(filter_frame, width=20)
entry_genre_filter.grid(row=0, column=1)

tk.Label(filter_frame, text="По страницам (> )").grid(row=1, column=0, sticky='w')
entry_pages_filter = tk.Entry(filter_frame, width=20)
entry_pages_filter.grid(row=1, column=1)

tk.Button(filter_frame, text="Применить фильтр", command=filter_books).grid(row=2, column=0, pady=5)
tk.Button(filter_frame, text="Сбросить фильтр", command=reset_filters).grid(row=2, column=1, pady=5)

# Изначальный вывод
refresh_table()

root.mainloop()
