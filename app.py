from flask_mail import Mail, Message
from config import *
from flask import *
from form import *
from db import *
import hashlib

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
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


@app.route("/all-users/")
def all_users_view():
    if is_auth():
        print(session["name"])
        data = all_users()
        return render_template("/user/all.html", data=data)
    else:
        return redirect("/")


@app.route("/delete-user/<email>/")
def delete_user_view(email):
    if is_auth():
        delete_user(email)
        return redirect("/all-users/")
    else:
        return redirect("/")


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



@app.route("/user/", methods=["post", "get"])
def user():
    if is_auth():
        form = UserUpdateInfo()
        if form.validate_on_submit():
            password = hashlib.md5(str(form.new_password.data).encode())
            password = password.hexdigest()
            email = session.get("email")
            update_password(email, password)
            return redirect("/logout/")
        return render_template("/user/user.html", form=form)
    else:
        return redirect("/login/")


@app.route("/register/", methods=["post", "get"])
def register():
    if is_auth():
        if session.get("can_add_users") == "true":
            form = RegisterNewUser()
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
            abort(302)
    else:
        return redirect("/login/")


@app.route("/logout/")
def logout():
    delete_session()
    return redirect("/login/")


@app.route("/", methods=["post", "get"])
@app.route("/login/", methods=["post", "get"])
def login():
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
            return render_template("/inventory/index.html", form=form, title="Внесение данных")
    else:
        return redirect("/login/")


@app.route("/inventory/delete/<id>", methods=["post", "get"])
def delete_inventory_view(id: int):
    if is_auth():
        id = int(id)
        delete_inventory(id)
        return redirect("/inventory/view")
    else:
        return redirect("/")


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
            return render_template("/inventory/view/place.html", data=data,
                                   title="Инвентарь помещения {}".format(place), empty=empty)
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
            if len(data) == 0:
                empty = True
            return render_template("/inventory/view/category.html", data=data,
                                   title="Товары категории {}".format(category), empty=empty)
        else:
            return render_template("non_privilege.html")
    else:
        return redirect("/login/")


if __name__ == '__main__':
    app.run()
