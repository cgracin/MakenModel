import sys
import os
import json
import math
import re

# pseudocode
# 1. Get user's colors
# 2. Get total colors from pdf
# 3. Calculate color score


def main():
    """Getting color codes to clean pdfs."""
    # Paints to grab: Tamiya, Tamiya Color Laqcuer Paint, Tamiya Paint Markers, Tamiya Polycarb Marker
    paints_grab_list = ["Tamiya", "Tamiya Color Lacquer Paint", "Tamiya Paint Markers", "Tamiya Polycarb Marker"]
    # Opening JSON file
    with open(os.path.join('scraping_data/paint_scrape_data.json'), 'r', encoding='UTF-8') as paint_data:
        data = json.load(paint_data)
        color_codes = get_color_codes_json(data, paints_grab_list)
        #print(color_codes)

    instruction_folder = "pdf_texts"

    get_parts_and_paints_from_instructions()

    return None

def get_color_codes_json(data, paint_types):
    """Getting color codes from Json."""
    do_not_add = ['Light Earth', 'Mud', 'Sand']
    color_codes =[]
    for paint_type in paint_types:
        for i in data[paint_type]:
            if i[0] not in do_not_add and not i[0].isdigit():
                color_codes.append(i[0])
    return color_codes



def get_parts_and_paints_from_instructions():
    directory = "pdf_texts"

    files = os.listdir(directory)

    for file in files:

        path = os.path.join(directory, file)

        with open(path, 'r', encoding='utf-8') as open_file:
            text = open_file.read()

        pattern = r'\b[A-Za-z]{1}[A-Za-z]-?\d+\b'

        # Find all matches of the pattern in the text
        matches = re.findall(pattern, text)

        print(path, matches)


if __name__ == "__main__":
    main()