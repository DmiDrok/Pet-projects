import turtle ##Графика
import random ##Функции рандома для рандомных цветов и прочего

import tkinter as tk ##Обычный tk
from tkinter import ttk ##Улучшеный tk
from tkinter import messagebox ##Будем делать всплывающие окна

import keyboard ##Может быть использовано для создания костылей (было использовано 13.12.2021)-(оптимизировано 15.12.2021)

import time ##Будем изредка использовать для задержки времени
import winsound ##Тут системные звуки

import sqlite3 as sql ##Библиотека с базой данных
import os ##Нужно для создания папок

import sys ##Будем использовать exit
import ctypes ##Для центровки экрана

user32 = ctypes.windll.user32

Size_Border = 0

Value_Menu = 0
PATH_DB = "D:\\Data_PingPong\\data.db"

class AskHowLongBorder:
    def __init__(self, width=280, height=240, title="Приветствуем вас!"):
        def size_globality_accept():
            print(size.get() )
            global Size_Border
            
            Size_Border = int(size.get())

            print("Длина границы: ", Size_Border)
            
            self.root.destroy()
            
            #turtle.clearscreen()
            PingPong = PingPongWindow()
            
        def quit_protocol():

            try:
                if messagebox.askokcancel("Подтвердите действие", "Вы хотите закрыть игру?") == True:
                    self.root.destroy() ##Закрываем окно
                    turtle.bye() ##Закрываем черепашку
                    
                    sys.exit() ##Безаварийный выход
            except:
                sys.exit() ##Безаварийный выход
             
            size_globality_accept()


        def some_event(event):
            if event.char=="\r":
                size_globality_accept()
        
        self.root = tk.Tk()
        self.root.geometry(f"{width}x{height}+{user32.GetSystemMetrics(0)//2-(width//2)}+{user32.GetSystemMetrics(1)//2-(height//2)-50}")
        self.root.resizable(False, False)
        self.root.configure(bg="#fff", pady=10)
        self.root.title(title)
        
        self.root.bind("<Key>", some_event)

        self.root.protocol("WM_DELETE_WINDOW", quit_protocol)
        

        size = tk.IntVar()
        size.set(240)

        label_text = tk.Label(self.root, text="Выберите размер игрового поля:", font=("Georgia", 12), bg="#fff")

        mini_size = tk.Radiobutton(self.root, text="Малый размер", font=("Georgia", 11), variable=size, value=140, bg="#fff", activebackground="#fff", cursor="hand2")
        normal_size = tk.Radiobutton(self.root, text="Средний размер", font=("Georgia", 11), variable=size, value=240, bg="#fff", activebackground="#fff", cursor="hand2")
        big_size = tk.Radiobutton(self.root, text="Большой размер", font=("Georgia", 11), variable=size, value=340, bg="#fff", activebackground="#fff", cursor="hand2")

        btn_accept = tk.Button(self.root, text="Начать игру!", bg="#fff", font=("Georgia", 11), cursor="hand2", command=size_globality_accept)

        label_text.pack()

        mini_size.pack(pady=15)
        normal_size.pack()
        big_size.pack(pady=15)

        btn_accept.pack()

        self.run()
        
    def run(self):
        self.root.mainloop()


