from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Email
from wtforms.fields.html5 import EmailField


class InventoryForm(FlaskForm):
    category = StringField("Номер категории", validators=[DataRequired()])
    categoryName = StringField("Название категории", validators=[DataRequired()])
    number = StringField("Номер товара", validators=[DataRequired()])
    number_name = StringField("Название товара", validators=[DataRequired()])
    place = SelectField("Место", choices=[("Администратор", "Администратор"),
                                          ("Раздевалка", "Раздевалка"),
                                          ("Оранжевый класс", "Оранжевый класс"),
                                          ("Зелёный класс", "Зелёный класс"),
                                          ("Инженерный стелаж", "Инженерный стелаж")], validators=[DataRequired()])
    submit = SubmitField("Подтвердить")


class CustomLoginForm(FlaskForm):
    name = StringField("Имя пользователя", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class UserUpdateInfo(FlaskForm):
    new_password = PasswordField("Новый пароль", validators=[DataRequired(),
                                                         Length(min=5, message="Пароль слишком короткий"),
                                                         EqualTo("new_password_repeat", message="Пароли не совпадают")])
    new_password_repeat = PasswordField("Подтвердите пароль", validators=[DataRequired()])
    submit = SubmitField("Обновить пароль")


class RegisterNewUser(FlaskForm):
    name = StringField("Имя пользователя", validators=[DataRequired()])
    password = PasswordField("Новый пароль", validators=[DataRequired(),
                                                         Length(min=5, message="Пароль слишком короткий"),
                                                         EqualTo("password_repeat", message="Пароли не совпадают")])
    password_repeat = PasswordField("Подтвердите пароль", validators=[DataRequired()])
    email = EmailField("Адресс электронной почты", validators=[DataRequired(), Email()])
    real_name = StringField("Имя", validators=[DataRequired()])
    surname = StringField("Фамилия", validators=[DataRequired()])
    can_view = BooleanField("Просмотр данных")
    can_add = BooleanField("Добавление данных")
    can_delete = BooleanField("Удаление данных")
    can_add_users = BooleanField("Добавление пользователей")
    submit = SubmitField("Добавить")


class ForgetPassword(FlaskForm):
    email = StringField("Почта")
    submit = SubmitField("Востановить")


class RenewPasswordWithCode(FlaskForm):
    code = StringField("Код в сообщение", validators=[DataRequired()])
    password = PasswordField("Новый пароль", validators=[DataRequired(),
                                                         Length(min=5, message="Пароль слишком короткий"),
                                                         EqualTo("password_repeat", message="Пароли не совпадают")])
    password_repeat = PasswordField("Подтвердите пароль", validators=[DataRequired()])
    submit = SubmitField("Обновить пароль")
