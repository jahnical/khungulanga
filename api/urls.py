from django.urls import include, path
from api.views.appointment import AppointmentView
from api.views.appointment_chat import AppointmentChatDetail, AppointmentChatView
from api.views.chat_message import ChatMessageView

from api.views.dermatologist import DermatologistDetail, DermatologistView
from api.views.disease import DiseaseDetail, DiseaseView
from api.views.notification import NotificationAPIView
from api.views.patient import PatientDetail, PatientView
from api.views.prediction import PredictionAPIView
from api.views.slot import SlotAPIView, SlotDetailAPIView
from .views.user_record import UserRecordView
from .views.diagnosis import DiagnosisDetailView, DiagnosisView

from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('devices', FCMDeviceAuthorizedViewSet)

app_name = 'api'
urlpatterns = [
    path('user/', UserRecordView.as_view(), name='users'),
    path('users/register/', UserRecordView.as_view(), name='register'),
    
    path('users/dermatologist/register/', DermatologistView.as_view(), name='derm.register'),
    
    path('diagnosis/', DiagnosisView.as_view(), name='diagnosis'),
    path('diagnosis/<int:pk>', DiagnosisDetailView.as_view(), name='diagnosis.detail'),
    
    path('dermatologists/nearby', DermatologistView.as_view(), name='dermatologist'),
    path("dermatologists/<username>/", DermatologistDetail.as_view(), name="dermatologist_detail"),
    
    path('diseases/', DiseaseView.as_view(), name='diseases'),   
    path("diseases/<int:pk>/", DiseaseDetail.as_view(), name="disease_detail"),
    
    path('patients/', PatientView.as_view(), name='patients'),   
    path("patients/<username>/", PatientDetail.as_view(), name="patient_detail"),
    
    path('appointment_chats/', AppointmentChatView.as_view(), name='appointment_chats'),   
    path("appointment_chats/<int:pk>/", AppointmentChatDetail.as_view(), name="appointment_chat_detail"),
    
    path('chat_messages/', ChatMessageView.as_view(), name='chat_messages'),  
    
    path('appointments/<int:pk>/', AppointmentView.as_view(), name='appointments'),
    path('appointments/', AppointmentView.as_view(), name='appointments'),
    
    path('slots/', SlotAPIView.as_view(), name='slots'),   
    path("slots/<int:pk>/", SlotDetailAPIView.as_view(), name="slot_detail"),
    path("slots/of/<int:derm_id>/", SlotAPIView.as_view(), name="slot_detail_of"),
    
    path('notifications/', NotificationAPIView.as_view(), name='notifications'),
    path("notifications/<int:pk>/", NotificationAPIView.as_view(), name="notifications_detail"),
    
    path("predictions/<int:pk>/", PredictionAPIView.as_view(), name="predictions_detail"),
    path("predictions/", PredictionAPIView.as_view(), name="predictions"),
    
    path('', include(router.urls)),
]