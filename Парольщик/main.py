import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import pyperclip
import winsound
import os

import sqlite3 as sql

PATH_DB = "db_dir/data.db"

class Window:
    def __init__(self, width=350, height=200, title="TKINTER"):
        self.root = tk.Tk()
        self.root.geometry(f"{width}x{height}+400+200")
        self.root.title(f"{title}")
        self.root.resizable(False, False)

        self.__connectDB()
        self.__interface()
        self.__run()


    def __run(self):
        self.root.mainloop()

    def __interface(self):
        new_login = 0
        new_password = 0
        array_logins = []

        def go_back():
            combobox.delete(0, tk.END)

            label_text["text"] = "Введи логин - получи пароль!"
            btn["text"] = "Показать!"
            btn["command"] = show_password

            btn_delete["text"] = "Удалить"
            btn_delete["command"] = delete_password_interface

        def show_password():
            global new_login
            global new_password
            
            global PATH_DB

            if combobox.get() in array_logins:
                
                with sql.connect(PATH_DB) as con:
                    cursor = con.cursor()
                    cursor.execute(f"""SELECT password FROM login_password WHERE login == '{combobox.get()}'""")
                    password = cursor.fetchone()[0]
                    print(password)
                    
                pyperclip.copy(password)
                messagebox.showinfo("Успешно", f"Логин: {combobox.get()}\nПароль: {password}")
                
            elif combobox.get() not in array_logins and len(combobox.get()) > 0:
                winsound.MessageBeep()
                if messagebox.askyesno("Ошибка", f"В базе данных нет логина '{combobox.get()}'.\nХотите добавить?"):
                    new_login = combobox.get()
                    array_logins.append(new_login)
                    combobox["value"] = array_logins
                    print(new_login)
                    with sql.connect(PATH_DB) as con:
                        cursor = con.cursor()
                        cursor.execute(f"""INSERT INTO login_password (login) VALUES ('{new_login}')""")
                    btn["command"] = add_password
                    label_text["text"] = "Введите пароль:"
                    btn["text"] = "Добавить!"
                    combobox.delete(0, tk.END)

            else:
                messagebox.showinfo("Ошибка", "Пустое поле")

        def add_password():
            global new_login
            global new_password
            
            global PATH_DB

            if len(combobox.get()) > 0:
                new_password = combobox.get()
                print(new_password)
                with sql.connect(PATH_DB) as con:
                    cursor = con.cursor()
                    cursor.execute(f"UPDATE login_password SET password = '{new_password}' WHERE login == '{new_login}'")
                    con.commit()
                messagebox.showinfo("Успешно", "Сохранено!")
                self.root.update()
                go_back()
                combobox.delete(0, tk.END)
            else:
                messagebox.showinfo("Ошибка", "Введите пароль!")

        def delete_password_interface():
            combobox.delete(0, tk.END)

            label_text["text"] = "Введи логин для удаления"
            btn["text"] = "Удалить!"
            btn["command"] = delete_password

            btn_delete["text"] = "Вернуться"
            btn_delete["command"] = go_back

        def delete_password():
            global PATH_DB
            
            if combobox.get() in array_logins and len(combobox.get()) > 0:
                delete_login = combobox.get()

                with sql.connect(PATH_DB) as con:
                    cursor = con.cursor()
                    cursor.execute(f"DELETE FROM login_password WHERE login = '{delete_login}'")
                    messagebox.showinfo("Успешно", f"Логин '{delete_login}' был успешно удалён!")

                array_logins.remove(delete_login)
                combobox["value"] = array_logins

                combobox.delete(0, tk.END)
                go_back()
        
        def check_event(event):    
            if event.char == "\r":
                show_password()
            elif event.keysym == "Delete":
                if label_text["text"] == "Введи логин - получи пароль!":
                    delete_password_interface()
                elif label_text["text"] == "Введи логин для удаления":
                    go_back()
                    
                
        with sql.connect(PATH_DB) as con:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM login_password")
            array_logins = cursor.fetchall()

            for i in range(len(array_logins)):
                array_logins[i] = array_logins[i][0]

            print(array_logins)
        
        self.root.bind("<Key>", check_event)
        
        main_frame = tk.Frame(self.root)
        label_text = tk.Label(main_frame, text="Введи логин - получи пароль!", font=("Arial", 15))
        combobox = ttk.Combobox(main_frame, font=("Arial", 15), values=array_logins)
        btn = tk.Button(main_frame, text="Показать!",
                        font=("Arial", 12),
                        cursor="hand2",
                        padx=10,
                        command=show_password,
                        )
        
        btn_delete = tk.Button(self.root, text="Удалить",
                               font=("Tahoma", 10),
                               cursor="hand2",
                               padx=10,
                               bd=4,
                               command=delete_password_interface,
                               )

        main_frame.pack(pady=50, padx=30)
        label_text.pack()
        combobox.pack(pady=5)
        btn.pack()
        btn_delete.place(x=250, y=160)

    def __connectDB(self):
        global PATH_DB
        
        if bool(os.path.exists("db_dir")) == False:
            os.mkdir("db_dir")
            
        with sql.connect(PATH_DB) as con:
            cursor = con.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS login_password(
                    login TEXT,
                    password TEXT
)""")
        

root = Window(title="Парольщик")