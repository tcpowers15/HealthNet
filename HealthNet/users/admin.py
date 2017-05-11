from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Hospital)
admin.site.register(Nurses)
admin.site.register(Prescription)
admin.site.register(PrivateMessage)
admin.site.register(Appointment)
admin.site.register(AppointmentCalendar)
admin.site.register(Test_Results)
