# Generated by Django 3.2.3 on 2021-07-08 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('misweb', '0021_remove_absensi_kamera'),
    ]

    operations = [
        migrations.AddField(
            model_name='absensi',
            name='kamera',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='misweb.kamera'),
        ),
    ]
