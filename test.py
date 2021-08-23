import math
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import re


# def slope(x1, y1, x2, y2):  # Line slope given two points:
#     """Two points slope"""
#     a = y2 - y1
#     b = x2 - x1
#     if b != 0:
#         return a / b
#     else:
#         return 0

def angle(pnt):
    """Angle bw two cartesian vectors"""
    a = np.array(pnt[0])
    b = np.array(pnt[1])
    c = np.array(pnt[2])

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)

    return np.degrees(angle)


def accept180(angl, thresh):
    # Accept position if the angle is less than 180 degrees multiplied by accept_threshold
    if (180 - abs(angl)) < thresh * 180:
        return True
    else:
        return False


class AngleCheck:
    """
        Current notations:
        WES - Wrist-Elbow-Shoulder
        WSH - Wrist-Shoulder-Hip
        WSK - Wrist-Shoulder-Knee
        SHK - Shoulder-Hip-Knee
        HKA - Hip-Knee-Ankle
        WHA - Wrist-Hip-Ankle
    """

    def __init__(self, data, plot=False):
        self.data = data
        self.plot = plot
        self.name_of_points = ['head0', 'head1', 'head2', 'head3', 'head4', 'first_shoulder', 'second_shoulder',
                               'first_elbow', 'second_elbow', 'first_wrist', 'second_wrist', 'first_ass',
                               'second_ass', 'first_knee', 'second_knee', 'first_foot', 'second_foot']
        self.list_of_angles = []

    def get_ang_res(self, f_point, s_point, t_point, func, accept_threshold=0.10, plot=False):

        if self.plot:
            fig, ax = plt.subplots()
            scat = ax.scatter(self.x, self.y)
            fig.canvas.draw()
            ax.set_xlim(0, 700)
            ax.set_ylim(700, 0)
            plt.scatter(f_point[0], f_point[1], c='red', s=30)
            plt.scatter(s_point[0], s_point[1], c='red', s=30)
            plt.scatter(t_point[0], t_point[1], c='red', s=30)
            plt.show()

        # Deviation
        deviation180 = round(180 - abs(angle([f_point, s_point, t_point])), 2)
        self.list_of_angles.append(angle([f_point, s_point, t_point]))

        return func((angle([f_point, s_point, t_point])), accept_threshold), deviation180

    def calculate(self, thr):
        kpnts = {k: v for k, v in zip(self.name_of_points, self.data)}
        self.x = [point[0] for point in kpnts.values()]
        self.y = [point[1] for point in kpnts.values()]

        if len(self.data) == 17:
            print(
                f"WES angle {self.get_ang_res(kpnts['first_wrist'], kpnts['first_elbow'], kpnts['first_shoulder'], accept180, thr[0])}")
            print(
                f"WSH angle {self.get_ang_res(kpnts['first_wrist'], kpnts['first_shoulder'], kpnts['first_ass'], accept180, thr[1])}")
            print(
                f"WSK angle {self.get_ang_res(kpnts['first_wrist'], kpnts['first_ass'], kpnts['first_knee'], accept180, thr[2])}")
            print(
                f"SHK angle {self.get_ang_res(kpnts['first_shoulder'], kpnts['first_ass'], kpnts['first_knee'], accept180, thr[3])}")
            print(
                f"HKA angle {self.get_ang_res(kpnts['first_ass'], kpnts['first_knee'], kpnts['first_foot'], accept180, thr[4])}")
            print(
                f"WHA angle {self.get_ang_res(kpnts['first_wrist'], kpnts['first_ass'], kpnts['first_foot'], accept180, thr[5])}")

            # while res are important develop
            dict_of_angles = {
                'WES angle': [self.list_of_angles[0],
                              self.get_ang_res(kpnts['first_wrist'], kpnts['first_elbow'], kpnts['first_shoulder'],
                                               accept180, thr[0])],
                'WSH angle': [self.list_of_angles[1],
                              self.get_ang_res(kpnts['first_wrist'], kpnts['first_shoulder'], kpnts['first_ass'],
                                               accept180,
                                               thr[1])],
                'WSK angle': [self.list_of_angles[2],
                              self.get_ang_res(kpnts['first_wrist'], kpnts['first_ass'], kpnts['first_knee'], accept180,
                                               thr[2])],
                'SHK angle': [self.list_of_angles[3],
                              self.get_ang_res(kpnts['first_shoulder'], kpnts['first_ass'], kpnts['first_knee'],
                                               accept180,
                                               thr[3])],
                'HKA angle': [self.list_of_angles[4],
                              self.get_ang_res(kpnts['first_ass'], kpnts['first_knee'], kpnts['first_foot'], accept180,
                                               thr[4])],
                'WHA angle': [self.list_of_angles[5],
                              self.get_ang_res(kpnts['first_wrist'], kpnts['first_ass'], kpnts['first_foot'], accept180,
                                               thr[5])],

            }
            #             with open("angeles.txt", "a") as file:
            #                 file.write(f'{dict_of_angles}\n\n')
            #                 file.close()
            print(dict_of_angles)
        else:
            print('wrong input')


