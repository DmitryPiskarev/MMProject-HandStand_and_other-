import math

import matplotlib.pyplot as plt

mmkeypoints_ar = [
    [73.630104, 171.40439, 0.8898602],
    [71.989296, 168.12277, 0.91372955],
    [70.34849, 168.12277, 0.88910663],
    [76.911705, 163.20035, 0.86160445],
    [70.34849, 161.55954, 0.58128905],
    [88.39736, 156.63712, 0.81900513],
    [83.47494, 153.3555, 0.5691762],
    [93.319786, 179.60843, 0.8689313],
    [86.75655, 174.686, 0.32007766],
    [78.55251, 181.24924, 0.44380537],
    [75.27091, 176.32681, 0.47355014],
    [96.6014, 122.18018, 0.63075316],
    [88.39736, 117.25776, 0.7483829],
    [90.03817, 81.159996, 0.62998295],
    [90.03817, 81.159996, 0.719999],
    [86.75655, 41.780617, 0.46977988],
    [88.39736, 41.780617, 0.48423153]
]

name_of_points = ['head0', 'head1', 'head2', 'head3', 'head4', 'first_shoulder', 'second_shoulder', 'first_elbow',
                  'second_elbow', 'first_wrist', 'second_wrist', 'first_ass', 'second_ass', 'first_knee', 'second_knee',
                  'first_foot', 'second_foot']
dict_of_points = {k: v for k, v in zip(name_of_points, mmkeypoints_ar)}

x = [point[0] for point in dict_of_points.values()]
y = [point[1] for point in dict_of_points.values()]
plt.plot(x, y, 'ro')
plt.axis([0, 900, 900, 0])


def slope(x1, y1, x2, y2):  # Line slope given two points:
    a = y2 - y1
    b = x2 - x1
    if b != 0:
        return a / b
    else:
        return 0


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


ac_thr_w_e_s = 0.4
ac_thr_a_k_f = 0.5
ac_thr_w_s_k = 0.5
if len(mmkeypoints_ar) == 17:
    print(
        f"угол кисти  локти плечи  {get_angle_res(dict_of_points['first_wrist'], dict_of_points['first_elbow'], dict_of_points['first_shoulder'], accept180, ac_thr_w_e_s)}")
    print(
        f" угол кисти плечи таз {get_angle_res(dict_of_points['first_wrist'], dict_of_points['first_shoulder'], dict_of_points['first_ass'], accept180)}")
    print(
        f" угол кисти плечи коленки {get_angle_res(dict_of_points['first_wrist'], dict_of_points['first_ass'], dict_of_points['first_knee'], accept180, ac_thr_w_s_k)}")
    print(
        f" угол плечи  таз колени {get_angle_res(dict_of_points['first_shoulder'], dict_of_points['first_ass'], dict_of_points['first_knee'], accept180)}")
    print(
        f" угол таз  коленки стопы {get_angle_res(dict_of_points['first_ass'], dict_of_points['first_knee'], dict_of_points['first_foot'], accept180, ac_thr_a_k_f)}")
    print(
        f" угол кисти  таз стопы {get_angle_res(dict_of_points['first_wrist'], dict_of_points['first_ass'], dict_of_points['first_foot'], accept180)}")
else:
    print('wrong input')
plt.show()
