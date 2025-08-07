from django.urls import path
from . import views

app_name = "cpromotion"

urlpatterns = [
    path("promos/", views.promos, name="promos"),
]