class PingPongWindow:

    def __init__(self):
        
        ##Методы для создания 1.папки и 2.базы данных, 3.взаимодействия с ней
        self.db_dir_create()
        self.create_db_colors()
        self.check_db_colors()
        
        self.window = turtle.Screen() ##Определяем переменную window принадлежащую классу PingPongWindow как экран
        self.window.tracer(1) ##Скорость по умолчанию
        self.window.title("Пинг-Понг Управление: (Стрелочки-w-a) Горячие клавиши: (q-a-z-space)") ##В имя окна ставим название игры непосредственно и кнопки просто для справки игрока(ов)
        self.window.setup(width=1.0, height=1.0) ##Делаем на полный экран
        self.window.bgcolor(self.dict_colors["bg"]) ##Ставим задний фон цветом чёрным
        self.window.onkey(self.create_menu, 'space') ##По нажатию на пробел будем вызывать меню
        self.window.listen() ##Ставим прослушку
        
        self.window.onkey(self.change_color_random, 'q') ##Тест (надо будет убрать (всё таки оказалось правильным))
        self.window.onkey(self.back_default, 'z') ##Тест (надо будет убрать (тут тоже хорошо работает, убирать не надо))
        self.window.onkey(self.color_choice_by_user, 'a') ##И это тоже хорошо
        
        self.Player1_score = 0 ##Переменная для счёта очков 1 игрока
        self.Player2_score = 0 ##Переменная для счёта очков 2 игрока
        
        self.border_paint(self.dict_colors["border"]) ##Рисуем границы нашего поля
        self.player1_create(self.dict_colors["player1"]) ##Делаем первого игрока
        self.player2_create(self.dict_colors["player2"]) ##Делаем второго игрока
        self.ball_create(self.dict_colors["ball"]) ##Делаем наш мячик
        #time.sleep(1)
        self.create_score_out_border(self.dict_colors["score"])
        
        ##На случай конфликтов в цветах (сливаются один с другим)
        if self.player1.color()[0] == self.window.bgcolor() or self.player2.color()[0] == self.window.bgcolor() or self.ball.color()[0] == self.window.bgcolor() or self.border.color()[0] == self.window.bgcolor():
            self.back_default()
            messagebox.showinfo("Конфликт", "Некоторые цвета конфликтовали и мы решили вернуть их к начальному состоянию ")
            
        self.ball_active()
        
        self.color_choice_by_user() ##Не нужно, можно убрать, но для гарантии стоит
        
        
        turtle.hideturtle() ##Сделано, поскольку игра на паузе и по центру при смене цвета появлялась черепашка. (не знаю как, но это помогло(возможно частично))
        self.window.mainloop() ##Зацикливаем наше окно для его незакрытия
        
        
        turtle.bye()
    
    ##Метод, создающий папку (Пытается на D - не получается - C, а если и там не получится, то на Е)    
    def db_dir_create(self):
        global PATH_DB
        
        try:
            if bool(os.path.exists("D:\\Data_PingPong\\")) == False:
                os.mkdir("D:\\Data_PingPong\\")
                PATH_DB = "D:\\Data_PingPong\\data.db"
        except:
            try:
                if bool(os.path.exists("E:\\Data_PingPong\\")) == False:
                    os.mkdir("E:\\Data_PingPong\\")
                    PATH_DB = "E:\\Data_PingPong\\data.db"
            except:
                if bool(os.path.exists("C:\\Data_PingPong\\")) == False:
                    os.mkdir("C:\\Data_PingPong\\")
                    PATH_DB = "C:\\Data_PingPong\\data.db"
                    
        ##В зависимости от того, где лежит папка - меняем  значение переменной PATH_DB      
        if os.path.exists("D:\\Data_PingPong\\"):
            PATH_DB = "D:\\Data_PingPong\\data.db"
        elif os.path.exists("C:\\Data_PingPong\\"):
            PATH_DB = "C:\\Data_PingPong\\data.db"
        elif os.path.exists("E:\\Data_PingPong\\"):
            PATH_DB = "E:\\Data_PingPong\\data.db"

        
        
    def create_db_colors(self):
        with sql.connect(PATH_DB) as con:
            cursor = con.cursor()
            
            #cursor.execute("""DROP TABLE IF EXISTS colors_standard""")
            
            cursor.execute("""CREATE TABLE IF NOT EXISTS colors_standard (
                color_bg TEXT DEFAULT NULL,
                color_border TEXT DEFAULT NULL,
                color_ball TEXT DEFAULT NULL,
                color_player1 TEXT DEFAULT NULL,
                color_player2 TEXT DEFAULT NULL,
                color_score TEXT DEFAULT NULL
)""")
            
            cursor.execute("""SELECT * FROM colors_standard""")
            array = cursor.fetchall()
            ##Делаем проверку, есть ли что-то в базе или нет (если нет, то добавляем параметры по умолчанию)
            if len(array) != 1:
                cursor.execute("""INSERT INTO colors_standard (color_bg, color_border, color_ball, color_player1, color_player2, color_score) VALUES ('black', 'green', 'green', 'green', 'green', 'white')""")
            elif len(array) >= 1:
                pass
            
    def check_db_colors(self):
        self.dict_colors = {
            "bg":"",
            "border":"",
            "ball":"",
            "player1":"",
            "player2":"",
            "score":"",
            }
        
        with sql.connect(PATH_DB) as con:
            cursor = con.cursor()
            
            cursor.execute("""SELECT * FROM colors_standard""")
            array = cursor.fetchall()
            
            print(array)
            
            self.dict_colors["bg"] = array[0][0]
            self.dict_colors["border"] = array[0][1]
            self.dict_colors["ball"] = array[0][2]
            self.dict_colors["player1"] = array[0][3]
            self.dict_colors["player2"] = array[0][4]
            self.dict_colors["score"] = array[0][5]
            
            print(self.dict_colors)
            
        #return dict_colors
    
    def border_paint(self, color='green', value_size=340): ##Меняя value_size - меняем размер поля (можно реализовать поля с разными размерами)
        
        global Size_Border
        
        self.border = turtle.Turtle()
        
        self.border.clear() ##На всякий случай
        
        self.border.speed(0) ##Ставим нашей черепашке, рисующей границы скорость максимальную
        self.border.color(color) ##Цветом ставим параметр color (по умолчание green-зелёный)
        self.border.width(7) ##Указываем ширину линий рисуемых черепашкой
        self.border.hideturtle() ##Скрываем черепашку
        
        self.border_value = Size_Border ##Размером сторон будет параметр value_size (по умолчанию 340), => что наше поле имеет форму квадрата
        
        
        self.border.up() ##Поднимаем для нерисования
        self.border.goto(self.border_value, self.border_value) ##Идём к координатам где начнём
        self.border.down() ##Опускаем для рисования
        
        ##Алгоритм для прорисовки поля
        self.border.goto(self.border_value, -self.border_value)
        self.border.goto(-self.border_value, -self.border_value)
        self.border.goto(-self.border_value, self.border_value)
        self.border.goto(self.border_value, self.border_value)
        
    def player1_create(self, color="green"):
        
        def moveUp(): ##Функция движения вверх
            
            if self.player1.position()[1] + 100 >= self.border_value:
                self.player1.setposition(self.player1.position()[0], self.player1.position()[1])
            else:
                self.player1.clear()
                self.player1.backward(100)
                self.player1.forward(50)
            
        def moveDown():##Функция движения вниз
            
            if self.player1.position()[1] -100 <= -self.border_value:
                self.player1.setposition(self.player1.position()[0], self.player1.position()[1])
            else:
                self.player1.clear()
                self.player1.forward(100)
                self.player1.backward(50)
        
        self.player1 = turtle.Turtle()
        self.player1.speed(0) ##Скорость - максимальная, но можно и без этого
        self.player1.hideturtle()  ##Скрываем нашу черепашку
        self.player1.color(color) ##Цветом ставим зелёный
        self.player1.width(7) ##Ставим ширину 
         
        self.player1.up() ##Поднимаем для нерисования
        self.player1.goto(self.border_value-20, self.border_value-15) ##Идём на координаты с отступом 20 отрезков от края
        self.player1.down() ##Опускаем для рисования
        
        ##Алгоритм для прорисовки
        self.player1.right(90)
        self.player1.forward(100)
        self.player1.backward(50)
        
        ##По нажатию на 'Up'(стрелки вверх) и 'Down'(стрелки вниз) происходят соотвественно движения вниз и вверх
        self.window.onkey(moveUp, 'Up') ##Отслеживаем нажатие стрелки вверх
        self.window.onkey(moveDown, 'Down') ##Отслеживаем нажатие стрелки вниз
        
    def player2_create(self, color="green"):
        
        def moveUp(): ##Функция движения вверх
            if self.player2.position()[1] + 100 >= self.border_value:
                self.player2.setposition(self.player2.position()[0], self.player2.position()[1])
            else:
                self.player2.clear()
                self.player2.forward(100)
                self.player2.backward(50)
        
        def moveDown(): ##Функция движения вниз
            if self.player2.position()[1] -100 <= -self.border_value:
                self.player2.setposition(self.player2.position()[0], self.player2.position()[1])
            else:
                self.player2.clear()
                self.player2.backward(100)
                self.player2.forward(50)
        
        self.player2 = turtle.Turtle()
        self.player2.speed(0) ##Скорость - максимальная, но можно и без этого
        self.player2.hideturtle() ##Скрываем нашу черепашку, поскольку она по центру и с ней не красиво
        self.player2.color(color) ##Цветом ставим зелёный
        self.player2.width(7) ##Ставим ширину
        
        self.player2.up() ##Поднимаем для нерисования
        self.player2.goto(-self.border_value+20, -self.border_value+15) ##Идём на координаты с отступом 20 отрезков от края
        self.player2.down() ##Опускаем для рисования
        
        ##Непосредственно рисуем
        self.player2.left(90)
        self.player2.forward(100)
        self.player2.backward(50)
        
        ##По нажатию на 'w' и 's' происходят соотвественно движения вниз и вверх
        self.window.onkey(moveUp, 'w')
        self.window.onkey(moveDown, 's')
        
        
        
    def ball_create(self, color="green"): ##Создаём мячик
        
        self.ball = turtle.Turtle()
        self.ball.shape('circle') ##Черепашка имеет форму круга
        self.ball.color(color) ##И зелёный цвет
        self.ball.up() ##Убираем полоску от мячика
        
    ##Вынесли в один метод, до этого было в методе ball_create
    def ball_active(self):
        
        global Size_Border
        
        small_padding_hit = 8
        
        if self.border_value == 140:
            small_padding_hit = 4
        elif self.border_value == 240:
            small_padding_hit = 4
        elif self.border_value == 340:
            small_padding_hit = 8
        
        array_speed = [-3, -2, -1, 1, 2, 3]
        
        if self.border_value == 140:
            array_speed = [-2, -1, 1, 2]
        
        
        self.change_x = random.choice(array_speed)
        self.change_y = random.choice(array_speed)
        
        ##Чтобы мячик не шёл только вверх или только в сторону
