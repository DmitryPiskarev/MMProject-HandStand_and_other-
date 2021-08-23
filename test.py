import subprocess
import re
from keypoint_classes import AngleCheck
from PIL import Image

mmpose_dir = '/home/kirill/PycharmProjects/MMproject/mmpose'
# mmpose_dir = '/home/dima/mmpose'
img_root = 'demo/resources/img/'
img = 'tst_img1.png'
img_out = 'vis_results'

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


mmpose_out_dataset_str = subprocess.check_output(["./subscript", mmpose_dir, img_root, img, img_out])

string_mm = mmpose_out_dataset_str.decode()
arr_of_strings = string_mm.replace("\n", "").replace(" ", "").split("}")
re_rule_f = '\'keypoints\':array\(.*?\)'
re_rule_s = '\[(.+?)\]'
arr_of_keypoint_str = []
data_data = []
for x in arr_of_strings:
    arr_of_keypoint_str.append(re.findall(re_rule_f, x))
if arr_of_keypoint_str:
    for y in arr_of_keypoint_str:
        if y:
            substring_arr = re.findall(re_rule_s, y[0])
            substring_arr[0] = substring_arr[0].replace('[', '')
            s_ar = [list(map(float, (x.split(',')))) for x in substring_arr]
            data_data.append(s_ar)

    AngleCheck(data_data[0], False).calculate([ac_thr_wes, ac_thr_wsh, ac_thr_wsk,
                                               ac_thr_shk, ac_thr_hka, ac_thr_wha])
    img_in = Image.open(f'{mmpose_dir}/{img_root}/{img}')
    img_out = Image.open(f'{mmpose_dir}/{img_out}/vis_{img}')
    img_in.show()
    img_out.show()
else:
    print(string_mm)
