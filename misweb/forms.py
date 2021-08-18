from django import forms
from django.forms import widgets
from .models import Employee, Kamera 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
 
# creating a form
class EmployeeForm(UserCreationForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Employee
        # specify fields to be used
        fields = [
            'nip',
            'name',
            'image',
        ]

class EditEmployeeForm(UserChangeForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Employee
        # specify fields to be used
        fields = [
            'is_staff',
            'nip',
            'name',
            'image',
        ]

class KameraForm(forms.ModelForm):

    class Meta:
        model = Kamera
        fields = [
            'periode_absensi',
            'min_face_size',
            'face_threshold',
            'true_threshold',
            'input_width',
            'input_height',
        ]