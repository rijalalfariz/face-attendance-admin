# **Face Recognition Attendance Web Management System**

```
Attendance System Using Face Recognition with NCNN
```

This projects have camera programs that run in Raspberry pi 3 up to 10+ fps (see [Facecam Repo](https://github.com/rijalalfariz/face-cam-cpp)), connected with django-restframework to MIS website for attendance maagement and information built with django.

---

## Dependencies

- Python
- MySQL Database (You can change yours also)
- XAMPP
- + requirements.txt

---

## Run

- Create your python virtual environment, activate it
- Create the database (not for the tables yet)

```shell
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

`python manage.py runserver` is added with `0.0.0.0:8000` so it can connects to camera devices (using network, or LAN)
if you run the camera programs to your own pc, its free to not include `0.0.0.0:8000`

---
