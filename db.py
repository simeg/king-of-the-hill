# -*- coding: utf-8 -*-
import time
import config
from flask import g
from sqlite3 import dbapi2 as sqlite3

app = config.app


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def update_user_time(user):
    user_last_active = int(user.__getitem__('last_active'))
    epoch_time = int(time.time())
    difference = int(epoch_time - user_last_active)

    # Set updated seconds to user
    conn = get_db()
    conn.execute('UPDATE users SET seconds = ? WHERE name = ?', [difference, user.__getitem__('name')])
    conn.commit()


def deactivate_user(user):
    name = user.__getitem__('name')
    conn = get_db()
    conn.execute('UPDATE users SET active = ? WHERE name = ?', [False, name])
    conn.commit()


def activate_user(user):
    name = user.__getitem__('name')
    conn = get_db()
    conn.execute('UPDATE users SET active = ? WHERE name = ?', [True, name])
    conn.commit()


def get_active_user():
    conn = get_db()
    cur = conn.execute('SELECT * FROM users WHERE active = ?', [True])
    return cur.fetchone()


def add_active_user(name):
    last_active_time = int(time.time())
    conn = get_db()
    conn.execute('INSERT INTO users (name, seconds, active, last_active) VALUES (?, ?, ?, ?)',
               [name, 0, True, last_active_time])
    conn.commit()
    cur = conn.execute('SELECT * FROM users ORDER BY id DESC LIMIT 1')
    return cur.fetchone()


def get_sorted_users():
    conn = get_db()
    cur = conn.execute('SELECT * FROM users ORDER BY seconds desc')
    return cur.fetchall()


def get_user_count():
    conn = get_db()
    cur = conn.execute('SELECT count(*) FROM users')
    return cur.fetchone()[0]


def get_user(name):
    conn = get_db()
    cur = conn.execute('SELECT * FROM users WHERE name = ?', [name])
    return cur.fetchone()
