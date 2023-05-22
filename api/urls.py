from django.urls import path
from api.views.appointment import AppointmentView
from api.views.appointment_chat import AppointmentChatDetail, AppointmentChatView
from api.views.chat_message import ChatMessageView

from api.views.dermatologist import DermatologistView
from api.views.disease import DiseaseDetail, DiseaseView
from api.views.patient import PatientDetail, PatientView
from .views.user_record import UserRecordView
from .views.diagnosis import DiagnosisView

app_name = 'api'
urlpatterns = [
    path('user/', UserRecordView.as_view(), name='users'),
    path('users/register/', UserRecordView.as_view(), name='register'),
    
    path('diagnosis/', DiagnosisView.as_view(), name='diagnosis'),
    path('diagnosis/<int:pk>', DiagnosisView.as_view(), name='diagnosis.delete'),
    
    path('dermatologists/nearby', DermatologistView.as_view(), name='dermatologist'),
    path("dermatologists/<int:pk>/", DermatologistView.as_view(), name="dermatologist_detail"),
    
    path('diseases/', DiseaseView.as_view(), name='diseases'),   
    path("diseases/<int:pk>/", DiseaseDetail.as_view(), name="disease_detail"),
    
    path('patients/', PatientView.as_view(), name='patients'),   
    path("patients/<username>/", PatientDetail.as_view(), name="patient_detail"),
    
    path('appointment_chats/', AppointmentChatView.as_view(), name='appointment_chats'),   
    path("appointment_chats/<username>/", AppointmentChatDetail.as_view(), name="appointment_chat_detail"),
    
    path('chat_messages/', ChatMessageView.as_view(), name='chat_messages'),  
    
    path('appointments/<int:pk>/', AppointmentView.as_view(), name='appointments')
]