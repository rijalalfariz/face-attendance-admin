from .forms import KameraForm, EmployeeForm, EditEmployeeForm
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView

from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy

import datetime, json

from misweb import serializers
from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import Employee, Absensi, Kamera
# from .forms import LoginForm
from django.apps import apps

class Itterasi():
    pengaturan_itter = 1
    pegawai_itter = 0

class TestApiView(APIView):
    """Test API View"""
    serializer_class = serializers.TestSerializer

    def get(self, request, pk):
        """Returns a list of APIView features"""
        for_kamera = Kamera.objects.filter(id=pk).last()
        periode = json.loads(for_kamera.periode_absensi)

        karyawan_state = True
        for_karyawan = Employee.objects.values_list('nip', flat=True)

        cam_dict = {
            "pengaturan": Itterasi.pengaturan_itter,
            "parameter": {
                "jadwal": periode,
                'min_face_size': for_kamera.min_face_size,
                'face_threshold': for_kamera.face_threshold,
                'true_threshold': for_kamera.true_threshold,
                'input_width': for_kamera.input_width,
                'input_height': for_kamera.input_height
            },
            'karyawan': Itterasi.pegawai_itter,
            'nip': for_karyawan
        }

        return Response(cam_dict)


class AbsensiApiView(APIView):
    """Test API View"""
    serializer_class = serializers.AbsensiSerializer

    def get(self, request, format=None):
        absen = Absensi.objects.values_list('id', 'employee', 'first_seen')
        return Response({'absen': absen})
        
    def post(self, request):
        """Create a hello message with our name"""
        nip_peg = request.data.get('employee')
        id_peg_obj = Employee.objects.filter(nip=nip_peg).last()
        apikey_cam_obj = Kamera.objects.filter(id=request.data.get('kamera')).last()
        if id_peg_obj is not None and apikey_cam_obj is not None:
            id_peg = id_peg_obj.id
            apikey_cam = apikey_cam_obj.apikey
            data = {'employee':id_peg, 'kamera':request.data.get('kamera')}
            serializer = self.serializer_class(data=data)
            apikey_validation = request.data.get('apikey')

            if serializer.is_valid() and apikey_cam == apikey_validation:
                nama_pegawai = serializer.validated_data.get('employee')
                id_absen = Absensi.objects.filter(employee=nama_pegawai, first_seen__date=datetime.datetime.now())

                if id_absen.exists():
                    absen_object = Absensi.objects.get(id=id_absen.last().id)
                    absen_object.last_seen = datetime.datetime.now()
                    absen_object.save()

                    testnip = serializer.validated_data.get('employee').nip
                    message = f'Save exist {absen_object.id}, request.data = {testnip}'
                    return Response({'message': message})
                    
                else:
                    serializer.save()
                    message = f'Exist? {id_absen}, request.data = {serializer.validated_data}'
                    return Response({'message': message})
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class TestView(TemplateView):
    """To Dashboard Page"""

    template_name = "test.html"


class DashboardView(TemplateView):
    """To Dashboard Page"""

    template_name = "dashboard.html"

    def get(self, request):
        tanggal = datetime.datetime.now()
        list_absensi = Absensi.objects.filter(first_seen__date=tanggal)
        list_pegawai = Employee.objects.all()
        jml_pegawai = list_pegawai.count()
        jml_absensi = list_absensi.count()
        rasio = (jml_absensi/jml_pegawai)*100

        statusAbsensi=[]
        for pegawai in list_pegawai:
            status = list_absensi.filter(employee=pegawai.id)
            nama = pegawai.name
            statusAbsensi.append(StatusPegawai(status=status.exists(), nama=nama, id_absensi=status.last()))
                    
        context={
            'list_absensi': list_absensi,
            'hari_ini': tanggal,
            'list_pegawai': statusAbsensi,
            'rasio': rasio,
            'jml_pegawai': jml_pegawai,
            'jml_absensi': jml_absensi,
        }
        return render(request, self.template_name, context)


class DaftarHadirView(TemplateView):
    """To Page Daftar Hadir"""

    template_name = "daftar-hadir.html"

    def post(self, request):
        tanggal = request.POST.get('tanggal')
        list_absensi = Absensi.objects.filter(first_seen__date=tanggal)
        list_pegawai = Employee.objects.all()
        
        statusAbsensi=[]
        for pegawai in list_pegawai:
            status = list_absensi.filter(employee=pegawai.id)
            nama = pegawai.name
            statusAbsensi.append(StatusPegawai(status=status.exists(), nama=nama, id_absensi=status.last()))

        context={
            'list_absensi': list_absensi,
            'hari_ini': tanggal,
            'list_pegawai': statusAbsensi,
        }
        return render(request, self.template_name, context)

    def get(self, request):
        tanggal = datetime.datetime.now()
        list_absensi = Absensi.objects.filter(first_seen__date=tanggal)
        list_pegawai = Employee.objects.all()

        statusAbsensi=[]
        for pegawai in list_pegawai:
            status = list_absensi.filter(employee=pegawai.id)
            nama = pegawai.name
            statusAbsensi.append(StatusPegawai(status=status.exists(), nama=nama, id_absensi=status.last()))

        context={
            'list_absensi': list_absensi,
            'hari_ini': tanggal,
            'list_pegawai': statusAbsensi,
        }
        return render(request, self.template_name, context)


