from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os

STATUS = (
    ('Admit', 'Admit'),
    ('Discharge', 'Discharge')
)

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.txt','.pdf','.doc','.docx','.odt']
    if not ext in valid_extensions:
        raise ValidationError(u'File not supported!')

class Hospital(models.Model):
    name = models.CharField(max_length=25, default="yourSuperCoolHospital")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class ActivityLog(models.Model):
    hospital = models.ForeignKey('Hospital', default=None)
    first_name = models.CharField(max_length=100, default=None)
    last_name = models.CharField(max_length=100, null=True)
    action = models.CharField(max_length=50, default=None)
    target_first = models.CharField(max_length=50, null=True)
    target_last = models.CharField(max_length=50, null=True)
    date = models.DateField(default=None)
    time = models.TimeField(default=None)

class Doctor(User):
    phone_number = models.CharField(max_length=50, default=None)
    id_num = models.IntegerField(default=None)
    hospital = models.ForeignKey('Hospital', default=None)

class Nurses(User):
    phone_number = models.CharField(max_length=50, default=None)
    id_num = models.IntegerField( default=None)
    hospital = models.ForeignKey('Hospital', default=None)


class HospitalAdmin(User):
    phone_number = models.CharField(max_length=50, default=None)
    id_num = models.IntegerField(default=None)
    hospital = models.ForeignKey('Hospital', default=None)


class Patient(User):
    birthday = models.DateTimeField(default=None)
    proof_of_insurance_id = models.IntegerField(default=None)
    proof_of_insurance_company = models.CharField(max_length=50, default=None)
    medical_file = models.FileField(validators=[validate_file_extension])
    medical_info = models.CharField(max_length=100, default=None)
    phone_number = models.CharField(max_length=50, default=None)
    gender = models.CharField(max_length=6, default=None)
    hospital = models.ForeignKey('Hospital', default=None)
    status = models.CharField(max_length=10, null=True, choices=STATUS)


#Need to discuss this one
class Prescription(models.Model):
    patient_name = models.ForeignKey('Patient', default=None)
    doctor = models.ForeignKey('Doctor', default=None)
    prescription_name = models.CharField(max_length=50, default=None)
    dosage = models.CharField(max_length=100, default=None)
    Taken_Per_Day = models.CharField(max_length=50, default=None)


class Test_Results(models.Model):
    patient_name = models.ForeignKey('Patient', default=None)
    doctor = models.ForeignKey('Doctor', default=None)
    test_name = models.CharField(max_length=100, default=None)
    results = models.CharField(max_length=500, default='Pending...')
    release = models.BooleanField(default=False)




class PrivateMessage(models.Model):
    message = models.CharField(max_length = 400, default=None)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

#Generally ignore this one, it's probably bungus
class System():
    Sys_Activities = models.CharField(max_length = 100, default=None)
    Sys_Stats = models.CharField(max_length = 100, default=None)


class AppointmentCalendar(models.Model):
    appointments = models.ForeignKey('Appointment', default=None)
    doctor = models.ForeignKey('Doctor', default=None)
    patient = models.ForeignKey('Patient', default=None)

class Appointment(models.Model):
    date = models.DateField("Date")
    start = models.TimeField("Start Time")
    end = models.TimeField("End Time")
    description = models.CharField(max_length = 300, default=None)
    doctor = models.ForeignKey('Doctor', default=None)
    patient = models.ForeignKey('Patient', default=None)
