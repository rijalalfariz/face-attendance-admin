# Generated by Django 3.2.3 on 2021-07-08 04:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('misweb', '0007_auto_20210708_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absensi',
            name='kamera',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='misweb.kamera'),
        ),
    ]
