"""
MakenModel index (main) view

URLS include:
/
"""

import flask
import arrow
import makenmodel


@makenmodel.app.route('/')
def show_index():
    '''Route for '/' url'''


    # TODO:
    # Redirect to login view if user is not logged in
    if not flask.session.get('username'):
        logged_in = False
        logname = ""

    elif flask.session.get('username'):
        logged_in = True
        logname = flask.session.get('username')


    context = {"logged_in": logged_in, "logname": logname}

    return flask.render_template("index.html", **context)
