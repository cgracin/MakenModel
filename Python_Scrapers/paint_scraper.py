from bs4 import BeautifulSoup
import requests


# # This is Tamiya Paint Markers paint just to test that it works
# url = 'https://www.scalemates.com/colors/tamiya-paint-markers--841'

# Tamiya test url
url = 'https://www.scalemates.com/colors/tamiya--655'

page = requests.get(url)

soup = BeautifulSoup(page.text, features='html.parser')


output = []

divs = soup.find_all('div', class_='ac dg bgl cc pr mt4')

for div in divs:

    style_attr = div.find('div', style=True)
    background_color = style_attr['style'].split(':')[3] if style_attr else None

    paint_code = div.find('span', class_='bgb nw')
    paint_code = paint_code.text if paint_code else None

    a_tags = div.find_all('a')

    paint_color = None

    for a_tag in a_tags:

        span = a_tag.find('span')
        if span:
            paint_color = ''.join(text for text in a_tag.stripped_strings if text != span.get_text(strip=True))


    shine_type = div.find('div', class_='ccf center dib nw bgn')
    type_paint = div.find('div', class_='cct center dib nw bgg')

    if not type_paint:
        type_paint = div.find('div', class_='cct center dib nw bgb')

    shine_type = shine_type.text if shine_type else None
    type_paint = type_paint.text if type_paint else None

    output.append([paint_code, paint_color, background_color, shine_type, type_paint])


print(output)










# matching_links = soup.select('a[href^="/colors/"]')

# nums_to_colors = []

# matching_links = soup.find_all(lambda tag: tag.name == 'a' and tag.get('href', '').startswith('/colors/'))

# for link in matching_links:

#     a_text = ''.join(link.find_all(string=True, recursive=False)).strip()

#     if link.find('span'):

#         span_text = link.find('span').get_text(strip=True)

#         num_color_pair = (span_text, a_text)
#         nums_to_colors.append(num_color_pair)

# print(nums_to_colors)
