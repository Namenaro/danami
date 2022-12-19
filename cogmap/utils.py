from common_utils import Point

import numpy as np

def get_coords_for_radius(center, radius):
    #|x|+|y|=radius ->  |y|=radius-|x|
    # x>0  -> y1 = radius-|x|
    if radius == 0:
        return [Point(center.x, center.y)]

    points = []
    for modx in range(0, radius+1):
        mody = radius - modx
        # x>0
        if modx != 0 and mody != 0:
            points.append(Point(modx + center.x, mody + center.y))
            points.append(Point(-modx + center.x, mody + center.y))
            points.append(Point(modx + center.x, -mody + center.y))
            points.append(Point(-modx + center.x, -mody + center.y))

        if modx == 0 and mody != 0:
            points.append(Point(modx+center.x, mody+center.y))
            points.append(Point(modx + center.x, -mody + center.y))

        if modx != 0 and mody == 0:
            points.append(Point(modx+center.x, mody+center.y))
            points.append(Point(-modx + center.x, mody + center.y))
    return points

def sense_1(point, picture):
    xlen = picture.shape[1]
    ylen = picture.shape[0]
    if point.x >= 0 and point.y >= 0 and point.x < xlen and point.y < ylen:
        val = picture[point.y, point.x]
        if val > 0:
            return True
    return False

def get_all_1_points(img):
    all_1_points=[]
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            point = Point(x,y)
            if sense_1(point, img):
                all_1_points.append(point)
    return all_1_points

def try_qrow_seq_of_points_with_u(start_point, binary_img, u, max_rad):
    if sense_1(start_point, binary_img) is False:
        return []
    seq_of_points = [start_point]
    last_point = start_point
    while True:
        next_expected_point = Point(x=last_point.x + u.x, y=last_point.y + u.y)
        next_real_point = find_nearest_1_with_exclusions(next_expected_point, binary_img, max_rad, exclusions=seq_of_points)
        if next_real_point is None:
            break
        seq_of_points.append(next_real_point)
        last_point = next_real_point
    # обратный проход
    u = get_backward_dir(u)
    last_point = seq_of_points[0]
    while True:
        next_expected_point = Point(x=last_point.x + u.x, y=last_point.y + u.y)
        next_real_point = find_nearest_1_with_exclusions(next_expected_point, binary_img, max_rad, exclusions=seq_of_points)
        if next_real_point is None:
            break
        seq_of_points.insert(0, next_real_point)
        last_point = next_real_point
    return seq_of_points


def remove_dubles(seqs_list):
    indexes_to_remove=set()
    for i in range(len(seqs_list)):
        for j in range(i+1, len(seqs_list)):
            if are_dubles(seqs_list[i], seqs_list[j]):
                indexes_to_remove.add(i)
                break
    new_seq_list = []
    for i in range(len(seqs_list)):
        if i not in indexes_to_remove:
            new_seq_list.append(seqs_list[i])
    return new_seq_list


def are_dubles(seq1, seq2):
    num_of_common_elements = 0
    for elt1 in seq1:
        for elt2 in seq2:
            if elt1 == elt2:
                num_of_common_elements +=1
                break
    max_len = max(len(seq1), len(seq2))
    diff = max_len - num_of_common_elements
    if num_of_common_elements>diff: # общего больше, чем разного (эвристика)
        #print("duble found")
        return True
    return False

def find_nearest_1(start_point, binary_img, max_rad):
    for r in range(1, max_rad):
        r_points = get_coords_for_radius(start_point, r)
        for point in r_points:
            if sense_1(picture=binary_img, point=point):
                return point
    return None

def find_nearest_1_with_exclusions(start_point, binary_img, max_rad, exclusions):
    for r in range(0, int(max_rad)):
        r_points = get_coords_for_radius(start_point, r)
        for point in r_points:
            if sense_1(picture=binary_img, point=point):
                if is_allowed_by_exclusions(start_point, point, exclusions):
                    return point
    return None

def is_allowed_by_exclusions(prev_point, candidate_point,  exclusions):
    dist = prev_point.dist_to( candidate_point)
    for exclusion in exclusions:
        if exclusion.dist_to( candidate_point) < dist:
            return False
    return True

def get_backward_dir(dir):
    bdir = Point(0,0)
    if dir.x!=0:
        bdir.x=-dir.x
    if dir.y!=0:
        bdir.y=-dir.y
    return bdir

def remove_points_from_list(points_list, points_to_remove):
    for point in points_to_remove:
        if point in points_list:
            points_list.remove(point)



def seqs_starts_to_binary_map(map_shape, seqs):
    binary_map = np.zeros(map_shape)
    for seq in seqs:
        point = seq[0]
        binary_map[point.y, point.x] = 1
    return binary_map
