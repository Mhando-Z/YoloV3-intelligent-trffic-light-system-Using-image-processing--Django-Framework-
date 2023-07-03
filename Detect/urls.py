from .views import line_chart, line_chart_json
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dect, name="Dect"),
    path('live_feed/', views.live_feed, name='live_feed'),
    path('detections/', views.detection, name='detections'),
    path('data/', views.Data, name='data'),
    path('chart/', line_chart, name='line_chart'),
    path('chartJSON/', line_chart_json, name='line_chart_json'),
]



