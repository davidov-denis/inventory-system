import sqlite3
import os

path_to_db = os.getcwd() + "\\db.sqlite"
print(path_to_db)


def all_users():
    conn = sqlite3.connect("D:\\inventory-system\\db.sqlite")
    cur = conn.cursor()
    sql = "SELECT * FROM users"
    data = cur.execute(sql).fetchall()
    cur.close()
    conn.close()
    return data


def delete_user(name):
    conn = sqlite3.connect("D:\\inventory-system\\db.sqlite")
    cur = conn.cursor()
    sql = f'DELETE FROM users WHERE name="{name}"'
    cur.execute(sql)
    cur.close()
    conn.commit()


def add_user(name, password, can_view, can_add, can_delete, can_add_users, email, real_name, surname):
    conn = sqlite3.connect("D:\\inventory-system\\db.sqlite")
    cur = conn.cursor()
    sql = f'INSERT INTO users VALUES ("{name}", "{password}", "{can_view}", "{can_add}", "{can_delete}", "{can_add_users}", "{email}", "{real_name}", "{surname}")'
    cur.execute(sql)
    cur.close()
    conn.commit()


def users(username):
    conn = sqlite3.connect("D:\\inventory-system\\db.sqlite")
    cur = conn.cursor()
    sql = 'SELECT * FROM users WHERE name="{}"'.format(username)
    data = cur.execute(sql).fetchall()
    cur.close()
    conn.close()
    return data


def from_db_order_by_category(category):
    conn = sqlite3.connect("D:\\inventory-system\\db.sqlite")
    cur = conn.cursor()
    sql = 'SELECT * FROM inventory WHERE category="{}" OR categoryName="{}"'.format(category, category)
    data = cur.execute(sql).fetchall()
    cur.close()
    conn.close()
    return data


def from_db_order_by_place(place):
    conn = sqlite3.connect("D:\\inventory-system\\db.sqlite")
    cur = conn.cursor()
    sql = 'SELECT * FROM inventory WHERE place="{}"'.format(place)
    print(sql)
    data = cur.execute(sql).fetchall()
    cur.close()
    conn.close()
    return data


def from_db():
    conn = sqlite3.connect("D:\\inventory-system\\db.sqlite")
    cur = conn.cursor()
    data = cur.execute("SELECT *  FROM inventory").fetchall()
    cur.close()
    conn.close()
    return data


def to_db(category, categoryName, number, number_name, place):
    conn = sqlite3.connect("D:\\inventory-system\\db.sqlite")
    cur = conn.cursor()
    cur.execute("INSERT INTO inventory VALUES (?, ?, ?, ?, ?)", (category, categoryName, number, number_name, place))
    conn.commit()
    conn.close()