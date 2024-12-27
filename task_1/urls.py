from django.urls import path
from . import views

urlpatterns = [
    path('service_record/', views.ServiceRecordView.as_view())
]