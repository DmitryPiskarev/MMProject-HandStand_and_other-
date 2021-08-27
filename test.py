import subprocess
import re
import os
from keypoint_classes import AngleCheck
from filters import *
from PIL import Image
import cv2

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
# BASE_DIR = os.getcwd() # Может так?
img_root = os.path.join(BASE_DIR, 'media/good_img')
# img_root = os.path.join(BASE_DIR, 'media/img_from_video/user1')

# Dima dont touch! ONLY COMMENT!!!!!  :))
mmpose_dir = '/home/kirill/PycharmProjects/MMproject/mmpose'
my_dir = '/home/kirill/PycharmProjects/HandstandProject/'

# mmpose_dir = '/home/dmitriy/mmcv/mmpose'
# my_dir = '/home/dmitriy/MMProject-HandStand_and_other-'

# f_root = os.path.join(BASE_DIR, 'media/filtered')
# img_out = os.path.join(BASE_DIR, 'media/out_img')

f_root = os.path.join(my_dir, 'media/filtered')
img_out = os.path.join(my_dir, 'media/out_img')

img = 'tst_img1.png'
array_of_results = []


def get_img_rezult(mmpose_root, img_name, img_root_dir, f_root_dir, img_out_dir):
    rez = {}
    # filter to test
    
    fltrs = {0:'GRAY', 1:'WB', 2:'BC', 3:'HSV', 4:'SHARPEN', 5:'MEDIANBLUR', 
             6:'AVERAGE', 7:'GAUSSIAN_BLUR', 8:'TRUNC', 9:'CLAHE', 10:'BILATERAL',
             11:'THRESH_TOZERO', 12:'VLINE', 13:'EMBOSS', 14:'BGR2RGB'}
    
    "NOTE: WB is not applicable for gray scale image! Please, keep appropriate order of filters."
    
    apply_following = [fltrs[1], fltrs[2], fltrs[4],  fltrs[5]]
    
    
    ### for tst_img5 - 18, 11, 9 and 5 made a good job
    ### for the
    resize = 500  # Set False to prevent resizing
    smooth = 3  # an additional numerical parameter like the smooth factor in the MEDIANBLUR
    alpha = 1.0  # Simple contrast control
    beta = 0  # Simple brightness control

    img_new = resized_and_filtered([mmpose_root, img_root_dir, img_name, f_root_dir], fltrs,
                                   resize, smooth, alpha, beta)

    thresholds = {'strict': [0.150, 0.032, 0.018, 0.027, 0.026, 0.015],  # Median
                  'conservative': [0.2, 0.06, 0.034, 0.048, 0.064, 0.031],  # Median + Standard deviation
                  'week': [0.323, 0.088, 0.049, 0.069, 0.101, 0.047]}  # Median + 2xStandard deviation

    # Previous thresholds' values
    # ac_thr_wes = 0.150 ac_thr_wsh = 0.037 ac_thr_wsk = 0.019 ac_thr_shk = 0.026
    # ac_thr_hka = 0.027 ac_thr_wha = 0.018

    ac_thr_wes, ac_thr_wsh, ac_thr_wsk, ac_thr_shk, ac_thr_hka, ac_thr_wha = thresholds['week']

    # retrieve data from mmpose
    mmpose_out_dataset_str = subprocess.check_output(["./subscript", mmpose_dir, f_root_dir, img_new, img_out_dir])

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
        for data in data_data:
            result = AngleCheck(data, False)
            result.calculate([ac_thr_wes, ac_thr_wsh, ac_thr_wsk,
                              ac_thr_shk, ac_thr_hka, ac_thr_wha])
            if result.flag:
                rez = result.dict_of_angles
                break
        img_in = Image.open(f'{img_root_dir}/{img_name}')
        img_in_f = Image.open(f'{f_root_dir}/{img_new}')
        img_out = Image.open(f'{img_out_dir}/vis_{img_new}')
        img_in.show()
        img_in_f.show()
        img_out.show()
        return rez
    else:
        print(string_mm)
        return rez

d = get_img_rezult(mmpose_root=mmpose_dir, 
                   img_name=img, 
                   img_root_dir=img_root, 
                   f_root_dir=f_root, 
                   img_out_dir=img_out)

print(f"++++++{d}")

## For all img of user

# path, dirs, files = next(os.walk(img_root))
# file_count = len(files)
# for i in range(file_count):
#     imgname = f"img_{i}.png"
#     array_of_results.append(
#         get_img_rezult(img_name=imgname, img_root_dir=img_root, f_root_dir=f_root, img_out_dir=img_out))
#
# print(array_of_results)