#         while self.change_x == 0 or self.change_y == 0:
#             self.change_x = random.randint(-3, 3)
#             self.change_y = random.randint(-3, 3)
            
        self.player1_max = 5 ##Для проверки, мячик дальше игрока1 или нет
        self.player2_max = 5 ##Для проверки, мячик дальше игрока2 или нет
        
        
        #colors = ["green", "yellow", "white"]
        
        while True:
            x, y = self.ball.position()
            
            #self.ball.color(random.choice(colors))
            
            ##Проверка на стены
            if x+self.change_x+10 >= self.border_value or x+self.change_y-10 <= -self.border_value:
                self.change_x = -self.change_x
            
            if y+self.change_y+15 >= self.border_value or y+self.change_y-15 <= -self.border_value:
                self.change_y = -self.change_y
            
            self.ball.setposition(x+self.change_x, y+self.change_y) ##Прибавляем постоянно

            ##Проверка на игрока 1
            if x+self.change_x+small_padding_hit == self.player1.position()[0] and y in range(int(self.player1.position()[1]-50), int(self.player1.position()[1]+50)):
                self.change_x = random.choice(array_speed[-2::])
                self.change_x = -self.change_x
            
            ##Проверям, обошёл ли мячик игрока 1
            if x >= self.player1.position()[0]+self.player1_max:
                if self.player2.position()[0] != -9999:
                    self.Player2_score += 1 ##В очки второго игрока прибавляем 1
                    self.Player2_score_out_border.clear()
                    self.Player2_score_out_border.write(self.Player2_score, font=("Segoe UI", 44))
                else:
                    self.Player2_score_out_border.clear()
                    self.Player2_score_out_border.write('')
                    
                print("Счёт второго игрока: ", self.Player2_score)
                self.change_x = random.choice(array_speed[-2::])
                self.change_y = random.choice(array_speed[-2::])
                self.ball.hideturtle()
                
                if self.border_value == 140:
                    self.ball.setposition(0, random.randint(50, 50))
                elif self.border_value == 240:
                    self.ball.setposition(0, random.randint(-150, 150))
                elif self.border_value == 340:
                    self.ball.setposition(0, random.randint(-250, 250))
                
                print(self.ball.position()[1])
                self.ball.showturtle()
                
            ##Проверка на игрока 2
            if x+self.change_x-small_padding_hit == self.player2.position()[0] and y in range(int(self.player2.position()[1]-50), int(self.player2.position()[1]+50)):
                self.change_x = random.choice(array_speed[0:2])
                self.change_x = -self.change_x
                
            ##Проверям, обошёл ли мячик игрока 2
            if x <= self.player2.position()[0]-self.player2_max:
                self.Player1_score += 1 ##В очки первого игрока прибавляем 1
                self.Player1_score_out_border.clear()
                self.Player1_score_out_border.write(self.Player1_score, font=("Segoe UI", 44))
                     
                print("Счёт первого игрока: ", self.Player1_score)
                self.change_x = random.choice(array_speed[0:2])
                self.change_y = random.choice(array_speed[0:2])
                self.ball.hideturtle()
                
                if self.border_value == 140:
                    self.ball.setposition(0, random.randint(50, 50))
                elif self.border_value == 240:
                    self.ball.setposition(0, random.randint(-150, 150))
                elif self.border_value == 340:
                    self.ball.setposition(0, random.randint(-250, 250))
                    
                self.ball.showturtle()
                
    
    def create_score_out_border(self, color="white"):
        
        ##Делаем видимым счёт первого игрока
        self.Player1_score_out_border = turtle.Turtle()
        self.Player1_score_out_border.color(color) ##Устанавливаем цвет по умолчанию, но потом будет проверка
        self.Player1_score_out_border.speed(0)           
        self.Player1_score_out_border.up()
        self.Player1_score_out_border.hideturtle()
        self.Player1_score_out_border.setposition(self.border_value+100, self.border_value-70)
        
        self.Player1_score_out_border.write(self.Player1_score, font=("Segoe UI", 44))
        
        ##Делаем видимым счёт второго игрока
        self.Player2_score_out_border = turtle.Turtle()
        self.Player2_score_out_border.color(color) ##Устанавливаем цвет по умолчанию, но потом будет проверка
        self.Player2_score_out_border.speed(0)
        self.Player2_score_out_border.up()
        self.Player2_score_out_border.hideturtle()
        self.Player2_score_out_border.setposition(-self.border_value-100, self.border_value-70)
        
        self.Player2_score_out_border.write(self.Player2_score, font=("Segoe UI", 44))
        
        ##Проверка на цвет окна и счётчиков чтобы они не сливались
