"""
MakenModel login view

URLS include:
/login
"""

import flask
import makenmodel

@makenmodel.app.route('/login')
def show_login():
    '''Shows login page'''
    context = {}

    return flask.render_template('login.html', **context)
