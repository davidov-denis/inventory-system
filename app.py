from flask import *
from form import *
from db import *
import hashlib


app = Flask(__name__)
app.config["SECRET_KEY"] = "very-secret-key--no-one-can-know-it"


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


def update_session(user):
    session.clear()
    session["name"] = user[0]
    session["can_view"] = user[2]
    session["can_add"] = user[3]
    session["can_delete"] = user[4]
    session["can_add_users"] = user[5]


@app.route("/user/")
def user():
    if is_auth():
        return render_template("/user/user.html")
    else:
        return redirect("/login/")


@app.route("/register/", methods=["post", "get"])
def register():
    if is_auth() and session.get("can_add_users") == "true":
        form = RegisterNewUser()
        if form.validate_on_submit():
            name = form.name.data
            password = hashlib.md5(str(form.password.data).encode())
            password = password.hexdigest()
            can_view = "true" if form.can_view.data else "false"
            can_add = "true" if form.can_add.data else "false"
            can_delete = "true" if form.can_delete.data else "false"
            can_add_users = "true" if form.can_add_users.data else "false"
            add_user(name, password, can_view, can_add, can_delete, can_add_users)
        return render_template("/user/register.html", form=form)
    else:
        return redirect("/login/")


@app.route("/logout/")
def logout():
    delete_session()
    return redirect("/login/")


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
                print("нет пользователя")
            else:
                if user[1] == password:
                    update_session(user)
                    return redirect("/user/")
        return render_template("/user/login.html", form=form)


@app.route('/inventory/', methods=["get", "post"])
def inventory():
    if is_auth():
        form = InventoryForm()
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
        return redirect("/login/")


@app.route("/inventory/view/")
def view_table():
    if is_auth():
        data = from_db()
        empty = False
        if len(data) == 0:
            empty = True
        return render_template("/inventory/view/all.html", data=data, title="Просмотр всей таблицы", empty=empty)
    else:
        return redirect("/login/")


@app.route("/inventory/view/order-by-place/<place>/")
def order_by_place(place):
    if is_auth():
        empty = False
        data = from_db_order_by_place(place)
        if len(data) == 0:
            empty = True
        print(data)
        return render_template("/inventory/view/place.html", data=data, title="Инвентарь помещения {}".format(place), empty=empty)
    else:
        return redirect("/login/")


@app.route("/inventory/view/order-by-category/<category>/")
def order_by_category(category):
    if is_auth():
        empty = False
        data = from_db_order_by_category(category)
        if len(data)  == 0:
            empty = True
        return render_template("/inventory/view/category.html", data=data, title="Товары категории {}".format(category), empty=empty)
    else:
        return redirect("/login/")

if __name__ == '__main__':
    app.run()