#         if self.window.bgcolor() == 'black':
#             self.Player1_score_out_border.color('white')
#             self.Player1_score_out_border.write(self.Player1_score, font=("Segoe UI", 44))
#             
#             self.Player2_score_out_border.clear()
#             self.Player2_score_out_border.color('white')
#             self.Player2_score_out_border.write(self.Player2_score, font=("Segoe UI", 44))
# 
#         elif self.window.bgcolor() == 'white':
#             self.Player1_score_out_border.color('black')
#             self.Player1_score_out_border.write(self.Player2_score, font=("Segoe UI", 44))
#             
#             self.Player2_score_out_border.clear()
#             self.Player2_score_out_border.color('black')
#             self.Player2_score_out_border.write(self.Player2_score, font=("Segoe UI", 44))  
    
    ##Раньше было функцией внутри change_color_random(), упразднено 19.12.2021
    def random_color_all(self):
        colors = ["green", "yellow", "grey", "purple", "white", "black", "orange", "blue", "red"]
    
        print(type(self.player1))
        
        self.player1.clear()
        self.player1.color(random.choice(colors))
        self.player1.setposition(self.player1.position()[0], self.player1.position()[1])
        ##Алгоритм по возвращению в центр оси
        self.player1.backward(50)
        self.player1.forward(100)
        self.player1.backward(50)
         
        self.player2.clear()
        self.player2.color(random.choice(colors))
        self.player2.setposition(self.player2.position()[0], self.player2.position()[1])
        ##Алгоритм по возвращению в центр оси
        self.player2.forward(50)
        self.player2.backward(100)
        self.player2.forward(50)

        self.ball.color(random.choice(colors))
               
        self.window.bgcolor(random.choice(colors)) ##Случайный цвет для заднего фона
        
        self.Player1_score_out_border.clear() ##Очищаем для надёжности
        self.Player1_score_out_border.color(random.choice(colors))
        
        self.Player2_score_out_border.clear() ##Очищаем для надёжности
        self.Player2_score_out_border.color(self.Player1_score_out_border.color()[0])
        
        ##Проверка чтобы счёт не сливался с задним фоном      
#             if self.window.bgcolor() == 'black' and self.Player1_score_out_border.color()[0] == 'black':
#                 self.Player1_score_out_border.clear()
#                 self.Player1_score_out_border.color('white')
#                 self.Player1_score_out_border.write(self.Player1_score, font=("Segoe UI", 44))
#                 
#                 self.Player2_score_out_border.clear()
#                 self.Player2_score_out_border.color('white')
#                 self.Player2_score_out_border.write(self.Player2_score, font=("Segoe UI", 44))
        
        ##Цикл выполняется пока цвет счётчиков совпадает с задним фоном
        while self.window.bgcolor().lower() == self.Player1_score_out_border.color()[0]:
            
            if self.player2.position()[0] != -9999:
                self.Player1_score_out_border.clear() ##Чистим
                self.Player1_score_out_border.color(random.choice(colors)) ##Задаем цвет
                self.Player1_score_out_border.write(self.Player1_score, font=("Segoe UI", 44)) ##Пишем
                
                self.Player2_score_out_border.clear() ##Чистим
                self.Player2_score_out_border.color(self.Player1_score_out_border.color()[0]) ##Задаем цвет
                self.Player2_score_out_border.write(self.Player2_score, font=("Segoe UI", 44)) ##Пишем
            else:
                self.Player1_score_out_border.clear() ##Чистим
                self.Player1_score_out_border.color(random.choice(colors)) ##Задаем цвет
                self.Player1_score_out_border.write("Один игрок", font=("Segoe UI", 30))
                
                self.Player2_score_out_border.color(self.window.bgcolor() )
                
        self.border_paint(random.choice(colors))

    def change_color_random(self):
        
        self.random_color_all()
        
        print("1")
        
        ##Проверка для того, чтобы цвета не сливались
        while self.player1.color()[0] == self.window.bgcolor() or self.player2.color()[0] == self.window.bgcolor() or self.ball.color()[0] == self.window.bgcolor() or self.border.color()[0] == self.window.bgcolor():
            self.player1.clear()
            self.player2.clear()
            self.random_color_all()
        
        ##Прорисовываем
        if self.player2.position()[0] != -9999:
            
            self.Player1_score_out_border.clear()
            self.Player1_score_out_border.write(self.Player1_score, font=("Segoe UI", 44))
             
            self.Player2_score_out_border.clear()
            self.Player2_score_out_border.write(self.Player2_score, font=("Segoe UI", 44))
        else:
            
            self.Player1_score_out_border.clear()
            self.Player1_score_out_border.write("Один игрок", font=("Segoe UI", 30))
            
            self.Player2_score_out_border.write("")
            self.Player2_score_out_border.color(self.window.bgcolor())

            
    def color_choice_by_user(self):
        
        def change_color_by_user():
                        
            if combo_player1.get() == combo_bg.get() or combo_player2.get() == combo_bg.get() or combo_ball.get() == combo_bg.get() or combo_border.get() == combo_bg.get() or combo_score.get() == combo_bg.get():
                winsound.MessageBeep()  ##Бибикаем об ошибке
                
                ##Сбрасываем всё по умолчанию
                combo_player1.current(self.array_colors.index(self.player1.color()[0].title()))
                combo_player2.current(self.array_colors.index(self.player2.color()[0].title()))
                combo_ball.current(self.array_colors.index(self.ball.color()[0].title()))
                combo_border.current(self.array_colors.index(self.border.color()[0].title()))
                combo_bg.current(self.array_colors.index(self.window.bgcolor().title()))
                print(self.Player1_score_out_border.color())
                combo_score.current(self.array_colors.index(self.Player1_score_out_border.color()[0].title()))
            else:
                self.player1.clear()
                self.player1.color(combo_player1.get())
                self.player1.setposition(self.player1.position()[0], self.player1.position()[1])
                ##Алгоритм по возвращению в центр оси
                self.player1.backward(50)
                self.player1.forward(100)
                self.player1.backward(50)
                
                self.player2.clear()
                self.player2.color(combo_player2.get())
                self.player2.setposition(self.player2.position()[0], self.player2.position()[1])
                ##Алгоритм по возвращению в центр оси
                self.player2.backward(50)
                self.player2.forward(100)
                self.player2.backward(50)
                
                
                self.ball.color(combo_ball.get()) ##Меняем цвет мячика
                
                self.border_paint(combo_border.get()) ##Меняем цвет границы
                self.window.bgcolor(combo_bg.get())  ##Меняем цвет фона
                
                ##Меняем цвет счётчиков первого и второго игроков с проверкой, на месте ли второй игрок (если на месте - выводим счёт, если же нет - меняем цвет надписи 'один игрок')
                if self.player2.position()[0] != -9999:
                    self.Player1_score_out_border.clear()
                    self.Player1_score_out_border.color(combo_score.get())
                    self.Player1_score_out_border.write(self.Player1_score, font=("Segoe UI", 44))
                    
                    self.Player2_score_out_border.clear()
                    self.Player2_score_out_border.color(combo_score.get())
                    self.Player2_score_out_border.write(self.Player2_score, font=("Segoe UI", 44))
                else:
                    self.Player1_score_out_border.clear()
                    self.Player1_score_out_border.color(combo_score.get())
                    self.Player1_score_out_border.write("Один игрок", font=("Segoe UI", 30))
                    
                    self.Player2_score_out_border.color(self.window.bgcolor())

                
