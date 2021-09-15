from os.path import join

from PIL import Image
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from .settings import BASE_DIR, MEDIA_ROOT
from django.utils.encoding import smart_str
import os
import PIL
import io
import sys

# a=str(BASE_DIR)
# print(a[:-11])
# sys.path.append(a[:-10])
# from our_mm_get import get_img_result


def index(request):
    return HttpResponse('BodySkills')


def give_img(request):
    img = 'tst_img4.png'
    response = HttpResponse(content_type='image/png')
    # response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('tst_img1.png')
    # response['X-Sendfile'] = smart_str(os.path.join(BASE_DIR, MEDIA_ROOT, 'good_img'))
    img = Image.open(os.path.join(BASE_DIR, MEDIA_ROOT, 'good_img', img))
    img.save(response, 'png')
    return response


@csrf_exempt
def img_in(request):
    if request.method == 'POST':
        img_b = request.FILES['image']
        img = Image.open(io.BytesIO(img_b.read()))
        users_path = 'user1'
        users_img_name = 'photo_name.jpg'
        dir_output = f'{MEDIA_ROOT}/{users_path}/'
        if not os.path.isdir(dir_output):
            os.mkdir(dir_output)
        img.save(f'{dir_output}/{users_img_name}')
        # get_img_result(img_name=users_img_name, img_root_dir=dir_output, f_root_dir=dir_output,
        #                     img_out_dir=dir_output, plot_all=False, plot_res=False)
    return HttpResponse('BodySkills')
