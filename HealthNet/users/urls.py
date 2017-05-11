from django.conf.urls import url, include
from django.views.static import serve
from .views import *
from . import views

urlpatterns = [
    url(r'^export_view/$', views.export_view,name='export_view'),
    url(r'^appointment_calendar/$', views.view_appointment_Calendar, name = 'view_calendar'),
    url(r'^register/', createUser.as_view() , name = 'RegistrationForm'),
    url(r'^hospital/', createHospital.as_view() , name = 'CreateHospital'),
    url(r'^registerDoctor/', createDoctor.as_view() , name = 'DoctorForm'),
    url(r'^registerNurse/', createNurse.as_view() , name = 'NurseForm'),
    url(r'^registerAdmin/', createAdmin.as_view(), name='AdminForm'),
    url(r'^update_user_profile/$', login_required(updateUserInformation.as_view()), name = 'edit_user'),
    url(r'^add_prescription/$', createPerscription.as_view(), name='add_prescription'),
    url(r'^add_new_test/$', createTestsandResults.as_view(), name='new_test'),
    url(r'^new_appointment/$', createAppointment.as_view(), name='new_appointment'),
    url(r'^new_appointment_D/$', createAppointmentDoctor.as_view(), name='new_appointment'),
    url(r'^new_appointment_N/$', createAppointmentNurse.as_view(), name='new_appointment'),
    url(r'^change_appointment/(?P<name>.*)/$', updateAppointment.as_view(), name='edit_appointment'),

    url(r'^media/(?P<pk>.*)/$', views.download, name='view_download'),
    #url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^$', home),
    url(r'^email/$', views.email, name='email'),
    url(r'^thanks/$', views.thanks, name='thanks'),
    url(r'^register/success/$', views.register_success),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', LogoutView.as_view()),
    #url(r'^appointment_calendar/$', views.view_appointment_Calendar, name = 'view_calendar'),
    url(r'^prescriptions/$', views.view_prescriptions, name='view_prescriptions'),
    url(r'^prescriptionsD/$', views.view_prescriptionsD, name='view_prescriptionsD'),
    url(r'^prescriptionsN/$', views.view_prescriptionsN, name='view_prescriptionsN'),
    url(r'^patient_details/$', views.patient_detail, name='patient_detail'),
    url(r'^view_tests/$', views.view_tests, name='view_tests'),
    url(r'^view_results/$', views.view_results, name='view_results'),
    url(r'^view_testsD/$', views.view_testsD, name='view_testsD'),
    url(r'^view_testsN/$', views.view_testsN, name='view_testsN'),
    url(r'^view_appointments/$', views.view_appointments, name='view_appointments'),
    url(r'^view_med/$', login_required(views.patview), name='view_med'),
    url(r'^update_prescription/(?P<pk>\d+)$', login_required(updatePrescription.as_view()), name = 'edit_prescription'),
    url(r'^delete_prescription/(?P<pk>\d+)$', login_required(deletePrescription.as_view()), name = 'delete_prescription'),
    url(r'^delete_appointment/(?P<pk>\d+)$', login_required(deleteAppointment.as_view()), name = 'delete_appointment'),
    url(r'^update_appointment/(?P<pk>\d+)$', login_required(updateAppointment.as_view()), name = 'edit_appointment'),
    url(r'^update_test/(?P<pk>\d+)$', login_required(updateTestsandResults.as_view()), name = 'edit_test'),
    url(r'^delete_test/(?P<pk>\d+)$', login_required(deleteTestsandResults.as_view()), name = 'delete_test'),
    url(r'^update_med/(?P<pk>\d+)$', login_required(UpdateMed.as_view()), name='edit_med'),
    url(r'^admitview/$', login_required(views.AdmitView), name = 'AdmitView'),
    url(r'^admit/(?P<pk>\d+)$', login_required(Admit.as_view()), name = 'Admit'),
    url(r'^transferview/$', login_required(views.TransferView), name = 'TransferView'),
    url(r'^transfer/(?P<pk>\d+)$', login_required(Transfer.as_view()), name = 'Transfer'),
    url(r'^about/$', about),
    url(r'^stats/$', statistics),
    url(r'^activity/$', SystemActivityLog)
]
