from django.db import models
from django.contrib.auth.models import User
from BodySkills.settings import MEDIA_ROOT


class BSUser(User):
    pass_hash = models.CharField(
        verbose_name='pass_hash',
        max_length=200,
        blank=True
    )
    is_deleted = models.BooleanField(default=False)


class BSUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(BSUser, unique=True,
                                null=False,
                                db_index=True,
                                on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='users_avatars',
        blank=True
    )
    age = models.IntegerField(
        verbose_name='возраст',
        blank=True,
        null=True,
        default=18,
    )
    aboutMe = models.TextField(verbose_name='о себе',
                               max_length=512,
                               blank=True)
    gender = models.CharField(verbose_name='пол',
                              max_length=1,
                              choices=GENDER_CHOICES,
                              blank=True)


class HandstandClassic(models.Model):
    user_id = models.ForeignKey(BSUser, on_delete=models.CASCADE)

    img_in_path = models.CharField(
        verbose_name='Путь к входящему фото',
        max_length=200,
        blank=True
    )
    result = models.CharField(
        verbose_name='Результат',
        max_length=200,
        blank=True
    )
    img_out_path = models.CharField(
        verbose_name='Путь к обработанному фото',
        max_length=200,
        blank=True
    )
    date = models.DateTimeField(
        verbose_name='время',
        auto_now_add=True,
    )


class HsCResInterpretation(models.Model):
    # users_handstandC = models.ForeignKey(HandstandClassic, on_delete=models.DO_NOTHING)
    WES = models.TextField(
        verbose_name='Путь к WES проблемам',
        max_length=300,
        blank=True
    )
    WSH = models.TextField(
        verbose_name='Путь к WSH проблемам',
        max_length=300,
        blank=True
    )
    WSK = models.TextField(
        verbose_name='Путь к WSK проблемам',
        max_length=300,
        blank=True
    )
    SHK = models.TextField(
        verbose_name='Путь к SHK проблемам',
        max_length=300,
        blank=True
    )
    HKA = models.TextField(
        verbose_name='Путь к HKA проблемам',
        max_length=300,
        blank=True
    )
    WHA = models.TextField(
        verbose_name='Путь к WHA проблемам',
        max_length=300,
        blank=True
    )
