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
    if (180-abs(angl)) < thresh * 180:
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
                  'first_elbow','second_elbow', 'first_wrist', 'second_wrist', 'first_ass', 
                  'second_ass', 'first_knee', 'second_knee','first_foot', 'second_foot']
        
    def get_ang_res(self, f_point, s_point, t_point, func, accept_threshold=0.10, plot=False):

        if self.plot:
            fig, ax = plt.subplots()
            scat = ax.scatter(self.x, self.y)
            fig.canvas.draw()
            ax.set_xlim(0,700)
            ax.set_ylim(700,0)
            plt.scatter(f_point[0], f_point[1], c='red', s=30)
            plt.scatter(s_point[0], s_point[1], c='red', s=30)
            plt.scatter(t_point[0], t_point[1], c='red', s=30)
            plt.show()
        
        # Deviation
        deviation180 = round(180 - abs(angle([f_point, s_point, t_point])), 2)

        return func((angle([f_point, s_point, t_point])), accept_threshold), deviation180
    
    def calculate(self, thr):
        kpnts = {k: v for k, v in zip(self.name_of_points, self.data)}
        self.x = [point[0] for point in kpnts.values()]
        self.y = [point[1] for point in kpnts.values()]

        if len(self.data) == 17:
            print(f"WES angle {self.get_ang_res(kpnts['first_wrist'], kpnts['first_elbow'], kpnts['first_shoulder'], accept180, thr[1])}")
            print(f"WSH angle {self.get_ang_res(kpnts['first_wrist'], kpnts['first_shoulder'], kpnts['first_ass'], accept180, thr[0])}")
            print(f"WSK angle {self.get_ang_res(kpnts['first_wrist'], kpnts['first_ass'], kpnts['first_knee'], accept180, thr[3])}")
            print(f"SHK angle {self.get_ang_res(kpnts['first_shoulder'], kpnts['first_ass'], kpnts['first_knee'], accept180, thr[0])}")
            print(f"HKA angle {self.get_ang_res(kpnts['first_ass'], kpnts['first_knee'], kpnts['first_foot'], accept180, thr[2])}")
            print(f"WHA angle {self.get_ang_res(kpnts['first_wrist'], kpnts['first_ass'], kpnts['first_foot'], accept180, thr[0])}")
        else:
            print('wrong input')
            
            
data = [[211.67487   , 499.757     ,   0.7409724 ],
       [217.45163   , 493.98026   ,   0.6473201 ],
       [211.67487   , 493.98026   ,   0.7073585 ],
       [229.00516   , 465.09634   ,   0.68155074],
       [229.00516   , 470.87314   ,   0.8027224 ],
       [211.67487   , 453.54288   ,   0.6729184 ],
       [200.1213    , 453.54288   ,   0.7856642 ],
       [188.56778   , 517.0873    ,   0.7536105 ],
       [188.56778   , 511.31046   ,   0.7705407 ],
       [188.56778   , 592.1852    ,   0.77075964],
       [188.56778   , 592.1852    ,   0.74275655],
       [211.67487   , 320.67715   ,   0.64588946],
       [200.1213    , 320.67715   ,   0.597564  ],
       [211.67487   , 193.58829   ,   0.8292259 ],
       [211.67487   , 193.58829   ,   0.84274936],
       [211.67487   , 101.160034  ,   0.62794626],
       [211.67487   , 101.160034  ,   0.5953075 ]]

ac_thr = 0.1
ac_thr_wes = 0.4
ac_thr_akf = 0.5
ac_thr_wsk = 0.5

AngleCheck(data, False).calculate([ac_thr, ac_thr_wes, ac_thr_akf, ac_thr_wsk])
