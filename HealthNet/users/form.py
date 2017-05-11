from django import forms
from .models import Patient, Nurses, Prescription, Test_Results, Appointment, Doctor, Hospital, HospitalAdmin
from django.contrib.auth.forms import UserCreationForm


GENDER_CHOICES = (
    ('Please select...', 'Please select...'),
    ('Male', 'Male'),
    ('Female', 'Female')
)
RELEASE = (
    ('True', 'Release'),
    ('False', 'Do Not Release')
)


class RegistrationForm(UserCreationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
    birthday = forms.DateField(help_text='Please Enter In Format: MM/DD/YYYY',required = True)
    proof_of_insurance_id = forms.IntegerField(required = True)
    proof_of_insurance_company = forms.CharField(required=True)
    medical_info = forms.CharField(required = True)
    medical_file = forms.FileField(label = 'Select a file', help_text='max. 42 megabytes', required = False)
    phone_number = forms.CharField(required = True)
    gender = forms.ChoiceField(required=True, choices=GENDER_CHOICES)
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=True)
    status = forms.ChoiceField(widget = forms.HiddenInput(), required = False)

    class Meta:
        model = Patient
        fields = ('username', 'first_name', 'last_name', 'gender', 'birthday', 'email'
                  , 'proof_of_insurance_id', 'proof_of_insurance_company', 'medical_info','medical_file', 'phone_number',
                  'hospital')

    def SaveRegistration(self,commit = True):
        newUser = super(RegistrationForm,self).save(commit = False)
        newUser.username = self.cleaned_data['username']
        newUser.email = self.cleaned_data['email']
        newUser.first_name = self.cleaned_data['first_name']
        newUser.last_name = self.cleaned_data['last_name']
        newUser.birthday = self.cleaned_data['birthday']
        newUser.proof_of_insurance_id = self.cleaned_data['proof_of_insurance_id']
        newUser.proof_of_insurance_company = self.cleaned_data['proof_of_insurance_company']
        newUser.medical_info = self.cleaned_data['medical_info']
        newUser.phone_number = self.cleaned_data['phone_number']
        newUser.gender = self.cleaned_data['gender']
        newUser.hospital = self.cleaned_data['hospital']
        newUser.medical_file = self.request.FILES['medical_file']
        if commit:
            newUser.save()

        return newUser

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea)

class DoctorForm(UserCreationForm):
    email = forms.EmailField(required = True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
    phone_number = forms.CharField(required = False)
    username = forms.CharField(required=True)
    id_num = forms.IntegerField(required=True)
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=True)

    class Meta:
        model = Doctor
        fields = ('username', 'email','first_name',
                  'last_name','phone_number', 'id_num', 'hospital')

    def SaveRegistration(self,commit = True):
        newUser = super(DoctorForm,self).save(commit = False)
        newUser.username = self.cleaned_data['username']
        newUser.password = self.cleaned_data['password']
        newUser.email = self.cleaned_data['email']
        newUser.first_name = self.cleaned_data['first_name']
        newUser.last_name = self.cleaned_data['last_name']
        newUser.phone_number = self.cleaned_data['phone_number']
        newUser.id_num = self.cleaned_data['id_num']
        newUser.hospital = self.cleaned_data['hospital']

        if commit:
            newUser.save()

        return newUser

class NurseForm(UserCreationForm):
    email = forms.EmailField(required = True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
    phone_number = forms.CharField(required = False)
    username = forms.CharField(required=True)
    id_num = forms.IntegerField(required=True)
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=True)

    class Meta:
        model = Nurses
        fields = ('username', 'email', 'first_name',
                  'last_name','phone_number', 'id_num', 'hospital')

    def SaveRegistration(self,commit = True):
        newUser = super(NurseForm,self).save(commit = False)
        newUser.username = self.cleaned_data['username']
        newUser.password = self.cleaned_data['password']
        newUser.email = self.cleaned_data['email']
        newUser.first_name = self.cleaned_data['first_name']
        newUser.last_name = self.cleaned_data['last_name']
        newUser.phone_number = self.cleaned_data['phone_number']
        newUser.id = self.cleaned_data['id_num']
        newUser.hospital = self.cleaned_data['hospital']

        if commit:
            newUser.save()

        return newUser


class AdminForm(UserCreationForm):
    email = forms.EmailField(required = True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
    phone_number = forms.CharField(required = False)
    username = forms.CharField(required=True)
    id_num = forms.IntegerField(required=True)
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=True)

    class Meta:
        model = HospitalAdmin
        fields = ('username', 'email','first_name',
                  'last_name','phone_number', 'id_num', 'hospital')

    def SaveRegistration(self,commit = True):
        newUser = super(AdminForm,self).save(commit = False)
        newUser.username = self.cleaned_data['username']
        newUser.password = self.cleaned_data['password']
        newUser.email = self.cleaned_data['email']
        newUser.first_name = self.cleaned_data['first_name']
        newUser.last_name = self.cleaned_data['last_name']
        newUser.phone_number = self.cleaned_data['phone_number']
        newUser.id_num = self.cleaned_data['id_num']
        newUser.hospital = self.cleaned_data['hospital']

        if commit:
            newUser.save()

        return newUser

