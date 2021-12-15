import tkinter as tk
from tkinter import messagebox

import os
import winsound
import sqlite3 as sql

##Для размешения по центру
import ctypes
user32 = ctypes.windll.user32

PATH_DATA = "base_file/data.db"

BALANCE = 0
SPEND = 0

VALUE_BALANCE = 0
VALUE_SPEND = 0


###Доделать чтобы не было NULL в обнулении баланса (Доделано 2.12.21)

class Window:
    def __init__(self, width=500, height=400, title="TKINTER GUI"):
        self.root = tk.Tk()
        self.root.geometry(f"{width}x{height}+{user32.GetSystemMetrics(0)//2-250}+{user32.GetSystemMetrics(1)//2-250}")
        self.root.title(title)
        self.root.resizable(False, False)
        self.root.configure(padx=15, pady=15)

        self.__connectDB()
        self.__interface()
        self.__run()

    def __run(self):
        self.root.mainloop()

    def __interface(self):
        global BALANCE
        global SPEND
        global CHECK_VAR

        def itog():
            if label_balance["text"] != "Баланс: Не указан":
                if BALANCE > SPEND:
                    messagebox.showinfo("Итог", f"Баланс превышает расходы.\nБаланс: {BALANCE}\nРасходы: {SPEND}\nРазница составляет {abs(BALANCE-SPEND)}")
                elif BALANCE < SPEND:
                    messagebox.showinfo("Итог", f"Расходы превышают баланс.\nБаланс: {BALANCE}\nРасходы: {SPEND}\nРазница составляет {abs(BALANCE-SPEND)}")
                elif BALANCE == SPEND:
                    messagebox.showinfo(f"Итог", "Баланс и расходы равны.\nБаланс: {BALANCE}\nРасходы: {SPEND}")
            elif label_balance["text"] == "Баланс: Не указан":
                messagebox.showinfo("Итог", f"Вы должны указать баланс!\nБаланс: Не указан\nРасходы: {SPEND}")
        
        def optimize_text():
            global SPEND

            if len(str(SPEND)) >= 5:
                label_spend["text"] = f"Расход: {SPEND}"
            elif len(str(SPEND)) >= 10:
                label_spend["text"] = f"{SPEND}"
            else:
                label_spend["text"] = f"Тотальный расход: {SPEND}"

        def clear():
            block_send["state"] = tk.NORMAL
            block_send.delete("1.0", tk.END)
            block_send["state"] = tk.DISABLED

        def zero_spend():
            global SPEND

            if SPEND == 0:
                winsound.MessageBeep()
            else:
                # print(VALUE_SPEND)
                with sql.connect(PATH_DATA) as con:
                    cursor = con.cursor()
                    cursor.execute(
                        f"""UPDATE spend_reason SET spend_zero = 1 WHERE rowid == (SELECT max(rowid) FROM spend_reason)""")

                block_send["state"] = tk.NORMAL
                block_send.insert(tk.END,f"----------------------------\nОбнуление расходов |{SPEND}|\n----------------------------\n")
                block_send["state"] = tk.DISABLED

                SPEND = 0
                label_spend["text"] = f"Тотальный расход: {SPEND}"

        def zero_balance():
            global BALANCE

            if BALANCE == 0:
                print(BALANCE)
                winsound.MessageBeep()
            else:
                with sql.connect(PATH_DATA) as con:
                    cursor = con.cursor()
                    cursor.execute("""UPDATE spend_reason SET balance_zero = 1 WHERE rowid == (SELECT max(rowid) FROM spend_reason)""")

                block_send["state"] = tk.NORMAL
                block_send.insert(tk.END,
                                  f"----------------------------\nОбнуление баланса |{BALANCE}|\n----------------------------\n")
                block_send["state"] = tk.DISABLED

                BALANCE = 0
                label_balance["text"] = f"Баланс: {BALANCE}"

        def zero_all():
            global BALANCE, SPEND

            if BALANCE == 0 and SPEND == 0:
                winsound.MessageBeep()
            else:
                block_send["state"] = tk.NORMAL
                block_send.insert(tk.END,
                                  f"----------------------------\nОбнуление расходов |{SPEND}|\n----------------------------\n")
                block_send.insert(tk.END,
                                  f"----------------------------\nОбнуление баланса |{BALANCE}|\n----------------------------\n")
                block_send["state"] = tk.DISABLED

                SPEND = 0
                BALANCE = 0

                label_spend["text"] = f"Тотальный расход: {SPEND}"
                label_balance["text"] = f"Баланс: {BALANCE}"

        def create_spend():
            def btn_event(event):
                if event.char == "\r":
                    add_spend_block()

            def add_spend_block():
                global BALANCE
                global SPEND
                global CHECK_VAR

                block_send["state"] = tk.NORMAL

                try:
                    if len(new_entry.get()) > 0 and (
                            type(int(eval(new_entry.get()))) == int or type(float(eval(new_entry.get()))) == float) and eval(new_entry.get()) >= 0:
                        SPEND += float(eval(new_entry.get()))
                        VALUE_SPEND = float(eval(new_entry.get()))
                        label_spend["text"] = f"Тотальный расход: {SPEND}"

                        if len(new_entry2.get()) > 0:
                            # label_spend_down["text"] = f"Расход: {new_entry.get()} - Причина расхода: {new_entry2.get()}"

                            with sql.connect(PATH_DATA) as con:
                                cursor = con.cursor()

                                cursor.execute("""SELECT * FROM spend_reason""")
                                data = cursor.fetchall()

                                if len(data) == 0:
                                    print(len(data))
                                    cursor.execute(
                                    f"""INSERT INTO spend_reason (spend, reason) VALUES ({eval(new_entry.get())}, '{new_entry2.get()}')""")
                                elif data[-1][0] == -1 and data[-1][1] == BALANCE:
                                    cursor.execute(f"""UPDATE spend_reason SET spend = {eval(new_entry.get())}, reason = '{new_entry2.get()}' WHERE rowid = (SELECT max(rowid) FROM spend_reason)""")
                                else:
                                    cursor.execute(f"""INSERT INTO spend_reason (spend, reason) VALUES ({eval(new_entry.get())}, '{new_entry2.get()}')""")

                            block_send.insert(tk.END,
                                              f"------------------\nРасход: {float(eval(new_entry.get()))} - Причина расхода: {new_entry2.get()}\n\n")
                        else:
                            # label_spend_down["text"] = f"Расход: {new_entry.get()}"
                            with sql.connect(PATH_DATA) as con:
                                cursor = con.cursor()

                                cursor.execute("""SELECT * FROM spend_reason""")
                                data = cursor.fetchall()

                                if len(data) == 0:
                                    print("Типо ноль", len(data))
                                    cursor.execute(
                                    f"""INSERT INTO spend_reason (spend) VALUES ({eval(new_entry.get())})""")
                                elif data[-1][0] == -1 and data[-1][1] == BALANCE:
                                    cursor.execute(f"""UPDATE spend_reason SET spend = {eval(new_entry.get())} WHERE rowid = (SELECT max(rowid) FROM spend_reason)""")
                                else:
                                    cursor.execute(f"""INSERT INTO spend_reason (spend) VALUES ({eval(new_entry.get())})""")

                            block_send.insert(tk.END,
                                              f"------------------\nРасход: {float(eval(new_entry.get()))} - Причина расхода: Не указано\n\n")

                        new_entry.delete(0, tk.END)
                        new_entry2.delete(0, tk.END)
                    else:
                        winsound.MessageBeep()
                        new_entry2.delete(0, tk.END)

                    optimize_text()
                except:
                    # print(type(float(new_entry.get())))
                    winsound.MessageBeep()
                    new_entry.delete(0, tk.END)
                    new_entry2.delete(0, tk.END)

                block_send["state"] = tk.DISABLED

            new_win = tk.Toplevel(self.root)
            new_win.geometry(f"200x130+{user32.GetSystemMetrics(0)//2-500}+{user32.GetSystemMetrics(1)-450}")
            new_win.title("Добавление расхода")
            new_win.resizable(False, False)

            new_win.bind("<Key>", btn_event)

            new_label = tk.Label(new_win, text="Сумма расхода:", font=("Tahoma", 10))
            new_label2 = tk.Label(new_win, text="Расход на что:", font=("Tahoma", 10))
            new_entry = tk.Entry(new_win)
            new_entry2 = tk.Entry(new_win)
            new_btn = tk.Button(new_win, text="Добавить", font=("Tahoma", 10),
                                cursor="hand2",
                                command=add_spend_block
                                )

            # new_win.pack()
            new_entry.focus_set()

            if new_win:
                new_win.focus_set()
                new_win.grab_set()

            # new_win.focus_set()
            new_label.pack()
            new_entry.pack()
            new_label2.pack()
            new_entry2.pack()
            new_btn.pack(pady=10)

        def change_balance():
            global BALANCE

            def btn_event(event):
                if event.char == "\r":
                    balance_new()

            def balance_new():
                global BALANCE

                try:
                    if len(new_entry.get()) > 0 and type(float(eval(new_entry.get()))) == float and eval(new_entry.get()) >= 0:
                        BALANCE = float(eval(new_entry.get()))

                        with sql.connect(PATH_DATA) as con:
                            cursor = con.cursor()
                            cursor.execute("""SELECT * FROM spend_reason""")

                            data_db = cursor.fetchall()

                            if len(data_db) > 0:
                                cursor.execute(f"""UPDATE spend_reason SET balance = {BALANCE} WHERE rowid == (SELECT max(rowid) FROM spend_reason)""")
                            else:
                                cursor.execute(f"""INSERT INTO spend_reason (balance) VALUES ({BALANCE})""")

                        label_balance["text"] = f"Баланс: {BALANCE}"
                        new_win.destroy()
                    
                    else:
                        winsound.MessageBeep()
                        new_entry.delete(0, tk.END)


                except ValueError:
                    winsound.MessageBeep()
                    new_entry.delete(0, tk.END)

            new_win = tk.Toplevel(self.root)
            new_win.geometry(f"200x90+{user32.GetSystemMetrics(0)//2-500}+{user32.GetSystemMetrics(1)-450}")
            new_win.resizable(False, False)

            new_win.bind("<Key>", btn_event)

            new_label = tk.Label(new_win, text="Баланс:", font=("Tahoma", 10))
            new_entry = tk.Entry(new_win)
            new_btn = tk.Button(new_win, text="Задать значение", font=("Tahoma", 10),
                                cursor="hand2",
                                command=balance_new,
                                )

            if new_win:
                new_win.focus_set()
                new_win.grab_set()

            new_entry.focus_set()
            new_label.pack()
            new_entry.pack()
            new_btn.pack(pady=5)

        def checkDB():
            global BALANCE, VALUE_BALANCE
            global SPEND, VALUE_SPEND

            #local_spend = SPEND

            block_send["state"] = tk.NORMAL

            with sql.connect(PATH_DATA) as con:
                cursor = con.cursor()
                cursor.execute("""SELECT * FROM spend_reason""")

                array_db = cursor.fetchall()
                print(array_db)
                for data in array_db:
                    if type(data[1]) == float or type(data[1]) == int:
                        BALANCE += float(data[1])

                    if data[0] != -1:
                        SPEND += data[0]

                    ##Тут мы будем чекать баланс и вставлять его в переременную
                    if type(data[1]) == float or type(data[1]) == int:
                        BALANCE = float(data[1])
                        label_balance["text"] = f"Баланс {BALANCE}"

                    if data[2] != "Не указано" and data[0] != -1:
                        print(len(data))
                        block_send.insert(tk.END,
                                          f"------------------\nРасход: {data[0]} - Причина расхода: {data[1]}\n\n")
                    elif data[2] == "Не указано" and data[0] != -1:
                        print(len(data))
                        block_send.insert(tk.END, f"------------------\nРасход: {data[0]} - Причина расхода: Не указана\n\n")
                    ##Тут мы будем чекать обнуление расходов
                    if data[3] == 1:
                        block_send.insert(tk.END, f"----------------------------\nОбнуление расходов |{SPEND}|\n----------------------------\n")
                        SPEND = 0
                    ##Тут мы чекаем обнуление баланса
                    if data[4] == 1:
                        block_send.insert(tk.END, f"----------------------------\nОбнуление баланса |{BALANCE}|\n----------------------------\n")
                        BALANCE = 0


                block_send["state"] = tk.DISABLED
                label_spend["text"] = f"Тотальный расход: {SPEND}"

        def clearDB():
            global SPEND

            if messagebox.askyesno("Подтвердите действие", "Вы действительно хотите очистить базу данных?"):
                with sql.connect(PATH_DATA) as con:
                    cursor = con.cursor()
                    cursor.execute("""DELETE FROM spend_reason""")

                BALANCE = 0
                label_balance["text"] = "Баланс: Не указан"

                SPEND = 0
                label_spend["text"] = f"Тотальный расход: {SPEND}"

                block_send["state"] = tk.NORMAL
                block_send.delete("1.0", tk.END)
                block_send["state"] = tk.DISABLED

            else:
                winsound.MessageBeep()

        menu = tk.Menu(self.root)

        down_menu = tk.Menu(self.root, tearoff=0)
        down_menu.add_command(label="Обнулить баланс", command=zero_balance)
        down_menu.add_command(label="Обнулить расходы", command=zero_spend)
        down_menu.add_command(label="Обнулить всё", command=zero_all)

        menu.add_cascade(label="Взаимодействие", menu=down_menu)
        menu.add_command(label="Рассчитать", command=itog)
        menu.add_command(label="Очистить базу данных", command=clearDB)
        self.root.config(menu=menu)

        top_frame = tk.Frame(self.root)

        left_frame = tk.Frame(top_frame)
        right_frame = tk.Frame(top_frame)

        label_balance = tk.Label(left_frame, text=f"Баланс: Не указан",
                                 font=("Tahoma", 11)
                                 )
        label_spend = tk.Label(left_frame, text=f"Тотальный расход: {SPEND}",
                               font=("Tahoma", 11)
                               )
        btn_add = tk.Button(right_frame, text="Добавить расход", cursor="hand2",
                            font=("Tahoma", 11),
                            command=create_spend
                            )
        btn_balance = tk.Button(self.root, text="Изменить", cursor="hand2",
                                font=("Tahoma", 7),
                                command=change_balance,
                                )

        down_frame_text = tk.Frame(self.root, width=500, height=30)
        text_down_frame = tk.Frame(down_frame_text)
        # down_frame_blocks = tk.LabelFrame(self.root, width=500, height=30)
        main_frame_blocks = tk.Frame(self.root)
        block_send = tk.Text(main_frame_blocks, font=("Tahoma", 11),
                             bg="#f0f0f0",
                             state=tk.DISABLED,
                             cursor="arrow",
                             width=400
                             )
        scroll = tk.Scrollbar(main_frame_blocks)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        block_send.config(yscrollcommand=scroll.set)
        scroll.config(command=block_send.yview)

        # spends_blocks = tk.LabelFrame(down_frame_blocks)
        text_spend = tk.Label(text_down_frame, text="История расходов:",
                              font=("Tahoma", 11),
                              )
        btn_clear = tk.Button(self.root, text="Очистить",
                              font=("Tahoma", 7),
                              cursor="hand2",
                              command=clear,
                              )

        btn_zero = tk.Button(self.root, text="Расходы(Обнулить)",
                             font=("Tahoma", 7),
                             cursor="hand2",
                             command=zero_spend,
                             )

        # a = tk.Label(spends_blocks, text="aaa")

        top_frame.pack(side=tk.TOP)
        right_frame.pack(side=tk.RIGHT, padx=40)
        label_balance.pack()
        label_spend.pack()
        left_frame.pack(side=tk.LEFT, padx=40)
        btn_add.pack()

        down_frame_text.pack(pady=20, side=tk.TOP)
        down_frame_text.pack_propagate(False)
        text_down_frame.pack(side=tk.LEFT)
        # down_frame_blocks.pack(side=tk.TOP)
        # down_frame_blocks.pack_propagate(False)
        # spends_blocks.pack(side=tk.LEFT)
        text_spend.pack(side=tk.LEFT)
        main_frame_blocks.pack(side=tk.TOP, fill=tk.X)
        block_send.pack(side=tk.LEFT, fill=tk.X)
        block_send.pack_propagate()
        # main_frame_blocks.pack_propagate(False)
        # a.pack()
        # btn_add.place(x=300, y=3)
        btn_balance.place(x=0, y=3)
        btn_clear.place(x=417, y=420)
        btn_zero.place(x=0, y=420)

        checkDB()
        optimize_text()

    def __connectDB(self):
        if bool(os.path.exists("base_file")) == False:
            os.mkdir("base_file")

        with sql.connect(PATH_DATA) as con:
            cursor = con.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS spend_reason(
                        spend REAL DEFAULT -1,
                        balance REAL,
                        reason TEXT DEFAULT 'Не указано',
                        spend_zero INTEGER, 
                        balance_zero INTEGER
            )""")

            cursor.execute("""SELECT * FROM spend_reason""")
            data = cursor.fetchall()
            print(data, len(data))

        print("Hello world")


root = Window(width=500, height=460, title="Расходильщик")

