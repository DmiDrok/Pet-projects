from flask import Flask, Blueprint, request, render_template, url_for,\
     redirect, session, g, current_app, flash, get_flashed_messages
import sqlite3


admin = Flask(__name__)
admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

##Проверка на админа
def isLogged():
    if session.get("admin") == "true":
        return True
    
    return False

##Загрузка стандартного изображения
def get_standard_image():
    binary_img = None
    with open(current_app.root_path + "\\static\\img\\img001.jpg") as f:
        binary_img = f.read()

    return binary_img

tovars_all = None  ##Все товары
@admin.before_request
def before_adm():
    global tovars_all, Tovars, db

    tovars_all = g.tovars_all


##Обработчик главной страницы админки
@admin.route("/")
def index():
    if not isLogged():
        return redirect(url_for('.login_adm'))
    
    print(request.get_data("info"))

    return render_template(
        "admin/index_adm.html",
        title="Админка/Главная",
        tov_len=len(tovars_all)
        ) 

##Обработчик входа в админку
@admin.route("/login", methods=["POST", "GET"])
def login_adm():
    
    ##Проверка на админа
    if isLogged():
        return redirect(url_for('.index'))

    if request.method == "POST":
        if request.form["login_adm"].strip() == "test" and request.form["password_adm"].strip() == "12345":
            session["admin"] = "true"
            return redirect(url_for('.index'))

    return render_template("admin/auth_admin.html")

##Добавление товара
@admin.route("/add_new_tov", methods=["POST", "GET"])
def add_tovar():

    ##Проверка на админа
    if not isLogged():
        return redirect(url_for('.login_adm'))

    print(current_app.root_path, "a3r2opafd")
    
    ##Обрабатываем пост:
    if request.method == "POST":
        if len(request.form["title_add_tov"].strip()) >= 5 and len(request.form["about_add_tov"].strip()) >= 5:
            if len(request.form["content_add_tov"].strip()) >= 20:
                if int(request.form["price_add_tov"].strip() ) >= 50:
                    title = request.form["title_add_tov"].strip() ##Название
                    about = request.form["about_add_tov"].strip() ##Немного о товаре
                    content = request.form["content_add_tov"].strip() ##Много о товаре
                    price = request.form["price_add_tov"].strip() ##Цена

                    file = request.files["file_img"] ##Картинку берём
                    image = file.read() ##Картинку считываем

                    with sqlite3.connect(current_app.root_path + "\\data.db") as conn:
                        cursor = conn.cursor()
                        cursor.execute("""INSERT INTO Tovars (image_tov, title_tov, about_tov, content_tov, price_tov) VALUES (?, ?, ?, ?, ?)""", (image, title, about, content, price))
                        conn.commit()
            


    return render_template(
        "admin/add_tovar.html",
        title="Добавление товара",
        submit_value="Добавить"
        )

##Редактирование товара
@admin.route("/redact_tovar/<tovar_id>/<title_to_redact>/<about_to_redact>/<content_to_redact>/<price_to_redact>", methods=["POST", "GET"])

