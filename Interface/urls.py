from . import views
from .views import line_chart, line_chart_json
from django.urls import path
from . import views  

urlpatterns = [
    path('', views.Home, name='Home'),
    path('Site/', views.Site, name='Site'),
    path('Reports/', views.Reports, name='Reports'),    
    path('Hmmm/', views.Hmmm, name='Hmmm'),
    path('live_feed/', views.live_feed, name='live_feed'),
    path('detections/', views.detection, name='detections'),
    path('data/', views.Data, name='data'),
    path('chart/', line_chart, name='line_chart'),
    path('chartJSON/', line_chart_json, name='line_chart_json'),
]

