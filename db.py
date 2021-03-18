import sqlite3


def users(username):
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    sql = 'SELECT name, password, can_view, can_add, can_delete, can_add_users FROM users WHERE name="{}"'.format(username)
    data = cur.execute(sql).fetchall()
    cur.close()
    conn.close()
    return data


def from_db_order_by_category(category):
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    sql = 'SELECT * FROM inventory WHERE category="{}" OR categoryName="{}"'.format(category, category)
    data = cur.execute(sql).fetchall()
    cur.close()
    conn.close()
    return data


def from_db_order_by_place(place):
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    sql = 'SELECT * FROM inventory WHERE place="{}"'.format(place)
    print(sql)
    data = cur.execute(sql).fetchall()
    cur.close()
    conn.close()
    return data


def from_db():
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    data = cur.execute("SELECT *  FROM inventory").fetchall()
    cur.close()
    conn.close()
    return data


def to_db(category, categoryName, number, number_name, place):
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    cur.execute("INSERT INTO inventory VALUES (?, ?, ?, ?, ?)", (category, categoryName, number, number_name, place))
    conn.commit()
    conn.close()