class AbsensiSayaView(TemplateView):
    """To Page Daftar Hadir"""

    template_name = "absensi-saya.html"

    def get(self, request):
        tanggal = datetime.datetime.now()
        list_absensi = Absensi.objects.filter(first_seen__date=tanggal)
        list_pegawai = Employee.objects.all()

        statusAbsensi=[]
        for pegawai in list_pegawai:
            status = list_absensi.filter(employee=pegawai.id)
            nama = pegawai.name
            statusAbsensi.append(StatusPegawai(status=status.exists(), nama=nama, id_absensi=status.last()))

        context={
            'list_absensi': list_absensi,
            'hari_ini': tanggal,
            'list_pegawai': statusAbsensi,
        }
        return render(request, self.template_name, context)


class ListPegawaiView(TemplateView):
    """To Page Daftar Hadir"""

    template_name = "list-pegawai.html"

    def get(self, request):
        list_pegawai = Employee.objects.all()
        context={
            'list_pegawai': list_pegawai,
        }
        return render(request, self.template_name, context)


class TambahPegawaiView(CreateView):
    # specify the model for create view
    template_name = 'misweb/employee_form.html'
    success_url = reverse_lazy('list-pegawai')
    form_class = EmployeeForm

    def post(self, request):
        form = EmployeeForm(request.POST, request.FILES)
        print(form.errors)

        if form.is_valid():
            print("valid")
            Itterasi.pegawai_itter = Itterasi.pegawai_itter + 1
            form.save()

        context={
            'form': EmployeeForm,
        }
        return redirect(self.success_url)


class EditPegawaiView(FormView):
    # specify the model you want to use
    success_url = '/list-pegawai/'
    template_name = 'misweb/employee_update_form.html'
    form_class = EditEmployeeForm

    def get(self, request, pk):
        id_peg = pk
        peg = Employee.objects.filter(id=id_peg).last()
        form = EditEmployeeForm(instance=peg)

        context={
            'object': peg,
            'form': form,
        }
        return render(request, self.template_name, context)


    def post(self, request, pk):
        pegawai = Employee.objects.filter(id=pk).last()
        form = EditEmployeeForm(request.POST, request.FILES, instance=pegawai)
        if request.FILES:
            delete_model(request, pk)

        if form.is_valid():
            print("valid")
            Itterasi.pegawai_itter = Itterasi.pegawai_itter + 1
            form.save()

        context={
            'form': EmployeeForm,
        }
        return redirect(self.success_url)


class PengaturanView(UpdateView):
    """To Page Daftar Hadir"""

    model = Kamera
    success_url = '/pengaturan/1/'
    template_name_suffix = '_update_form'
    fields = [
        'periode_absensi',
        'min_face_size',
        'face_threshold',
        'true_threshold',
        'input_width',
        'input_height',
    ]

    def post(self, request, pk):
        for_kamera = request.POST.get('for-camera')
        if for_kamera == None:
            for_kamera = pk
        list_kamera = Kamera.objects.all()
        kamera = Kamera.objects.filter(id=for_kamera).last()
        form = KameraForm(request.POST, instance=kamera)

        if form.is_valid():
            Itterasi.pengaturan_itter = Itterasi.pengaturan_itter + 1
            form.save()

        context={
            'kamera': kamera,
            'list_kamera': list_kamera,
            'for_kamera': for_kamera,
            'form': KameraForm,
        }
        return redirect('pengaturan', for_kamera)

    def get(self, request, pk):
        for_kamera = pk
        list_kamera = Kamera.objects.all()
        kamera = Kamera.objects.filter(id=for_kamera).last()
        form = KameraForm(instance=kamera)

        context={
            'kamera': kamera,
            'list_kamera': list_kamera,
            'for_kamera': for_kamera,
            'form': form,
        }
        return render(request, 'misweb/kamera_update_form.html', context)


class StatusPegawai():
    def __init__(self, nama, status, id_absensi):
        self.nama = nama
        self.status = status
        self.id_absensi = id_absensi


def delete_model(request, pk):
    item = get_object_or_404(Employee, id=pk)
    if item:
        Itterasi.pegawai_itter = Itterasi.pegawai_itter + 1
        ref = item.id
        item.delete()
        data = {'ref': ref, 'message': 'Object with id %s has been deleted' %ref}
        return JsonResponse(data)

