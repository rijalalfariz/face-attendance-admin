# Generated by Django 3.2.3 on 2021-07-08 04:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('misweb', '0016_alter_absensi_kamera'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='absensi',
            name='kamera',
        ),
    ]
