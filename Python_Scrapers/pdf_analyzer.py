import sys
import os
import json
from classifier_paint_part import *
from text_preprocessor import *

EXTRACTED_JSON_FOLDER = "json_extracted"

def retrieve_json(file_path):
    """Retrieve JSON from files."""
    with open(file_path, "r", encoding="iso-8859-1") as file:
        try:
            json_file = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error retrieving JSON: {file_path}")
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

            processed_text = get_parts_and_paints_from_instructions(json_text)
            processed_text = get_en_text(json_text, text_langs)
            # text_tokens = 


if __name__ == "__main__":
    main()
