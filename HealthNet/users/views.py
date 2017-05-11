from django.conf import settings
from django.template.loader import get_template
from django.template import RequestContext
from django.views.static import serve
import os, tempfile, zipfile
from importlib import import_module
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf
from .form import *
from .models import *
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import ListView, DetailView, View, RedirectView
from django.core.urlresolvers import reverse, reverse_lazy
from users.form import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import send_mail, BadHeaderError
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import DeleteView
from django.http import Http404, HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import json
import datetime

def download(request, pk):
    filename =pk 
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition']='attachment: filename=%s' % filename
    return response

def export_view(request):

    user = request.user
    patient = Patient.objects.get(user_ptr=user)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="patient_info.pdf"'

    p = canvas.Canvas(response, pagesize=letter)

    width, height = letter
    p.setLineWidth(.3)
    p.setFont('Helvetica', 25)
    p.drawString(10, height-50, "PATIENT: " + user.first_name + " " + user.last_name)
    p.drawString(10, height-100, "Gender: " + patient.gender)
    p.drawString(10, height-150, "Email: " + user.email)
    p.drawString(10, height-200, "Birthday: " + patient.birthday.strftime('%m/%d/%y'))
    p.drawString(10, height-250, "Proof of Insurance Company: " + patient.proof_of_insurance_company)
    p.drawString(10, height-300, "Proof of Insurance: " + str(patient.proof_of_insurance_id))
    p.drawString(10, height-350, "Medical info: " + patient.medical_info)
    p.drawString(10, height-400, "Hospital: " + patient.hospital.__str__())
    p.drawString(10, height-450, "Phone Number: " + patient.phone_number)

    p.showPage()
    p.save()
    return response

class createUser(CreateView):
    model = Patient
    form_class = RegistrationForm
    template_name = 'register.html'

    def get_success_url(self):
        patient = Patient.objects.last()
        ActivityLog.objects.create(hospital=patient.hospital, first_name=patient.first_name, last_name=patient.last_name,
        action='Created a Healthnet Account', target_first='', target_last='',date=datetime.date.today(), time=datetime.datetime.now())
        return '/'

class createAdmin(CreateView):
    model = HospitalAdmin
    form_class = AdminForm
    template_name = 'register_admin.html'

    def get_success_url(self):
        current_user = self.request.user
        admin = HospitalAdmin.objects.last()
        hospital = Hospital.objects.get(hospitaladmin=admin)
        ActivityLog.objects.create(hospital=hospital, first_name=current_user, last_name='',
                                   action='Created a Healthnet Account for ', target_first=admin.first_name,
                                   target_last=admin.last_name, date=datetime.date.today(), time=datetime.datetime.now())
        return '/'


class createHospital(CreateView):
    model = Hospital
    form_class = HospitalForm
    template_name = 'hospital.html'

    def get_success_url(self):
        current_user = self.request.user
        hospital = Hospital.objects.last()
        ActivityLog.objects.create(hospital=hospital, first_name=current_user, last_name='',
                                   action='Created a Hospital', target_first='', target_last='',
                                   date=datetime.date.today(), time=datetime.datetime.now())
        return '/'

def patient_detail(request):
    current_user = request.user
    if Patient.objects.filter(user_ptr=current_user).exists():
        return render(request, 'patient_detail.html', {'info': Patient.objects.get(user_ptr=current_user)})
    return None


class updateUserInformation(UpdateView):
    model = Patient
    template_name = 'update.html'
    fields = ['username', 'first_name', 'last_name', 'gender', 'birthday', 'email'
                  , 'proof_of_insurance_company', 'proof_of_insurance_id', 'medical_info','medical_file', 'phone_number']

    def get_success_url(self):
        current_user = self.request.user
        patient = Patient.objects.get(user_ptr=current_user)
        ActivityLog.objects.create(hospital=patient.hospital, first_name=patient.first_name, last_name=patient.last_name,
                                   action='Updated their user information', target_first='',
                                   target_last='', date=datetime.date.today(), time=datetime.datetime.now())
        return '/'

    def get_object(self):
        current_user = self.request.user
        info = Patient.objects.get(user_ptr=current_user)
        return info

