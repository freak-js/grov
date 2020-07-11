from django.contrib import admin
from django.urls import path

from hvoya_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('settings/', views.settings, name='settings'),
    path('generate_test_data/', views.generate_test_data, name='generate_test_data')
]
