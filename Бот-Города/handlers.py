from main import bot, dp ##Импорт бота и диспетчера из main
from aiogram import types ##Импорт types для обработчика

from cities import all_cities ##Импорт списка всех городов
import random ##Импорт модуля 'random'

from aiogram.dispatcher import FSMContext ##Необходимо для аннотирования
from aiogram.dispatcher.filters.state import State, StatesGroup ##Для создания машины состояний

import csv ##Будем заносить города в таблицу
import keyboards_tg ##Импортируем клавиатуры

import emoji ##Импортируем эмодзи
import sqlite3 ##Будем делать базу с рекордами игроков

data_score = {} ##Словарь, где мы будем хранить счёт игрока (айди:счёт)

class FSM_Cities(StatesGroup): ##Описываем машину состояний
    start_dialog = State()
    endP_dialog = State()


##Ответ на /start
@dp.message_handler(commands=["start"], state=None)
async def say_about_bot(message: types.Message, state: FSMContext):

    global data_score ##Берём data_score из глобальной области видимости

    #data_score[message.from_user.id] = 0 ##Записываем счёт по умолчанию 0

    ##Заносим игрока в базу
    db = sqlite3.connect("data/users_records/records.db")

    cursor = db.cursor()
    ##Создаём базу если не существует
    cursor.execute("""CREATE TABLE IF NOT EXISTS records_users(
        score INTEGER,
        first_name TEXT,
        id INTEGER
    )""")

    ##В данном блоке мы проверяем, есть ли пользователь в базе, если есть - ставим ему в счёт счёт из базы данных
    ##Сделана такая схема на случай непредвиденного выключения программы (бота)
    try:
        cursor.execute("""SELECT score, id FROM records_users""")
        l = cursor.fetchall()

        if message.from_user.id not in l[0]:
            print(l)
            data_score[message.from_user.id] = 0 ##Записываем счёт по умолчанию 0
        else:
            print(l)
            for i in l:
                for j in range(len(i)):
                    if i[j] == message.from_user.id:
                        data_score[message.from_user.id] = i[j-1]
    #############################################################

    except IndexError:
        print("---Поймано исключение 'IndexError'---")
        data_score[message.from_user.id] = 0

    cursor.execute(f"""DELETE FROM records_users WHERE id == {message.from_user.id}""")
    cursor.execute(f"""INSERT INTO records_users (score, first_name, id) VALUES ({data_score[message.from_user.id]}, '{message.from_user.first_name}', {message.from_user.id})""")
    db.commit()


    print("-----Пользователь {} написал: {} и вошёл в игру-----".format(message.from_user.username, message.text)) ##В консоль выводим сообщение пользователя
    await FSM_Cities.start_dialog.set() ##Входим в состояние

    city = random.choice(all_cities) ##Город
    last_word = "" ##Последняя буква

    ##Ставим символ в последнюю букву
    if city.lower()[-1] in "ьъ":
        last_word = city[-2]
    else:
        last_word = city[-1]

    ##Заносим счёт пользователя в базу данных
    with open("data/users_records/records.csv", "a+", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(
            ["score", "first_name", "chat_id"]
        )

        writer.writerow(
            [data_score[message.from_user.id], message.from_user.first_name, message.from_user.id]
        )

    ##Записываем город в список уже использованных
    method_to_open = "w"
    if data_score[message.from_user.id] != 0:
        method_to_open = "a+"

    with open(f"data//users_history//uses_cities_{message.from_user.id}.csv", method_to_open, newline="") as file:
        writer = csv.writer(file)

        writer.writerow(
            ["city_name", "chat_id"]
        )

        writer.writerow(
            [city, message.from_user.id]
        )

    await message.answer(f'Привет, я бот, с которым ты можешь поиграть в игру <b>"Города"</b>\nЯ начинаю: <b>{city}</b>, тебе нужно назвать город на букву <b>"{last_word.title()}"</b>',
                         #reply_markup=keyboards_tg.frame_start_buttons
                         )

##Ответ на /start уже в игре
@dp.message_handler(commands=["start"], state=FSM_Cities.start_dialog)
async def say_bot(message: types.Message):
    await bot.send_message(f"<b>{message.from_user.first_name}</b>, ты уже находишься в игре!")

##Ответ на /records
@dp.message_handler(commands=["records"], state=None)
async def say_about_records(message: types.Message, state: FSMContext):
    global data_score

    db = sqlite3.connect("data/users_records/records.db")
    cursor = db.cursor()
    cursor.execute("""SELECT score, first_name FROM records_users ORDER BY score DESC""")
    list_score = cursor.fetchall()

    if len(list_score) >= 5:
        await bot.send_message(message.from_user.id, f"""<u><b>Топ лучших игроков</b></u>

<b>1. {list_score[0][1]}</b> набрал {list_score[0][0]} очка(ов) {emoji.emojize(':star:')}
<b>2. {list_score[1][1]}</b> набрал {list_score[1][0]} очка(ов) {emoji.emojize(':star:')}
<b>3. {list_score[2][1]}</b> набрал {list_score[2][0]} очка(ов) {emoji.emojize(':star:')}
<b>4. {list_score[3][1]}</b> набрал {list_score[3][0]} очка(ов) {emoji.emojize(':star:')}
<b>5. {list_score[4][1]}</b> набрал {list_score[4][0]} очка(ов) {emoji.emojize(':star:')}""")
    elif len(list_score) >= 4:
        await bot.send_message(message.from_user.id, f"""<u><b>Топ лучших игроков</b></u>

<b>1. {list_score[0][1]}</b> набрал {list_score[0][0]} очка(ов) {emoji.emojize(':star:')}
<b>2. {list_score[1][1]}</b> набрал {list_score[1][0]} очка(ов) {emoji.emojize(':star:')}
<b>3. {list_score[2][1]}</b> набрал {list_score[2][0]} очка(ов) {emoji.emojize(':star:')}
<b>4. {list_score[3][1]}</b> набрал {list_score[3][0]} очка(ов) {emoji.emojize(':star:')}""")

    elif len(list_score) >= 3:
        await bot.send_message(message.from_user.id, f"""<u><b>Топ лучших игроков</b></u>

<b>1. {list_score[0][1]}</b> набрал {list_score[0][0]} очка(ов) {emoji.emojize(':star:')}
<b>2. {list_score[1][1]}</b> набрал {list_score[1][0]} очка(ов) {emoji.emojize(':star:')}
<b>3. {list_score[2][1]}</b> набрал {list_score[2][0]} очка(ов) {emoji.emojize(':star:')}""")

    elif len(list_score) >= 2:
        await bot.send_message(message.from_user.id, f"""<u><b>Топ лучших игроков</b></u>

<b>1. {list_score[0][1]}</b> набрал {list_score[0][0]} очка(ов) {emoji.emojize(':star:')}
<b>2. {list_score[1][1]}</b> набрал {list_score[1][0]} очка(ов) {emoji.emojize(':star:')}""")
    elif len(list_score) >= 1:
        await bot.send_message(message.from_user.id, f"""<u><b>Топ лучших игроков</b></u>

<b>1. {list_score[0][1]}</b> набрал {list_score[0][0]} очка(ов) {emoji.emojize(':star:')}""")

##Ответ на /records в процессе игры
@dp.message_handler(commands=["records"], state=FSM_Cities.start_dialog)
async def say_about_records(message: types.Message, state: FSMContext):
    global data_score


    db = sqlite3.connect("data/users_records/records.db")
    cursor = db.cursor()
    cursor.execute("""SELECT score, first_name FROM records_users ORDER BY score DESC""")
    list_score = cursor.fetchall()

    if len(list_score) >= 5:
        await bot.send_message(message.from_user.id, f"""<u><b>Топ лучших игроков</b></u>
        
<b>1. {list_score[0][1]}</b> набрал {list_score[0][0]} очка(ов) {emoji.emojize(':star:')}
<b>2. {list_score[1][1]}</b> набрал {list_score[1][0]} очка(ов) {emoji.emojize(':star:')}
<b>3. {list_score[2][1]}</b> набрал {list_score[2][0]} очка(ов) {emoji.emojize(':star:')}
<b>4. {list_score[3][1]}</b> набрал {list_score[3][0]} очка(ов) {emoji.emojize(':star:')}
<b>5. {list_score[4][1]}</b> набрал {list_score[4][0]} очка(ов) {emoji.emojize(':star:')}""")
    elif len(list_score) >= 4:
        await bot.send_message(message.from_user.id, f"""<u><b>Топ лучших игроков</b></u>

<b>1. {list_score[0][1]}</b> набрал {list_score[0][0]} очка(ов) {emoji.emojize(':star:')}
<b>2. {list_score[1][1]}</b> набрал {list_score[1][0]} очка(ов) {emoji.emojize(':star:')}
<b>3. {list_score[2][1]}</b> набрал {list_score[2][0]} очка(ов) {emoji.emojize(':star:')}
<b>4. {list_score[3][1]}</b> набрал {list_score[3][0]} очка(ов) {emoji.emojize(':star:')}""")

    elif len(list_score) >= 3:
        await bot.send_message(message.from_user.id, f"""<u><b>Топ лучших игроков</b></u>

<b>1. {list_score[0][1]}</b> набрал {list_score[0][0]} очка(ов) {emoji.emojize(':star:')}
<b>2. {list_score[1][1]}</b> набрал {list_score[1][0]} очка(ов) {emoji.emojize(':star:')}
<b>3. {list_score[2][1]}</b> набрал {list_score[2][0]} очка(ов) {emoji.emojize(':star:')}""")

    elif len(list_score) >= 2:
        await bot.send_message(message.from_user.id, f"""<u><b>Топ лучших игроков</b></u>

<b>1. {list_score[0][1]}</b> набрал {list_score[0][0]} очка(ов) {emoji.emojize(':star:')}
<b>2. {list_score[1][1]}</b> набрал {list_score[1][0]} очка(ов) {emoji.emojize(':star:')}""")
    elif len(list_score) >= 1:
        await bot.send_message(message.from_user.id, f"""<u><b>Топ лучших игроков</b></u>

<b>1. {list_score[0][1]}</b> набрал {list_score[0][0]} очка(ов) {emoji.emojize(':star:')}""")


##Ответ на /rules
@dp.message_handler(commands=["rules"], state=None)
async def say_about_rules(message: types.Message):
    with open("about/rules.txt", "r") as file:
        text_file = file.read()
        await bot.send_message(message.from_user.id, text_file)

##Ответ на /rules при включённой машине состояний
@dp.message_handler(commands=["rules"], state=FSM_Cities.start_dialog)
async def say_rules(message: types.Message, state: FSMContext):
    with open("about/rules.txt", "r") as file:
        text_file = file.read()
        await bot.send_message(message.from_user.id, text_file)


##Обработка /statgame при не активированной игре
@dp.message_handler(commands=["statgame"], state=None)
async def say_about_statgame(message: types.Message):
    await bot.send_message(message.from_user.id, f"<b>{message.from_user.first_name}</b>, для начала начни игру.")


##Обработка /statgame при активированной игре
@dp.message_handler(commands=["statgame"], state=FSM_Cities.start_dialog)
async def say_statgame(message: types.Message, state: FSMContext):
    global data_score

    await bot.send_message(message.from_user.id, f"Статистика пользователя <b>{message.from_user.first_name}</b>\n\nСчёт:  <b>{data_score[message.from_user.id]}{emoji.emojize(':star:')}</b>")


##Обработка выключения игры
@dp.message_handler(commands=["endgame"], state=FSM_Cities.start_dialog)
async def endgame(message: types.Message, state: FSMContext):

    global data_score ##Берём data_score из глобальной области видимости

    print(f"-----Пользователь {message.from_user.username} покинул игру-----")
    await message.answer(f"Игра с пользователем <b>{message.from_user.first_name}</b> завершена.\n\n <b>{message.from_user.first_name}</b>, твой счёт:  <b>{data_score[message.from_user.id]} {emoji.emojize(':star:')}</b>.")

    data_score[message.from_user.id] = 0  ##При выходе из игры обнуляем счёт игрока

    ##Из базы данных удаляем этого пользователя
    db = sqlite3.connect("data/users_records/records.db")
    cursor = db.cursor()
    cursor.execute(f"""DELETE from records_users WHERE id == {message.from_user.id}""")
    db.commit()

    await state.finish()


##Обработка нажатий на замену города
@dp.callback_query_handler(lambda button: button.data=="replace", state=FSM_Cities.start_dialog)
async def reply_to_replace(callback_query: types.CallbackQuery, state: FSMContext):

    global data_score ##Берём data_score из глобальной области видимости

    try:
        if data_score[callback_query.from_user.id] > 0: ##Блок будет работать при условии, что счёт игрока больше 0

            city = random.choice(all_cities)

            if city[-1] in "ьъ":
                last_word = city[-2]
            else:
                last_word = city[-1]

            with open(f"data//users_history//uses_cities_{callback_query.from_user.id}.csv", "a+", newline="") as file:
                writer = csv.writer(file)

                writer.writerow(
                    [city, callback_query.from_user.id]
                )

            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.from_user.id,
                                   f'<b>{callback_query.from_user.first_name}</b>, ты попросил замену города и мы вычитаем из твоего счёта 1 балл. Итак, новый город - <b>{city}</b>, тебе на <b>"{last_word.title()}"</b>'
                                   )

            data_score[callback_query.from_user.id] -= 1
            print(f"Замена города {data_score[callback_query.from_user.id]}")
            ##Заносим счёт в базу данных
            db = sqlite3.connect("data/users_records/records.db")
            cursor = db.cursor()
            cursor.execute(f"""UPDATE records_users SET score = {data_score[callback_query.from_user.id]} WHERE id == {callback_query.from_user.id}""")
            db.commit()

        elif data_score[callback_query.from_user.id] == 0: ##Если же ноль - то бот отсылает предупреждение
            await bot.send_message(callback_query.from_user.id, f"<b>{callback_query.from_user.first_name}</b>, ты уже много раз использовал замену города, твой счёт не может быть отрицательным!")
    except KeyError:
        #data_score[callback_query.from_user.id] = 0
        pass


