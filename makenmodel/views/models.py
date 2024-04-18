"""
MakenModel find_models view

URLS include:

"""

import flask
import makenmodel


@makenmodel.app.route('/models/')
def show_find_models():
    logname = flask.session.get('username')


    context = {}

    context['logname'] = logname

    return flask.render_template('models.html', **context)


@makenmodel.app.route('/models/find/')
def find_model_identifiers_by_paint_availability():
    logname = flask.session.get('username')
    connection = makenmodel.model.get_db()

    cur = connection.execute(
        "SELECT unique_paint_identifier FROM user_paints "
        "WHERE username = ?",
        (logname,)
    )
    user_paints = [item['unique_paint_identifier'] for item in cur.fetchall()]

    model_identifiers_by_missing_count = {0: [], 1: [], 2: [], 3: []}

    if not user_paints:
        cur_more = connection.execute("""
            SELECT unique_instruction_identifier FROM instructions
            ORDER BY unique_instruction_identifier
            LIMIT 20
        """)
        model_identifiers_by_missing_count['more'] = cur_more.fetchall()
    else:
        instruction_query = connection.execute("""
            SELECT unique_instruction_identifier
            FROM instructions
        """)
        all_instruction_ids = [item['unique_instruction_identifier'] for item in instruction_query.fetchall()]

        for identifier in all_instruction_ids:
            cur = connection.execute(
                'SELECT unique_paint_identifier '
                'FROM instructions_to_paints '
                'WHERE unique_instruction_identifier = ?',
                (identifier,)
            )
            instruction_paints =  cur.fetchall()

            print(instruction_paints)
            break



    context = {
        'logname': logname,
        'exact_match': model_identifiers_by_missing_count.get(0, []),
        'missing_one': model_identifiers_by_missing_count.get(1, []),
        'missing_two': model_identifiers_by_missing_count.get(2, []),
        'missing_three': model_identifiers_by_missing_count.get(3, []),
        'missing_more': model_identifiers_by_missing_count.get('more', [])
    }

    return flask.render_template('find_models.html', **context)