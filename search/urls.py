from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url('events/$', views.events_view),
    path('events/<slug:slug>/', views.events_detail_view),
]