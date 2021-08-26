import cv2
import os
from PIL import ImageFilter, Image
import numpy as np
from varname import nameof


def extract_lines(path, write=False, vline=True):
    """
        Extracts vertical/horizontal lines from the input image
    """
    # Get rid of JPG artifacts
    img = cv2.imread(os.path.join(path[0], path[1], path[2]))
    img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)[1]

    # Create structuring elements
    horizontal_size = 11
    vertical_size = 11
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical_size))

    # Morphological opening
    mask1 = cv2.morphologyEx(img, cv2.MORPH_OPEN, horizontalStructure)
    mask2 = cv2.morphologyEx(img, cv2.MORPH_OPEN, verticalStructure)

    if write:
        cv2.imwrite(os.path.join(path[0], path[3], '{}_{}'.format(nameof(mask1), path[2])), mask1)
        cv2.imwrite(os.path.join(path[0], path[3], '{}_{}'.format(nameof(mask2), path[2])), mask2)

    if vline:
        return mask2, '{}_{}'.format(nameof(mask2), path[2])
    else:
        return mask1, '{}_{}'.format(nameof(mask1), path[2])


def bc_adjustment(image, a, b):
    new_image = np.zeros(image.shape, image.dtype)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            for c in range(image.shape[2]):
                new_image[y, x, c] = np.clip(a * image[y, x, c] + b, 0, 255)

    return new_image


def white_balance_loops(img):
    result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    for x in range(result.shape[0]):
        for y in range(result.shape[1]):
            l, a, b = result[x, y, :]
            # fix for CV correction
            l *= 100 / 255.0
            result[x, y, 1] = a - ((avg_a - 128) * (l / 100.0) * 1.1)
            result[x, y, 2] = b - ((avg_b - 128) * (l / 100.0) * 1.1)
    result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    return result


