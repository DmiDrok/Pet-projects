from flask import Flask, render_template, make_response, url_for, request, session, redirect, g, flash, get_flashed_messages
import os
import sqlite3
from FData import FData
from werkzeug.security import generate_password_hash, check_password_hash

##Конфигурация
SECRET_KEY = "a48#eec6d2ed8@e48fbd1dd857$e3c5a%40f27f593__60ce79a7dc4@#f44edfb6cba"
DATABASE = "tmp/sdb.db"

##WSGI приложение
app = Flask(__name__)
app.config.from_object(__name__) ##Загружаем конфиг


##Создаём ДБ
def create_db():
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        with app.open_resource("create_db.sql", "r") as f:
            cursor.executescript(f.read())

        db.row_factory = sqlite3.Row
        db.commit()

        return db


##Получаем ДБ в контекст запроса
def get_db():
    if bool(hasattr(g, "link_db")) == False:
        g.link_db = sqlite3.connect(DATABASE)

    return g.link_db

##Выполнится когда приложение выключится (контекст приложения разрушается - выполняем)
@app.teardown_appcontext
def close_connection(error):
    if bool(hasattr(g, "link_db")) == True:
        g.link_db.close()


##Выполнится перед запросом
Fdb = None
@app.before_request
def before():
    """Установление соединения с БД перед каждым запросом пользователя"""
    global Fdb

    db = get_db()
    Fdb = FData(db)

##Обработчик главной страницы
@app.route("/index/<username>", methods=["POST", "GET"])
def index(username):


    ##Не зарегистрирован - регистрируйся
    if "name" not in session:
        return redirect(url_for("registration"))
    ##Если пользователь заходит на страницу другого пользователя
    if session.get("name") != username:
        return redirect(url_for("index", username=session.get("name")))


    ##Если зарегистрирован    
    elif "name" in session:

        all_posts = []
        is_admin = False

        ##Проверка на админа
        if "admin" in session and session.get("admin") == "true":
            is_admin = True

        ##Обрабатываем запросы
        if request.method == "POST":
            #if is_admin == True:
                #Fdb.DeletePost(request.form[""])

            if len(request.form["some_tag"]) >= 2 and len(request.form["some_tag"]) <= 15:
                result_of_func = Fdb.GetOnTag(request.form["some_tag"].lower())
                if bool(result_of_func) == True:
                    all_posts = result_of_func[0]
                    count_posts = result_of_func[1] ##Берём кол-во постов для флеша
                    flash(f"'{request.form['some_tag']}' - {count_posts} статья(ей)")
                else:
                    flash(f"'{request.form['some_tag']}' -  ничего не найдено")
                    all_posts = Fdb.GetPosts()
        else:
            all_posts = Fdb.GetPosts()

        

        ##Ссылки
        links_reg = {
            "Главная":f"/index/{session.get('name')}",
            "Добавить статью":"/add_post"
        }

        menu = links_reg
        user_name = username
        #all_posts = Fdb.GetPosts()

        content = render_template("index.html", title="Главная страница", menu=menu, user_name=user_name, all_posts=all_posts, is_admin=is_admin)

        res = make_response(content, 200)
        return res

@app.route("/something")
def a():
    return "a"

##Обработчик регистрации
@app.route("/registration", methods=["POST", "GET"])
def registration():

    ##Если пользователь был зарегистрирован - редирект на его страницу
    if "name" in session:
        return redirect(url_for("index", username=session.get("name")))

    db = get_db() ##Получаем БД в рамках запроса
    Fdb = FData(db)

    ##Принимаем запрос
    if request.method == "POST":
        if len(request.form["login"].strip()) >= 5 and len(request.form["pass"].strip()) >= 5:
            if request.form["pass"].strip() == request.form["pass2"].strip():
                ##Вносим значения из формы в ДБ
                if bool(Fdb.RegUser(request.form["login"].strip(), generate_password_hash(request.form["pass"].strip()))) == True:
                    return redirect(url_for("auth"))
                else:
                    print(request.form["pass"], request.form["pass2"])
                    flash("Такой логин уже присутствует на сайте!", category="error")
            else:
                print(request.form["pass"], request.form["pass2"])
                flash("Пароли не совпадают!", category="error")
        else:
            print(request.form["pass"], request.form["pass2"])
            flash("Логин и пароль должны быть больше 5 символов!")

    ##Проверка на зарегистрированного пользователя или нет
    if "name" in session:
        return redirect(url_for("index"))

    value_button = "Зарегистрироваться"
    handler = url_for("registration")
    url_ask = url_for("auth")
    text_ask = "Есть аккаунт?"

    content = render_template("reg.html",
        title="Регистрация",
        value_button=value_button,
        handler=handler,
        url_ask=url_ask,
        text_ask=text_ask,
        registrate=True,
    )

    res = make_response(content, 200)
    return res