def redact_tovar(tovar_id, title_to_redact, about_to_redact, content_to_redact, price_to_redact):

    ##Проверка на админа
    if not isLogged():
        return redirect(url_for('.login_adm'))

    if request.method == "POST":
        if len(request.form["title_add_tov"].strip()) >= 5 and len(request.form["about_add_tov"].strip()) >= 5:
            if len(request.form["content_add_tov"].strip()) >= 20:
                if int(request.form["price_add_tov"].strip() ) >= 50:
                    title_to_redact = request.form["title_add_tov"].strip() ##Название
                    about_to_redact = request.form["about_add_tov"].strip() ##Немного о товаре
                    content_to_redact = request.form["content_add_tov"].strip() ##Много о товаре
                    price_to_redact = request.form["price_add_tov"].strip() ##Цена

                    if request.files["file_img"]:
                        file = request.files["file_img"] ##Картинку берём
                        image_to_redact = file.read() ##Картинку считываем

                        ##Обновляем базу данных
                        with sqlite3.connect(current_app.root_path + "\\data.db") as conn:
                            cursor = conn.cursor()
                            cursor.execute("""UPDATE tovars SET image_tov = ?, title_tov = ?, about_tov = ?, content_tov = ?, price_tov = ? WHERE id == ?""", (image_to_redact, title_to_redact, about_to_redact, content_to_redact, price_to_redact, tovar_id))

                            #return url_for(".redact_tovar", tovar_id=tovar_id)

                    else:
                        with sqlite3.connect(current_app.root_path + "\\data.db") as conn:
                            cursor = conn.cursor()
                            cursor.execute("""UPDATE tovars SET title_tov = ?, about_tov = ?, content_tov = ?, price_tov = ? WHERE id == ?""", (title_to_redact, about_to_redact, content_to_redact, price_to_redact, tovar_id))

                    #flash("Успешно изменено!", category="success")
                    return redirect(url_for("page_tovar", tovar_id=tovar_id))

    
    return render_template(
        "admin/redact_tovar.html",
        title="Изменение товара", 
        submit_value="Изменить",

        insert_title=title_to_redact,
        insert_about=about_to_redact,
        insert_content=content_to_redact.replace("%3C", "<").replace("%2F", "/").replace("%3E", ">"),
        insert_price=price_to_redact
        )

##Обработчик просмотра корзин пользователей
@admin.route("/all_users", methods=["POST", "GET"])
def all_users():
    all_users = []

    ##Если пришёл запрос, а именно - нужно найти пользователя по email
    if request.method == "POST":
        try:
            with sqlite3.connect(current_app.root_path + "\\data.db") as conn:
                conn.row_factory = sqlite3.Row

                cursor = conn.cursor()
                email = request.form["email_search"].strip()
                cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")

                all_users = cursor.fetchall()
        except Exception as err:
            print(err)

        return render_template("admin/all_users.html", title="Пользователи", all_users=all_users)

    try:
        with sqlite3.connect(current_app.root_path + "\\data.db") as conn:
            conn.row_factory = sqlite3.Row

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users ORDER BY id DESC")

            all_users = cursor.fetchall()

    except Exception as err:
        print(err)

    print(all_users)
    return render_template("admin/all_users.html", title="Пользователи", all_users=all_users)

##Обработчик страницы информации о пользователе
@admin.route("/user/<user_id>/<path:user_email>")
def user_page(user_id, user_email):


    res = []

    try:
        with sqlite3.connect(current_app.root_path + "\\data.db") as conn:
            conn.row_factory = sqlite3.Row

            cursor = conn.cursor()
            cursor.execute(f"""SELECT * FROM users WHERE id == {user_id}""")
            res = cursor.fetchall()
            print(res[0]["id"], "---")

    except Exception as err:
        print(err)


    return render_template(
        "admin/user_page.html",
        title=user_email,
        user_info = res[0],
        )

##Обработчик корзины пользователя
@admin.route("/user_basket/<user_id>/<path:user_email>")
def user_basket(user_id, user_email):

    all_tovars = []
    total_price = 0

    with sqlite3.connect(current_app.root_path + "\\data.db") as conn:
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM basket WHERE user_id == {user_id}""")
        basket = cursor.fetchall()

        ##Добавляем в список всех товаров атрибуты из другой таблицы
        for i in basket:
            el_to_add = cursor.execute(f"SELECT * FROM tovars WHERE id == {i['tovar_id']}").fetchall()
            total_price += el_to_add[0]["price_tov"]
            all_tovars.extend([el_to_add])

       

    print(total_price, "--------")

    return render_template(
        "admin/user_basket.html",
         title=f"{user_email} - Корзина",
         all_tovars = all_tovars,
         total_price=total_price,
    )


##Выход из админки
@admin.route("/logout")
def logoud_admin():
    session.pop("admin", None)
    return "Успешно вышли!"