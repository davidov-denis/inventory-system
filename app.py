from flask import *
from form import *
from db import *
import hashlib


app = Flask(__name__)
app.config["SECRET_KEY"] = "very-secret-key--no-one-can-know-it"

@app.route("/login/")
def login():
    form = CustomLoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = hashlib.md5(form.password.data)
        if users(username=name) == 0:
            print("No")
        else:
            print("YES")
    return pass


@app.route('/inventory/', methods=["get", "post"])
def index():
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


@app.route("/inventory/view/")
def view_table():
    data = from_db()
    empty = False
    if len(data) == 0:
        empty = True
    return render_template("/inventory/view/all.html", data=data, title="Просмотр всей таблицы", empty=empty)


@app.route("/inventory/view/order-by-place/<place>/")
def order_by_place(place):
    empty = False
    data = from_db_order_by_place(place)
    if len(data) == 0:
        empty = True
    print(data)
    return render_template("/inventory/view/place.html", data=data, title="Инвентарь помещения {}".format(place), empty=empty)


@app.route("/inventory/view/order-by-category/<category>/")
def order_by_category(category):
    empty = False
    data = from_db_order_by_category(category)
    if len(data)  == 0:
        empty = True
    return render_template("/inventory/view/category.html", data=data, title="Товары категории {}".format(category), empty=empty)


if __name__ == '__main__':
    app.run()
