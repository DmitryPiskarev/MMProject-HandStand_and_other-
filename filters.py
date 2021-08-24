import cv2
import os
from PIL import ImageFilter, Image
import numpy as np


def resized_and_filtered(dirs, fltr_type):
    """
    - dirs is a list of directories in the followinf order:
        mmpose_dir, img_root, img, filtered_root
    - fltr_type - type of filter
    """
    src = cv2.imread(os.path.join(dirs[0], dirs[1], dirs[2]), cv2.IMREAD_UNCHANGED)
    # percent by which the image is resized
    max_image_height = 500
    scale_pct = float(max_image_height / src.shape[0])
    # calculate the 50 percent of original dimensions
    width = int(src.shape[1] * scale_pct)
    height = int(src.shape[0] * scale_pct)
    # dsize
    dsize = (width, height)
    # resize image
    output = cv2.resize(src, dsize)

    if fltr_type == 'CLAHE':
        # -----Converting image to LAB Color model-----------------------------------
        lab = cv2.cvtColor(output, cv2.COLOR_BGR2LAB)
        # -----Splitting the LAB image to different channels-------------------------
        l, a, b = cv2.split(lab)
        # -----Applying CLAHE to L-channel-------------------------------------------
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        # -----Merge the CLAHE enhanced L-channel with the a and b channel-----------
        limg = cv2.merge((cl, a, b))
        # -----Converting image from LAB Color model to RGB model--------------------
        final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    elif fltr_type == 'GRAY':
        # -----Converting to GRAY color space----------------------------------------
        final = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

    elif fltr_type == 'MEDIANBLUR':
        # -----Making blured image---------------------------------------------------
        final = cv2.medianBlur(output, 3)

    elif fltr_type == 'GRAY_HSV':
        # -----Converting to GRAY color space----------------------------------------
        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        # -----Converting to HSV color space-----------------------------------------
        final = cv2.cvtColor(gray, cv2.COLOR_BGR2HSV)
    elif fltr_type == 'SHARPEN':
        img = Image.fromarray(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
        pil_img = img.filter(ImageFilter.SHARPEN)
        final = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    elif fltr_type == 'kernel':
        kernel3 = np.array([[0, -1, 0],
                            [-1, 5, -1],
                            [0, -1, 0]])
        final = cv2.filter2D(src=output, ddepth=-1, kernel=kernel3)


    else:
        final = output

    out_name = '{}_{}_{}.png'.format(dirs[2].split('.')[0], scale_pct, fltr_type)
    if not cv2.imwrite(os.path.join(dirs[0], dirs[3], '{}'.format(out_name)), final):
        raise Exception("Could not write image")

    cv2.imwrite(os.path.join(dirs[0], dirs[3], '{}'.format(out_name)), final)
    return out_name