# Suspicious WES angle 29, 30, 32, 36, 37, 38(less), 41 43, 44, 45, 46, 48
# Suspicious WSH angle 34, 36, 42, 45
# Suspicious HKA angle 41
# Suspicious SHK angle 47

# data = [[91.063324, 272.36313, 0.8157366],
#         [84.76651, 272.36313, 0.8523694],
#         [91.063324, 278.65994, 0.79907167],
#         [84.76651, 266.0663, 0.8775567],
#         [97.36014, 272.36313, 0.6498351],
#         [94.21173, 247.17587, 0.6690098],
#         [106.805374, 262.9179, 0.7052514],
#         [97.36014, 291.2536, 0.56708306],
#         [97.36014, 291.2536, 0.86998916],
#         [97.36014, 332.18292, 0.68419474],
#         [94.21173, 332.18292, 0.82392687],
#         [97.36014, 168.4657, 0.6219564],
#         [103.65695, 168.4657, 0.67523414],
#         [103.65695, 105.49753, 0.7835887],
#         [103.65695, 105.49753, 0.68537617],
#         [103.65695, 48.82617, 0.6098028],
#         [106.805374, 51.97458, 0.5526638]]

thresholds = {'strict': [0.150, 0.032, 0.018, 0.027, 0.026, 0.015],  # Median
              'conservative': [0.2, 0.06, 0.034, 0.048, 0.064, 0.031],  # Median + Standard deviation
              'week': [0.323, 0.088, 0.049, 0.069, 0.101, 0.047]}  # Median + 2xStandard deviation

# Previous thresholds' values
# ac_thr_wes = 0.150
# ac_thr_wsh = 0.037
# ac_thr_wsk = 0.019
# ac_thr_shk = 0.026
# ac_thr_hka = 0.027
# ac_thr_wha = 0.018

ac_thr_wes, ac_thr_wsh, ac_thr_wsk, ac_thr_shk, ac_thr_hka, ac_thr_wha = thresholds['conservative']

# take data from mmpose


mmpose_out_dataset_str = subprocess.check_output(["./subscript"])

string_mm = mmpose_out_dataset_str.decode()
# print(string_mm)
arr_of_strings = string_mm.replace("\n", "").replace(" ", "").split("}")
re_rule_f = '\'keypoints\':array\(.*?\)'
re_rule_s = '\[(.+?)\]'
arr_of_keypoint_str = []
data_data = []
for x in arr_of_strings:
    arr_of_keypoint_str.append(re.findall(re_rule_f, x))

for y in arr_of_keypoint_str:
    if y:
        substring_arr = re.findall(re_rule_s, y[0])
        substring_arr[0] = substring_arr[0].replace('[', '')
        s_ar = [list(map(float, (x.split(',')))) for x in substring_arr]
        data_data.append(s_ar)

AngleCheck(data_data[0], False).calculate([ac_thr_wes, ac_thr_wsh, ac_thr_wsk,
                                   ac_thr_shk, ac_thr_hka, ac_thr_wha])
