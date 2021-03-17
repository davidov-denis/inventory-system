from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class InventoryForm(FlaskForm):
    category = StringField("Номер категории", validators=[DataRequired()])
    categoryName = StringField("Название категории", validators=[DataRequired()])
    number = StringField("Номер товара", validators=[DataRequired()])
    number_name = StringField("Название товара", validators=[DataRequired()])
    place = SelectField("Место", choices=[("Администратор", "Администратор"), ("Раздевалка", "Раздевалка"), ("Оранжевый класс", "Оранжевый класс"), ("Зелёный класс", "Зелёный класс"), ("Инженерный стелаж", "Инженерный стелаж")], validators=[DataRequired()])
    submit = SubmitField("Подтвердить")


class CustomLoginForm(FlaskForm):
    name = StringField("Имя пользователя", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")