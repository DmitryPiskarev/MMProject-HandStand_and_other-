import cv2
import os
from PIL import ImageFilter, Image
import numpy as np
from varname import nameof


def resize_img(img, max_image_height):
    scale_pct = float(max_image_height / img.shape[0])
    width = int(img.shape[1] * scale_pct)
    height = int(img.shape[0] * scale_pct)
    dsize = (width, height)

    return cv2.resize(img, dsize), round(scale_pct*100, 0)

class Filtering:
    def __init__(self, img, ftype, path, alpha, beta, sharp_profile, smooth):
        self.img = img
        self.ftype = ftype
        self.kernels = [np.array([[0, -1, 0],[-1, 5, -1],[0, -1, 0]]),
                        np.array([[-2, -1, 0],[-1, 1, 1],[0, 1, 2]]),
                        np.ones((5, 5), np.float32) / 25,
                        np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])]
        self.path = path
        self.smooth = smooth
        self.a = alpha
        self.b = beta
        self.sharp_ind = sharp_profile

    def extract_lines(self, write=False, vline=True):
        """
            Extracts vertical/horizontal lines from the input image
        """
        # Get rid of JPG artifacts
        img = cv2.threshold(self.img, 128, 255, cv2.THRESH_BINARY)[1]

        # Create structuring elements
        horizontal_size = 11
        vertical_size = 11
        horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
        verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical_size))

        # Morphological opening
        mask1 = cv2.morphologyEx(self.img, cv2.MORPH_OPEN, horizontalStructure)
        mask2 = cv2.morphologyEx(self.img, cv2.MORPH_OPEN, verticalStructure)

        if write:
            cv2.imwrite(os.path.join(self.path[0], self.path[3], '{}_{}'.format(nameof(mask1), self.path[2])), mask1)
            cv2.imwrite(os.path.join(self.path[0], self.path[3], '{}_{}'.format(nameof(mask2), self.path[2])), mask2)

        if vline:
            return mask2, '{}_{}'.format(nameof(mask2), self.path[2])
        else:
            return mask1, '{}_{}'.format(nameof(mask1), self.path[2])

    def brightness_contrast_adj(self):
        new_image = np.zeros(self.img.shape, self.img.dtype)
        for y in range(self.img.shape[0]):
            for x in range(self.img.shape[1]):
                for c in range(self.img.shape[2]):
                    new_image[y, x, c] = np.clip(self.a * self.img[y, x, c] + self.b, 0, 255)
        return new_image

    def unsharp_mask(self, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
        """Return a sharpened version of the image, using an unsharp mask."""
        blurred = cv2.GaussianBlur(self.img, kernel_size, sigma)
        sharpened = float(amount + 1) * self.img - float(amount) * blurred
        sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
        sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
        sharpened = sharpened.round().astype(np.uint8)
        if threshold > 0:
            low_contrast_mask = np.absolute(self.img - blurred) < threshold
            np.copyto(sharpened, self.img, where=low_contrast_mask)
        return sharpened

    def wb(self):
        result = cv2.cvtColor(self.img, cv2.COLOR_BGR2LAB)
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

    def clache(self):
        lab = cv2.cvtColor(self.img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    def gray(self):
        return cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

    def bgr2rgb(self):
        return cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

    def rgb(self):
        return cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

    def medianb(self):
        return cv2.medianBlur(self.img, self.smooth)

    def sharpen(self):
        return cv2.filter2D(self.img, -1, self.kernels[self.sharp_ind])

    def emboss(self):
#         image = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        return cv2.filter2D(self.img, -1, self.kernels[1])

    def avg(self):
#         image = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        return cv2.filter2D(self.img, -1, self.kernels[2])

    def bilateral(self):
#         image = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        return cv2.bilateralFilter(self.img, 9, 75, 75)

    def trunc(self):
#         image = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        _, final = cv2.threshold(self.img, 127, 255, cv2.THRESH_TRUNC)
        return final

    def threstozero(self):
#         image = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        _, final = cv2.threshold(self.img, 127, 255, cv2.THRESH_TOZERO)
        return final

    def hcv(self):
        return cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

    def gblur(self):
#         image = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        return cv2.GaussianBlur(self.img, (5, 5), 0)

    def hsv2bgr(self):
        return cv2.cvtColor(self.img, cv2.COLOR_HSV2BGR)

    def saturation(self):
        hsvImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        hsvImg[...,1] = hsvImg[...,1]*self.a
        hsvImg[...,2] = hsvImg[...,2]*self.b
        return cv2.cvtColor(hsvImg,cv2.COLOR_HSV2BGR)

    def gray2rgb(self):
        return cv2.cvtColor(self.img, cv2.COLOR_GRAY2RGB)


    def apply_filter(self):
        if self.ftype == 'CLAHE':
            res = self.clache()

        elif self.ftype == 'GRAY':
            res = self.gray()

        elif self.ftype == 'BGR2RGB':
            res = self.bgr2rgb()

        elif self.ftype == 'MEDIANBLUR':
            res = self.medianb()

        elif self.ftype == 'HSV':
            res = self.hcv()

        elif self.ftype == 'SHARPEN':
            res = self.sharpen()

        elif self.ftype == 'EMBOSS':
            res = self.emboss()

        elif self.ftype == 'VLINE':
            res = self.extract_lines(write=False, vline=True)[0]

        elif self.ftype == 'AVERAGE':
            res = self.avg()

        elif self.ftype == 'GAUSSIAN_BLUR':
            res = self.gblur()

        elif self.ftype == 'BILATERAL':
            res = self.bilateral()

        elif self.ftype == 'TRUNC':
            res = self.trunc()

        elif self.ftype == 'BC':
            res = self.brightness_contrast_adj()

        elif self.ftype == 'WB':
            res = self.wb()

        elif self.ftype == 'THRESH_TOZERO':
            res = self.threstozero()

        elif self.ftype == 'HSV2BGR':
            res = self.hsv2bgr()

        elif self.ftype == 'SATURATION':
            res = self.saturation()

        elif self.ftype == 'UNSHARP_MASK':
            res = self.unsharp_mask()

        elif self.ftype == 'GRAY2RGB':
            res = self.gray2rgb()

        else:
            res = self.img

        return res

def resized_and_filtered(dirs, filtres, max_image_height, alpha, beta, sharp_profile, smooth=3):
    """
    - dirs is a list of directories in the followinf order:
        mmpose_dir, img_root, img, filtered_root
    - fltrs - list of filters
    - max_image_height - desirable image height
    - smooth - MEDIANBLUR smoothing factor
    - alpha, beta - brightness and contrast adjustable parameters
    """

    src = cv2.imread(os.path.join(dirs[0], dirs[1], dirs[2]), cv2.IMREAD_UNCHANGED)

    ### Resize
    if max_image_height:
        output, scale_pct = resize_img(src, max_image_height)
    else:
        scale_pct = 'no'
        output = src
    ###

    if filtres:
        output = Filtering(output, filtres[0], dirs, alpha, beta, sharp_profile, smooth).apply_filter()
        for i in range(1, len(filtres)):
            output = Filtering(output, filtres[i], dirs, alpha, beta, sharp_profile, smooth).apply_filter()

    out_name = '{}_{}_{}.png'.format(dirs[2].split('.')[0], scale_pct, "_".join(filtres))

    if not cv2.imwrite(os.path.join(dirs[0], dirs[3], '{}'.format(out_name)), output):
        raise Exception("Could not write image")
#     else:
#         cv2.imwrite(os.path.join(dirs[0], dirs[3], '{}'.format(out_name)), final)
    return out_name
