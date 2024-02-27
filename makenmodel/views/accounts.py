"""
MakenModel login view

URLS include:
/accounts/login
/accounts/create_account

"""

import flask
import makenmodel
import hashlib
import uuid
import pathlib
import os



@makenmodel.app.route('/accounts/login/')
def show_login():
    '''Shows login page'''
    context = {}

    return flask.render_template('login.html', **context)


@makenmodel.app.route('/accounts/create-account/')
def show_create_account():
    '''Shows create account page'''
    context = {}

    return flask.render_template('create_account.html', **context)


@makenmodel.app.route('/accounts/create-account/', methods=['POST'])
def create_account():
    '''This route accepts post requests and makes an account in the database'''

    connection = makenmodel.model.get_db()

    context = {}

    username = flask.request.form['username']
    email = flask.request.form['email']
    password = flask.request.form['password']
    verify_password = flask.request.form['verify_password']

    # Checking if user provided a profile picture
    if 'profile_pic_filename' in flask.request.files:
        profile_pic_filename = flask.request.files['profile_pic_filename'].filename
        context['profile_pic_filename'] = profile_pic_filename

    # TODO: remove this shit
    context['username'] = username
    context['password'] = password
    context['email'] = email
    context['verify_password'] = verify_password

    cur = connection.execute(
        "SELECT COUNT(*) AS count FROM users WHERE username = ?",
        (username,)
    )
    count = cur.fetchone()['count']

    if count > 0:
        context['username_error'] = 'Sorry, that username has already been taken'

    cur = connection.execute(
        "SELECT COUNT(*) AS count FROM users WHERE email = ?",
        (email,)
    )
    count = cur.fetchone()['count']

    if count > 0:
         context['email_error'] = 'You already have an account associated with that email'

    # If there are no conflicting emails or usernames in input
    if 'username_error' not in context and 'email_error' not in context:
        return flask.render_template('test.html', **context)

    # If there is a username or email conflict
    return flask.render_template('create_account.html', **context)
