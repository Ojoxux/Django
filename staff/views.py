from django.shortcuts import get_object_or_404, redirect, render

from .forms import EmployeeForm
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


def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("employee_list")
    else:
        form = EmployeeForm()

    return render(
        request,
        "staff/employee_form.html",
        {
            "form": form,
            "page_title": "新規社員登録",
            "submit_label": "登録する",
        },
    )


def employee_edit(request, user_id):
    employee = get_object_or_404(Employee, id=user_id)

    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect("employee_list")
    else:
        form = EmployeeForm(instance=employee)

    return render(
        request,
        "staff/employee_form.html",
        {
            "form": form,
            "page_title": f"{employee.name}さんの情報を編集",
            "submit_label": "更新する",
        },
    )


def employee_delete(request, user_id):
    employee = get_object_or_404(Employee, id=user_id)

    if request.method == "POST":
        employee.delete()
        return redirect("employee_list")

    return render(request, "staff/employee_confirm_delete.html", {"employee": employee})
