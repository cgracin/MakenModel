# pylint: disable=C0114
# pylint: disable=C0103
# pylint: disable=W0401
# pylint: disable=W0614

import os
import json
from classifier_paint_part import *
from text_preprocessor import *
from database_transfer import *



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


            # NOTE: This maps a unique_instruction_identifier to a unique_paint_identifer for all paints a model requires
            transfer_instruction_to_paint_database(path, paint_set)


if __name__ == "__main__":
    main()
