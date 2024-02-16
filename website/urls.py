from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.website , name='website'),
    path('answer/', views.answer, name='answer')
]