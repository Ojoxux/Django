from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.employee_list, name="employee_list"),
    path("user/<int:user_id>/", views.employee_detail, name="employee_detail"),
]
