# NEED:
# parts / page
# paints / page
#

# HAVE:
# scale score
import json
from ftlangdetect import detect

# Returns string of all (mostly) english text from an instructions JSON file
def get_en_text(fname):
    with open(fname, 'r', encoding='utf-8') as js:
        text = json.load(js)
        text = text['text']
        en_lines = []
        text = text.split('\n')
        for line in text:
            nl = ''
            for word in line.split():
                if detect(text=word, low_memory=False)['lang'] not in ['ja', 'de', 'zh'] or word.isdigit():
                    nl += word + ' '
            en_lines.append(nl)
        return ' '.join([line.strip() for line in en_lines if line != ''])


def calculate_diff_score(parts, paints, num_pages, keywords, scale_score):
    params = [0.25, 0.25, 0.25, 0.25]
    unique_parts = set(parts)
    part_score = len(unique_parts) / num_pages
    paint_score = len(paints) / len(unique_parts)
    diff_score = params[0] * part_score + params[1] * paint_score + params[2] * scale_score + params[3] * len(keywords)
    return diff_score