#             if combo_bg.get() == "Black" and self.Player1_score_out_border.color()[0] == 'black':
#                 self.Player1_score_out_border.clear()
#                 self.Player1_score_out_border.color('White')
#                 self.Player1_score_out_border.write(self.Player1_score, font=("Segoe UI", 44))
#                 
#                 self.Player2_score_out_border.clear()
#                 self.Player2_score_out_border.color('White')
#                 self.Player2_score_out_border.write(self.Player2_score, font=("Segoe UI", 44))
#                 
#             elif combo_bg.get() == "White" and self.Player1_score_out_border.color()[0] == 'white':
#                 self.Player1_score_out_border.clear()
#                 self.Player1_score_out_border.color('black')
#                 self.Player1_score_out_border.write(self.Player1_score, font=("Segoe UI", 44))
#                 
#                 self.Player2_score_out_border.clear()
#                 self.Player2_score_out_border.color('black')
#                 self.Player2_score_out_border.write(self.Player2_score, font=("Segoe UI", 44))
                

            
        self.window_choice = tk.Tk()
        self.window_choice.geometry("300x460")
        self.window_choice.resizable(False, False)
        self.window_choice.configure(bg="#fff")
        self.window_choice.title("Ручной выбор цвета")
        
        self.array_colors = ["Green", "Yellow", "Grey", "Purple", "White", "Black", "Orange", "Blue", "Red"]
        
        ##Фрейм для всех выборов
        frame_choice = tk.Frame(self.window_choice, padx=5, pady=5, bg="#fff")
        
        label_ball = tk.Label(frame_choice, text="Цвет мячика:", bg="#fff",
                              font=("Georgia", 12),
                              ) ##Пишем что меняем
        
        combo_ball = ttk.Combobox(frame_choice, values=self.array_colors) ##Делаем комбобокс для мячика
        combo_ball.current(self.array_colors.index(self.ball.color()[0].title())) ##Вставляем в комбобокс по умолчанию значение green (по индексу)
        
        label_player1 = tk.Label(frame_choice, text="Цвет первого игрока:", bg="#fff",
                                 font=("Georgia", 12),
                                 ) ##Лейбл (текст), обозначающий что делает combo_player1
        
        combo_player1 = ttk.Combobox(frame_choice, values=self.array_colors)
        combo_player1.current(self.array_colors.index(self.player1.color()[0].title())) ##Метод .title() - для заглавной первой буквы
        
        label_player2 = tk.Label(frame_choice, text="Цвет второго игрока:", bg="#fff",
                                 font=("Georgia", 12),
                                 )
        
        combo_player2 = ttk.Combobox(frame_choice, values=self.array_colors)
        combo_player2.current(self.array_colors.index(self.player2.color()[0].title()))
        
        label_border = tk.Label(frame_choice, text="Цвет рамки:", bg="#fff",
                                font=("Georgia", 12)
                                )
        
        combo_border = ttk.Combobox(frame_choice, value=self.array_colors)
        combo_border.current(self.array_colors.index(self.border.color()[0].title()))
        
        label_bg = tk.Label(frame_choice, text="Цвет фона:", bg="#fff",
                                font=("Georgia", 12)
                                )
        
        combo_bg = ttk.Combobox(frame_choice, value=self.array_colors)
        combo_bg.current(self.array_colors.index(self.window.bgcolor().title()))
        
        label_score = tk.Label(frame_choice, text="Цвет счётчика", bg="#fff",
                               font=("Georgia", 12)
                               )
        
        combo_score = ttk.Combobox(frame_choice, value=self.array_colors)
        combo_score.current(self.array_colors.index(self.Player1_score_out_border.color()[0].title()))
        
        button_accept = tk.Button(frame_choice, text="Применить", bg="#fff",
                          font=("Georgia", 12),
                          cursor="hand2",
                          padx=5,
                          command=change_color_by_user,
                          )
        
        frame_choice.pack()
        
        label_ball.pack()
        combo_ball.pack(pady=10)
        
        label_player1.pack()
        combo_player1.pack(pady=10)
                
        label_player2.pack()
        combo_player2.pack(pady=10)
        
        label_border.pack()
        combo_border.pack(pady=10)
        
        label_bg.pack()
        combo_bg.pack(pady=10)
        
        label_score.pack()
        combo_score.pack(pady=10)
        
        button_accept.pack(pady=10)
            
    def back_default(self):
        
        turtle.clear()
        
        self.player1.clear() ##Очищаем всё что было нарисовано
        self.player1.color('green') ##Ставим цвет обратно зелёный
        self.player1.setposition(self.player1.position()[0], self.player1.position()[1])
        ##Алгоритм по возвращению в центр оси
        self.player1.backward(50)
        self.player1.forward(100)
        self.player1.backward(50)
        
        self.player2.clear() ##Очищаем всё что было нарисовано
        self.player2.color('green') ##Ставим цвет обратно зелёный
        self.player2.setposition(self.player2.position()[0], self.player2.position()[1])
        
        ##Алгоритм по возвращению в центр оси
        self.player2.forward(50)
        self.player2.backward(100)
        self.player2.forward(50)
        
        self.ball.color('green')
        self.border_paint('green')
        self.window.bgcolor('black')
        
        ##Меняем цвет счётчиков очков на белый, чтобы не сливался с чёрным фоном
