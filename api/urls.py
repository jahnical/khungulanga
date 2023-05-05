from django.urls import path
from .views.user_record import UserRecordView
from .views.diagnosis import DiagnosisView

app_name = 'api'
urlpatterns = [
    path('user/', UserRecordView.as_view(), name='users'),
    path('users/register/', UserRecordView.as_view(), name='register'),
    path('diagnosis/', DiagnosisView.as_view(), name='diagnosis'),
]