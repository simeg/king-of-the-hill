# -*- coding: utf-8 -*-
import config
import db
from flask import request, g, redirect, url_for, \
    render_template, flash, session

app = config.app


@app.cli.command('initdb')
def initdb_command():
    db.init_db()
    print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return handle_post_request(request)
    elif request.method == 'GET':
        return handle_get_request(request)


def handle_post_request(req):
    name = req.form['name']
    name = name.title()  # Capitalize all words (good for first and last name)
    user = db.get_user(name)
    session['block'] = None
    if user:  # User already exist
        # Set updated time for current leader
        active_user = db.get_active_user()
        db.update_user_time(active_user)
        # Deactivate current leader
        db.deactivate_user(active_user)
        # Active new user
        db.activate_user(user)
        # Set URL parameter
        session['block'] = True
    else:  # User is new
        if db.get_user_count() > 0:
            # Set old leader to inactive
            active_user = db.get_active_user()
            db.deactivate_user(active_user)
            # Update old leader's time
            db.update_user_time(active_user)
        # Add new user and set it to active
        db.add_active_user(name)
    return redirect(url_for('index'))


def handle_get_request(req):
    if db.get_user_count():
        active_user = db.get_active_user()
        block_param = session.get('block')
        if block_param is None:
            db.update_user_time(active_user)
        session['block'] = None
        return render_template('index.html', user=active_user, users=db.get_sorted_users())
    else:  # No user exist
        return render_template('index.html')