#         self.Player1_score_out_border.clear()
#         self.Player1_score_out_border.color('white')
#         self.Player1_score_out_border.write(self.Player1_score, font=("Segoe UI", 44))
#             
#         self.Player2_score_out_border.clear()
#         self.Player2_score_out_border.color('white')
#         self.Player2_score_out_border.write(self.Player2_score, font=("Segoe UI", 44))
        
        if self.player2.position()[0] != -9999:
            
            self.Player1_score_out_border.clear()
            self.Player1_score_out_border.color('white')
            self.Player1_score_out_border.write(self.Player1_score, font=("Segoe UI", 44))
             
            self.Player2_score_out_border.clear()
            self.Player2_score_out_border.color('white')
            self.Player2_score_out_border.write(self.Player2_score, font=("Segoe UI", 44))
        else:
            
            self.Player1_score_out_border.clear()
            self.Player1_score_out_border.color('white')
            self.Player1_score_out_border.write("Один игрок", font=("Segoe UI", 30))
            
            self.Player2_score_out_border.write("")
            self.Player2_score_out_border.color(self.window.bgcolor())

    
    def solo_game_activate(self): ##Нужно доделать эа
        
        print("Solo_Game...")
        
        ##Обнуляем счёт первого и второго игрока
        self.Player1_score = 0 
        self.Player2_score = 0
        
        self.Player2_score_out_border.clear()
        self.Player2_score_out_border.color(self.window.bgcolor())
        
        self.Player1_score_out_border.setposition(self.Player1_score_out_border.position()[0]-50, self.Player1_score_out_border.position()[1])
 
        self.Player1_score_out_border.clear()
        #if self.window.bgcolor() == self.Player1_score_out_border.color()[0]:
        self.Player1_score_out_border.write("Один игрок", font=("Segoe UI", 30)) 
                       
        ##Описываем для одиночной игры (скрытие второго игрока и т.д.)

        #self.border_paint('red', 200)
        
        self.player2.up()
        self.player2.setposition(-9999, -9999)
        self.player2.clear()
        
        self.player2_max = 100
        
        self.btn_solo_game["text"] = "Игра вдвоём"
        self.btn_solo_game["command"] = lambda: self.duo_game_back()
        
    def duo_game_back(self):
        
        ##Обнуляем всё
        self.Player1_score = 0
        self.Player2_score = 0
        
        ##Расставляем наши счётчики
        self.Player1_score_out_border.clear()
        self.Player1_score_out_border.setposition(self.Player1_score_out_border.position()[0]+50, self.Player1_score_out_border.position()[1])
        self.Player1_score_out_border.write(self.Player1_score, font=("Segoe UI", 44))
        
        self.Player2_score_out_border.clear()
        self.Player2_score_out_border.color(self.Player1_score_out_border.color()[0])
        self.Player2_score_out_border.write(self.Player2_score, font=("Segoe UI", 44))
        
        
        ##Отстраиваем всё обратно               
        self.player2.goto(-self.border_value+20, -self.border_value+15)  ##Возвращаем второго игрока на место
        self.player2_max = 5
        
        self.player2.clear()
        self.player2.down() 
        self.player2.forward(100)
        self.player2.backward(50)

        self.btn_solo_game["text"] = "Один игрок"
        self.btn_solo_game["command"] = lambda: self.solo_game_activate()
    
