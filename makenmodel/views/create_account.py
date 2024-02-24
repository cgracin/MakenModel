"""
MakenModel create_account view

URLS include:
/create-account
"""

import flask
import makenmodel

@makenmodel.app.route('/create-account')
def show_create_account():

    context = {}

    return flask.render_template('create_account.html', **context)