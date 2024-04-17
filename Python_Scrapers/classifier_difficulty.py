# NEED:
# parts / page
# paints / parts

# HAVE:
# scale score
def calculate_diff_score(parts, num_paints, num_pages, scale, naive_bayes_score):
    params = [0.25, 0.25, 0.25]
    num_parts = len(parts)
    parts_per_page = len(parts) / num_pages
    paints_per_part = num_paints / num_parts
    num_parts = num_parts
    scale_score = get_scale_score(scale)
    diff_score = params[0] * paints_per_part + params[1] * (paints_per_part * naive_bayes_score) + params[2] * scale_score

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