from django.urls import path

from api.views.dermatologist import DermatologistView
from .views.user_record import UserRecordView
from .views.diagnosis import DiagnosisView

app_name = 'api'
urlpatterns = [
    path('user/', UserRecordView.as_view(), name='users'),
    path('users/register/', UserRecordView.as_view(), name='register'),
    path('diagnosis/', DiagnosisView.as_view(), name='diagnosis'),
    path('dermatologists/nearby', DermatologistView.as_view(), name='dermatologist'),
    path("dermatologists/<int:pk>/", DermatologistView.as_view(), name="dermatologist_detail"),
]