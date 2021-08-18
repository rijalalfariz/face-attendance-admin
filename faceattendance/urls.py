"""faceattendance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.conf.urls.static import static
from django.conf import settings

from misweb.views import (
    DashboardView,
    DaftarHadirView,
    ListPegawaiView,
    PengaturanView,
    TambahPegawaiView,
    EditPegawaiView,
    delete_model,
    TestView,
    TestApiView,
    AbsensiApiView,
    AbsensiSayaView
    )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', DashboardView.as_view(), name='dashboard'),
    path('test/', TestView.as_view(), name='test'),
    path('daftar-hadir/', DaftarHadirView.as_view(), name='daftar-hadir'),
    path('absensi-saya/', AbsensiSayaView.as_view(), name='absensi-saya'),

    path('list-pegawai/', ListPegawaiView.as_view(), name='list-pegawai'),
    path('tambah-pegawai/', TambahPegawaiView.as_view(), name='tambah-pegawai'),
    path('edit-pegawai/<pk>/', EditPegawaiView.as_view(), name='edit-pegawai'),
    path('hapus-pegawai/<pk>/', delete_model, name='hapus-pegawai'),

    path('test-api-view/<pk>/', TestApiView.as_view()),
    path('absensi-api-view/', AbsensiApiView.as_view()),

    path('pengaturan/<pk>/', PengaturanView.as_view(), name='pengaturan'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
