# NEED:
# parts / page
# paints / parts

# HAVE:
# scale score
def calculate_diff_score(parts, paints, num_pages, keywords, scale_score):
    params = [0.25, 0.25, 0.25, 0.25]
    unique_parts = set(parts)
    part_score = len(unique_parts) / num_pages
    paint_score = len(paints) / len(unique_parts)
    diff_score = params[0] * part_score + params[1] * paint_score + params[2] * scale_score + params[3] * len(keywords)
    return diff_score

def get_scale_score(scale):
    ratings = {}
    with open('../data/scale_ratings.txt', 'r', encoding='utf-8') as fin:
        for line in fin.readlines():
            line = line.split()
            ratings[line[0]] = float(line[1])
    known_scales = ratings.keys()
    # If model scale is not in our list, find the closest existing scale
    if ':' in scale:
        if scale not in ratings.keys() and scale.split(':')[1].isdigit():
            scale_denom = int(scale.split(':')[1])
            closest_scale_key = ''
            closest_scale_val = 999

            for key in known_scales:
                curr_diff = abs(scale_denom - int(key.split(':')[1]))
                if curr_diff < closest_scale_val:
                    closest_scale_key = key
                    closest_scale_val = curr_diff
            scale = closest_scale_key

    return ratings.get(scale, 0.5)
