# Generated by Django 3.2.3 on 2021-07-08 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('misweb', '0013_auto_20210708_1124'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kamera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apikey', models.CharField(max_length=255)),
                ('nama_kamera', models.CharField(max_length=255)),
                ('periode_absensi', models.CharField(max_length=255)),
                ('min_face_size', models.IntegerField()),
                ('face_threshold', models.DecimalField(decimal_places=2, max_digits=4)),
                ('true_threshold', models.DecimalField(decimal_places=2, max_digits=4)),
                ('input_width', models.IntegerField()),
                ('input_height', models.IntegerField()),
            ],
        ),
    ]