#     def check_score_players(self):
#         
#         winsound.MessageBeep()
#         
#         if self.player2.position()[0] != -9999:
#             if self.Player1_score > 0 or self.Player2_score > 0:
#                 messagebox.showinfo("Счёт", f"Первый игрок набрал: {self.Player1_score} очко(a/ов)\nВторой игрок набрал: {self.Player2_score} очко(a/ов)", parent=self.root) ##Благодаря параметру parent фокус с self.root убираться не будет
#             else:
#                 messagebox.showinfo("Счёт", f"У обоих по нулям!", parent=self.root) ##Благодаря параметру parent фокус с self.root убираться не будет
#         else:
#             winsound.MessageBeep()
#             messagebox.showinfo("Уведомление", "Включен режим одного игрока!")

    ##Описываем метод для создания меню с проверкой, чтобы была возможность сделать только одно меню
    def create_menu(self):
        global Menu, Value_Menu
      
        if Value_Menu == 0:
            Value_Menu = 1
            
            self.ball.hideturtle()
            
            if self.border_value == 140:
                self.ball.setposition(0, random.randint(-50, 50))
            elif self.border_value == 240:
                self.ball.setposition(0, random.randint(-150, 150))
            elif self.border_value == 340:
                self.ball.setposition(0, random.randint(-250, 250))
            
            self.ball.showturtle()
            
            self.change_x = 0
            self.change_y = 0
            
            
            #self.ball = 0
            
            Menu = self.MenuWindow() ##Можно и без него, но с ним спокойнее, оставлено с момента когда ещё MenuWindow являлся классом (F)
            
        ##Проверяем, включен ли режим одного игрока
        if self.player2.position()[0] != -9999: ##Если позиция игрока2 на привычных нам координатах (на игровых)
            
            self.btn_solo_game["text"] = "Один игрок" ##В менюшке пишем возврат к режиму одного игрока
            #self.player2.clear()
            self.btn_solo_game["command"] = lambda: self.solo_game_activate() ##Командой ставим активацию режима одного игрока
            
        else: ##Иначе
            
            self.btn_solo_game["text"] = "Играть вдвоём" ##В менюшке пишем возврат к режиму двух игроков
            #self.player2.clear() 
            self.btn_solo_game["command"] = lambda: self.duo_game_back() ##Командой ставим активацию режима двух игроков          
            
    def MenuWindow(self, width=200, height=390, title="Пинг-Понг Меню"):
        
        def close_menu_protocol():
            global Value_Menu
            
            Value_Menu = 0 ##Меняем для неоткрытия повторно
            self.root.destroy()
            
            #self.ball.hideturtle()
            self.ball.setposition(self.ball.position()[0], self.ball.position()[1])
            #self.ball.showturtle()
            
            self.ball_active()
        
        self.root = tk.Tk() ##Создаём окно
        #self.root.wait_window()
        
        #self.root.wm_state("iconic") ##Используем .wm_state("iconic") для сворачивания окна по умолчанию
        
        self.root.geometry(f"{width}x{height}") ##Ширина x Высота окна
        self.root.resizable(False, False) ##Растягивание по оси 'x' , 'y'
        self.root.configure(bg="#fff") ##Задний фон #fff - т.е. белыйwww
        self.root.title(title) ##Заголовок окна
        self.root.protocol("WM_DELETE_WINDOW", close_menu_protocol) ##Ставим протокол (грубо: функцию) на событие выхода
        
        self.root.focus_set() ##Берём фокус на окно менюшки
        #self.root.grab_set()
        
        ##Функция для рестарта
        def restart_game():
            global Value_Menu
            
            self.Player1_score = 0 ##Обнуляем счёт 1 игрока
            self.Player2_score = 0 ##Обнуляем счёт 2 игрока
            
            Value_Menu = 0
            
            self.root.destroy()
            turtle.clearscreen()
            #turtle.bye()
            
            self.AskBorderRestart()
            
            
            #Ask_User = AskHowLongBorder()
            
        def this_colors_to_database():
            with sql.connect(PATH_DB) as con:
                cursor = con.cursor()
                
                cursor.execute("""DROP TABLE IF EXISTS colors_standard""")
                
                cursor.execute("""CREATE TABLE IF NOT EXISTS colors_standard (
                color_bg TEXT,
                color_border TEXT,
                color_ball TEXT,
                color_player1 TEXT,
                color_player2 TEXT,
                color_score TEXT
)""")
                
                cursor.execute(f"""INSERT INTO colors_standard (color_bg, color_border, color_ball, color_player1, color_player2, color_score) VALUES ('{self.window.bgcolor()}', '{self.border.color()[0]}', '{self.ball.color()[0]}', '{self.player1.color()[0]}', '{self.player2.color()[0]}', '{self.Player1_score_out_border.color()[0]}')""")
        
        def standard_colors_select():
            dict_colors = {
                "bg":"",
                "border":"",
                "ball":"",
                "player1":"",
                "player2":"",
                "score":"",
                }
            
            with sql.connect(PATH_DB) as con:
                cursor = con.cursor()
                
                cursor.execute("""SELECT * FROM colors_standard""")
                
                array = cursor.fetchall()
                
                dict_colors["bg"] = array[0][0]
                dict_colors["border"] = array[0][1]
                dict_colors["ball"] = array[0][2]
                dict_colors["player1"] = array[0][3]
                dict_colors["player2"] = array[0][4]
                dict_colors["score"] = array[0][5]
                
                self.window.bgcolor(dict_colors["bg"])
                
                self.border.clear()
                self.border_paint(dict_colors["border"])
                
                self.player1.clear()
                self.player1_create(dict_colors["player1"])
                
                self.player2.clear()
                if self.player2.position()[0] != -9999:
                    self.player2_create(dict_colors["player2"])
                    self.Player1_score_out_border.clear()
                    self.Player2_score_out_border.clear()
                    self.create_score_out_border(dict_colors["score"])
                else:
                    self.Player1_score_out_border.clear()
                    self.Player1_score_out_border.color(dict_colors["score"])
                    self.Player1_score_out_border.write("Один игрок", font=("Segoe UI", 30))
                
                self.ball.hideturtle()
                self.ball_create(dict_colors["ball"])
            
            ##Проверка на случай конфликта цветов
            if self.player1.color()[0] == self.window.bgcolor() or self.player2.color()[0] == self.window.bgcolor() or self.ball.color()[0] == self.window.bgcolor() or self.border.color()[0] == self.window.bgcolor():
                while self.player1.color()[0] == self.window.bgcolor() or self.player2.color()[0] == self.window.bgcolor() or self.ball.color()[0] == self.window.bgcolor() or self.border.color()[0] == self.window.bgcolor():
                    self.player1.clear()
                    self.player2.clear()
                    self.back_default()
                ##Уведомление пользователю
                messagebox.showinfo("Конфликт", "Некоторые цвета конфликтовали и мы решили вернуть их к начальному состоянию", parent=self.root)
        
        ##Делаем заголовок
        label_menu = tk.Label(self.root, text="Меню Пинг-Понга",
                              font=("Georgia", 14),
                              bg="#fff"
                              )
        
        ##Отдельный Фрейм для кнопок с командами
        special_frame = tk.Frame(self.root, bg="#fff")
        
        btn_restart = tk.Button(special_frame, text="Перезапустить", 
                                font=("Georgia", 12),
                                cursor="hand2",
                                bg="#fff",
                                bd=3,
                                command=restart_game,
                                ) ##Кнопка перезапуска игры
        
        btn_random_colors = tk.Button(special_frame, text="Случайные цвета(q)",
                                      font=("Georgia", 12),
                                      cursor="hand2",
                                      bg="#fff",
                                      command=lambda: self.change_color_random()
                                      ) ##Кнопка случайных цветов
        
        btn_default_colors = tk.Button(special_frame, text="Начальные цвета(z)",
                                       font=("Georgia", 12),
                                       cursor="hand2",
                                       bg="#fff",
                                       command=lambda: self.back_default(),
                                       ) ##Кнопка для цветов по умолчанию
        
        btn_choose_colors = tk.Button(special_frame, text="Выбрать цвета(a)",
                                      font=("Georgia", 12),
                                      cursor="hand2",
                                      bg="#fff",
                                      command=lambda: self.color_choice_by_user()
                                      ) ##Кнопка для ручного выбора цветов
        
        self.btn_solo_game = tk.Button(special_frame, text="Один игрок",
                                      font=("Georgia", 12),
                                      cursor="hand2",
                                      bg="#fff",
                                      command=lambda: self.solo_game_activate()
                                      ) ##Кнопка для одиночной игры
        
