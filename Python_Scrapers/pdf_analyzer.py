# pylint: disable=C0114
# pylint: disable=C0103
# pylint: disable=W0401
# pylint: disable=W0614

import os
import json
from classifier_paint_part import *
from text_preprocessor import *
from database_transfer import *
import csv

EXTRACTED_JSON_FOLDER = "json_extracted/"


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
    folder_path = ["easy", "medium", "hard"]
    for f_path in folder_path:
        path = os.path.join(EXTRACTED_JSON_FOLDER, f_path)
        json_directory = os.listdir(path)
        id_text = []
        for json_path in json_directory:
            json_path2 = os.path.join(path, json_path)
            json_data = retrieve_json(json_path2)
            if json_data:
                json_text = json_data["text"]
                text_langs, num_pages = get_info_from_json(json_data["pages"])

                paint_set, non_unique_paint_counter, item_parts, cleaned_list = get_parts_and_paints_from_instructions(
                    json_text)
                # NOTE: paint_set = set of paints used in model
                # NOTE: non_unique_paint_counter = number of paints NOT UNIQUE
                # NOTE: item_parts = [set of all parts in instructions ] UNDERESTIMATE
                # NOTE: cleaned_list = [array of tokens of json_text without model_parts and paints ] NOT CLEANED
                # EXAMPLE: ['this', 'is', 'an', 'example']
                processed_text = get_en_text(cleaned_list, text_langs)

                json_id = json_path[:-5]
                id_text.append({"ID": json_id, "TEXT": processed_text})
                # print(id_text)
            # print(id_text)
            # field names
            fields = ['ID', 'TEXT']

            # name of csv file
            filename = f"{f_path}_vocab.csv"

            # writing to csv file
            with open(filename, 'w') as csvfile:
                # creating a csv dict writer object
                writer = csv.DictWriter(csvfile, fieldnames=fields)

                # writing headers (field names)
                writer.writeheader()

                # writing data rows
                writer.writerows(id_text)

            # NOTE: This maps a unique_instruction_identifier to a unique_paint_identifer for all paints a model requires
            transfer_instruction_to_paint_database(path, paint_set)


if __name__ == "__main__":
    main()