from django.urls import path
from . import views

#namespace für url
app_name = 'configuration'
urlpatterns = [
    #leere Anführungszeichen heißt, dass das bei Aufruf der App gesetzt wird
    path('', views.index, name='index'),
]
