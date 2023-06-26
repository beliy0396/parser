import ttkbootstrap as ttk
import os
import sqlite3
from tkinter import *
from ttkbootstrap.dialogs import Messagebox

class Main(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db


    def init_main(self):
        label_title = ttk.Label(self, text='Авторизация в системе', font=("Helvetica", 24, 'bold'))
        label_title.pack(pady=50)

        label_login = ttk.Label(self, text='Введите логин', font=("Helvetica", 14, 'bold'))
        label_login.pack()
        self.entry_login = ttk.Entry(self, bootstyle="secondary", font=("Helvetica", 10, 'bold'))
        self.entry_login.pack(pady=(5, 30))

        label_password = ttk.Label(self, text='Введите пароль', font=("Helvetica", 14, 'bold'))
        label_password.pack()
        self.entry_password = ttk.Entry(self, bootstyle="secondary", font=("Helvetica", 10, 'bold'))
        self.entry_password.pack(pady=(5, 30))

        btn_authorization = ttk.Button(self, text='Авторизация', bootstyle="secondary", width=20,
                                       command=self.check_login_and_password)
        btn_authorization.pack()

    def check_login_and_password(self):
        login = self.entry_login.get()
        password = self.entry_password.get()

        with sqlite3.connect("db.db") as file_db:
            cur = file_db.cursor()
        response = cur.execute(f"SELECT id FROM users WHERE login = '{login}' AND password = '{password}'")
        results = response.fetchall()

        if results:
            success = Messagebox.show_info('Успешная авторизация!')
            root.withdraw()
            self.open()
        else:
            dont_success = Messagebox.show_info('Неверный логин или пароль!')

    def open(self):
        root.withdraw()
        os.system("python main.py")
        root.destroy()

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.cur = self.conn.cursor()

        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, login TEXT, password TEXT)'''
        )
        self.conn.commit()

if __name__ == "__main__":
    root = ttk.Window(themename='darkly')
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Авторизация')
    root.iconbitmap('')
    root.geometry('800x500')
    root.resizable(False, False)
    root.mainloop()