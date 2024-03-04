"""
MakenModel toolbox view

URLS include:
/toolbox
"""

import flask
import makenmodel

@makenmodel.app.route('/toolbox/overview/')
def show_toolbox():
    '''Renders the toolbox overview view'''

    logname = flask.session['username']

    connection = makenmodel.model.get_db()

    context = {}

    context['logname'] = logname
    context['active_page'] = 'overview'

    cur = connection.execute(
        "SELECT COUNT(*) AS paint_count "
        "FROM user_paints "
        "WHERE username = ?",
        (logname,)
    )
    paint_count = cur.fetchone()['paint_count']

    if paint_count:
        context['num_paints'] = paint_count
    else:
        context['num_paints'] = 0

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

    connection = makenmodel.model.get_db()

    logname = flask.session['username']

    context = {}

    context['logname'] = logname

    cur = connection.execute(
        "SELECT p.* FROM user_paints up "
        "JOIN paints p ON up.unique_paint_identifier = p.unique_paint_identifier "
        "WHERE up.username = ?",
        (logname,)
    )
    paint_details = cur.fetchall()
    context['paint_details'] = paint_details

    print(paint_details)

    return flask.render_template('your_paints.html', **context)


@makenmodel.app.route('/toolbox/add-paints/', methods=['POST'])
def add_paints():
    '''Route to add paint to database'''
    context = {}

    connection = makenmodel.model.get_db()

    logname = flask.session['username']
    context['logname'] = logname

    brand = flask.request.form['brand']
    paint_info = flask.request.form['paint']

    context['brand'] = brand

    # print(paint_info)
    paint_info = paint_info.split(' ')

    paint_code = paint_info[0]

    paint_type = paint_info[-1]

    paint_info.pop(0)
    paint_info.pop(-1)

    paint_name = (' ').join(paint_info)
    # slice off the ()
    paint_code = paint_code[1:-1]

    # slice off the ()
    paint_type = paint_type[1:-1]

    print(paint_code, paint_name, paint_type)

    if paint_type != 'null':
        cur = connection.execute(
            "SELECT unique_paint_identifier FROM paints "
            "WHERE brand = ? AND paint_code = ? AND paint_name = ? AND paint_type = ?",
            (brand, paint_code, paint_name, paint_type)
        )
    else:
        cur = connection.execute(
            "SELECT unique_paint_identifier FROM paints "
            "WHERE brand = ? AND paint_code = ? AND paint_name = ?",
            (brand, paint_code, paint_name)
        )

    identifier = cur.fetchone()['unique_paint_identifier']

    cur = connection.execute(
        "SELECT * FROM user_paints "
        "WHERE username = ? AND unique_paint_identifier = ?",
        (logname, identifier)
    )
    exists = cur.fetchone()

    if exists:
        context['repeat_color'] = "This paint is already in your collection!"

    # Inserting username and identifier into db
    connection.execute(
        "INSERT OR IGNORE INTO user_paints (username, unique_paint_identifier) "
        "VALUES (?, ?)",
        (logname, identifier)
    )
    connection.commit()

    if not exists:
        context['success_message'] = 'Paint added to your collection!'

    return flask.render_template('add_paints.html', **context)
