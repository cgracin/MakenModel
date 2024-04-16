from ftlangdetect import detect
import json

# Returns string of all (mostly) english text from a JSON file
def get_en_text(pdf_text, langs):
    if len(langs) == 0:
        langs = ["ja", "de", "zh"]
        
    en_lines = []
    text = pdf_text.split('\n')
    for line in text:
        nl = ''
        for word in line.split():
            if detect(text=word, low_memory=False)['lang'] not in langs or word.isdigit():
                nl += word + ' '
        en_lines.append(nl)
    return ' '.join([line.strip() for line in en_lines if line != ''])
