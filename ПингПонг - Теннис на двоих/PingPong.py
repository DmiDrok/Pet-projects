import turtle
import random

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import keyboard

import time
import winsound

Value_Menu = 0

class PingPongWindow:
    def __init__(self):
      
        self.window = turtle.Screen()
        self.window.setup(width=1.0, height=1.0) ##Делаем на полный экран
        self.window.bgcolor('black')
        self.window.onkey(self.create_menu, 'space') ##По нажатию на пробел будем вызывать меню
        self.window.listen() ##Ставим прослушку
        
        self.window.onkey(self.change_color_random, 'q') ##Тест (надо будет убрать)
        self.window.onkey(self.back_default, 'z') ##Тест (надо будет убрать)
        self.window.onkey(self.color_choice_by_user, 'a')
        
        
        self.border_paint() ##Рисуем границы нашего поля
        self.player1_create() ##Делаем первого игрока
        self.player2_create() ##Делаем второго игрока
        self.ball_create() ##Делаем наш мячик
        
        self.color_choice_by_user() ##Не нужно, можно убрать, но для гарантии стоит
        
        
        self.window.mainloop()
        
        
    def border_paint(self, color='green'):
        
        self.border = turtle.Turtle()
        
        self.border.clear() ##На всякий случай
        
        self.border.speed(0)
        self.border.color(color)
        self.border.width(4)
        self.border.hideturtle()
        
        self.border_value = 340
        
        self.border.up()
        self.border.goto(self.border_value, self.border_value)
        self.border.down()
        
        self.border.goto(self.border_value, -self.border_value)
        self.border.goto(-self.border_value, -self.border_value)
        self.border.goto(-self.border_value, self.border_value)
        self.border.goto(self.border_value, self.border_value)
        
    def player1_create(self, color="green"):
        
        def moveUp():
            
            if self.player1.position()[1] + 100 >= self.border_value:
                self.player1.setposition(self.player1.position()[0], self.player1.position()[1])
            else:
                self.player1.clear()
                self.player1.backward(100)
                self.player1.forward(50)
            
        def moveDown():
            
            if self.player1.position()[1] -100 <= -self.border_value:
                self.player1.setposition(self.player1.position()[0], self.player1.position()[1])
            else:
                self.player1.clear()
                self.player1.forward(100)
                self.player1.backward(50)
        
        self.player1 = turtle.Turtle()
        self.player1.speed(0)
        self.player1.hideturtle()  ##Скрываем нашу черепашку
        self.player1.color(color)
        self.player1.width(5)
        
        self.player1.up()
        self.player1.goto(self.border_value-20, self.border_value-15)
        self.player1.down()
        
        self.player1.right(90)
        self.player1.forward(100)
        self.player1.backward(50)
        
        self.window.onkeypress(moveUp, 'Up') ##Отслеживаем нажатие стрелки вверх
        self.window.onkeypress(moveDown, 'Down') ##Отслеживаем нажатие стрелки вниз
        
    def player2_create(self):
        
        def moveUp():
            if self.player2.position()[1] + 100 >= self.border_value:
                self.player2.setposition(self.player2.position()[0], self.player2.position()[1])
            else:
                self.player2.clear()
                self.player2.forward(100)
                self.player2.backward(50)
        
        def moveDown():
            if self.player2.position()[1] -100 <= -self.border_value:
                self.player2.setposition(self.player2.position()[0], self.player2.position()[1])
            else:
                self.player2.clear()
                self.player2.backward(100)
                self.player2.forward(50)
        
        self.player2 = turtle.Turtle()
        self.player2.speed(0)
        self.player2.hideturtle()
        self.player2.color('green')
        self.player2.width(5)
        
        self.player2.up()
        self.player2.goto(-self.border_value+20, -self.border_value+15)
        self.player2.down()
        
        self.player2.left(90)
        self.player2.forward(100)
        self.player2.backward(50)
        
        self.window.onkeypress(moveUp, 'w')
        self.window.onkeypress(moveDown, 's')
        
        
        
    def ball_create(self):
        self.ball = turtle.Turtle()
        self.ball.shape('circle')
        self.ball.color('green')
        self.ball.up() ##Убираем полоску от мячика
        
        change_x = random.randint(-2, 2)
        change_y = random.randint(-2, 2)
        
        while change_x == 0 or change_y == 0:
            change_x = random.randint(-2, 2)
            change_y = random.randint(-2, 2)
        
        
        #colors = ["green", "yellow", "white"]
        
        while True:
            x, y = self.ball.position()
            
            #self.ball.color(random.choice(colors))
            
            ##Проверка на стены
            if x+change_x+10 >= self.border_value or x+change_y-10 <= -self.border_value:
                change_x = -change_x
            
            if y+change_y+10 >= self.border_value or y+change_y-10 <= -self.border_value:
                change_y = -change_y
            
            self.ball.setposition(x+change_x, y+change_y) ##Прибавляем постоянно

            ##Проверка на игрока 1
            if x+change_x+10 == self.player1.position()[0] and y in range(int(self.player1.position()[1]-50), int(self.player1.position()[1]+50)):
                change_x = random.randint(1, 2)
                change_x = -change_x
            
            ##Проверям, обошёл ли мячик игрока 1
            if x >= self.player1.position()[0]+5:
                change_x = random.randint(1, 2)
                change_y = random.randint(1, 2)
                self.ball.setposition(0, 0)
                
            ##Проверка на игрока 2
            if x+change_x-10 == self.player2.position()[0] and y in range(int(self.player2.position()[1]-100), int(self.player2.position()[1]+100)):
                change_x = -change_x
                
            ##Проверям, обошёл ли мячик игрока 2
            if x <= self.player2.position()[0]-5:
                change_x = random.randint(-2, -1)
                change_y = random.randint(-2, -1)
                self.ball.setposition(0, 0)
    
    def change_color_random(self):
        
        def random_color_all():
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
                   
            self.ball.clear()
            self.ball.color(random.choice(colors))
            
            self.window.bgcolor(random.choice(colors)) ##Случайный цвет для заднего фона

            self.border_paint(random.choice(colors))
        
        random_color_all()
        
        print(self.window.bgcolor())
        
        ##Проверка для того, чтобы цвета не сливались
        while self.player1.color()[0] == self.window.bgcolor() or self.player2.color()[0] == self.window.bgcolor() or self.ball.color()[0] == self.window.bgcolor() or self.border.color()[0] == self.window.bgcolor():
            random_color_all()
            
    def color_choice_by_user(self):
        
        def change_color_by_user():
            
            if combo_player1.get() == combo_bg.get() or combo_player2.get() == combo_bg.get() or combo_ball.get() == combo_bg.get() or combo_border.get() == combo_bg.get():
                winsound.MessageBeep()  ##Бибикаем об ошибке
                
                ##Сбрасываем всё по умолчанию
                combo_player1.current(0)
                combo_player2.current(0)
                combo_ball.current(0)
                combo_border.current(0)   
                combo_bg.current(5)
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

            
        self.window_choice = tk.Tk()
        self.window_choice.geometry("300x390")
        self.window_choice.configure(bg="#fff")
        self.window_choice.title("Ручной выбор цвета")
        
        self.array_colors = ["Green", "Yellow", "Grey", "Purple", "White", "Black", "Orange", "Blue", "Red"]
        
        ##Фрейм для всех выборов
        frame_choice = tk.Frame(self.window_choice, padx=5, pady=5, bg="#fff")
        
        label_ball = tk.Label(frame_choice, text="Цвет мячика:", bg="#fff",
                              font=("Georgia", 12),
                              ) ##Пишем что меняем
        
        combo_ball = ttk.Combobox(frame_choice, values=self.array_colors) ##Делаем комбобокс для мячика
        combo_ball.current(0) ##Вставляем в комбобокс по умолчанию значение green (по индексу)
        
        label_player1 = tk.Label(frame_choice, text="Цвет первого игрока:", bg="#fff",
                                 font=("Georgia", 12),
                                 )
        
        combo_player1 = ttk.Combobox(frame_choice, values=self.array_colors)
        combo_player1.current(0)
        
        label_player2 = tk.Label(frame_choice, text="Цвет второго игрока:", bg="#fff",
                                 font=("Georgia", 12),
                                 )
        
        combo_player2 = ttk.Combobox(frame_choice, values=self.array_colors)
        combo_player2.current(0)
        
        button_accept = tk.Button(frame_choice, text="Применить", bg="#fff",
                                  font=("Georgia", 12),
                                  cursor="hand2",
                                  padx=5,
                                  command=change_color_by_user,
                                  )
        
        label_border = tk.Label(frame_choice, text="Цвет рамки:", bg="#fff",
                                font=("Georgia", 12)
                                )
        
        combo_border = ttk.Combobox(frame_choice, value=self.array_colors)
        combo_border.current(0)
        
        label_bg = tk.Label(frame_choice, text="Цвет фона:", bg="#fff",
                                font=("Georgia", 12)
                                )
        
        combo_bg = ttk.Combobox(frame_choice, value=self.array_colors)
        combo_bg.current(5)
        
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
        
        button_accept.pack(pady=10)
            
    def back_default(self):
        
        turtle.clear()
        
        self.player1.clear()
        self.player1.color('green')
        self.player1.setposition(self.player1.position()[0], self.player1.position()[1])
        ##Алгоритм по возвращению в центр оси
        self.player1.backward(50)
        self.player1.forward(100)
        self.player1.backward(50)
        
        self.player2.clear()
        self.player2.color('green')
        self.player2.setposition(self.player2.position()[0], self.player2.position()[1])
        ##Алгоритм по возвращению в центр оси
        self.player2.forward(50)
        self.player2.backward(100)
        self.player2.forward(50)
        
        self.ball.color('green')
        self.border_paint('green')
        self.window.bgcolor('black')

    
    ##Описываем метод для создания меню с проверкой, чтобы была возможность сделать только одно меню
    def create_menu(self):
        global Menu, Value_Menu
            
        if Value_Menu == 0:
            Value_Menu = 1
            Menu = self.MenuWindow()
            print(type(Menu))
    
    def MenuWindow(self, width=200, height=280, title="Пинг-Понг Меню"):
        self.root = tk.Tk() ##Создаём окно
        
        #self.root.wm_state("iconic") ##Используем .wm_state("iconic") для сворачивания окна по умолчанию
        
        self.root.geometry(f"{width}x{height}") ##Ширина x Высота окна
        self.root.resizable(False, False) ##Растягивание по оси 'x' , 'y'
        self.root.configure(bg="#fff") ##Задний фон #fff - т.е. белый
        self.root.title(title) ##Заголовок окна
        
        self.root.focus_set() ##Берём фокус на окно менюшки 
        
        ##Функция для рестарта
        def restart_game():
            text_wait = tk.Label(self.root, text="Подождите...",
                     font=("Georgia", 14),
                     bg="#fff",
                     )
            text_wait.pack()
            
            turtle.clearscreen()
            
            PingPong = 0
            time.sleep(1)
            
            text_wait.pack_forget()
            
            PingPong = PingPongWindow()
            
        
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
                                command=restart_game,
                                ) ##Кнопка перезапуска игры
        
        btn_random_colors = tk.Button(special_frame, text="Случайные цвета(q)",
                                      font=("Georgia", 12),
                                      cursor="hand2",
                                      bg="#fff",
                                      command=lambda: self.change_color_random()
                                      ) ##Кнопка случайных цветов
        
        btn_default_colors = tk.Button(special_frame, text="Цвета по умолчанию(z)",
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
                                      )
        
        
        label_menu.pack() ##Размещаем заголовок
        special_frame.pack(pady=15)
        btn_restart.pack()
        btn_random_colors.pack(pady=15)
        btn_default_colors.pack()
        btn_choose_colors.pack(pady=15)

Menu = 0
PingPong = PingPongWindow()

turtle.bye()