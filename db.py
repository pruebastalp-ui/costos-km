import mysql.connector
from flask import g
from config import MYSQL_CONFIG

def get_db():
    if "db" not in g:
        g.db = mysql.connector.connect(**MYSQL_CONFIG)
    return g.db

def close_db(_=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def query_all(sql, params=None):
    cur = get_db().cursor(dictionary=True)
    cur.execute(sql, params or ())
    rows = cur.fetchall()
    cur.close()
    return rows

def query_one(sql, params=None):
    cur = get_db().cursor(dictionary=True)
    cur.execute(sql, params or ())
    row = cur.fetchone()
    cur.close()
    return row

def execute(sql, params=None):
    cur = get_db().cursor()
    cur.execute(sql, params or ())
    last_id = cur.lastrowid
    cur.close()
    return last_id

def executemany(sql, seq):
    cur = get_db().cursor()
    cur.executemany(sql, seq)
    cur.close()

def commit():
    get_db().commit()

def rollback():
    get_db().rollback()
