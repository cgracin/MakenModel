"""
MakenModel toolbox view

URLS include:
/toolbox
"""

import flask
import makenmodel

@makenmodel.app.route('/toolbox/overview/')
def show_toolbox():
    '''Renders the toolbox view'''

    logname = flask.session['username']

    context = {}

    context['logname'] = logname
    context['active_page'] = 'overview'

    return flask.render_template('toolbox.html', **context)


@makenmodel.app.route('/toolbox/add-paints/')
def show_add_paints():
    '''Shows the tab where users add paints to their collection'''

    logname = flask.session['username']

    context = {}

    context['logname'] = logname

    return flask.render_template('add_paints.html', **context)

@makenmodel.app.route('/toolbox/your-paints')
def show_your_paints():
    '''Shows the paints the user has in their collection'''

    logname = flask.session['username']

    context = {}

    context['logname'] = logname

    return flask.render_template('your_paints.html', **context)
