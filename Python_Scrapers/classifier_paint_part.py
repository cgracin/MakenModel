import sys
import os
import json
import math
import re
import flask
import pathlib
import sqlite3

# pseudocode
# 1. Get user's colors
# 2. Get total colors from pdf
# 3. Calculate color score

SCRAPED_PAINT = "scraping_data/paint_scrape_data.json"
COLOR_CODES = []

def get_color_codes_json():
    """Getting color codes from JSON."""
    # Paints to grab: Tamiya, Tamiya Color Laqcuer Paint, Tamiya Paint Markers, Tamiya Polycarb Marker
    paints_grab_list = ["Tamiya", "Tamiya Color Lacquer Paint", "Tamiya Paint Markers", "Tamiya Polycarb Marker"]

    # Opening JSON file
    with open(os.path.join(SCRAPED_PAINT), "r", encoding="utf-8") as paint_data:
        data = json.load(paint_data)
    do_not_add = ["Light Earth", "Mud", "Sand"]
    color_codes = []
    for paint_type in paints_grab_list:
        for i in data[paint_type]:
            if i[0] not in do_not_add and not i[0].isdigit():
                color_codes.append(i[0])
    return color_codes


def get_parts_and_paints_from_instructions(pdf_text):

    pdf_text.replace('\n', ' ')
    split_pdf = pdf_text.split(' ')

    clean_text_list = [text.replace('\n', ' ').split() for text in split_pdf]

    flat_list = [item for sublist in clean_text_list for item in sublist]

    color_codes = get_color_codes_json()

    paint_codes_no_hyphen = [code.replace('-', '') for code in color_codes]

    non_unique_paint_counter = 0
    paint_set = set()
    without_codes = []

    for item in flat_list:
        copy_item = item.replace('-', '')
        copy_item = copy_item.replace('(', '')
        copy_item = copy_item.replace(')', '')


        if copy_item in paint_codes_no_hyphen:
            non_unique_paint_counter += 1
            item = item.replace('(', '')
            item = item.replace(')', '')
            paint_set.add(item)
        else:
            without_codes.append(item)

    pattern = re.compile(r'\b[A-Z]\d+\b')

    item_parts = []

    cleaned_list = []
    # Find all matches of the pattern in the list of strings.
    for item in without_codes:
    # Find all matches of the pattern in the current item.
        matches = pattern.findall(item)
        if matches:
            item_parts.extend(matches)  # Add the found item parts to the item_parts list.
            # Replace the found item parts with an empty string in the current item.
            cleaned_item = pattern.sub("", item).strip()
            if cleaned_item:  # If there is any non-matching text left, add it to the cleaned list.
                cleaned_list.append(cleaned_item)
        else:
            # If no item parts are found, add the item as it is to the cleaned list.
            cleaned_list.append(item)

    # print(paint_set, non_unique_paint_counter)
    # print(item_parts)
    # print(cleaned_list)

    return paint_set, non_unique_paint_counter, item_parts, cleaned_list


def dict_factory(cursor, row):
    """Convert database row objects to a dictionary keyed on column name.

    This is useful for building dictionaries which are then used to render a
    template.  Note that this would be inefficient for large queries.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def get_db():
    """Open a new database connection."""
    root_folder = pathlib.Path(__file__).resolve().parent.parent
    DATABASE_FILENAME = root_folder / "var" / "makenmodel.sqlite3"
    connection = sqlite3.connect(str(DATABASE_FILENAME))
    connection.row_factory = dict_factory
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

