# NEED:
# parts / page
# paints / page
#

# HAVE:
# scale score

def calculate_diff_score(num_parts, num_paints, num_pages, scale_score):
    params = [0.45, 0.2, 0.35]
    part_score = num_parts / num_pages
    paint_score = num_paints / num_pages
    diff_score = params[0] * part_score + params[1] * paint_score + params[2] * scale_score
    return diff_score