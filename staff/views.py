from django.shortcuts import render

from .models import Employee


def employee_list(request):
    employees = Employee.objects.all().order_by("-joined_date")
    return render(
        request,
        "staff/list.html",
        {"employees": employees, "total_count": employees.count()},
    )


def employee_detail(request, user_id):
    try:
        employee = Employee.objects.get(id=user_id)
    except Employee.DoesNotExist:
        return render(request, "staff/404.html", status=404)
    return render(request, "staff/detail.html", {"employee": employee})