#         check_score = tk.Button(special_frame, text="Узнать счёт",
#                                       font=("Georgia", 12),
#                                       cursor="hand2",
#                                       bg="#fff",
#                                       command=lambda: self.check_score_players(),
#                                       )
        
        self.btn_color_standard_select = tk.Button(special_frame, text="Цвета по умолчанию",
                                      font=("Georgia", 12),
                                      cursor="hand2",
                                      bg="#fff",
                                      command=standard_colors_select,
                                      )
        
        self.btn_color_standard = tk.Button(special_frame, text="Эти цвета по умолчанию",
                                      font=("Georgia", 12),
                                      cursor="hand2",
                                      bg="#fff",
                                      bd=3,
                                      command=this_colors_to_database,
                                      )
        
        
        label_menu.pack() ##Размещаем заголовок
        special_frame.pack(pady=15) ##Размещаем фрейм(блок) со всеми кнопками
        btn_restart.pack() ##Размещаем кнопку рестарта
        btn_random_colors.pack(pady=15) ##Размещаем кнопку рандомных цветов
        btn_default_colors.pack() ##Размещаем кнопку стандартных цветов
        btn_choose_colors.pack(pady=15) ##Размещаем кнопку ручного выбора цветов
        self.btn_solo_game.pack() ##Размещаем кнопку одиночной игры
#         check_score.pack(pady=15) ##Размещаем кнопку для счёта
        self.btn_color_standard_select.pack(pady=15)
        self.btn_color_standard.pack()
        
        #self.root.grab_set() 
        #self.root.wait_window() ##Используем wait_window для паузы при менюшке
    
    def AskBorderRestart(self, width=300, height=150, title="Выберите размер"):
        
        def size_bd_accept():
            global Size_Border
            
            try:
                Size_Border = int(dict_size[combo_choice_size.get()])
                print(Size_Border, type(Size_Border))
            
                self.root_ask.destroy()
                PingPong = PingPongWindow()
            except:
                combo_choice_size.delete(0, tk.END)
                combo_choice_size.current(random.randint(0, 3))
        
        def quit_protocol():
            try:
                if messagebox.askokcancel("Подтвердите действие", "Вы хотите закрыть игру?") == True:
                    self.root_ask.destroy() ##Закрываем наше окошко с выбором размера     
                    turtle.bye() ##Закрываем черепашку
    
                    sys.exit() ##Безаварийный выход
            except:
                sys.exit() ##Безаварийный выход
                
            size_bd_accept() ##Вызываем функцию, в которой уже приняли размеры и делаем поле под них
        
        def some_event(event):
            if event.char == "\r":
                size_bd_accept()
            
        
        self.root_ask = tk.Tk()
        self.root_ask.geometry(f"{width}x{height}+{user32.GetSystemMetrics(0)//2-(width//2)}+{user32.GetSystemMetrics(1)//2-(height//2)-100}")
        self.root_ask.title(title)
        self.root_ask.configure(bg="#fff", pady=15)
        
        self.root_ask.bind("<Key>", some_event)
        
        self.root_ask.protocol("WM_DELETE_WINDOW", quit_protocol)

        
        label_text = tk.Label(self.root_ask, text="Выберите размер игрового поля:", font=("Georgia", 12), bg="#fff")
        
        dict_size = {
            "Малый размер":140,
            "Средний размер":240,
            "Большой размер":340,
            }
        
        list_size = ["Малый размер", "Средний размер", "Большой размер"]
        
        combo_choice_size = ttk.Combobox(self.root_ask, values=list_size, font=("Georgia", 12))
        #combo_choice_size.current(1)
        
        
        ##Этим алгоритмом вставляем наше нынешнее значение в комбобокс
        j = 0
        for key in dict_size:
            if dict_size[key] == self.border_value:
                combo_choice_size.current(j) ##Непосредственно вставляем
                break   ##Выходим из цикла
            j += 1 ##Прибавляем j (индекс)
        
        size_accept = tk.Button(self.root_ask, text="Перезапустить и начать!", bg="#fff", font=("Georgia", 11), cursor="hand2",
                                command=size_bd_accept,
                                )
        
        label_text.pack()
        combo_choice_size.pack(pady=15)
        size_accept.pack()
        
        #self.root_ask.wait_window()
        self.root_ask.focus_set()
        self.root_ask.grab_set()
        self.root_ask.mainloop()

try:
    Ask_User = AskHowLongBorder()
        
    Menu = 0 ##Не обязательно через переменную, поскольку MenuWindow более не класс, оставим же в память!
    turtle.bye() ##Для надёжности
    
    os.system("pause")
except:
    pass
