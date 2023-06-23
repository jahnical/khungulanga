from django.contrib import admin

from api.models.appointment import Appointment
from api.models.clinic import Clinic
from api.models.dermatologist import Dermatologist
from api.models.diagnosis import Diagnosis
from api.models.disease import Disease
from api.models.notification import Notification
from api.models.patient import Patient
from api.models.prediction import Prediction
from api.models.slot import Slot
from api.models.treatment import Treatment

# Register your models here.
admin.site.site_header = 'Khungulanga Admin'
admin.site.site_title = 'Khungulanga Admin'
admin.site.index_title = 'Khungulanga Admin'
admin.site.register([Patient, Dermatologist, Clinic, Disease, Prediction, Treatment, Appointment, Slot, Diagnosis, Notification])
