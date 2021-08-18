from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, BaseUserManager
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
import datetime

import os



def image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.nip}.jpg'

    return os.path.join('faceimg', filename)


class EmployeeManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, nip, name, image, password=None):
        """Create a new user profiles"""
        if not nip:
            raise ValueError('NIP tidak valid')

        user = self.model(nip=nip, name=name, image=image)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, nip, name, image, password):
        """Create a new superuser with given details"""
        user = self.create_user(nip, name, image, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class Employee(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    nip = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to = image_path)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = EmployeeManager()

    USERNAME_FIELD = 'nip'
    REQUIRED_FIELDS = ['name', 'image']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of our user"""
        return self.name
    
    def delete_url(self):
        return reverse('hapus-pegawai', kwargs={'pk': self.id})

class Kamera(models.Model):
    """Handle attendance"""
    apikey = models.CharField(max_length=255)
    nama_kamera = models.CharField(max_length=255)
    periode_absensi = models.TextField()
    min_face_size = models.IntegerField()
    face_threshold = models.DecimalField(decimal_places=2, max_digits=4)
    true_threshold = models.DecimalField(decimal_places=2, max_digits=4)
    input_width = models.IntegerField()
    input_height = models.IntegerField()

    def __str__(self):
        return self.nama_kamera

class Absensi(models.Model):
    """Handle attendance"""
    employee = models.ForeignKey("misweb.Employee", on_delete=models.CASCADE)
    kamera = models.ForeignKey("misweb.Kamera", on_delete=models.CASCADE, default=-1)
    first_seen = models.DateTimeField(auto_now=False, default=timezone.now)
    last_seen = models.DateTimeField(auto_now=False, default=timezone.now)

    def __str__(self):
        return self.employee.name
