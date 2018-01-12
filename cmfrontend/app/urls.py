from django.conf.urls import url
from . import views

urlpatterns = [
   url(r'describe_input', views.describe_input),
   url(r'diagonos_input', views.diagonos_input),
]
