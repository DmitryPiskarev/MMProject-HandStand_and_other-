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

name_of_points = ['head0', 'head1', 'head2', 'head3', 'head4', 'first_shoulder', 'second_shoulder', 'first_elbow',
                  'second_elbow', 'first_wrist', 'second_wrist', 'first_ass', 'second_ass', 'first_knee', 'second_knee',
                  'first_foot', 'second_foot']
dict_of_points = {k: v for k, v in zip(name_of_points, mmkeypoints_ar)}

x = [point[0] for point in dict_of_points.values()]
y = [point[1] for point in dict_of_points.values()]
plt.plot(x, y, 'ro')
plt.axis([0, 900, 900, 0])


# plt.show()

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


def get_angle_res(f_point, s_point, t_point, func, accept_threshold=0.10):
    slp1 = slope(f_point[0], f_point[1], s_point[0], s_point[1])
    slp2 = slope(s_point[0], s_point[1], t_point[0], t_point[1])
    return func((angle(slp1, slp2)), accept_threshold)


print(get_angle_res(dict_of_points['first_wrist'], dict_of_points['first_shoulder'], dict_of_points['first_ass'],
                    accept180))
