from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Email, Length, DataRequired

##Форма регистрации
class RegForm(FlaskForm):
    email = StringField("", validators=[Email(), Length(min=3, max=100)], render_kw={"placeholder":"Email"})
    password = PasswordField("", validators=[DataRequired(), Length(min=3, max=100)], render_kw={"placeholder":"Пароль"})
    password2 = PasswordField("", validators=[DataRequired(), Length(min=3, max=100)], render_kw={"placeholder":"Пароль повтороно"})
    submit = SubmitField("Регистрация")

##Форма авторизации
class AuthForm(FlaskForm):
    email = StringField("", validators=[Email(), Length(min=3, max=100)], render_kw={"placeholder":"Email"})
    password = PasswordField("", validators=[DataRequired(), Length(min=3, max=100)], render_kw={"placeholder":"Пароль"})
    remember_me = BooleanField("Запомнить", default=False)
    submit = SubmitField("Авторизация")