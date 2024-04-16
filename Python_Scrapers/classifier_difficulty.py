# NEED:
# parts / page
# paints / parts
#

# HAVE:
# scale score
def calculate_diff_score(parts, paints, num_pages, keywords, scale_score):
    params = [0.25, 0.25, 0.25, 0.25]
    unique_parts = set(parts)
    part_score = len(unique_parts) / num_pages
    paint_score = len(paints) / len(unique_parts)
    diff_score = params[0] * part_score + params[1] * paint_score + params[2] * scale_score + params[3] * len(keywords)
    return diff_score
