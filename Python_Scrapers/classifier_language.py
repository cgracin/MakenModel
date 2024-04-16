from ftlangdetect import detect
import json

# Returns string of all (mostly) english text from a JSON file
def get_en_text(pdf_text, langs):
    en_lines = []
    text = pdf_text.split('\n')
    for line in text:
        nl = ''
        for word in line.split():
            print(detect(text=word, low_memory=False)["lang"])
            if detect(text=word, low_memory=False)['lang'] not in langs or word.isdigit():
                nl += word + ' '
        en_lines.append(nl)
    return ' '.join([line.strip() for line in en_lines if line != ''])
