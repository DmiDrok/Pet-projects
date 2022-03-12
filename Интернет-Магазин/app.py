from flask import Flask, render_template, url_for, make_response, g, current_app,\
     session, redirect, request, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from admin.admin import admin
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from UserLogin import UserLogin
from forms import RegForm, AuthForm
from datetime import datetime

##Конфигурация
SECRET_KEY = "sdkfoakewfoawefmxv,xcv-[dsfg-k2kasd.p))2-__32rsfa"

##WSGI - приложение
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config.from_object(__name__)

##Логин-Менеджер
login_manager = LoginManager(app)
login_manager.login_view = "auth"
login_manager.login_message = "Для просмотра товаров необходима авторизация на сайте."
login_manager.login_message_category = "succes"

##Загрузка информации о пользователе, все его атрибуты
@login_manager.user_loader
def load_user(user_id):
    return UserLogin().get_user(Users, user_id)

##Эскиз админки
admin = app.register_blueprint(admin, url_prefix="/admin")

##База данных
db = SQLAlchemy(app)


##Таблица пользователей
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(50), nullable=False) ##Почта
    password = db.Column(db.String(500), nullable=False) ##Пароль
    date_reg = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"user_id = {id}"

##Таблица товаров
class Tovars(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    image_tov = db.Column(db.LargeBinary(), nullable=False)
    title_tov = db.Column(db.String(30), nullable=False)
    about_tov = db.Column(db.String(50), nullable=False)
    content_tov = db.Column(db.String(1000), nullable=False)
    price_tov = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return f"tovar_id = {id}"

##Таблица корзины
class Basket(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, nullable=False)
    tovar_id = db.Column(db.Integer, db.ForeignKey("tovars.id"))

    def __repr__(self):
        return f"column_id = {id}"


tovars_all = None ##Переменная для дальнейшего использования всего списка товаров
basket = None ##Переменная для дальнейшего использования корзины
@app.before_request
def before():
    ##Получаем все товары
    global tovars_all
    tovars_all = Tovars.query.all()
    if bool(hasattr(g, "tovars_all")) == False:
        g.tovars_all = tovars_all



##Проверка на админа
def isAdmin():
    admin = False
    if session.get("admin") == "true":
        admin = True

    return admin

##Авторизация
@app.route("/authorization", methods=["POST", "GET"])
def auth():

    ##Проверка: авторизован ли пользователь
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    ##Форма
    form = AuthForm()

    ##Обработка WTForms формы
    if form.validate_on_submit():
        print("dsfsdf")
        password_db = Users.query.filter_by(email=form.email.data.strip()).first().password
        print(password_db)
        if check_password_hash(password_db, form.password.data.strip()):
            user = Users.query.filter_by(email=form.email.data.strip()).first()
            if user:
                userlogin = UserLogin().create_user(user)
                rm = form.remember_me.data  ##True/False
                login_user(userlogin, remember=rm)
                return redirect(url_for("index"))

    return render_template(
     "auth.html",
     title="Авторизация",
     title_header="Авторизация",
     admin=isAdmin(),
     submit_value="Авторизация",
     ask_href=url_for("reg"),
     ask_text="Нет аккаунта?",
     form=form,
     )

##Регистрация
@app.route("/registration", methods=["POST", "GET"])
def reg():

    ##Проверка: авторизован ли пользователь
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    ##Форма
    form = RegForm()

    ##Обработка WTForms формы
    if form.validate_on_submit():
        if not Users.query.filter_by(email=form.email.data.strip()).first():
            if form.password.data.strip() == form.password2.data.strip():
                email = form.email.data.strip()
                password = generate_password_hash(form.password.data.strip())

                ##Добавляем в БД
                u = Users(email=email, password=password)
                db.session.add(u)
                db.session.flush()
                db.session.commit()

                return redirect(url_for("auth"))
            else:
                flash("Пароли не совпадают!", category="error")
        else:
            flash("Такой пользователь уже присутствует на сайте!", category="error") 


    return render_template(
        "reg.html",
        title="Регистрация",
        title_header="Регистрация",
        admin=isAdmin(),
        submit_value="Регистрация",
        ask_href=url_for("auth"),
        ask_text="Есть аккаунт?",
        form=form,
    )

##Получить изображение
@app.route("/img_get/<column_id>")
def getting(column_id):
    binary_img = Tovars.query.filter_by(id=column_id).first().image_tov

    res = make_response(binary_img)
    res.headers["Content-type"] = "image/jpg"

    return res


##Обработчик главной страницы
@app.route("/")
@app.route("/page=<page_number>")
def index(page_number=1):

    ##Скрипт для пагинации (переключателя страниц)
    if len(tovars_all) >= 4:

        tovars_to_page = []
        tovars_to_page.extend([tovars_all[0:4]])
        el = 4
        a = el
        while el != len(tovars_all):
            el += 1
            if el % 4 == 0: ##Если индекс делится нацело
                print(el)
                tovars_to_page.extend([tovars_all[a:el]])
                a = el

            elif tovars_all.index(tovars_all[el]) == len(tovars_all)-1: ##Если индекс элемента в списке равен индеку последнего (т.е. если элемент является последним)
                tovars_to_page.extend([tovars_all[a:el+1]])
                break

                   

        return render_template(
            "index.html",
            list_tov=tovars_to_page[int(page_number)-1],
            admin=isAdmin(),
            num_pages=len(tovars_to_page),
            page_number=int(page_number),
            )

    return render_template(
        "index.html",
        list_tov=tovars_all,
        admin=isAdmin(),
        num_pages=1,
        page_number=int(page_number),
    )


##Обработчик страницы с товаром
@app.route("/tovar/<tovar_id>")
@login_required
def page_tovar(tovar_id):

    ##Переменные по стандарту для кнопки добавления
    btn_class = "default"
    btn_text = "Добавить в корзину"
    form_action = url_for("add_to_basket", user_id=current_user.get_id(), tovar_id=tovar_id)

    ##Если товар уже был куплен
    if Basket.query.filter_by(user_id=current_user.get_id(), tovar_id=tovar_id).first():
        btn_class="active"
        btn_text="Добавлено"
        form_action = url_for("remove_from_basket", user_id=current_user.get_id(), tovar_id=tovar_id)

    return render_template(
        "tovar.html",
         admin=isAdmin(),
         id_tovar=tovar_id,
         id_user=current_user.get_id(),
         text_info=Tovars.query.filter_by(id=tovar_id).first().content_tov,
         price_info = Tovars.query.filter_by(id=tovar_id).first().price_tov,

         class_for_btn=btn_class,
         text_for_btn=btn_text,
         action_for_form=form_action
    )

##Обработчик корзины
@app.route("/basket")
@login_required
def basket():

    basket = Basket.query.filter_by(user_id=current_user.get_id()).all()
    basket_to_page = []
    sum_tovars = 0

    ##Убираем из корзины всё что не связано с нашим пользователем
    #for i in basket:
    #    if i.user_id != int(current_user.get_id()):
    #        print("Прокнуло")
    #        basket.remove(i)

    ##Добавляем в список всех товаров атрибуты из другой таблицы
    for i in basket:
        el_to_add = Tovars.query.filter_by(id=i.tovar_id).first()
        basket_to_page.extend([el_to_add])

    if len(basket_to_page) == 0:
        flash("В корзине нет товаров...", category="success")

    ##Добавляем цену товара в общую сумму
    for tovar in basket_to_page:
        sum_tovars += tovar.price_tov

    return render_template(
        "basket.html",
        admin=isAdmin(),

        basket=basket_to_page,
        user_id=int(current_user.get_id()),
        sum_tovars=sum_tovars,
    )

##Переправка на редактирование товара
@app.route("/redact_middle/<tovar_id>", methods=["POST", "GET"])
def redact_middle(tovar_id):

    ##Выборка товара и его атрибутов для дальнейшей переправке в шаблон на случай редактирования
    tovar = Tovars.query.filter_by(id=tovar_id).first()

    title_tovar = tovar.title_tov#.replace(" ", "_").replace(",", "_").replace("?", "_").replace("#", "_").replace("=", "_").replace("&", "_").replace("$", "_")
    about_tovar = tovar.about_tov#.replace(" ", "_").replace(",", "_").replace("?", "_").replace("#", "_").replace("=", "_").replace("&", "_").replace("$", "_")
    content_tovar = tovar.content_tov.replace("<", "%3C").replace("/", "%2F").replace(">", "%3E")
    image_tovar = tovar.image_tov
    price_tovar = tovar.price_tov

    return redirect(url_for(
        "admin.redact_tovar", 
        tovar_id=tovar_id, 
        title_to_redact=title_tovar,
        about_to_redact=about_tovar,
        content_to_redact=content_tovar,
        price_to_redact=price_tovar,
        ))


##Обработчик удаления товара
@app.route("/delete_tovar/<tovar_id>", methods=["POST", "GET"])
def delete_tovar(tovar_id):

    ##Обязательно делаем проверку на админа
    if not isAdmin():
        return redirect(url_for("index"))

    ##Обрабатываем сам запрос
    if request.method == "POST":
        Tovars.query.filter_by(id=tovar_id).delete() ##Удаляем элемент из БД
        db.session.flush()
        db.session.commit()
        print(tovars_all)

    return redirect(url_for("index"))


##Обработчик добавления в корзину
@app.route("/to_basket/<user_id>?<tovar_id>", methods=["POST", "GET"])
@login_required
def add_to_basket(user_id, tovar_id):

    if request.method == "POST":
        if not Basket.query.filter_by(user_id=user_id, tovar_id=tovar_id).first():
            b = Basket(user_id=user_id, tovar_id=tovar_id)
            db.session.add(b)
            db.session.flush()
            db.session.commit()
        

    return redirect(url_for('page_tovar', tovar_id=tovar_id))

##Обработчик удаления из корзины
@app.route("/remove_from_basket/<user_id>?<tovar_id>", methods=["POST", "GET"])
@login_required
def remove_from_basket(user_id, tovar_id):

    if request.method == "POST":
        if Basket.query.filter_by(user_id=user_id, tovar_id=tovar_id).first():
            Basket.query.filter_by(user_id=user_id, tovar_id=tovar_id).delete()
            db.session.commit()

    return redirect(url_for("page_tovar", tovar_id=tovar_id))

##Обработчик удаления из корзины на странице самой корзины
@app.route("/remove_out_basket/<user_id>?<tovar_id>", methods=["POST", "GET"])
def remove_out_basket(user_id, tovar_id):

    if request.method == "POST":
        if Basket.query.filter_by(user_id=user_id, tovar_id=tovar_id).first():
            Basket.query.filter_by(user_id=user_id, tovar_id=tovar_id).delete()
            db.session.commit()

    return redirect(url_for("basket", tovar_id=tovar_id))

##Обработчик покупки товаров из корзины
@app.route("/buy_basket/<user_id>/<display_vidget>", methods=["POST", "GET"])
@login_required
def buy_basket(user_id, display_vidget):

    
    ##Проверка на соответствие айди в url и айди пользователя
    if int(current_user.get_id()) != int(user_id):
        return redirect(url_for('basket'))

    basket = Basket.query.filter_by(user_id=current_user.get_id()).all()
    basket_to_page = []
    sum_tovars = 0

    #for i in basket:
        #if i.user_id != int(current_user.get_id()):
            #basket.remove(i)

    for i in basket:
        el_to_add = Tovars.query.filter_by(id=i.tovar_id).first()
        basket_to_page.extend([el_to_add])

    ##Добавляем цену товара в общую сумму
    for tovar in basket_to_page:
        sum_tovars += tovar.price_tov

    print(sum_tovars)

    return render_template(
        "buy_basket.html",
        admin=isAdmin(),
        finally_price=sum_tovars,
        display_vidget=display_vidget,
        )

##Обработчик отображения виджета оплаты
@app.route("/display_vidget", methods=["POST", "GET"])
def display_vidget():
    return redirect(url_for("buy_basket", user_id=current_user.get_id(), display_vidget="display"))

##Обработчик выхода из профиля
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth'))


##Точка входа или запуск приложения
if __name__ == "__main__":
    app.run(debug=True)