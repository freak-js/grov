from django.contrib import admin
from django.urls import path

from hvoya_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('change_settings/', views.change_settings, name='change_settings'),
    path('create_new_flower/', views.change_settings, name='create_new_flower'),
    path('generate_test_data/', views.generate_test_data, name='generate_test_data')
]
