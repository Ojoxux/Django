from django import forms

from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ("name", "dept", "role", "email", "joined_date")
        widgets = {
            "joined_date": forms.DateInput(attrs={"type": "date"}),
        }