##Обработка нажатия на подсказку
@dp.callback_query_handler(lambda button: button.data=="help", state=FSM_Cities.start_dialog)
async def reply_to_help(callback_query: types.CallbackQuery, state: FSMContext):

    print("Пользователь нажал на 'Случайный город'")

    use_city = "" ##Уже использованный город, который мы определим позже

    ##Читаем файл чтобы определить последний использованный город в чате
    with open(f"data//users_history//uses_cities_{callback_query.from_user.id}.csv", "r") as file:
        reader = csv.DictReader(file)

        for line in reader:
            use_city = line["city_name"] ##Определяем город

    help_city = random.choice(all_cities) ##Рандомный город

    while help_city.lower()[0] != use_city.lower()[-1]: ##Пока первая буква рандомного города не будет равна последней названного города
        help_city = random.choice(all_cities)

    ##Тут мини-скриптик по вставке звёздочке в город для чуть усложнения задачи
    save_array = [word for word in help_city]
    save_array[random.randint(1, len(help_city)-2)] = "*"

    help_city = ""
    for i in save_array:
        help_city += i
    #############################################################################

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           f"<b>{callback_query.from_user.first_name}</b>, даю тебе подсказку: <b>{help_city}</b>",
                           #reply_markup=keyboards_tg.frame_start_buttons
                           )