class PrescriptionForm(forms.ModelForm):
    patient_name = forms.ModelChoiceField(queryset=Patient.objects.all(), required=True)
    prescription_name = forms.CharField(required=True)
    dosage = forms.CharField(required=True)
    Taken_Per_Day = forms.CharField(required=True)

    class Meta:
        model = Prescription
        fields = ('patient_name', 'prescription_name', 'dosage', 'Taken_Per_Day')

    def SavePrescription(self,commit = True):
        newPrescription = super(PrescriptionForm,self).save(commit = False)
        newPrescription.patient_name = self.cleaned_data['patient_name']
        newPrescription.prescription_name = self.cleaned_data['prescription_name']
        newPrescription.dosage = self.cleaned_data['dosage']
        newPrescription.Taken_Per_Day = self.cleaned_data['Taken_Per_Day']

        if commit:
            newPrescription.save()

        return newPrescription


class TestsandResultsForm(forms.ModelForm):
#    def __init__(self, *args, **kwargs):
#        self.user = kwargs.pop('user')
#        super(TestsandResultsForm, self).__init__(*args, **kwargs)

    patient_name = forms.ModelChoiceField(queryset=Patient.objects.all(), required=True)
    test_name = forms.CharField(required=True)
    results = forms.CharField(required=False)
    release = forms.ChoiceField(required=True, choices=RELEASE)
   
    class Meta:
        model = Test_Results
        fields = ('patient_name', 'test_name', 'results', 'release')

    def SaveTestandResults(self, commit=True):
        newTestandResults = super(TestsandResultsForm,self).save(commit=False)
        newTestandResults.patient_name = self.cleaned_data['patient_name']
        newTestandResults.test_name = self.cleaned_data['test_name']
        newTestandResults.result = self.cleaned_data['results']
        newTestandResults.release = self.cleaned_data['release']
        doctor = Doctor.objects.filter(user=self.user)
        if doctor.exists():
            newTestandResults.doctor = doctor
        if commit:
            newTestandResults.save()

        return newTestandResults


class TestsandResultsUpdateForm(forms.ModelForm):
    patient_name = forms.ModelChoiceField(queryset=Patient.objects.all(), required=True)
    test_name = forms.CharField(required=True)
    results = forms.CharField(required=False)
    release = forms.ChoiceField(required=True, choices=RELEASE)

    class Meta:
        model = Test_Results
        fields = ('patient_name', 'test_name', 'results', 'release')



class AppointmentFormDoctor(forms.ModelForm):
    date = forms.DateField(required=True)
    start = forms.TimeField(required=True)
    end = forms.TimeField(required=True)
    description = forms.CharField(required=True)
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), required=True)

    class Meta:
        model = Appointment
        fields = ('date', 'description', 'patient', 'start', 'end')

    def SaveAppointment(self, commit=True):
        newAppointment = super(AppointmentFormDoctor,self).save(commit=False)
        newAppointment.date = self.cleaned_data['date']
        newAppointment.description = self.cleaned_data['description']
        newAppointment.patient = self.cleaned_data['patient']
        newAppointment.start = self.cleaned_data['start']
        newAppointment.end = self.cleaned_data['end']

        if commit:
            newAppointment.save()

        return newAppointment

class AppointmentFormPatient(forms.ModelForm):
    date = forms.DateTimeField(required=True)
    start = forms.TimeField(required=True)
    end = forms.TimeField(required=True)
    description = forms.CharField(required=True)
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), required=True)

    class Meta:
        model = Appointment
        fields = ('date', 'description', 'doctor', 'start', 'end')

    def SaveAppointment(self, commit=True):
        newAppointment = super(AppointmentFormPatient,self).save(commit=False)
        newAppointment.date = self.cleaned_data['date']
        newAppointment.description = self.cleaned_data['description']
        newAppointment.doctor = self.cleaned_data['doctor']
        newAppointment.start = self.cleaned_data['start']
        newAppointment.end = self.cleaned_data['end']

        if commit:
            newAppointment.save()

        return newAppointment

class AppointmentFormNurse(forms.ModelForm):
    date = forms.DateTimeField(required=True)
    start = forms.TimeField(required=True)
    end = forms.TimeField(required=True)
    description = forms.CharField(required=True)
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), required=True)
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), required=True)

    class Meta:
        model = Appointment
        fields = ('date', 'description', 'doctor', 'patient', 'start', 'end')

    def SaveAppointment(self, commit=True):
        newAppointment = super(AppointmentFormNurse,self).save(commit=False)
        newAppointment.date = self.cleaned_data['date']
        newAppointment.description = self.cleaned_data['description']
        newAppointment.doctor = self.cleaned_data['doctor']
        newAppointment.patient = self.cleaned_data['patient']
        newAppointment.start = self.cleaned_data['start']
        newAppointment.end = self.cleaned_data['end']

        if commit:
            newAppointment.save()

        return newAppointment


class HospitalForm(forms.ModelForm):
    name = forms.CharField(required=True)

    class Meta:
        model = Hospital
        fields = 'name',

    def SaveAppointment(self, commit=True):
        newHospital = super(HospitalForm,self).save(commit=False)
        newHospital.name = self.cleaned_data['name']

        if commit:
            newHospital.save()

        return newHospital
