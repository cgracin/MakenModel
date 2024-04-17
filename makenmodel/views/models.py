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
    user_paints = {row[0] for row in cur.fetchall()}

    print(user_paints)

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
            SELECT instructions.unique_instruction_identifier
            FROM instructions
        """)
        all_instruction_ids = [row[0] for row in instruction_query.fetchall()]

        for instruction_id in all_instruction_ids:
            paint_count_query = connection.execute("""
                SELECT COUNT(*) FROM instructions_to_paints
                WHERE unique_instruction_identifier = ?
            """, (instruction_id,))
            needed_paint_count = paint_count_query.fetchone()[0]

            matching_paint_query = connection.execute("""
                SELECT COUNT(*) FROM instructions_to_paints
                WHERE
                    unique_instruction_identifier = ? AND
                    unique_paint_identifier IN (SELECT unique_paint_identifier FROM user_paints WHERE username = ?)
            """, (instruction_id, logname))
            matching_paint_count = matching_paint_query.fetchone()[0]

            missing_paints = needed_paint_count - matching_paint_count

            if missing_paints > 3:
                model_identifiers_by_missing_count.setdefault('more', []).append(instruction_id)
            else:
                model_identifiers_by_missing_count[missing_paints].append(instruction_id)

        # If there are more than 20 models in the 'more' category, limit to the top 20.
        if 'more' in model_identifiers_by_missing_count and len(model_identifiers_by_missing_count['more']) > 20:
            model_identifiers_by_missing_count['more'] = model_identifiers_by_missing_count['more'][:20]

    context = {
        'logname': logname,
        'exact_match': model_identifiers_by_missing_count.get(0, []),
        'missing_one': model_identifiers_by_missing_count.get(1, []),
        'missing_two': model_identifiers_by_missing_count.get(2, []),
        'missing_three': model_identifiers_by_missing_count.get(3, []),
        'missing_more': model_identifiers_by_missing_count.get('more', [])
    }

    return flask.render_template('find_models.html', **context)