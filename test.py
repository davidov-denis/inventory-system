import sqlite3


conn = sqlite3.connect("db.sqlite")
cur = conn.cursor()
a = cur.execute("SELECT category, categoryName, number, name, place FROM inventory").fetchall()
cur.close()
conn.close()
print(a)