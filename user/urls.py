from django.urls import path
from . import views

urlpatterns = [
    path('', views.logReg, name='Login'),
    path('Logout/', views.logt, name='Logout'),
    path('Profile/', views.Profile, name='Profile'),
    path('Nav/', views.Nav, name='Nav'),
    path('ProfileEdit/<str:pk>/', views.ProfileEdit, name='ProfileEdit')
]
