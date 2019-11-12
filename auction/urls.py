from django.urls import path,include
from .views import show


urlpatterns = [
    path('detail/<int:productpk>',show,name='product'),
]