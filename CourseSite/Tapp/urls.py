from django.urls import path
from . import views

app_name = "Tapp"
urlpatterns = [
    path('',views.index,name="index")
]