def resized_and_filtered(dirs, fltr_type, max_image_height, smooth, alpha, beta):
    """
    - dirs is a list of directories in the followinf order:
        mmpose_dir, img_root, img, filtered_root
    - fltr_type - type of filter
    """
    kernels = [np.array([[0, -1, 0],
                         [-1, 5, -1],
                         [0, -1, 0]]),
               np.array([[-2, -1, 0],
                         [-1, 1, 1],
                         [0, 1, 2]]),
               np.ones((5, 5), np.float32) / 25]

    src = cv2.imread(os.path.join(dirs[0], dirs[1], dirs[2]), cv2.IMREAD_UNCHANGED)

    if max_image_height:
        # percent by which the image is resized
        scale_pct = float(max_image_height / src.shape[0])
        # calculate the 50 percent of original dimensions
        width = int(src.shape[1] * scale_pct)
        height = int(src.shape[0] * scale_pct)
        # dsize
        dsize = (width, height)
        # resize image
        output = cv2.resize(src, dsize)
    else:
        scale_pct = 'no'
        output = src

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
        image = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        final = cv2.medianBlur(image, smooth)

    elif fltr_type == 'MEDIANBLUR_NG':
        final = cv2.medianBlur(output, smooth)

    elif fltr_type == 'GRAY_HSV':
        final = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)

    elif fltr_type == 'HSV':
        final = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)

    elif fltr_type == 'SHARPEN':
        img = Image.fromarray(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
        pil_img = img.filter(ImageFilter.SHARPEN)
        final = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    elif fltr_type == 'SHARPEN2':
        image = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        kernel = kernels[0]
        final = cv2.filter2D(image, -1, kernel)

    elif fltr_type == 'SHARPEN2_NG':  # NG means NO GRAY
        kernel3 = kernels[0]
        final = cv2.filter2D(src=output, ddepth=-1, kernel=kernel3)

    elif fltr_type == 'EMBOSS':
        image = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        kernel = kernels[1]
        final = cv2.filter2D(image, -1, kernel)

    elif fltr_type == 'VLINE':
        final = extract_lines(dirs, vline=True)[0]

    elif fltr_type == 'AVERAGE':
        image = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        kernel = kernels[2]
        final = cv2.filter2D(image, -1, kernel)

    elif fltr_type == 'AVERAGE_NG':
        kernel = kernels[2]
        final = cv2.filter2D(output, -1, kernel)

    elif fltr_type == 'AVERAGE_SHARP':
        image = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        final = cv2.filter2D(image, -1, kernels[2])
        final = cv2.filter2D(final, -1, kernels[0])

    elif fltr_type == 'GAUSSIAN_BLUR':
        image = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        final = cv2.GaussianBlur(image, (5, 5), 0)

    elif fltr_type == 'GAUSSIAN_BLUR_NG':
        final = cv2.GaussianBlur(output, (5, 5), 0)

    elif fltr_type == 'BILATERAL':
        image = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        final = cv2.bilateralFilter(image, 9, 75, 75)

    elif fltr_type == 'BILATERAL_NG':
        final = cv2.bilateralFilter(output, 9, 75, 75)

    elif fltr_type == 'AVERAGE_SHARP_BILATERAL':
        image = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        final = cv2.filter2D(image, -1, kernels[2])
        final = cv2.filter2D(final, -1, kernels[0])
        final = cv2.bilateralFilter(final, 9, 75, 75)

    elif fltr_type == 'TRUNC':
        image = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        _, final = cv2.threshold(image, 127, 255, cv2.THRESH_TRUNC)

    elif fltr_type == 'TRUNC_NG':
        _, final = cv2.threshold(output, 127, 255, cv2.THRESH_TRUNC)

    elif fltr_type == 'PURE_BC':
        final = bc_adjustment(output, alpha, beta)

    elif fltr_type == 'BC_TRUNC':
        image = bc_adjustment(output, alpha, beta)
        _, final = cv2.threshold(image, 127, 255, cv2.THRESH_TRUNC)

    elif fltr_type == 'WB':
        final = white_balance_loops(output)

    elif fltr_type == 'WB_TRUNC':
        final = white_balance_loops(output)
        image = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        _, final = cv2.threshold(image, 127, 255, cv2.THRESH_TRUNC)

    elif fltr_type == 'WB_TRUNC_NG':
        image = white_balance_loops(output)
        _, final = cv2.threshold(image, 127, 255, cv2.THRESH_TRUNC)

    elif fltr_type == 'THRESH_TOZERO':
        image = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        _, final = cv2.threshold(image, 127, 255, cv2.THRESH_TOZERO)

    elif fltr_type == 'THRESH_TOZERO_NG':
        _, final = cv2.threshold(output, 127, 255, cv2.THRESH_TOZERO)

    elif fltr_type == 'GB_TRUNC':
        image = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        image = cv2.GaussianBlur(image, (5, 5), 0)
        _, final = cv2.threshold(image, 127, 255, cv2.THRESH_TOZERO)

    elif fltr_type == 'GB_WB_TRUNC':
        image = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        image = cv2.GaussianBlur(image, (5, 5), 0)
        image = white_balance_loops(image)
        _, final = cv2.threshold(image, 127, 255, cv2.THRESH_TOZERO)

    elif fltr_type == 'SH2_TRUNC':
        image = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        kernel = kernels[0]
        image = cv2.filter2D(image, -1, kernel)
        _, final = cv2.threshold(image, 127, 255, cv2.THRESH_TRUNC)

    elif fltr_type == 'SH2_MB_TRUNC':
        image = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        kernel = kernels[0]
        image = cv2.filter2D(image, -1, kernel)
        image = cv2.medianBlur(image, smooth)
        _, final = cv2.threshold(image, 127, 255, cv2.THRESH_TRUNC)


    else:
        final = output

    out_name = '{}_{}_{}.png'.format(dirs[2].split('.')[0], scale_pct, fltr_type)
    if not cv2.imwrite(os.path.join(dirs[0], dirs[3], '{}'.format(out_name)), final):
        raise Exception("Could not write image")

    cv2.imwrite(os.path.join(dirs[0], dirs[3], '{}'.format(out_name)), final)
    return out_name