##Обработчик авторизации
@app.route("/", methods=["POST", "GET"])
def auth():


    if "name" in session:
        return redirect(url_for("index", username=session.get("name")))

    ##Обработчик формы авторизации
    if request.method == "POST":
        if len(request.form["login"].strip()) >= 5 and len(request.form["pass"].strip()) >= 5:
            if len(request.form.getlist("remember_me")) > 0:
                session["remember_me"] = "true"
                session.permanent = True ##Делаем хранение данных на 31 день
            if Fdb.GetUser(request.form["login"].strip(), request.form["pass"].strip()) == True:
                print("ПОЙМАЛИ ТРУ!!!")
                session["name"] = request.form["login"].strip()
                return redirect(url_for("index", username=session.get("name")))

            else:
                flash("Проверьте корректность введённых данных!", category="error")
            
            
    value_button = "Авторизоваться"
    handler = url_for("auth")
    url_ask = url_for("registration")
    text_ask = "Нет аккаунта?"

    content = render_template("auth.html",
        title="Авторизация",
        value_button=value_button,
        handler=handler,
        url_ask=url_ask,
        text_ask=text_ask
        )

    res = make_response(content, 200)
    return res

##Обработчик страницы с добавлением поста
@app.route("/add_post", methods=["POST", "GET"])
def add_post():

    #Если пользователь не зарегистрирован - пусть регистрируется
    if "name" not in session:
        return redirect(url_for("registration"))

    links_reg = {
            "Главная":f"/index/{session.get('name')}",
            "Добавить статью":"/add_post"
    }
   
    ##Добавление статьи в БД
    if request.method == "POST":
        if len(request.form["post_name"].strip()) >= 5 and len(request.form["post_content"].strip()) >= 5:
            Fdb.AddPost(request.form["post_name"].strip(), request.form["post_content"].strip(), request.form["post_tag"].strip(), session["name"])

    content = render_template("add_post.html", title="Создание поста", menu=links_reg)

    res = make_response(content, 200)
    return res

##Обработчик для отображения статей на сайте
@app.route("/post/<int:post_id>")
def display_post(post_id):


    if "name" not in session:
        return redirect(url_for("registration"))

    links_reg = {
        "Главная":f"/index/{session.get('name')}",
        "Добавить статью":"/add_post"
    }

    post = Fdb.GetPost(post_id)

    return render_template("post.html", title="Просмотр статьи", menu=links_reg, user_name=session["name"], post=post)

##Обработчик странички пользователя
@app.route("/user/<username>")
def page_user(username):

    if "name" not in session:
        return redirect(url_for("registration"))

    links_reg = {
        "Главная":f"/index/{session.get('name')}",
        "Добавить статью":"/add_post"
    }

    ##Информация о пользователе для отображения
    num_user_posts = Fdb.GetNumPost(username)
    date_reg = Fdb.GetUserReg(username)
    late_post = Fdb.GetLatePost(username)

    ##Если ошибка (нет постов от пользователя - то меняем переменную на 0)
    if num_user_posts != False:
        pass
    else:
        num_user_posts = 0

    content = render_template("user_page.html", title="Просмотр страницы",\
        username=username, menu=links_reg, num_posts=num_user_posts,\
        date_reg=date_reg, late_post=late_post,
        )

    res = make_response(content, 200)

    return res

@app.route("/clear")
def clear_all():
    session.pop("name", None)
    session.permanent = False
    return "Очистка прошла успешна!"

@app.errorhandler(404)
def NotFound(error):
    if "name" not in session: ##Не зарегистрирован - на регистрацию
        return redirect(url_for("registration"))

    return redirect(url_for("index", username=session["name"])) ##Зарегистрирован - на главную страницу

if __name__ == "__main__":
    app.run("localhost", debug=True)