##Обработка сообщений  с городами
@dp.message_handler(state=FSM_Cities.start_dialog)
async def process_playing(message: types.Message, state: FSMContext):

    global data_score ##Берём data_score из глобальной области видимости

    print("Пользователь написал: {}".format(message.text)) ##В консоль выводим сообщение пользователя

    user_city = message.text.lower().title() ##Город, названный пользователем

    ##Ответ для пользователя, если города нет в базе
    if user_city not in all_cities and user_city[0].lower() != "/":
        await message.answer(f'Хмм, я не знаю города <b>"{user_city}"</b>...')
        return False

    uses_cities_list = [] ##Список использованных городов

    ##Заполним список uses_cities_list
    with open(f"data//users_history//uses_cities_{message.from_user.id}.csv", "r") as file:
        reader = csv.DictReader(file)

        for line in reader:
            uses_cities_list.append(line["city_name"])

    print(uses_cities_list)


    ##Взаимодействие с файлами и пользователем
    with open(f"data//users_history//uses_cities_{message.from_user.id}.csv", "r") as file: ##Открываем файл для проверки: Правильный ли город назвал пользователь
        reader = csv.DictReader(file)

        for line in reader: ## В данном цикле проверка на: #1.Совпдание id пользователя и id в файле #Совпадение первой буквы сообщения от пользователя с последней буквой города в файле

            last_word = "" ##Последняя буква в строке города будет тут

            if uses_cities_list[-1].lower()[-1] in "ьъ":
                last_word = uses_cities_list[-1].lower()[-2]
            else:
                last_word = uses_cities_list[-1].lower()[-1]

            ##Ответ пользователю, если город уже был использован в игре
            if user_city in uses_cities_list and user_city[0].lower() == last_word:
                await message.answer(
                    f'Город <b>"{user_city}"</b> уже был использован в игре, <b>{message.from_user.first_name}</b>.')
                print(uses_cities_list)
                return False

            if message.text.lower()[0] == last_word\
                and user_city in all_cities:

                #last_word = "" ##Последняя буква в строке города будет тут

                if message.text.lower()[-1] in "ьъ": ##Проверям: последняя буква в ьъ?
                    last_word = message.text.lower()[-2] ##Если да - то предпоследняя буква
                else:
                    last_word = message.text.lower()[-1] ##Иначе - то последняя

                await message.answer(f'Верно, город <b>{user_city}</b> существует.\nТеперь назови город на букву <b>"{last_word.title()}"</b>',
                                     reply_markup=keyboards_tg.frame_start_buttons
                                     )
                ##В данном блоке try-except мы, при существовании ключа с айди пользователя - прибавляем к счёту 1, а при возбуждении исключения KeyError - создаём пару ключ-значение
                try:
                    data_score[message.from_user.id] += 1

                    db = sqlite3.connect("data/users_records/records.db")
                    cursor = db.cursor()
                    cursor.execute(f"""UPDATE records_users SET score = {data_score[message.from_user.id]} WHERE id =={message.from_user.id}""")
                    db.commit()

                except KeyError:
                    #data_score[message.from_user.id] = 1
                    pass

                with open("data/users_records/records.csv", "a+") as file_records:
                    writer = csv.writer(file_records)


                ##Добавим город в список использованных
                with open(f"data//users_history//uses_cities_{message.from_user.id}.csv", "a+", newline="") as file:
                    writer = csv.writer(file)

                    writer.writerow(
                        [user_city, message.from_user.id]
                    )

                break
