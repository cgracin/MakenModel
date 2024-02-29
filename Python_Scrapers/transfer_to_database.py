import os
import sys
import sqlite3
import json


# pylint: disable=C0103

data_folder = 'scraping_data'

def get_db():
    db_folder = 'var'
    db_filename = 'makenmodel.sqlite3'

    db_filename = os.path.join(db_folder, db_filename)

    database = sqlite3.connect(str(db_filename))

    database.execute("PRAGMA foreign_keys = ON")

    return database



def transfer_paint_data():
    '''Transfers scraped paint info to database'''

    connection = get_db()

    print(data_folder)

    paint_filename = 'paint_scrape_data.json'

    paint_path = os.path.join(data_folder, paint_filename)

    with open(paint_path, 'r', encoding='utf-8') as data:
        paint_data = json.load(data)


    insert_query = '''
    INSERT INTO paints (brand, paint_name, paint_code, background_color, shine_type, paint_type)
    VALUES (?, ?, ?, ?, ?, ?);
    '''

    cursor = connection.cursor()

    for brand in paint_data.keys():
        cursor.execute("INSERT OR IGNORE INTO brands (brand) VALUES (?)", (brand,))


    for brand, paints in paint_data.items():
        for paint in paints:
            paint_code, paint_name, background_color, shine_type, paint_type = paint
            cursor.execute(
                "INSERT INTO paints(brand, paint_name, paint_code, background_color, shine_type, paint_type) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (brand, paint_name, paint_code, background_color, shine_type, paint_type)
                )

    connection.commit()


    if connection is not None:
        connection.close()


def main():

    function = sys.argv[1]


    if function == 'transfer_paint':
        transfer_paint_data()

    elif function == 'all':
        transfer_paint_data()


if __name__ == '__main__':
    main()
