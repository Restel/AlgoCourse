import sys
import math
# load input


from collections import namedtuple
import random


def clockwiseangle(point, origin):
    """

    :param point: is a list of x,y coordinates
    :param origin: pivot point
    :return:
    """
    refvec = [0, 1]
    # Vector between point and the origin: v = p - o
    vector = [point[0]-origin[0], point[1]-origin[1]]
    # Length of vector: ||v||
    lenvector = math.hypot(vector[0], vector[1])
    # If length is zero there is no angle
    if lenvector == 0:
        return 0,0
    # Normalize vector: v/||v||
    normalized = [vector[0]/lenvector, vector[1]/lenvector]
    dotprod  = normalized[0]*refvec[0] + normalized[1]*refvec[1]
    diffprod = refvec[1]*normalized[0] - refvec[0]*normalized[1]
    angle = math.atan2(diffprod, dotprod)
    if angle < 0:
        return 2*math.pi+angle, lenvector
    return angle, lenvector

def data():
    str = sys.stdin.readline()
    N = str.split("\n")[0]
    N = int(N)
    crd = []
    for i in range(N):
        char_x, _ = sys.stdin.readline().split("\n")
        char_crd = char_x.split(" ")
        #int_x = int(char_x)
        crd.append([i, int(char_crd[0]), int(char_crd[1])])
        #print(int_x)
    #print(crd)
    return N, crd

def slope(x1, y1, x2, y2): # Line slope given two points:
    #print(x1, y1, x2, y2)
    if x2 != x1:
        return (y2-y1)/(x2-x1)
    else:
        return 0

def angle(s1):
    """
    computes the angle between the vertical line and a line with slope s1
    :param s1:
    :return: an float angle in degrees
    """
    if s1 == 0:
        return 90.0
    else:
        return math.degrees(math.atan(abs(1/s1)))

# lineA = ((0.6, 3.6), (1.6, 3))
# lineB = ((1.6, 3), (2, 3.6))
#
# slope1 = slope(lineA[0][0], lineA[0][1], lineA[1][0], lineA[1][1])
# slope2 = slope(lineB[0][0], lineB[0][1], lineB[1][0], lineB[1][1])
#
# ang = angle(slope1, slope2)

def sort_points_by_angle(crd, N, pivot):
    """
    The function sorts all points by increasing angle between lines drawn from pivot to a point and from a pivot vertically up
    :pre:
    :pos:
    :param crd: a list of lists, where each element is  id,x,y coordinates of a point
    :param N: the number of points
    :param pivot: id of a pivot coordinate, [0, N-1]
    :return: a list with id of points sorted by the angle
    """
    max_y = 10000
    angles = []
    for i in range(N):
        if (crd[i][0] == crd[pivot][0]):
            continue
        slope_i = slope(crd[pivot][1], crd[pivot][2], crd[i][1], crd[i][2])
        #print(slope_i)
        angle_i = angle(slope_i)
        #print("Angle of ", i, " is ", angle_i)
        angles.append((i, angle_i))
    angles = sorted(angles, key = lambda k: k[1])
    sorted_id = [i[0] for i in angles]
    return(sorted_id)


def convex_hull(crd, N):
    """

    :param crd: a list of lists, where each element is  id,x,y coordinates of a point
    :param N: the number of points
    :return: a list of points that form a convex hull
    """
    initial = 0
    sorted_id = sort_points_by_angle(crd, N, initial)
    print(sorted_id)
    convex_hull = []
    pivot = sorted_id[0]
    while initial != pivot:
        convex_hull.append(pivot)
        sorted_id = sort_points_by_angle(crd, N, pivot)
        print(sorted_id)
        pivot = sorted_id[0]
        print("next point", pivot)
    print("Convex Hull:", convex_hull)

def find_unique_allocations(set):
    unique_data = [list(x) for x in set(tuple(x) for x in set)]
    return(unique_data)

def main():
    N, crd = data()
    allocations = []
    Lily_alloc = []
    for i in range(N):
        origin = crd[i][1:3]
        sorted_items = sorted(crd, key=lambda k: clockwiseangle(k[1:3], origin))
        #for j in range(N):
         #   print("Point", crd[j][1:3], "has angle ", clockwiseangle(crd[j][1:3], origin))
        Lily = sorted_items[0:N//2]
        Lily = [elem[0] for elem in Lily]
        Lily = frozenset(tuple(Lily))
        Lily_alloc.append(Lily)

        #print("Origin", origin, "sorted", sorted(crd, key = lambda k: clockwiseangle(k[1:3], origin)))
        allocations.append(sorted(crd, key = lambda k: clockwiseangle(k[1:3], origin)))
    Lily_alloc = list(Lily_alloc)
    print(len(Lily_alloc))
main()