class createPerscription(CreateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'createPrescription.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.doctor = Doctor.objects.get(user_ptr=self.request.user)
        return super(createPerscription, self).form_valid(form)

    def get_success_url(self):
        current_user = self.request.user
        doctor = Doctor.objects.filter(user_ptr=current_user)
        hospital = Hospital.objects.get(doctor=doctor)
        prescription = Prescription.objects.last()
        ActivityLog.objects.create(hospital=hospital, first_name=current_user.first_name, last_name=current_user.last_name,action='Created Prescription for ', target_first=prescription.patient_name.first_name,target_last=prescription.patient_name.last_name, date=datetime.date.today(),time=datetime.datetime.now())
        return '/'

class updatePrescription(UpdateView):
    model = Prescription
    template_name = 'updatePrescription.html'
    
    fields=['prescription_name', 'dosage', 'Taken_Per_Day']

    def get_success_url(self, **kwargs):
        current_user = self.request.user
        doctor = Doctor.objects.filter(user_ptr=current_user)
        hospital = Hospital.objects.get(doctor=doctor)
        prescription = Prescription.objects.get(id=self.kwargs['pk'])
        ActivityLog.objects.create(hospital=hospital, first_name=current_user.first_name,
                                   last_name=current_user.last_name,action='Updated Prescription for ',
                                   target_first=prescription.patient_name.first_name,target_last=prescription.patient_name.last_name,
                                   date=datetime.date.today(),time=datetime.datetime.now())
        return reverse('view_prescriptionsD')
    
    def get_context_data(self, **kwargs):
        context = super(updatePrescription, self).get_context_data(**kwargs)
        context['action'] = reverse('edit_prescription', kwargs={'pk': self.get_object().id})

        return context


class deletePrescription(DeleteView):
    model = Prescription
    template_name = 'prescription_confirm_delete.html'

    def get_success_url(self):
        current_user = self.request.user
        doctor = Doctor.objects.filter(user_ptr=current_user)
        hospital = Hospital.objects.get(doctor=doctor)
        ActivityLog.objects.create(hospital=hospital, first_name=current_user.first_name, last_name=current_user.last_name,
                                   action='Deleted a Prescription ', target_first='',
                                   target_last='', date=datetime.date.today(),
                                   time=datetime.datetime.now())
        return reverse('view_prescriptionsD')

    def get_object(self, queryset=None):
        qs = super(deletePrescription, self).get_object()
        return qs


def view_prescriptions(request):
    current_user = request.user
    prescriptions = Prescription.objects.filter(patient_name__user_ptr=current_user)
    return render(request, 'users/Prescription_view.html', {'prescriptions':prescriptions})

def view_prescriptionsD(request):
    prescriptions = Prescription.objects.all()
    return render(request, 'users/Prescription_viewD.html', {'prescriptions':prescriptions})

def view_prescriptionsN(request):
    current_user = request.user
    nurse = Nurses.objects.filter(user_ptr=current_user)
    hospital = Hospital.objects.filter(nurses=nurse)
    patients = Patient.objects.filter(hospital=hospital)
    prescriptions = Prescription.objects.filter(patient_name__in=patients)
    return render(request, 'users/Prescription_viewN.html', {'prescriptions': prescriptions})


class createTestsandResults(CreateView):
    model = Test_Results
    form_class = TestsandResultsForm
    template_name = 'createTestandResults.html'

    def get_success_url(self):
        current_user = self.request.user
        doctor = Doctor.objects.filter(user_ptr=current_user)
        hospital = Hospital.objects.get(doctor=doctor)
        test = Test_Results.objects.last()
        ActivityLog.objects.create(hospital=hospital, first_name=current_user.first_name, last_name=current_user.last_name,
                                   action='Created a Test for ', target_first=test.patient_name.first_name,
                                   target_last=test.patient_name.last_name, date=datetime.date.today(),
                                   time=datetime.datetime.now())
        return '/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.doctor = Doctor.objects.get(user_ptr=self.request.user)
        return super(createTestsandResults, self).form_valid(form)

def view_tests(request):
    current_user = request.user
    tests_and_results = Test_Results.objects.filter(patient_name__user_ptr=current_user)
    return render(request, 'users/Tests_view.html', {'tests':tests_and_results})

def view_testsD(request):
    current_user = request.user
    tests_and_results = Test_Results.objects.filter(doctor__user_ptr=current_user)
    return render(request, 'users/TestANDResults_view.html', {'tests':tests_and_results})

def view_testsN(request):
    current_user = request.user
    nurse = Nurses.objects.get(user_ptr=current_user)
    patients = Patient.objects.filter(hospital=nurse.hospital)
    tests_and_results = Test_Results.objects.filter(patient_name__in=patients)
    return render(request, 'users/test_viewN.html', {'tests':tests_and_results})

def view_results(request):
    current_user = request.user
    tests_and_results = Test_Results.objects.filter(patient_name__user_ptr=current_user, release=True)
    return render(request, 'users/Results_view.html', {'tests': tests_and_results})

class updateTestsandResults(UpdateView):
    model = Test_Results
    form_class = TestsandResultsForm
    template_name = 'updateTestandResults.html'
    success_url = '/'

    def get_success_url(self):
        current_user = self.request.user
        doctor = Doctor.objects.filter(user_ptr=current_user)
        hospital = Hospital.objects.get(doctor=doctor)
        test = Test_Results.objects.get(id=self.kwargs['pk'])
        ActivityLog.objects.create(hospital=hospital, first_name=current_user.first_name,
                                   last_name=current_user.last_name,
                                   action='Updated Prescription for ', target_first=test.patient_name.first_name,
                                   target_last=test.patient_name.last_name, date=datetime.date.today(),
                                   time=datetime.datetime.now())
        return reverse('view_testsD')

    def get_context_data(self, **kwargs):
        context = super(updateTestsandResults, self).get_context_data(**kwargs)
        context['action'] = reverse('edit_test', kwargs={'pk': self.get_object().id})

        return context


class deleteTestsandResults(DeleteView):
    model = Test_Results
    template_name = 'prescription_confirm_delete.html'

    def get_success_url(self):
        current_user = self.request.user
        doctor = Doctor.objects.filter(user_ptr=current_user)
        hospital = Hospital.objects.get(doctor=doctor)
        ActivityLog.objects.create(hospital=hospital, first_name=current_user.first_name,
                                   last_name=current_user.last_name,
                                   action='Deleted a Test ', target_first='',
                                   target_last='', date=datetime.date.today(),
                                   time=datetime.datetime.now())
        return reverse('view_testsD')

    def get_object(self, queryset=None):
        qs = super(deleteTestsandResults, self).get_object()
        return qs

class createAppointment(CreateView):
    model = Appointment
    form_class = AppointmentFormPatient
    template_name = "createAppointment.html"

    def get_success_url(self):
        current_user = self.request.user
        user = Patient.objects.filter(user_ptr=current_user)
        hospital = Hospital.objects.get(patient=user)
        appointment = Appointment.objects.last()
        target = appointment.doctor
        ActivityLog.objects.create(hospital=hospital, first_name=current_user.first_name, last_name=current_user.last_name,
                                   action='Created an Appointment for ', target_first=target.first_name,
                                   target_last=target.last_name, date=datetime.date.today(),
                                   time=datetime.datetime.now())
        return '/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.patient = Patient.objects.get(user_ptr=self.request.user)
        return super(createAppointment, self).form_valid(form)

class createAppointmentDoctor(CreateView):
    model = Appointment
    form_class = AppointmentFormDoctor
    template_name = "createAppointment.html"

    def get_success_url(self):
        current_user = self.request.user
        user = Doctor.objects.filter(user_ptr=current_user)
        hospital = Hospital.objects.get(doctor=user)
        appointment = Appointment.objects.last()
        target = appointment.patient
        ActivityLog.objects.create(hospital=hospital, first_name=current_user.first_name, last_name=current_user.last_name,
                                   action='Created an Appointment for ', target_first=target.first_name,
                                   target_last=target.last_name, date=datetime.date.today(),
                                   time=datetime.datetime.now())
        return '/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.doctor = Doctor.objects.get(user_ptr=self.request.user)
        return super(createAppointmentDoctor, self).form_valid(form)

class createAppointmentNurse(CreateView):
    model = Appointment
    form_class = AppointmentFormNurse
    template_name = "createAppointment.html"

    def get_success_url(self):
        current_user = self.request.user
        user = Nurses.objects.filter(user_ptr=current_user)
        hospital = Hospital.objects.get(nurses=user)
        appointment = Appointment.objects.last()
        target = appointment.patient
        ActivityLog.objects.create(hospital=hospital, first_name=current_user.first_name, last_name=current_user.last_name,
                                   action='Created an Appointment for ', target_first=target.first_name,
                                   target_last=target.last_name, date=datetime.date.today(),
                                   time=datetime.datetime.now())
        return '/'

class updateAppointment(UpdateView):
    model = Appointment
    template_name = 'updateAppointment.html'
    fields = ['date', 'description', 'doctor', 'patient']

    def get_success_url(self):
        return reverse('view_appointments')

    def get_context_data(self, **kwargs):
        context = super(updateAppointment, self).get_context_data(**kwargs)
        context['action'] = reverse('edit_appointment', kwargs={'pk': self.get_object().id})

        return context


class deleteAppointment(DeleteView):
    model = Appointment
    template_name = 'appointment_confirm_delete.html'

    def get_success_url(self):
        current_user = self.request.user
        if Doctor.objects.filter(user_ptr=current_user).exists():
            doctor = Doctor.objects.filter(user_ptr=current_user)
            hospital = Hospital.objects.get(doctor=doctor)
        if Nurses.objects.filter(user_ptr=current_user).exists():
            nurse = Nurses.objects.filter(user_ptr=current_user)
            hospital = Hospital.objects.get(nurse=nurse)
        if Patient.objects.filter(user_ptr=current_user).exists():
            patient = Patient.objects.filter(user_ptr=current_user)
            hospital = Hospital.objects.get(patient=patient)
        ActivityLog.objects.create(hospital=hospital, first_name=current_user.first_name,
                                   last_name=current_user.last_name,
                                   action='Deleted an Appointment ', target_first='',
                                   target_last='', date=datetime.date.today(),
                                   time=datetime.datetime.now())
        return reverse('view_appointments')

    def get_object(self, queryset=None):
        qs = super(deleteAppointment, self).get_object()
        return qs


def view_appointments(request):
    current_user = request.user
    if Doctor.objects.filter(user_ptr=current_user).exists():
        appointments = Appointment.objects.filter(doctor__user_ptr=current_user)
        return render_to_response('users/calendar_view.html', {'appointments': appointments})
    if Nurses.objects.filter(user_ptr=current_user).exists():
        nurse = Nurses.objects.filter(user_ptr=current_user)
        hospital = Hospital.objects.filter(nurses=nurse)
        patients = Patient.objects.filter(hospital=hospital)
        appointments = Appointment.objects.filter(patient__in=patients)
        return render_to_response('users/calendar_viewP.html', {'appointments': appointments})
    if Patient.objects.filter(user_ptr=current_user).exists():
        appointments = Appointment.objects.filter(patient__user_ptr=current_user)
        return render_to_response('users/calendar_view.html', {'appointments': appointments})

class createDoctor(CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'register_doctor.html'

    def get_success_url(self):
        current_user = self.request.user
        if HospitalAdmin.objects.filter(user_ptr=current_user).exists():
            admin = HospitalAdmin.objects.get(user_ptr=current_user)
            doctor = Doctor.objects.last()
            hospital = Hospital.objects.get(hospitaladmin=admin)
            ActivityLog.objects.create(hospital=hospital, first_name=current_user.first_name,
                                       last_name=current_user.last_name,
                                       action='Created a Healthnet Account for ', target_first=doctor.first_name,
                                       target_last=doctor.last_name, date=datetime.date.today(),
                                       time=datetime.datetime.now())
        if self.request.user.is_superuser:
            doctor = Doctor.objects.last()
            hospital = Hospital.objects.get(doctor=doctor)
            ActivityLog.objects.create(hospital=hospital, first_name=current_user, last_name='',
                                       action='Created a Healthnet Account for ', target_first=doctor.first_name,
                                       target_last=doctor.last_name, date=datetime.date.today(),
                                       time=datetime.datetime.now())
        return '/'

class createNurse(CreateView):
    model = Nurses
    form_class = NurseForm
    template_name = 'register_nurse.html'

    def get_success_url(self):
        current_user = self.request.user
        if HospitalAdmin.objects.filter(user_ptr=current_user).exists():
            admin = HospitalAdmin.objects.get(user_ptr=current_user)
            nurse = Nurses.objects.last()
            hospital = Hospital.objects.get(hospitaladmin=admin)
            ActivityLog.objects.create(hospital=hospital, first_name=current_user.first_name, last_name=current_user.last_name,
                                       action='Created a Healthnet Account for ', target_first=nurse.first_name,
                                       target_last=nurse.last_name, date=datetime.date.today(),
                                       time=datetime.datetime.now())
        if self.request.user.is_superuser:
            nurse = Nurses.objects.last()
            hospital = Hospital.objects.get(nurses=nurse)
            ActivityLog.objects.create(hospital=hospital, first_name=current_user, last_name='',
                                       action='Created a Healthnet Account for ', target_first=nurse.first_name,
                                       target_last=nurse.last_name, date=datetime.date.today(), time=datetime.datetime.now())
        return '/'


def AdmitView(self):
    patients = Patient.objects.all()
    return render_to_response('Select.html', {'patients': patients})

class Admit(UpdateView):
    model = Patient
    template_name = 'Admit.html'
    fields = ['status']

    def get_success_url(self):
        return reverse('AdmitView')

    def get_context_data(self, **kwargs):
        context = super(Admit, self).get_context_data(**kwargs)
        context['action'] = reverse('Admit', kwargs={'pk': self.get_object().id})

        return context

def TransferView(request):
    current_user = request.user
    doctor = Doctor.objects.filter(user_ptr=current_user)
    hospital = Hospital.objects.filter(doctor=doctor)
    patients = Patient.objects.filter(hospital=hospital)
    return render_to_response('transfer.html', {'patients': patients})

class Transfer(UpdateView):
    model = Patient
    template_name = 'transferPatient.html'
    fields = ['hospital']

    def get_success_url(self):
        return reverse('TransferView')

    def get_context_data(self, **kwargs):
        context = super(Transfer, self).get_context_data(**kwargs)
        context['action'] = reverse('Transfer', kwargs={'pk': self.get_object().id})

        return context


def patview(request):
    current_user = request.user
    if Doctor.objects.filter(user_ptr=current_user).exists():
        doctor = Doctor.objects.filter(user_ptr=current_user)
        hospital = Hospital.objects.filter(doctor=doctor)
        patients = Patient.objects.filter(hospital=hospital)
    if Nurses.objects.filter(user_ptr=current_user).exists():
        nurse = Nurses.objects.filter(user_ptr=current_user)
        hospital = Hospital.objects.filter(nurses=nurse)
        patients = Patient.objects.filter(hospital=hospital)
    return render_to_response('updateView.html', {'patients': patients})


class UpdateMed(UpdateView):
    model = Patient
    template_name = 'updateMed.html'
    fields = ['medical_file', 'medical_info']

    def get_success_url(self):
        return reverse('view_med')

    def get_context_data(self, **kwargs):
        context = super(UpdateMed, self).get_context_data(**kwargs)
        context['action'] = reverse('edit_med', kwargs={'pk': self.get_object().id})

        return context

#These have not been implemented in the forms yet
class createPrivateMessage(CreateView):
    model = PrivateMessage
    #form_class = PrivateMessageForm

def view_appointment_Calendar(request):
    current_user = request.user
    if Doctor.objects.filter(user_ptr=current_user).exists():
        appointments = Appointment.objects.filter(doctor__user_ptr=current_user)
    if Nurses.objects.filter(user_ptr=current_user).exists():
        nurse = Nurses.objects.filter(user_ptr=current_user)
        hospital = Hospital.objects.filter(nurses=nurse)
        patients = Patient.objects.filter(hospital=hospital)
        appointments = Appointment.objects.filter(patient__in=patients)
    if Patient.objects.filter(user_ptr=current_user).exists():
        appointments = Appointment.objects.filter(patient__user_ptr=current_user)
    return render(request, 'Calendar/calendarView.html', {'appointments' : appointments})

#This is a really unfunctional login page just to check the url
#def loginPage(request):
#    c ={ }
#    c.update(csrf(request))
#    return render_to_response('users/login.html',c)
#def auth_view(request):
#    username = request.POST.get('username','')
#    password = request.POST.get('password','')
#    user = auth.authenticate(username=username,password=password)
#
#    if user is not None:
#        auth.login(request,user)
#        return HttpResponseRedirect('users/loggedin')
#    else:
#        return HttpResponseRedirect('users/invalid')

def loggedin(request):
    return render_to_response('users/loggedin.html',
                              {'full_name':request.user.username})

def invalid_login(request):
    return render_to_response('invalid_login.html')


class LogoutView(RedirectView):
    url = '/'
    def get(self,request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/users/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response(
        'users/register.html',
        variables,
    )


def register_success(request):
    return render_to_response(
        'users/success.html',
    )


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def email(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('thanks')
    return render(request, "email.html", {'form': form})

def thanks(request):
    return HttpResponse('Thank you for your message.')


@login_required
def home(request):
    current_user = request.user
    if Patient.objects.filter(user_ptr=current_user).exists():
        return render_to_response('home.html', {'user': current_user})
    if Nurses.objects.filter(user_ptr=current_user).exists():
        return render_to_response('NurseHome.html', {'user': current_user})
    if Doctor.objects.filter(user_ptr=current_user).exists():
        return render_to_response('DoctorHome.html', {'user': current_user})
    if HospitalAdmin.objects.filter(user_ptr=current_user).exists():
        return render_to_response('HAdminHome.html', {'user': current_user})
    if request.user.is_superuser:
        return render_to_response('AdminHome.html', {'user': current_user})
    return render(request, 'home.html')


def about(request):
    return render_to_response('about.html')


def statistics(request):
    current_user = request.user
    admin = HospitalAdmin.objects.filter(user_ptr=current_user)
    hospitals = Hospital.objects.filter(hospitaladmin=admin)
    hospital = Hospital.objects.get(hospitaladmin=admin)
    patient = Patient.objects.filter(hospital=hospitals)
    doctor = Doctor.objects.filter(hospital=hospitals)
    nurse = Nurses.objects.filter(hospital=hospitals)
    return render_to_response('Statistics.html', {'hospital': hospital, 'patient': patient, 'doctor': doctor,
                                                  'nurse': nurse})

def SystemActivityLog(request):
    current_user = request.user
    admin = HospitalAdmin.objects.filter(user_ptr=current_user)
    hospitals = Hospital.objects.filter(hospitaladmin=admin)
    hospital = Hospital.objects.get(hospitaladmin=admin)
    activities = ActivityLog.objects.filter(hospital=hospitals)
    return render_to_response('ActivityLog.html', {'hospital': hospital, 'activities': activities})
