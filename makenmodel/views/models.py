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

    model_identifiers_by_missing_count = {0: [], 1: [], 2: [], 3: [], 'more': []}

    missing_dict = {}

    if not user_paints:
        cur_more = connection.execute("""
            SELECT unique_instruction_identifier FROM instructions
            ORDER BY unique_instruction_identifier
            LIMIT 20
        """)
        model_identifiers_by_missing_count['more'] = cur_more.fetchall()
    else:
        model_set = set()

        for paint_id in user_paints:
        # Fetch all instruction identifiers that use the paint
            cur = connection.execute(
                "SELECT unique_instruction_identifier FROM instructions_to_paints WHERE unique_paint_identifier = ?",
                (paint_id,)
            )
            # Add each instruction identifier to the set to ensure uniqueness
            paint_models = {item['unique_instruction_identifier'] for item in cur.fetchall()}
            model_set.update(paint_models)


        for model in model_set:
            missing_dict[model] = 0

        for model in missing_dict:
            cur = connection.execute(
                "SELECT unique_paint_identifier "
                "FROM instructions_to_paints "
                "WHERE unique_instruction_identifier = ?",
                (model,)
            )
            all_paints = [row['unique_paint_identifier'] for row in cur.fetchall()]

            for paint_id in all_paints:
                if paint_id not in user_paints:
                    missing_dict[model] = missing_dict.get(model, 0) + 1

    for model, num_missing in missing_dict.items():
        if num_missing == 0:
            model_identifiers_by_missing_count[0].append(model)
        if num_missing == 1:
            model_identifiers_by_missing_count[1].append(model)
        if num_missing == 2:
            model_identifiers_by_missing_count[2].append(model)
        if num_missing == 3:
            model_identifiers_by_missing_count[3].append(model)
        if num_missing > 3:
            model_identifiers_by_missing_count['more'].append(model)


    context = {
        'logname': logname,
        'exact_match': model_identifiers_by_missing_count.get(0, []),
        'missing_one': model_identifiers_by_missing_count.get(1, []),
        'missing_two': model_identifiers_by_missing_count.get(2, []),
        'missing_three': model_identifiers_by_missing_count.get(3, []),
        'missing_more': model_identifiers_by_missing_count.get('more', [])
    }

    return flask.render_template('find_models.html', **context)