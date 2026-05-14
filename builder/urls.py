from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('form/', views.home, name='form'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('resume/<int:id>/', views.view_resume, name='view_resume'),
    path('edit/<int:id>/', views.edit_resume, name='edit_resume'),
    path('generate/', views.generate_resume, name='generate_resume'),
]


