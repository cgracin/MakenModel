# pylint: disable=C0114
# pylint: disable=C0103
# pylint: disable=W0401
#pylint: disable=W0614

import os
import json
import pathlib
import sqlite3
from classifier_paint_part import *
from classifier_language import *



EXTRACTED_JSON_FOLDER = "json_extracted"

def retrieve_json(file_path):
    """Retrieve JSON from files."""
    with open(file_path, "r", encoding="iso-8859-1") as file:
        try:
            json_file = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error retrieving JSON: {file_path}")
            print(f'Error Description {e}')
            return None
        return json_file

def get_info_from_json(json_pages):
    """Retrieve translated languages from JSON"""
    languages = set()
    num_pages = json_pages[-1]["pageNumber"]
    for pages in json_pages:
        if "detectedLanguages" in pages.keys():
            detected_langs = pages["detectedLanguages"]
            for lang in detected_langs:
                lang_code = lang["languageCode"]
                if lang_code != "en":
                    languages.add(lang_code)
    return languages, num_pages

def get_db():
    """Open a new database connection."""
    root_folder = pathlib.Path(__file__).resolve().parent.parent
    DATABASE_FILENAME = root_folder / "var" / "makenmodel.sqlite3"
    connection = sqlite3.connect(str(DATABASE_FILENAME))
    connection.row_factory = dict_factory
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def dict_factory(cursor, row):
    """Convert database row objects to a dictionary keyed on column name.

    This is useful for building dictionaries which are then used to render a
    template.  Note that this would be inefficient for large queries.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

def main():
    """Analyze extracted PDF text"""
    json_directory = os.listdir(EXTRACTED_JSON_FOLDER)
    instruction_texts = {}

    for file in json_directory:
        path = os.path.join(EXTRACTED_JSON_FOLDER, file)
        json_data = retrieve_json(path)
        if json_data:
            json_text = json_data["text"]
            text_langs, num_pages = get_info_from_json(json_data["pages"])

            paint_set, non_unique_paint_counter, item_parts, cleaned_list = get_parts_and_paints_from_instructions(json_text)

            # NOTE: paint_set = set of paints used in model
            # NOTE: non_unique_paint_counter = number of paints NOT UNIQUE
            # NOTE: item_parts = [set of all parts in instructions ] UNDERESTIMATE
            # NOTE: cleaned_list = [array of tokens of json_text without model_parts and paints ] NOT CLEANED
                # EXAMPLE: ['this', 'is', 'an', 'example']
            # processed_text = get_en_text(json_text, text_langs)


if __name__ == "__main__":
    main()
