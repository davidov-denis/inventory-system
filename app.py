from flask_mail import Mail, Message
from flask import *
from form import *
from db import *
import hashlib


app = Flask(__name__)
app.config["SECRET_KEY"] = "very-secret-key--no-one-can-know-it"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'denis150105ddd@gmail.com'  # введите свой адрес электронной почты здесь
app.config['MAIL_DEFAULT_SENDER'] = 'denis150105ddd@gmail.com'  # и здесь
app.config['MAIL_PASSWORD'] = '150105dd'  # введите пароль
mail = Mail(app)


def random_code():
    from random import randint
    alf = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code = ""
    for _ in range(6):
        code += alf[randint(0, 35)]
    return code


def is_auth():
    if "name" in session:
        return True
    else:
        return False


def delete_session():
    session.pop("name", None)
    session.pop("can_view", None)
    session.pop("can_add", None)
    session.pop("can_delete", None)
    session.pop("can_add_users", None)
    session.pop("email", None)
    session.pop("real_name", None)
    session.pop("surname", None)


def update_session(user):
    session.clear()
    session["name"] = user[0]
    session["can_view"] = user[2]
    session["can_add"] = user[3]
    session["can_delete"] = user[4]
    session["can_add_users"] = user[5]
    session["email"] = user[6]
    session["real_name"] = user[7]
    session["surname"] = user[8]


@app.route("/forget-password/active-code/<email>", methods=["post", "get"])
def active_code(email):
    form = RenewPasswordWithCode()
    if form.validate_on_submit():
        code = form.code.data
        password = hashlib.md5(str(form.password.data).encode())
        password = password.hexdigest()
        if check_code(email, code):
            update_password(email, password)
            return redirect("/")
        else:
            return render_template("/user/active-code.html", form=form, nocode=True)
        update_password(email, code, password)
    return render_template("/user/active-code.html", form=form, nocode=False)


@app.route("/forget-password/", methods=["post", "get"])
def forget_password():
    form = ForgetPassword()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        email = chek_name__or_email(name, email)
        if email:
            code = random_code()
            delete_last_code(email)
            add_code(email, code)
            msg = Message("Востановление пароля", recipients=[email])
            msg.html = f"<h1>{code}</h1>"
            mail.send(msg)
            return redirect("/forget-password/active-code/{}".format(email))
        else:
            return render_template("/user/forget_password.html", form=form, error=True)
    return render_template("/user/forget_password.html", form=form, error=False)


@app.route("/email/")
def email():
    msg = Message("Test", recipients=["denis150105ddd@yandex.ru"])
    msg.html = "<h1>Test</h1>"
    mail.send(msg)


# @app.route("/all-users/", methods=["get", "post"])
# def all_users():
#     data = all_users()
#     if request.method == "POST":
#         name = request.form.get("name")
#         delete_user(name)
#     return render_template("/user/all-users.html", data=data)


@app.route("/user/")
def user():
    if is_auth():
        return render_template("/user/user.html")
    else:
        return redirect("/login/")


@app.route("/register/", methods=["post", "get"])
def register():
    if is_auth():
        form = RegisterNewUser()
        if session.get("can_add_users") == "true":
            if form.validate_on_submit():
                name = form.name.data
                password = hashlib.md5(str(form.password.data).encode())
                password = password.hexdigest()
                can_view = "true" if form.can_view.data else "false"
                can_add = "true" if form.can_add.data else "false"
                can_delete = "true" if form.can_delete.data else "false"
                can_add_users = "true" if form.can_add_users.data else "false"
                email = form.email.data
                real_name = form.real_name.data
                surname = form.surname.data
                for i in all_users():
                    if i[0] == name or (i[8] == surname and i[7] == real_name):
                        return render_template("/user/register.html", form=form, user_added=True)
                add_user(name, password, can_view, can_add, can_delete, can_add_users, email, real_name, surname)
            return render_template("/user/register.html", form=form, user_added=False)
        else:
            render_template("non_privilege.html")
    else:
        return redirect("/login/")


@app.route("/logout/")
def logout():
    delete_session()
    return redirect("/login/")


@app.route("/", methods=["post", "get"])
@app.route("/login/", methods=["post", "get"])
def login():
    print(request.path)
    if is_auth():
        return redirect("/user/")
    else:
        form = CustomLoginForm()
        if form.validate_on_submit():
            name = form.name.data
            password = hashlib.md5(str(form.password.data).encode())
            password = password.hexdigest()
            user = users(username=name)[0]
            if len(user) == 0:
                return redirect("/login/")
            else:
                if user[1] == password:
                    update_session(user)
                    return redirect("/login/")
                else:
                    return redirect("/login/")
        return render_template("/user/login.html", form=form)


@app.route('/inventory/', methods=["get", "post"])
def inventory():
    if is_auth():
        form = InventoryForm()
        if session.get("can_add") == "true":
            if form.validate_on_submit():
                category = form.category.data
                categoryName = form.categoryName.data
                number = form.number.data
                number_name = form.number_name.data
                place = form.place.data
                to_db(category, categoryName, number, number_name, place)
                return redirect("/")
            else:
                return render_template("/inventory/index.html", form=form, title="Внесение данных")
        else:
            return render_template("non_privilege.html")
    else:
        return redirect("/login/")


@app.route("/inventory/view/")
def view_table():
    if is_auth():
        if session.get("can_view") == "true":
            data = from_db()
            empty = False
            if len(data) == 0:
                empty = True
            return render_template("/inventory/view/all.html", data=data, title="Просмотр всей таблицы", empty=empty)
        else:
            return render_template("non_privilege.html")
    else:
        return redirect("/login/")


@app.route("/inventory/view/order-by-place/<place>/")
def order_by_place(place):
    if is_auth():
        if session.get("can_view") == "true":
            empty = False
            data = from_db_order_by_place(place)
            if len(data) == 0:
                empty = True
            print(data)
            return render_template("/inventory/view/place.html", data=data, title="Инвентарь помещения {}".format(place), empty=empty)
        else:
            return render_template("non_privilege.html")
    else:
        return redirect("/login/")


@app.route("/inventory/view/order-by-category/<category>/")
def order_by_category(category):
    if is_auth():
        if session.get("can_view") == "true":
            empty = False
            data = from_db_order_by_category(category)
            if len(data)  == 0:
                empty = True
            return render_template("/inventory/view/category.html", data=data, title="Товары категории {}".format(category), empty=empty)
        else:
            return render_template("non_privilege.html")
    else:
        return redirect("/login/")


if __name__ == '__main__':
    app.run()
