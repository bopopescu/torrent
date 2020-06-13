from django.urls import path, include

from user import views

urlpatterns = [
    path('', include('django_registration.backends.activation.urls')),
    path('', include('django.contrib.auth.urls')),
    path('uploads/', views.UploadsList.as_view(), name='uploads'),
]
