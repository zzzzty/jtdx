from django.urls import path,include
from .views import show,bigshow


urlpatterns = [
    path('detail/<int:productpk>',show,name='product'),
    path('bigdetail/<int:productpk>',bigshow,name='bigshow'),
]