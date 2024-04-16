import json
from ftlangdetect import detect

# Returns string of all (mostly) english text from a JSON file
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