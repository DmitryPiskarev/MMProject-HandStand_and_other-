# Generated by Django 3.2.5 on 2021-09-15 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hscresinterpretation',
            name='users_handstandC',
        ),
    ]
