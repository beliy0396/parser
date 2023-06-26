import ttkbootstrap as ttk
import sqlite3
import pandas as pd
from tkinter import *
import requests


class Main(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db

    def init_main(self):
        self.tree = ttk.Treeview(self, columns=('IP', 'Дата и время запроса'), show='headings')
        self.tree.heading('IP', text='IP-адрес')
        self.tree.heading('Дата и время запроса', text='Дата и время запроса')
        self.tree.column('IP', width=350, anchor=ttk.CENTER)
        self.tree.column('Дата и время запроса', width=350, anchor=ttk.CENTER)
        self.tree.pack(pady=25)

        get_and_insert_btn = ttk.Button(self, text="Загрузить данные", bootstyle="secondary", command=self.get_data)
        get_and_insert_btn.pack(side=ttk.LEFT, padx=47, pady=5)

        sort_by_time_new_btn = ttk.Button(self, text="Сортировать(новые записи)", bootstyle="secondary", command=self.sort_by_time_new)
        sort_by_time_new_btn.pack(side=ttk.LEFT, padx=47, pady=5)

        sort_by_time_old_btn = ttk.Button(self, text="Сортировать(старые записи)", bootstyle="secondary", command=self.sort_by_time_old)
        sort_by_time_old_btn.pack(side=ttk.LEFT, padx=47, pady=5)



    def get_data(self):
        response = requests.get('http://158.160.34.105:5002/logs?')
        data = response.json()

        self.db.cur.execute('CREATE TABLE IF NOT EXISTS logs (ip_address TEXT, request_time TEXT)')
        self.db.cur.execute('DELETE FROM logs')
        for item in data:
            ip_address = item.get('ip_address', '')
            request_time = item.get('request_time', '')
            self.db.cur.execute('INSERT INTO logs VALUES (?, ?)', (ip_address, request_time))
        self.db.conn.commit()
        self.load_table()



    def sort_by_time_new(self):
        self.db.cur.execute(
            '''SELECT * FROM logs ORDER BY request_time DESC'''
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

    def sort_by_time_old(self):
        self.db.cur.execute(
            '''SELECT * FROM logs ORDER BY request_time ASC'''
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]


    def load_table(self):
        self.db.cur.execute(
            '''SELECT * FROM logs'''
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.cur = self.conn.cursor()

        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS logs(ip_address TEXT, request_time TEXT)'''
        )
        self.conn.commit()

if __name__ == "__main__":
    root = ttk.Window(themename='darkly')
    db = DB()
    app = Main(root)
    app.pack()
    root.title('API')
    root.iconbitmap('')
    root.geometry('800x300')
    root.resizable(False, False)
    root.mainloop()