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

data = [[ 40.03208   , 124.01081   ,   0.8453804 ],
       [ 37.151375  , 122.57044   ,   0.80337894],
       [ 37.151375  , 124.01081   ,   0.84347403],
       [ 35.71102   , 116.80903   ,   0.8963101 ],
       [ 34.270668  , 115.36869   ,   0.6300535 ],
       [ 41.472435  , 108.16691   ,   0.8087631 ],
       [ 41.472435  , 106.72657   ,   0.6220643 ],
       [ 45.793495  , 126.89152   ,   0.8191618 ],
       [ 45.793495  , 126.89152   ,   0.7553381 ],
       [ 44.35314   , 147.05646   ,   0.85301363],
       [ 44.35314   , 147.05646   ,   0.80053496],
       [ 40.03208   ,  73.59843   ,   0.72605896],
       [ 40.03208   ,  72.15809   ,   0.7087054 ],
       [ 40.03208   ,  46.231728  ,   0.5841695 ],
       [ 37.151375  ,  44.791374  ,   0.63503903],
       [ 38.59173   ,  20.305367  ,   0.5414063 ],
       [ 38.59173   ,  21.74572   ,   0.68132   ]]


thresholds = {'strict': [0.150, 0.032, 0.018, 0.027, 0.026, 0.015], # Median
              'conservative': [0.2, 0.06, 0.034, 0.048, 0.064, 0.031], # Median + Standard deviation
              'week': [0.323, 0.088, 0.049, 0.069, 0.101, 0.047]} # Median + 2xStandard deviation

# Previous thresholds' values
# ac_thr_wes = 0.150
# ac_thr_wsh = 0.037
# ac_thr_wsk = 0.019
# ac_thr_shk = 0.026
# ac_thr_hka = 0.027
# ac_thr_wha = 0.018

ac_thr_wes, ac_thr_wsh, ac_thr_wsk, ac_thr_shk, ac_thr_hka, ac_thr_wha = thresholds['strict']

AngleCheck(data, False).calculate([ac_thr_wes, ac_thr_wsh, ac_thr_wsk, 
                                   ac_thr_shk, ac_thr_hka, ac_thr_wha])
