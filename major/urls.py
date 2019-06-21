from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.major_insert,name='major_insert'),
]