import sqlite3
import os


def update_password(email: str, password: str):
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    sql = f'UPDATE users SET password="{password}" WHERE email="{email}"'
    cur.execute(sql)
    conn.commit()
    conn.close()


def check_code(email: str, code: str) -> bool:
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    sql = f'SELECT code FROM forget_password WHERE email="{email}"'
    data = cur.execute(sql).fetchall()
    cur.close()
    conn.close()
    if data[0][0] == code:
        return True
    else:
        return False


def delete_last_code(email: str):
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    sql = f'DELETE FROM forget_password WHERE email="{email}"'
    cur.execute(sql)
    conn.commit()
    conn.close()


def add_code(email: str, code: str):
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    sql = f'INSERT INTO forget_password VALUES ("{email}", "{code}")'
    cur.execute(sql)
    conn.commit()
    conn.close()

# плохо работает
def chek_name__or_email(email: str) -> bool:
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    sql = f'SELECT * FROM users WHERE email="{email}"'
    data = cur.execute(sql).fetchall()
    cur.close()
    conn.close()
    if len(data) == 0:
        return False
    else:
        return data[0][6]


def all_users() -> list:
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    sql = "SELECT * FROM users"
    data = cur.execute(sql).fetchall()
    cur.close()
    conn.close()
    return data


def delete_user(email: str):
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    sql = f'DELETE FROM users WHERE email="{email}"'
    cur.execute(sql)
    cur.close()
    conn.commit()


def add_user(name: str, password: str, can_view: str, can_add: str, can_delete: str, can_add_users: str, email: str, real_name: str, surname: str):
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    sql = f'INSERT INTO users VALUES ("{name}", "{password}", "{can_view}", "{can_add}", "{can_delete}", "{can_add_users}", "{email}", "{real_name}", "{surname}")'
    cur.execute(sql)
    cur.close()
    conn.commit()


def users(username: str) -> list:
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    sql = 'SELECT * FROM users WHERE name="{}"'.format(username)
    data = cur.execute(sql).fetchall()
    cur.close()
    conn.close()
    return data


def delete_inventory(id: int):
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    sql = f'DELETE FROM inventory WHERE id="{id}"'
    cur.execute(sql)
    conn.commit()
    conn.close()


def from_db_order_by_category(category: str) -> list:
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    sql = 'SELECT * FROM inventory WHERE category="{}" OR categoryName="{}"'.format(category, category)
    data = cur.execute(sql).fetchall()
    cur.close()
    conn.close()
    return data


def from_db_order_by_place(place: str) -> list:
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    sql = 'SELECT * FROM inventory WHERE place="{}"'.format(place)
    print(sql)
    data = cur.execute(sql).fetchall()
    cur.close()
    conn.close()
    return data


def from_db() -> list:
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    data = cur.execute("SELECT *  FROM inventory").fetchall()
    cur.close()
    conn.close()
    return data


def to_db(category: str, categoryName: str, number: str, number_name: str, place: str):
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    cur.execute("INSERT INTO inventory VALUES (?, ?, ?, ?, ?, NULL)", (category, categoryName, number, number_name, place))
    conn.commit()
    conn.close()
