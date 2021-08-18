import math
import matplotlib.pyplot as plt
import numpy as np


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
                f"WSH angle {self.get_ang_res(kpnts['first_wrist'], kpnts['first_shoulder'], kpnts['first_ass'], accept180, thr[0])}")
            print(
                f"WSK angle {self.get_ang_res(kpnts['first_wrist'], kpnts['first_ass'], kpnts['first_knee'], accept180, thr[0])}")
            print(
                f"SHK angle {self.get_ang_res(kpnts['first_shoulder'], kpnts['first_ass'], kpnts['first_knee'], accept180, thr[0])}")
            print(
                f"HKA angle {self.get_ang_res(kpnts['first_ass'], kpnts['first_knee'], kpnts['first_foot'], accept180, thr[0])}")
            print(
                f"WHA angle {self.get_ang_res(kpnts['first_wrist'], kpnts['first_ass'], kpnts['first_foot'], accept180, thr[0])}")

            # while res are important develop
            dict_of_angles = {
                'WES angle': [self.list_of_angles[0],
                              self.get_ang_res(kpnts['first_wrist'], kpnts['first_elbow'], kpnts['first_shoulder'],
                                               accept180, thr[0])],
                'WSH angle': [self.list_of_angles[1],
                              self.get_ang_res(kpnts['first_wrist'], kpnts['first_shoulder'], kpnts['first_ass'],
                                               accept180,
                                               thr[0])],
                'WSK angle': [self.list_of_angles[2],
                              self.get_ang_res(kpnts['first_wrist'], kpnts['first_ass'], kpnts['first_knee'], accept180,
                                               thr[0])],
                'SHK angle': [self.list_of_angles[3],
                              self.get_ang_res(kpnts['first_shoulder'], kpnts['first_ass'], kpnts['first_knee'],
                                               accept180,
                                               thr[0])],
                'HKA angle': [self.list_of_angles[4],
                              self.get_ang_res(kpnts['first_ass'], kpnts['first_knee'], kpnts['first_foot'], accept180,
                                               thr[0])],
                'WHA angle': [self.list_of_angles[5],
                              self.get_ang_res(kpnts['first_wrist'], kpnts['first_ass'], kpnts['first_foot'], accept180,
                                               thr[0])],

            }
            # with open("angeles.txt", "a") as file:
            #     file.write(f'{dict_of_angles}\n\n')
            #     file.close()
            print(dict_of_angles)
        else:
            print('wrong input')


data = [
    [2.2852112e+01, 4.4085107e+02, 9.2905760e-01],
    [2.2852112e+01, 4.3642249e+02, 7.2721934e-01],
    [2.2852112e+01, 4.3642249e+02, 9.5708144e-01],
    [2.9236374e+00, 4.3420819e+02, 7.3028135e-01],
    [1.6209282e+01, 4.3642249e+02, 9.5176470e-01],
    [5.1379089e+00, 4.6077954e+02, 5.9542584e-01],
    [2.2852112e+01, 4.6299377e+02, 8.8409925e-01],
    [2.2852112e+01, 4.8956506e+02, 3.4178093e-01],
    [3.3923477e+01, 4.9842218e+02, 9.5276344e-01],
    [2.2852112e+01, 4.5192242e+02, 2.8219289e-01],
    [3.8352020e+01, 4.8956506e+02, 6.5208131e-01],
    [5.1379089e+00, 5.2499347e+02, 5.2827275e-01],
    [1.1780731e+01, 5.2720776e+02, 7.5720334e-01],
    [5.1379089e+00, 5.7592181e+02, 6.9049054e-01],
    [1.6209282e+01, 5.7370752e+02, 8.6312115e-01],
    [2.9236374e+00, 6.2242157e+02, 8.0288780e-01],
    [7.0935822e-01, 6.1135016e+02, 4.8813617e-01]
]

ac_thr = 0.1
# ac_thr_wes = 0.4
# ac_thr_akf = 0.5
# ac_thr_wsk = 0.5

AngleCheck(data, False).calculate([ac_thr])
