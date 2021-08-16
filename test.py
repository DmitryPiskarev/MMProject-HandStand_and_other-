import math
import matplotlib.pyplot as plt

def slope(x1, y1, x2, y2):  # Line slope given two points:
    """Two points slope"""
    a = y2 - y1
    b = x2 - x1
    if b != 0:
        return a / b
    else:
        return 0

def angle(s1, s2):
    """Angle bw two cartesian vectors"""
    return round(math.degrees(math.atan((s2 - s1) / (1 + (s2 * s1)))), 2)


def accept180(angl, thresh):
    # Accept position if the angle is less than 180 degrees multiplied by accept_threshold
    if abs(angl) < thresh * 180:
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
        slp1 = slope(f_point[0], f_point[1], s_point[0], s_point[1])
        slp2 = slope(s_point[0], s_point[1], t_point[0], t_point[1])

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

        return func((angle(slp1, slp2)), accept_threshold)
    
    def calculate(self, thr):
        kpnts = {k: v for k, v in zip(self.name_of_points, self.data)}
        self.x = [point[0] for point in kpnts.values()]
        self.y = [point[1] for point in kpnts.values()]

        if len(self.data) == 17:
            print(f"WES angle {self.get_ang_res(kpnts['first_wrist'], kpnts['first_elbow'], kpnts['first_shoulder'], accept180, thr[1])}")
            print(f"WSH angle {self.get_ang_res(kpnts['first_wrist'], kpnts['first_shoulder'], kpnts['first_ass'], accept180, thr[0])}")
            print(f"WSK angle {self.get_ang_res(kpnts['first_wrist'], kpnts['first_ass'], kpnts['first_knee'], accept180, thr[3])}")
            print(f"SHK angle {self.get_ang_res(kpnts['first_shoulder'], kpnts['first_ass'], kpnts['first_knee'], accept180, thr[0])}")
            print(f"HKA angle {self.get_ang_res(kpnts['first_ass'], kpnts['first_knee'], kpnts['first_foot'], accept180, thr[3])}")
            print(f"WHA angle {self.get_ang_res(kpnts['first_wrist'], kpnts['first_ass'], kpnts['first_foot'], accept180, thr[0])}")
        else:
            print('wrong input')
  


            
data = [
            [313.9518    , 489.6005    ,   0.7283645 ],
            [320.12283   , 489.6005    ,   0.6645787 ],
            [313.9518    , 489.6005    ,   0.72944766],
            [332.46487   , 471.08743   ,   0.66028035],
            [326.29385   , 477.25845   ,   0.82653844],
            [307.7808    , 446.40335   ,   0.6953033 ],
            [301.60977   , 446.40335   ,   0.78552604],
            [289.26773   , 520.45557   ,   0.7425771 ],
            [289.26773   , 520.45557   ,   0.74586296],
            [283.0967    , 594.5078    ,   0.7675216 ],
            [283.0967    , 594.5078    ,   0.76537216],
            [301.60977   , 329.1539    ,   0.66259456],
            [307.7808    , 341.49594   ,   0.61462903],
            [307.7808    , 193.39139   ,   0.818356  ],
            [307.7808    , 193.39139   ,   0.7711457 ],
            [307.7808    , 100.82608   ,   0.63019484],
            [313.9518    , 100.82608   ,   0.60619974]
        ]

ac_thr = 0.1
ac_thr_wes = 0.4
ac_thr_akf = 0.5
ac_thr_wsk = 0.5

AngleCheck(data, True).calculate([ac_thr, ac_thr_wes, ac_thr_akf, ac_thr_wsk])
