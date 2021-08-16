import math

import matplotlib.pyplot as plt

mmkeypoints_ar = [
    [3.1721896e+02, 4.7955447e+02, 6.5885240e-01],
    [3.2307602e+02, 4.8541153e+02, 6.6802812e-01],
    [3.2307602e+02, 4.7955447e+02, 6.7749655e-01],
    [3.3479007e+02, 4.6784048e+02, 6.9285399e-01],
    [3.2893307e+02, 4.6784048e+02, 7.8769869e-01],
    [3.1136197e+02, 4.5026938e+02, 6.2045842e-01],
    [2.9964792e+02, 4.5612637e+02, 7.8962851e-01],
    [2.8793393e+02, 5.2055371e+02, 6.5508807e-01],
    [2.8793393e+02, 5.1469666e+02, 7.5310457e-01],
    [2.8793393e+02, 5.9669495e+02, 6.6400248e-01],
    [2.8793393e+02, 5.9669495e+02, 7.2509509e-01],
    [3.0550497e+02, 3.2141489e+02, 6.3775474e-01],
    [2.9964792e+02, 3.2727188e+02, 5.4493171e-01],
    [3.1136197e+02, 1.9256039e+02, 8.3411884e-01],
    [3.0550497e+02, 1.9256039e+02, 8.1357610e-01],
    [3.1136197e+02, 9.8847992e+01, 6.1659563e-01],
    [3.1136197e+02, 1.0470505e+02, 5.3114772e-01]
]
# d = {
#     'head0': ar[0],
#     'head1': ar[1],
#     'head2': ar[2],
#     'head3': ar[3],
#     'head4': ar[4],
#     'first_shoulder': ar[5],
#     'second_shoulder': ar[6],
#     'first_elbow': ar[7],
#     'second_elbow': ar[8],
#     'first_wrist': ar[9],
#     'second_wrist': ar[10],
#     'first_ass': ar[11],
#     'second_ass': ar[12],
#     'first_knee': ar[13],
#     'second_knee': ar[14],
#     'first_foot': ar[15],
#     'second_foot': ar[16],
# }
name_of_points = ['head0', 'head1', 'head2', 'head3', 'head4', 'first_shoulder', 'second_shoulder', 'first_elbow',
                  'second_elbow', 'first_wrist', 'second_wrist', 'first_ass', 'second_ass', 'first_knee', 'second_knee',
                  'first_foot', 'second_foot']
dict_of_points = {k: v for k, v in zip(name_of_points, mmkeypoints_ar)}

x = [point[0] for point in dict_of_points.values()]
y = [point[1] for point in dict_of_points.values()]
plt.plot(x, y, 'ro')
plt.axis([0, 900, 900, 0])


# for i_x, i_y in zip(x, y):
#     plt.text(i_x, i_y, '({}, {})'.format(i_x, i_y))
#
# for k, v in dict_of_points.items():
#     print(k, v)


def slope(x1, y1, x2, y2):  # Line slope given two points:
    return (y2 - y1) / (x2 - x1)


def angle(s1, s2):
    return round(math.degrees(math.atan((s2 - s1) / (1 + (s2 * s1)))), 2)


def accept180(angl, thresh):
    # Accept position if the angle is less than 180 degrees multiplied by accept_threshold
    if abs(angl) < thresh * 180:
        return True
    else:
        return False


accept_threshold = 0.10

lineA = ((dict_of_points['first_wrist'][0], dict_of_points['first_wrist'][1]),
         (dict_of_points['first_shoulder'][0], dict_of_points['first_shoulder'][1]))
lineB = (((dict_of_points['first_shoulder'][0], dict_of_points['first_shoulder'][1])),
         (dict_of_points['first_ass'][0], dict_of_points['first_ass'][1]))

slp1 = slope(lineA[0][0], lineA[0][1], lineA[1][0], lineA[1][1])
slp2 = slope(lineB[0][0], lineB[0][1], lineB[1][0], lineB[1][1])

ang = angle(slp1, slp2)
print(accept180(ang, accept_threshold))

# plt.show()
