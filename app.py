from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)


def to_db(category, categoryName, number, name, quality, place):
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    cur.execute("INSERT INTO inventory VALUES (?, ?, ?, ?, ?, ?)", (category, categoryName, number, name, quality, place))
    conn.commit()
    conn.close()


def check(category, categoryName, number, name, quality, place):
    if category == "" or categoryName == "" or number == "" or name == "" or quality == "" or place == "":
        return False
    else:
        return True


@app.route('/', methods=["get", "post"])
def index():
    if request.method == "POST":
        category = request.form.get("category")
        categoryName = request.form.get("categoryName")
        number = request.form.get("number")
        name = request.form.get("name")
        quality = request.form.get("quality")
        place = request.form.get("place")
        if check(category, categoryName, number, name, quality, place):
            print("OK")
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
