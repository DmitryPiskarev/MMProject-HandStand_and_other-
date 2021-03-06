import matplotlib.pyplot as plt
import numpy as np


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
        self.flag = True
        self.dict_of_angles = {}

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
            self.dict_of_angles = {
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

            for x in self.dict_of_angles.values():
                if int(x[1][1]) > 40 or kpnts['head0'][1] < kpnts['first_ass'][1]:
                    self.flag = False
            # print(dict_of_angles)

            #             with open("angeles.txt", "a") as file:
            #                 file.write(f'{dict_of_angles}\n\n')
            #                 file.close()
        else:
            print('wrong input')
