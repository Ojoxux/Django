from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.employee_list, name="employee_list"),
    path("new/", views.employee_create, name="employee_create"),
    path("edit/<int:user_id>/", views.employee_edit, name="employee_edit"),
    path("delete/<int:user_id>/", views.employee_delete, name="employee_delete"),
    path("user/<int:user_id>/", views.employee_detail, name="employee_detail"),
]
